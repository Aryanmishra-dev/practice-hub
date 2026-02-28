from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


class DifficultyEnum(str, Enum):
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
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: str
    is_active: bool
    question_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Question Models =============

class QuestionBase(BaseModel):
    category_id: str
    difficulty: DifficultyEnum
    question_text: str = Field(..., min_length=10)
    options: List[OptionBase] = Field(..., min_length=2)
    correct_option: str
    explanation: Optional[str] = None
    tags: Optional[List[str]] = []

    @validator("correct_option")
    def validate_correct_option(cls, v, values):
        if "options" in values:
            option_ids = [opt.id for opt in values["options"]]
            if v not in option_ids:
                raise ValueError(f"correct_option must be one of {option_ids}")
        return v


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    category_id: Optional[str] = None
    difficulty: Optional[DifficultyEnum] = None
    question_text: Optional[str] = Field(None, min_length=10)
    options: Optional[List[OptionBase]] = None
    correct_option: Optional[str] = None
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


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
    options: List[OptionBase]
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True


# ============= Quiz Models =============

class QuizConfig(BaseModel):
    category_id: str
    difficulty: Optional[str] = None  # Can be "mixed" or a specific difficulty
    question_count: int = Field(default=10, ge=1, le=50)
    time_limit_seconds: Optional[int] = None
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
    questions: List[QuestionPublic]


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
    explanation: Optional[str]


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
    weak_areas: List[str]
    recommendations: List[str]


# ============= User Models =============

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: str
    avatar_url: Optional[str] = None
    role: str = "user"
    created_at: datetime

    class Config:
        from_attributes = True


# ============= User Stats Models =============

class UserStatsResponse(BaseModel):
    id: str
    user_id: str
    category_id: Optional[str]
    category_name: Optional[str]
    difficulty: Optional[str]
    total_attempts: int
    correct_attempts: int
    accuracy: float
    avg_time_seconds: Optional[float]
    last_practiced_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserProgressResponse(BaseModel):
    total_questions_answered: int
    overall_accuracy: float
    total_time_spent_seconds: int
    current_streak: int
    longest_streak: int
    categories_practiced: int
    favorite_category: Optional[str]
    improvement_trend: str
    last_7_days_accuracy: float
    stats_by_category: List[UserStatsResponse]
    stats_by_difficulty: dict[str, dict]


class RecommendationResponse(BaseModel):
    recommended_category: str
    recommended_difficulty: str
    reason: str
    estimated_improvement: Optional[str] = None


# ============= Admin Models =============

class BulkUploadResult(BaseModel):
    success_count: int
    error_count: int
    errors: List[dict]


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
    items: List[Any]
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
