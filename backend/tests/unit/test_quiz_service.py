"""Unit tests for quiz service / data loading logic."""

import pytest

from app.api.v1.questions import (
    CATEGORIES,
    load_questions_from_file,
    transform_question,
)


class TestLoadQuestionsFromFile:
    """Tests for loading questions from JSON files."""

    def test_load_all_questions(self) -> None:
        """Loading without difficulty returns all questions."""
        questions = load_questions_from_file()
        assert len(questions) > 0

    def test_load_easy_questions(self) -> None:
        """Loading with 'easy' difficulty returns only easy questions."""
        questions = load_questions_from_file("easy")
        assert len(questions) > 0
        for q in questions:
            assert q.get("difficulty") == "Easy"

    def test_load_normal_questions(self) -> None:
        """Loading with 'normal' difficulty returns questions."""
        questions = load_questions_from_file("normal")
        assert len(questions) > 0

    def test_load_hard_questions(self) -> None:
        """Loading with 'hard' difficulty returns questions."""
        questions = load_questions_from_file("hard")
        assert len(questions) > 0

    def test_load_expert_questions(self) -> None:
        """Loading with 'expert' difficulty returns questions."""
        questions = load_questions_from_file("expert")
        assert len(questions) > 0

    def test_load_invalid_difficulty_returns_all(self) -> None:
        """Loading with invalid difficulty returns all questions."""
        questions = load_questions_from_file("nonexistent")
        assert len(questions) > 0


class TestTransformQuestion:
    """Tests for question transformation from JSON to API format."""

    def test_basic_transform(self) -> None:
        """Question is transformed with all required fields."""
        raw = {
            "id": "test_1",
            "question": "What is ePO?",
            "options": ["A management tool", "A database", "An OS", "A language"],
            "answer": "A management tool",
            "difficulty": "Easy",
            "explanation": "ePO is a management tool.",
        }
        result = transform_question(raw)

        assert result["id"] == "test_1"
        assert result["category_id"] == "epo"
        assert result["difficulty"] == "easy"
        assert result["question_text"] == "What is ePO?"
        assert result["correct_option"] == "A"
        assert result["explanation"] == "ePO is a management tool."
        assert len(result["options"]) == 4

    def test_options_format(self) -> None:
        """Options are transformed to {id, text} objects."""
        raw = {
            "id": "test_2",
            "question": "Test?",
            "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
            "answer": "Opt B",
            "difficulty": "Normal",
        }
        result = transform_question(raw)

        assert result["options"][0] == {"id": "A", "text": "Opt A"}
        assert result["options"][1] == {"id": "B", "text": "Opt B"}
        assert result["correct_option"] == "B"

    def test_difficulty_mapping(self) -> None:
        """All difficulty levels are mapped correctly."""
        mapping = {"Easy": "easy", "Normal": "medium", "Hard": "hard", "Expert": "expert"}
        for raw_diff, expected in mapping.items():
            raw = {
                "id": f"test_{raw_diff}",
                "question": "Test question?",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "difficulty": raw_diff,
            }
            assert transform_question(raw)["difficulty"] == expected

    def test_missing_explanation(self) -> None:
        """Missing explanation returns None."""
        raw = {
            "id": "test_3",
            "question": "Test?",
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "difficulty": "Easy",
        }
        result = transform_question(raw)
        assert result["explanation"] is None


class TestCategories:
    """Tests for category data."""

    def test_categories_exist(self) -> None:
        """At least one category exists."""
        assert len(CATEGORIES) > 0

    def test_category_structure(self) -> None:
        """Categories have all required fields."""
        for cat in CATEGORIES:
            assert "id" in cat
            assert "name" in cat
            assert "is_active" in cat
            assert cat["is_active"] is True
