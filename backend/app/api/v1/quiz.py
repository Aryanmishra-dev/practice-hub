"""Quiz session endpoints.

Handles quiz start, answer submission, and result retrieval using the
QuizService for all business logic via dependency injection.
"""

from fastapi import APIRouter, Depends

from app.models.schemas import (
    QuizConfig,
    QuizStartResponse,
    AnswerSubmission,
    AnswerResult,
    QuizResult,
    DifficultyStats,
)
from app.repositories.quiz_repository import QuizRepository
from app.services.quiz_service import QuizService

router = APIRouter()


def get_quiz_service() -> QuizService:
    """Dependency — create a QuizService with its repository."""
    return QuizService(repository=QuizRepository())


@router.post("/quiz/start", response_model=QuizStartResponse)
async def start_quiz(
    config: QuizConfig,
    service: QuizService = Depends(get_quiz_service),
):
    """Start a new quiz session."""
    result = service.start_quiz(
        category_id=config.category_id,
        difficulty=config.difficulty,
        question_count=config.question_count,
    )
    return QuizStartResponse(
        session_id=result["session_id"],
        questions=result["questions"],
    )


@router.post("/quiz/submit", response_model=AnswerResult)
async def submit_answer(
    submission: AnswerSubmission,
    service: QuizService = Depends(get_quiz_service),
):
    """Submit an answer for a question."""
    result = service.submit_answer(
        question_id=submission.question_id,
        selected_option=submission.selected_option,
        time_taken_seconds=submission.time_taken_seconds,
    )
    return AnswerResult(
        is_correct=result["is_correct"],
        correct_option=result["correct_option"],
        explanation=result.get("explanation"),
    )


@router.post("/quiz/{session_id}/complete", response_model=QuizResult)
async def complete_quiz(
    session_id: str,
    service: QuizService = Depends(get_quiz_service),
):
    """Complete a quiz session and get results."""
    result = service.complete_quiz(session_id)
    return QuizResult(
        session_id=result["session_id"],
        total_questions=result["total_questions"],
        correct_answers=result["correct_answers"],
        accuracy=result["accuracy"],
        total_time_seconds=result["total_time_seconds"],
        average_time_per_question=result["average_time_per_question"],
        difficulty_breakdown={
            k: DifficultyStats(**v)
            for k, v in result["difficulty_breakdown"].items()
        },
        weak_areas=result["weak_areas"],
        recommendations=result["recommendations"],
    )


@router.get("/quiz/{session_id}/result", response_model=QuizResult)
async def get_quiz_result(
    session_id: str,
    service: QuizService = Depends(get_quiz_service),
):
    """Get the result of a completed quiz session."""
    return await complete_quiz(session_id, service)
