"""User progress, analytics, and authentication endpoints."""

import random  # noqa: S311 — used for mock data, not cryptography
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.schemas import (
    PaginatedResponse,
    QuizHistoryItem,
    RecommendationResponse,
    UserProgressResponse,
    UserStatsResponse,
)

router = APIRouter()

GUEST_USER_ID = "guest"


# ============= Authentication Models =============
class SignupRequest(BaseModel):
    """User signup request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    full_name: str = Field(..., description="User full name")


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    """Authentication response with token."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")


# In-memory user store (replace with database in production)
_users_db: dict[str, dict] = {}


@router.post("/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest) -> AuthResponse:
    """Register a new user account.

    Args:
        request: Signup request with email, password, and full name.

    Returns:
        Authentication response with JWT token.

    Raises:
        HTTPException: If email already registered.
    """
    if request.email in _users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user_id = f"user_{len(_users_db) + 1}"
    hashed_password = get_password_hash(request.password)

    _users_db[request.email] = {
        "user_id": user_id,
        "email": request.email,
        "full_name": request.full_name,
        "password_hash": hashed_password,
        "created_at": datetime.now(UTC),
    }

    token = create_access_token(data={"sub": user_id, "email": request.email})

    return AuthResponse(
        access_token=token,
        token_type="bearer",  # noqa: S106
        user_id=user_id,
        email=request.email,
    )


@router.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest) -> AuthResponse:
    """Authenticate user and return JWT token.

    Args:
        request: Login request with email and password.

    Returns:
        Authentication response with JWT token.

    Raises:
        HTTPException: If credentials are invalid.
    """
    user = _users_db.get(request.email)

    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(data={"sub": user["user_id"], "email": user["email"]})

    return AuthResponse(
        access_token=token,
        token_type="bearer",  # noqa: S106
        user_id=user["user_id"],
        email=user["email"],
    )


# ============= Progress & Analytics =============


def generate_mock_progress() -> UserProgressResponse:
    """Generate mock progress data."""
    return UserProgressResponse(
        total_questions_answered=random.randint(50, 200),  # noqa: S311
        overall_accuracy=round(random.uniform(60, 90), 2),  # noqa: S311
        total_time_spent_seconds=random.randint(3600, 14400),  # noqa: S311
        current_streak=random.randint(1, 14),  # noqa: S311
        longest_streak=random.randint(7, 30),  # noqa: S311
        categories_practiced=1,
        favorite_category="ePO Server Administration",
        improvement_trend=random.choice(["improving", "stable", "declining"]),  # noqa: S311
        last_7_days_accuracy=round(random.uniform(65, 95), 2),  # noqa: S311
        stats_by_category=[
            UserStatsResponse(
                id="stat_1",
                user_id=GUEST_USER_ID,
                category_id="epo",
                category_name="ePO Server Administration",
                difficulty=None,
                total_attempts=random.randint(50, 150),  # noqa: S311
                correct_attempts=random.randint(30, 100),  # noqa: S311
                accuracy=round(random.uniform(60, 90), 2),  # noqa: S311
                avg_time_seconds=round(random.uniform(20, 60), 2),  # noqa: S311
                last_practiced_at=datetime.now(UTC),
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
        difficulty = random.choice(difficulties)  # noqa: S311
        total = 10
        score = random.randint(4, 10)  # noqa: S311

        history.append(
            QuizHistoryItem(
                id=f"quiz_{i}",
                category_name="ePO Server Administration",
                difficulty=difficulty,
                score=score,
                total_questions=total,
                accuracy=round((score / total) * 100, 2),
                completed_at=datetime.now(UTC) - timedelta(days=i),
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

    return random.choice(recommendations)  # noqa: S311
