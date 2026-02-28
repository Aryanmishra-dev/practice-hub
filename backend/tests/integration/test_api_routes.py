"""Integration tests for API routes."""

import pytest
from httpx import AsyncClient


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    @pytest.mark.integration
    async def test_health_check(self, async_client: AsyncClient) -> None:
        """Health endpoint returns 200 with status info."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "api_version" in data


class TestCategoriesEndpoint:
    """Tests for /api/v1/categories endpoints."""

    @pytest.mark.integration
    async def test_get_categories(self, async_client: AsyncClient) -> None:
        """GET /categories returns a list of categories."""
        response = await async_client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    @pytest.mark.integration
    async def test_category_structure(self, async_client: AsyncClient) -> None:
        """Each category has required fields."""
        response = await async_client.get("/api/v1/categories")
        cat = response.json()[0]
        assert "id" in cat
        assert "name" in cat
        assert "is_active" in cat
        assert "question_count" in cat
        assert cat["question_count"] > 0

    @pytest.mark.integration
    async def test_get_category_by_id(self, async_client: AsyncClient) -> None:
        """GET /categories/:id returns a single category."""
        response = await async_client.get("/api/v1/categories/epo")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "epo"

    @pytest.mark.integration
    async def test_get_category_not_found(self, async_client: AsyncClient) -> None:
        """GET /categories/:id with invalid ID returns 404."""
        response = await async_client.get("/api/v1/categories/nonexistent")
        assert response.status_code == 404


class TestQuestionsEndpoint:
    """Tests for /api/v1/categories/:id/questions endpoint."""

    @pytest.mark.integration
    async def test_get_questions(self, async_client: AsyncClient) -> None:
        """GET questions for a category returns questions."""
        response = await async_client.get("/api/v1/categories/epo/questions?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    @pytest.mark.integration
    async def test_questions_have_required_fields(self, async_client: AsyncClient) -> None:
        """Each question has all required fields."""
        response = await async_client.get("/api/v1/categories/epo/questions?limit=1")
        q = response.json()[0]
        assert "id" in q
        assert "question_text" in q
        assert "options" in q
        assert "correct_option" in q
        assert "difficulty" in q

    @pytest.mark.integration
    async def test_filter_by_difficulty(self, async_client: AsyncClient) -> None:
        """Difficulty filter returns only matching questions."""
        response = await async_client.get(
            "/api/v1/categories/epo/questions?difficulty=easy&limit=5"
        )
        assert response.status_code == 200
        for q in response.json():
            assert q["difficulty"] == "easy"


class TestQuizEndpoints:
    """Tests for /api/v1/quiz/* endpoints."""

    @pytest.mark.integration
    async def test_start_quiz(self, async_client: AsyncClient, sample_quiz_config: dict) -> None:
        """POST /quiz/start creates a session and returns questions."""
        response = await async_client.post("/api/v1/quiz/start", json=sample_quiz_config)
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "questions" in data
        assert len(data["questions"]) == sample_quiz_config["question_count"]

    @pytest.mark.integration
    async def test_submit_answer(self, async_client: AsyncClient, sample_quiz_config: dict) -> None:
        """POST /quiz/submit grades an answer correctly."""
        # Start a quiz to get a valid question ID
        start_resp = await async_client.post("/api/v1/quiz/start", json=sample_quiz_config)
        questions = start_resp.json()["questions"]
        question_id = questions[0]["id"]

        submission = {
            "question_id": question_id,
            "selected_option": "A",
            "time_taken_seconds": 10,
        }
        response = await async_client.post("/api/v1/quiz/submit", json=submission)
        assert response.status_code == 200
        data = response.json()
        assert "is_correct" in data
        assert "correct_option" in data

    @pytest.mark.integration
    async def test_complete_quiz(self, async_client: AsyncClient, sample_quiz_config: dict) -> None:
        """POST /quiz/:session_id/complete returns quiz results."""
        # Start a quiz
        start_resp = await async_client.post("/api/v1/quiz/start", json=sample_quiz_config)
        session_id = start_resp.json()["session_id"]
        questions = start_resp.json()["questions"]

        # Submit answers
        for q in questions:
            await async_client.post(
                "/api/v1/quiz/submit",
                json={
                    "question_id": q["id"],
                    "selected_option": "A",
                    "time_taken_seconds": 10,
                },
            )

        # Complete quiz
        response = await async_client.post(f"/api/v1/quiz/{session_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert "total_questions" in data
        assert "correct_answers" in data
        assert "accuracy" in data
        assert "difficulty_breakdown" in data

    @pytest.mark.integration
    async def test_complete_invalid_session(self, async_client: AsyncClient) -> None:
        """Completing a non-existent session returns 400."""
        response = await async_client.post("/api/v1/quiz/invalid_session/complete")
        assert response.status_code == 400


class TestUserEndpoints:
    """Tests for /api/v1/user/* endpoints."""

    @pytest.mark.integration
    async def test_get_user_progress(self, async_client: AsyncClient) -> None:
        """GET /user/progress returns mock progress data."""
        response = await async_client.get("/api/v1/user/progress")
        assert response.status_code == 200
        data = response.json()
        assert "total_questions_answered" in data
        assert "overall_accuracy" in data

    @pytest.mark.integration
    async def test_get_user_history(self, async_client: AsyncClient) -> None:
        """GET /user/history returns paginated history."""
        response = await async_client.get("/api/v1/user/history?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    @pytest.mark.integration
    async def test_get_recommendations(self, async_client: AsyncClient) -> None:
        """GET /user/recommendations returns a recommendation."""
        response = await async_client.get("/api/v1/user/recommendations")
        assert response.status_code == 200
        data = response.json()
        assert "recommended_category" in data
        assert "recommended_difficulty" in data
