"""Service layer — business logic for quiz operations.

Contains quiz session management, answer grading, and result calculation.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from app.core.exceptions import NotFoundError, QuizSessionError
from app.core.logging import get_logger
from app.repositories.quiz_repository import QuizRepository

logger = get_logger("services.quiz")

# Import custom Prometheus metrics (optional — graceful if not available)
try:
    from app.core.metrics import (
        QUIZ_SESSIONS_STARTED,
        ANSWERS_GRADED,
        QUIZ_SCORE_DISTRIBUTION,
        QUESTION_RESPONSE_TIME,
    )

    _METRICS_AVAILABLE = True
except ImportError:
    _METRICS_AVAILABLE = False

# In-memory session store (use Redis in production)
quiz_sessions: dict[str, dict] = {}


class QuizService:
    """Business logic for quiz operations."""

    def __init__(self, repository: QuizRepository) -> None:
        self.repo = repository

    def get_categories(self) -> list[dict]:
        """Get all active categories.

        Returns:
            List of category dicts with question counts.
        """
        return self.repo.get_all_categories()

    def get_category(self, category_id: str) -> dict:
        """Get a single category by ID.

        Args:
            category_id: The category identifier.

        Returns:
            Category dict.

        Raises:
            NotFoundError: If category doesn't exist.
        """
        cat = self.repo.get_category_by_id(category_id)
        if not cat:
            raise NotFoundError("Category", category_id)
        return cat

    def get_questions(
        self,
        category_id: str,
        difficulty: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """Get questions for a category.

        Args:
            category_id: The category identifier.
            difficulty: Optional difficulty filter.
            limit: Maximum questions to return.

        Returns:
            List of question dicts.
        """
        return self.repo.get_questions(category_id, difficulty, limit)

    def get_question(self, question_id: str) -> dict:
        """Get a single question by ID.

        Args:
            question_id: The question identifier.

        Returns:
            Question dict.

        Raises:
            NotFoundError: If question doesn't exist.
        """
        q = self.repo.get_question_by_id(question_id)
        if not q:
            raise NotFoundError("Question", question_id)
        return q

    def start_quiz(
        self,
        category_id: str,
        difficulty: Optional[str] = None,
        question_count: int = 10,
    ) -> dict:
        """Start a new quiz session.

        Args:
            category_id: Category for the quiz.
            difficulty: Difficulty filter (or 'mixed').
            question_count: Number of questions.

        Returns:
            Dict with session_id and public questions.

        Raises:
            NotFoundError: If no questions found.
        """
        diff = difficulty if difficulty != "mixed" else None
        file_map = {"easy": "easy", "medium": "normal", "hard": "hard", "expert": "expert"}
        file_diff = file_map.get(diff) if diff else None

        raw = self.repo.load_questions_from_file(file_diff)
        if not raw:
            raise NotFoundError("Questions", f"difficulty={difficulty}")

        import random

        questions = [self.repo.transform_question(q) for q in raw]
        random.shuffle(questions)
        questions = questions[:question_count]

        session_id = f"session_{uuid.uuid4().hex[:12]}"
        quiz_sessions[session_id] = {
            "id": session_id,
            "category_id": category_id,
            "difficulty": difficulty,
            "questions": questions,
            "answers": {},
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
        }

        logger.info("Started quiz session %s (%d questions)", session_id, len(questions))

        if _METRICS_AVAILABLE:
            QUIZ_SESSIONS_STARTED.labels(
                category_id=category_id,
                difficulty=difficulty or "mixed",
            ).inc()

        # Return public questions (no correct answer)
        public_questions = [
            {
                "id": q["id"],
                "category_id": q["category_id"],
                "difficulty": q["difficulty"],
                "question_text": q["question_text"],
                "options": q["options"],
                "tags": q.get("tags", []),
            }
            for q in questions
        ]

        return {"session_id": session_id, "questions": public_questions}

    def submit_answer(
        self,
        question_id: str,
        selected_option: str,
        time_taken_seconds: int,
    ) -> dict:
        """Grade a submitted answer.

        Args:
            question_id: The question being answered.
            selected_option: The selected option ID.
            time_taken_seconds: Time taken to answer.

        Returns:
            Dict with is_correct, correct_option, explanation.

        Raises:
            NotFoundError: If question not found.
        """
        # Search in active sessions first
        question = None
        session = None

        for sess in quiz_sessions.values():
            for q in sess["questions"]:
                if q["id"] == question_id:
                    question = q
                    session = sess
                    break
            if question:
                break

        # Fallback to file lookup
        if not question:
            question = self.repo.get_question_by_id(question_id)

        if not question:
            raise NotFoundError("Question", question_id)

        is_correct = selected_option == question["correct_option"]

        if _METRICS_AVAILABLE:
            ANSWERS_GRADED.labels(is_correct=str(is_correct).lower()).inc()
            QUESTION_RESPONSE_TIME.observe(time_taken_seconds)

        if session:
            session["answers"][question_id] = {
                "selected_option": selected_option,
                "is_correct": is_correct,
                "time_taken_seconds": time_taken_seconds,
                "answered_at": datetime.now(timezone.utc).isoformat(),
            }

        return {
            "is_correct": is_correct,
            "correct_option": question["correct_option"],
            "explanation": question.get("explanation"),
        }

    def complete_quiz(self, session_id: str) -> dict:
        """Complete a quiz session and calculate results.

        Args:
            session_id: The session to complete.

        Returns:
            Quiz result dict.

        Raises:
            QuizSessionError: If session not found.
        """
        if session_id not in quiz_sessions:
            raise QuizSessionError(f"Quiz session not found: {session_id}")

        session = quiz_sessions[session_id]
        session["completed_at"] = datetime.now(timezone.utc).isoformat()

        questions = session["questions"]
        answers = session["answers"]

        total_questions = len(questions)
        correct_answers = sum(1 for a in answers.values() if a["is_correct"])
        total_time = sum(a["time_taken_seconds"] for a in answers.values())

        # Difficulty breakdown
        difficulty_breakdown: dict[str, dict[str, int]] = {}
        for q in questions:
            diff = q["difficulty"]
            if diff not in difficulty_breakdown:
                difficulty_breakdown[diff] = {"total": 0, "correct": 0}
            difficulty_breakdown[diff]["total"] += 1
            answer = answers.get(q["id"])
            if answer and answer["is_correct"]:
                difficulty_breakdown[diff]["correct"] += 1

        # Recommendations
        weak_areas = []
        recommendations = []
        for diff, stats in difficulty_breakdown.items():
            if stats["total"] > 0:
                accuracy = stats["correct"] / stats["total"]
                if accuracy < 0.6:
                    weak_areas.append(diff)
                    recommendations.append(f"Practice more {diff} level questions")

        if not recommendations:
            recommendations.append("Great job! Keep practicing to maintain your skills.")

        logger.info(
            "Quiz %s completed: %d/%d correct (%.1f%%)",
            session_id,
            correct_answers,
            total_questions,
            (correct_answers / total_questions * 100) if total_questions > 0 else 0,
        )

        score_pct = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
        if _METRICS_AVAILABLE:
            QUIZ_SCORE_DISTRIBUTION.observe(score_pct)

        return {
            "session_id": session_id,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": score_pct,
            "total_time_seconds": total_time,
            "average_time_per_question": round(total_time / total_questions, 2) if total_questions > 0 else 0,
            "difficulty_breakdown": difficulty_breakdown,
            "weak_areas": weak_areas,
            "recommendations": recommendations,
        }
