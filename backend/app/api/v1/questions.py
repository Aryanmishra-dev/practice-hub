"""Category and question endpoints.

Uses the QuizService for all business logic via dependency injection.
"""

from fastapi import APIRouter, Depends, Query

from app.models.schemas import CategoryResponse, QuestionResponse
from app.repositories.quiz_repository import QuizRepository
from app.services.quiz_service import QuizService

router = APIRouter()


def get_quiz_service() -> QuizService:
    """Dependency — create a QuizService with its repository."""
    return QuizService(repository=QuizRepository())


@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(
    service: QuizService = Depends(get_quiz_service),
):
    """Get all active categories."""
    return service.get_categories()


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    service: QuizService = Depends(get_quiz_service),
):
    """Get a specific category by ID."""
    return service.get_category(category_id)


@router.get("/categories/{category_id}/questions")
async def get_category_questions(
    category_id: str,
    difficulty: str | None = Query(None, description="Filter by difficulty"),
    limit: int = Query(50, ge=1, le=100, description="Number of questions to return"),
    service: QuizService = Depends(get_quiz_service),
):
    """Get questions for a specific category (includes correct_option for client-side grading)."""
    return service.get_questions(category_id, difficulty, limit)


@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    service: QuizService = Depends(get_quiz_service),
):
    """Get a specific question by ID (includes correct answer for review)."""
    return service.get_question(question_id)
