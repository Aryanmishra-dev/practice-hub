from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import json
from pathlib import Path

from app.models.schemas import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
    CategoryCreate,
    CategoryResponse,
    BulkUploadResult,
    AdminStatsResponse,
    PaginatedResponse,
)
from app.core.security import get_current_admin_user

router = APIRouter()

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
    # Load questions from files to get accurate counts
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    total_questions = 0
    questions_by_difficulty = {"easy": 0, "medium": 0, "hard": 0, "expert": 0}
    
    difficulty_files = {
        "easy": PROJECT_ROOT / "quiz_easy.json",
        "medium": PROJECT_ROOT / "quiz_normal.json",
        "hard": PROJECT_ROOT / "quiz_hard.json",
        "expert": PROJECT_ROOT / "quiz_expert.json",
    }
    
    for diff, file_path in difficulty_files.items():
        if file_path.exists():
            with open(file_path, "r") as f:
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
    categories: List[CategoryCreate],
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
    questions: List[QuestionCreate],
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
    category_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    current_user: dict = Depends(get_current_admin_user),
):
    """Get all questions (admin view with pagination)."""
    # Load from files
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
    all_questions = []
    
    files = [
        PROJECT_ROOT / "quiz_easy.json",
        PROJECT_ROOT / "quiz_normal.json",
        PROJECT_ROOT / "quiz_hard.json",
        PROJECT_ROOT / "quiz_expert.json",
    ]
    
    for file_path in files:
        if file_path.exists():
            with open(file_path, "r") as f:
                data = json.load(f)
                all_questions.extend(data)
    
    # Filter
    if difficulty:
        difficulty_map = {"easy": "Easy", "medium": "Normal", "hard": "Hard", "expert": "Expert"}
        all_questions = [q for q in all_questions if q.get("difficulty") == difficulty_map.get(difficulty, difficulty)]
    
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
