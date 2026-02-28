import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.security import get_current_admin_user
from app.models.schemas import (
    AdminStatsResponse,
    BulkUploadResult,
    CategoryCreate,
    PaginatedResponse,
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)

router = APIRouter()

# Path to quiz JSON data files
_PACKAGE_ROOT = Path(__file__).parent.parent.parent  # backend/
_PROJECT_ROOT = _PACKAGE_ROOT.parent  # QUIZ-FORGE/
_DATA_DIR = _PACKAGE_ROOT / "data"  # backend/data/


def _resolve_data_file(filename: str) -> Path:
    """Find quiz data file, checking Docker path first, then project root."""
    docker_path = _DATA_DIR / filename
    if docker_path.exists():
        return docker_path
    return _PROJECT_ROOT / filename


_DIFFICULTY_FILES: dict[str, Path] = {
    "easy": _resolve_data_file("quiz_easy.json"),
    "medium": _resolve_data_file("quiz_normal.json"),
    "hard": _resolve_data_file("quiz_hard.json"),
    "expert": _resolve_data_file("quiz_expert.json"),
}

# In-memory storage for demo (in production, use database)
questions_db: dict = {}
categories_db: dict = {
    "epo": {
        "id": "epo",
        "name": "ePO Server Administration",
        "description": "Questions about Trellix ePO server",
        "icon": "file-text",
        "display_order": 1,
        "is_active": True,
    }
}


@router.get("/admin/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    current_user: dict = Depends(get_current_admin_user),
):
    """Get admin dashboard statistics."""
    total_questions = 0
    questions_by_difficulty = {"easy": 0, "medium": 0, "hard": 0, "expert": 0}

    for diff, file_path in _DIFFICULTY_FILES.items():
        if file_path.exists():
            with file_path.open() as f:
                data = json.load(f)
                count = len(data)
                total_questions += count
                questions_by_difficulty[diff] = count

    return AdminStatsResponse(
        total_questions=total_questions,
        total_categories=len(categories_db),
        total_users=100,  # Mock
        questions_by_difficulty=questions_by_difficulty,
        questions_by_category={"ePO Server Administration": total_questions},
        active_users_today=25,  # Mock
        quizzes_taken_today=50,  # Mock
    )


@router.post("/admin/categories/bulk", response_model=BulkUploadResult)
async def bulk_upload_categories(
    categories: list[CategoryCreate],
    current_user: dict = Depends(get_current_admin_user),
):
    """Bulk upload categories."""
    success_count = 0
    errors = []

    for i, category in enumerate(categories):
        try:
            cat_id = category.name.lower().replace(" ", "_")
            categories_db[cat_id] = {
                "id": cat_id,
                **category.model_dump(),
                "is_active": True,
            }
            success_count += 1
        except Exception as e:
            errors.append({"row": i + 1, "message": str(e)})

    return BulkUploadResult(
        success_count=success_count,
        error_count=len(errors),
        errors=errors,
    )


@router.post("/admin/questions/bulk", response_model=BulkUploadResult)
async def bulk_upload_questions(
    questions: list[QuestionCreate],
    current_user: dict = Depends(get_current_admin_user),
):
    """Bulk upload questions."""
    success_count = 0
    errors = []

    for i, question in enumerate(questions):
        try:
            q_id = f"q_{len(questions_db) + 1}"
            questions_db[q_id] = {
                "id": q_id,
                **question.model_dump(),
                "is_active": True,
                "version": 1,
            }
            success_count += 1
        except Exception as e:
            errors.append({"row": i + 1, "message": str(e)})

    return BulkUploadResult(
        success_count=success_count,
        error_count=len(errors),
        errors=errors,
    )


@router.get("/admin/questions")
async def get_all_questions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: str | None = None,
    difficulty: str | None = None,
    current_user: dict = Depends(get_current_admin_user),
):
    """Get all questions (admin view with pagination)."""
    all_questions = []

    for file_path in _DIFFICULTY_FILES.values():
        if file_path.exists():
            with file_path.open() as f:
                data = json.load(f)
                all_questions.extend(data)

    # Filter
    if difficulty:
        difficulty_map = {"easy": "Easy", "medium": "Normal", "hard": "Hard", "expert": "Expert"}
        all_questions = [
            q
            for q in all_questions
            if q.get("difficulty") == difficulty_map.get(difficulty, difficulty)
        ]

    # Paginate
    total = len(all_questions)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = all_questions[start:end]

    return PaginatedResponse(
        items=paginated,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.put("/admin/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: str,
    update: QuestionUpdate,
    current_user: dict = Depends(get_current_admin_user),
):
    """Update a question."""
    if question_id not in questions_db:
        raise HTTPException(status_code=404, detail="Question not found")

    question = questions_db[question_id]
    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        question[key] = value

    question["version"] = question.get("version", 1) + 1

    return question


@router.delete("/admin/questions/{question_id}")
async def delete_question(
    question_id: str,
    current_user: dict = Depends(get_current_admin_user),
):
    """Soft delete a question."""
    if question_id not in questions_db:
        raise HTTPException(status_code=404, detail="Question not found")

    questions_db[question_id]["is_active"] = False

    return {"message": "Question deleted successfully"}
