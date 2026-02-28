from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timedelta
import random

from app.models.schemas import (
    UserProgressResponse,
    UserStatsResponse,
    RecommendationResponse,
    QuizHistoryItem,
    PaginatedResponse,
)

router = APIRouter()

GUEST_USER_ID = "guest"


# Mock user data (no auth required)
def generate_mock_progress() -> UserProgressResponse:
    """Generate mock progress data."""
    return UserProgressResponse(
        total_questions_answered=random.randint(50, 200),
        overall_accuracy=round(random.uniform(60, 90), 2),
        total_time_spent_seconds=random.randint(3600, 14400),
        current_streak=random.randint(1, 14),
        longest_streak=random.randint(7, 30),
        categories_practiced=1,
        favorite_category="ePO Server Administration",
        improvement_trend=random.choice(["improving", "stable", "declining"]),
        last_7_days_accuracy=round(random.uniform(65, 95), 2),
        stats_by_category=[
            UserStatsResponse(
                id="stat_1",
                user_id=GUEST_USER_ID,
                category_id="epo",
                category_name="ePO Server Administration",
                difficulty=None,
                total_attempts=random.randint(50, 150),
                correct_attempts=random.randint(30, 100),
                accuracy=round(random.uniform(60, 90), 2),
                avg_time_seconds=round(random.uniform(20, 60), 2),
                last_practiced_at=datetime.utcnow(),
            )
        ],
        stats_by_difficulty={
            "easy": {"total": 50, "correct": 45, "accuracy": 90.0},
            "medium": {"total": 60, "correct": 42, "accuracy": 70.0},
            "hard": {"total": 30, "correct": 18, "accuracy": 60.0},
            "expert": {"total": 10, "correct": 4, "accuracy": 40.0},
        },
    )


def generate_mock_history(limit: int = 10) -> list:
    """Generate mock quiz history."""
    history = []
    difficulties = ["easy", "medium", "hard", "expert"]
    
    for i in range(limit):
        difficulty = random.choice(difficulties)
        total = 10
        score = random.randint(4, 10)
        
        history.append(
            QuizHistoryItem(
                id=f"quiz_{i}",
                category_name="ePO Server Administration",
                difficulty=difficulty,
                score=score,
                total_questions=total,
                accuracy=round((score / total) * 100, 2),
                completed_at=datetime.utcnow() - timedelta(days=i),
            )
        )
    
    return history


@router.get("/user/progress", response_model=UserProgressResponse)
async def get_user_progress():
    """Get progress overview (mock data)."""
    return generate_mock_progress()


@router.get("/user/analytics/{category_id}", response_model=UserProgressResponse)
async def get_category_analytics(category_id: str):
    """Get detailed analytics for a specific category."""
    progress = generate_mock_progress()
    progress.stats_by_category = [
        s for s in progress.stats_by_category if s.category_id == category_id
    ]
    return progress


@router.get("/user/history")
async def get_user_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Get quiz history (mock data)."""
    all_history = generate_mock_history(limit=50)
    
    paginated = all_history[offset : offset + limit]
    
    return PaginatedResponse(
        items=paginated,
        total=len(all_history),
        page=(offset // limit) + 1,
        page_size=limit,
        total_pages=(len(all_history) + limit - 1) // limit,
    )


@router.get("/user/recommendations", response_model=RecommendationResponse)
async def get_recommendations():
    """Get practice recommendations."""
    recommendations = [
        RecommendationResponse(
            recommended_category="ePO Server Administration",
            recommended_difficulty="medium",
            reason="Your accuracy on medium questions has dropped 10% this week",
            estimated_improvement="Practice 15 more questions to improve",
        ),
        RecommendationResponse(
            recommended_category="ePO Server Administration",
            recommended_difficulty="hard",
            reason="You haven't practiced hard questions in a while",
            estimated_improvement="Try 10 hard questions to challenge yourself",
        ),
        RecommendationResponse(
            recommended_category="ePO Server Administration",
            recommended_difficulty="expert",
            reason="Expert level needs more attention",
            estimated_improvement="Review explanations for previously missed questions",
        ),
    ]
    
    return random.choice(recommendations)
