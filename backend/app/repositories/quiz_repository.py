"""Repository layer — data access for quiz questions and categories.

Separates data-loading logic from API routes and business logic.
"""

import json
import random
from pathlib import Path

from app.core.logging import get_logger

logger = get_logger("repositories.quiz")

# Path to quiz JSON files
# In local dev: files are at the project root (../../.. from this file)
# In Docker: files are copied to /app/data/
_PACKAGE_ROOT = Path(__file__).parent.parent.parent  # backend/
_PROJECT_ROOT = _PACKAGE_ROOT.parent  # QUIZ-FORGE/
_DATA_DIR = _PACKAGE_ROOT / "data"  # backend/data/


def _resolve_data_file(filename: str) -> Path:
    """Find quiz data file, checking Docker path first, then project root."""
    docker_path = _DATA_DIR / filename
    if docker_path.exists():
        return docker_path
    return _PROJECT_ROOT / filename


QUIZ_FILES: dict[str, Path] = {
    "easy": _resolve_data_file("quiz_easy.json"),
    "normal": _resolve_data_file("quiz_normal.json"),
    "hard": _resolve_data_file("quiz_hard.json"),
    "expert": _resolve_data_file("quiz_expert.json"),
    "all": _resolve_data_file("quiz_bank.json"),
}

DIFFICULTY_FILE_MAP: dict[str, str] = {
    "easy": "easy",
    "medium": "normal",
    "hard": "hard",
    "expert": "expert",
}

DIFFICULTY_DISPLAY_MAP: dict[str, str] = {
    "Easy": "easy",
    "Normal": "medium",
    "Hard": "hard",
    "Expert": "expert",
}

# In-memory category store
CATEGORIES: list[dict] = [
    {
        "id": "epo",
        "name": "ePO Server Administration",
        "description": "Questions about Trellix ePO server installation, configuration, and management",
        "icon": "file-text",
        "display_order": 1,
        "is_active": True,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }
]


class QuizRepository:
    """Data access layer for quiz questions and categories."""

    def get_all_categories(self) -> list[dict]:
        """Return all active categories with question counts.

        Returns:
            List of category dictionaries.
        """
        categories = []
        total_questions = len(self.load_questions_from_file())
        for cat in CATEGORIES:
            cat_copy = cat.copy()
            cat_copy["question_count"] = total_questions
            categories.append(cat_copy)
        return categories

    def get_category_by_id(self, category_id: str) -> dict | None:
        """Get a single category by ID.

        Args:
            category_id: The category identifier.

        Returns:
            Category dict or None if not found.
        """
        for cat in CATEGORIES:
            if cat["id"] == category_id:
                cat_copy = cat.copy()
                cat_copy["question_count"] = len(self.load_questions_from_file())
                return cat_copy
        return None

    def load_questions_from_file(self, difficulty: str | None = None) -> list[dict]:
        """Load raw questions from JSON files.

        Args:
            difficulty: Optional difficulty filter (easy/normal/hard/expert).

        Returns:
            List of raw question dictionaries from JSON.
        """
        questions: list[dict] = []

        if difficulty and difficulty in QUIZ_FILES:
            file_path = QUIZ_FILES[difficulty]
            if file_path.exists():
                with file_path.open() as f:
                    data = json.load(f)
                    questions.extend(data)
        else:
            for diff, file_path in QUIZ_FILES.items():
                if diff != "all" and file_path.exists():
                    with file_path.open() as f:
                        data = json.load(f)
                        questions.extend(data)

        logger.debug("Loaded %d questions (difficulty=%s)", len(questions), difficulty)
        return questions

    def transform_question(self, q: dict) -> dict:
        """Transform a raw JSON question into the API format.

        Args:
            q: Raw question dict from JSON file.

        Returns:
            Transformed question dict with standardized fields.
        """
        options = [
            {"id": chr(65 + i), "text": opt_text} for i, opt_text in enumerate(q.get("options", []))
        ]

        correct_answer = q.get("answer", "")
        correct_option = "A"
        for i, opt_text in enumerate(q.get("options", [])):
            if opt_text == correct_answer:
                correct_option = chr(65 + i)
                break

        return {
            "id": q.get("id", ""),
            "category_id": "epo",
            "difficulty": DIFFICULTY_DISPLAY_MAP.get(q.get("difficulty", "Easy"), "easy"),
            "question_text": q.get("question", ""),
            "options": options,
            "correct_option": correct_option,
            "explanation": q.get("explanation"),
            "tags": [],
            "is_active": True,
            "version": 1,
        }

    def get_questions(
        self,
        category_id: str,
        difficulty: str | None = None,
        limit: int = 50,
        shuffle: bool = True,
    ) -> list[dict]:
        """Get transformed questions for a category.

        Args:
            category_id: The category to fetch questions for.
            difficulty: Optional difficulty filter.
            limit: Maximum number of questions.
            shuffle: Whether to randomize order.

        Returns:
            List of transformed question dicts.
        """
        file_difficulty = DIFFICULTY_FILE_MAP.get(difficulty) if difficulty else None
        raw = self.load_questions_from_file(file_difficulty)
        questions = [self.transform_question(q) for q in raw]
        questions = [q for q in questions if q["category_id"] == category_id]

        if shuffle:
            random.shuffle(questions)

        return questions[:limit]

    def get_question_by_id(self, question_id: str) -> dict | None:
        """Find a single question by its ID.

        Args:
            question_id: The question identifier.

        Returns:
            Transformed question dict or None.
        """
        raw = self.load_questions_from_file()
        for q in raw:
            if q.get("id") == question_id:
                return self.transform_question(q)
        return None
