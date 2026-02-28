"""Unit tests for Pydantic model validation."""

import pytest
from pydantic import ValidationError

from app.models.schemas import (
    AnswerSubmission,
    CategoryCreate,
    DifficultyEnum,
    OptionBase,
    QuestionPublic,
    QuizConfig,
)


class TestDifficultyEnum:
    """Tests for DifficultyEnum."""

    def test_valid_difficulties(self) -> None:
        """All valid difficulty values are accepted."""
        for diff in ["easy", "medium", "hard", "expert"]:
            assert DifficultyEnum(diff).value == diff

    def test_invalid_difficulty(self) -> None:
        """Invalid difficulty raises ValueError."""
        with pytest.raises(ValueError):
            DifficultyEnum("nightmare")


class TestOptionBase:
    """Tests for OptionBase model."""

    def test_valid_option(self) -> None:
        """Valid option is created successfully."""
        opt = OptionBase(id="A", text="Answer A")
        assert opt.id == "A"
        assert opt.text == "Answer A"


class TestCategoryCreate:
    """Tests for CategoryCreate model."""

    def test_valid_category(self) -> None:
        """Valid category is created."""
        cat = CategoryCreate(name="Test Category", description="A test", display_order=1)
        assert cat.name == "Test Category"

    def test_empty_name_rejected(self) -> None:
        """Empty category name is rejected."""
        with pytest.raises(ValidationError):
            CategoryCreate(name="", display_order=1)

    def test_long_name_rejected(self) -> None:
        """Category name > 100 chars is rejected."""
        with pytest.raises(ValidationError):
            CategoryCreate(name="x" * 101, display_order=1)


class TestQuizConfig:
    """Tests for QuizConfig model."""

    def test_default_values(self) -> None:
        """Default quiz config values are set."""
        config = QuizConfig(category_id="epo")
        assert config.question_count == 10
        assert config.difficulty is None
        assert config.exclude_answered is False

    def test_question_count_min(self) -> None:
        """Question count below minimum is rejected."""
        with pytest.raises(ValidationError):
            QuizConfig(category_id="epo", question_count=0)

    def test_question_count_max(self) -> None:
        """Question count above maximum is rejected."""
        with pytest.raises(ValidationError):
            QuizConfig(category_id="epo", question_count=51)

    def test_valid_config(self) -> None:
        """Fully specified config is valid."""
        config = QuizConfig(
            category_id="epo",
            difficulty="easy",
            question_count=20,
            time_limit_seconds=600,
        )
        assert config.category_id == "epo"
        assert config.question_count == 20


class TestAnswerSubmission:
    """Tests for AnswerSubmission model."""

    def test_valid_submission(self) -> None:
        """Valid answer submission is accepted."""
        sub = AnswerSubmission(question_id="q1", selected_option="A", time_taken_seconds=15)
        assert sub.question_id == "q1"
        assert sub.time_taken_seconds == 15

    def test_negative_time_rejected(self) -> None:
        """Negative time is rejected."""
        with pytest.raises(ValidationError):
            AnswerSubmission(question_id="q1", selected_option="A", time_taken_seconds=-1)


class TestQuestionPublic:
    """Tests for QuestionPublic model (no correct_option)."""

    def test_public_question_no_answer(self) -> None:
        """Public question model does not include correct_option."""
        q = QuestionPublic(
            id="q1",
            category_id="epo",
            difficulty=DifficultyEnum.easy,
            question_text="What is ePO?",
            options=[OptionBase(id="A", text="Tool"), OptionBase(id="B", text="Database")],
        )
        assert not hasattr(q, "correct_option") or "correct_option" not in q.model_fields
