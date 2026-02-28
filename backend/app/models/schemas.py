from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DifficultyEnum(StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    expert = "expert"


# ============= Option Models =============


class OptionBase(BaseModel):
    id: str
    text: str


class OptionCreate(OptionBase):
    pass


# ============= Category Models =============


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    icon: str | None = None
    display_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    icon: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class CategoryResponse(CategoryBase):
    id: str
    is_active: bool
    question_count: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Question Models =============


class QuestionBase(BaseModel):
    category_id: str
    difficulty: DifficultyEnum
    question_text: str = Field(..., min_length=10)
    options: list[OptionBase] = Field(..., min_length=2)
    correct_option: str
    explanation: str | None = None
    tags: list[str] | None = []

    @field_validator("correct_option")
    @classmethod
    def validate_correct_option(cls, v: str, info: Any) -> str:  # noqa: N805
        if "options" in info.data:
            option_ids = [opt.id for opt in info.data["options"]]
            if v not in option_ids:
                raise ValueError(f"correct_option must be one of {option_ids}")
        return v


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    category_id: str | None = None
    difficulty: DifficultyEnum | None = None
    question_text: str | None = Field(None, min_length=10)
    options: list[OptionBase] | None = None
    correct_option: str | None = None
    explanation: str | None = None
    tags: list[str] | None = None
    is_active: bool | None = None


class QuestionResponse(QuestionBase):
    id: str
    is_active: bool
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuestionPublic(BaseModel):
    """Public question response (hides correct answer)."""

    id: str
    category_id: str
    difficulty: DifficultyEnum
    question_text: str
    options: list[OptionBase]
    tags: list[str] | None = []

    class Config:
        from_attributes = True


# ============= Quiz Models =============


class QuizConfig(BaseModel):
    category_id: str
    difficulty: str | None = None  # Can be "mixed" or a specific difficulty
    question_count: int = Field(default=10, ge=1, le=50)
    time_limit_seconds: int | None = None
    exclude_answered: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category_id": "epo",
                    "difficulty": "medium",
                    "question_count": 10,
                    "time_limit_seconds": 600,
                    "exclude_answered": False,
                }
            ]
        }
    }


class QuizStartResponse(BaseModel):
    session_id: str
    questions: list[QuestionPublic]


class AnswerSubmission(BaseModel):
    question_id: str
    selected_option: str
    time_taken_seconds: int = Field(ge=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question_id": "q_001",
                    "selected_option": "B",
                    "time_taken_seconds": 25,
                }
            ]
        }
    }


class AnswerResult(BaseModel):
    is_correct: bool
    correct_option: str
    explanation: str | None


class DifficultyStats(BaseModel):
    total: int
    correct: int


class QuizResult(BaseModel):
    session_id: str
    total_questions: int
    correct_answers: int
    accuracy: float
    total_time_seconds: int
    average_time_per_question: float
    difficulty_breakdown: dict[str, DifficultyStats]
    weak_areas: list[str]
    recommendations: list[str]


# ============= User Models =============


class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: str
    avatar_url: str | None = None
    role: str = "user"
    created_at: datetime

    class Config:
        from_attributes = True


# ============= User Stats Models =============


class UserStatsResponse(BaseModel):
    id: str
    user_id: str
    category_id: str | None
    category_name: str | None
    difficulty: str | None
    total_attempts: int
    correct_attempts: int
    accuracy: float
    avg_time_seconds: float | None
    last_practiced_at: datetime | None

    class Config:
        from_attributes = True


class UserProgressResponse(BaseModel):
    total_questions_answered: int
    overall_accuracy: float
    total_time_spent_seconds: int
    current_streak: int
    longest_streak: int
    categories_practiced: int
    favorite_category: str | None
    improvement_trend: str
    last_7_days_accuracy: float
    stats_by_category: list[UserStatsResponse]
    stats_by_difficulty: dict[str, dict]


class RecommendationResponse(BaseModel):
    recommended_category: str
    recommended_difficulty: str
    reason: str
    estimated_improvement: str | None = None


# ============= Admin Models =============


class BulkUploadResult(BaseModel):
    success_count: int
    error_count: int
    errors: list[dict]


class AdminStatsResponse(BaseModel):
    total_questions: int
    total_categories: int
    total_users: int
    questions_by_difficulty: dict[str, int]
    questions_by_category: dict[str, int]
    active_users_today: int
    quizzes_taken_today: int


# ============= Pagination Models =============


class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============= Quiz History Models =============


class QuizHistoryItem(BaseModel):
    id: str
    category_name: str
    difficulty: str
    score: int
    total_questions: int
    accuracy: float
    completed_at: datetime

    class Config:
        from_attributes = True
