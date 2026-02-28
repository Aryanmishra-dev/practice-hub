"""Test configuration and shared fixtures."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_app() -> FastAPI:
    """Return the FastAPI application instance."""
    return app


@pytest.fixture
async def async_client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing API endpoints."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_quiz_config() -> dict[str, Any]:
    """Sample quiz configuration for testing."""
    return {
        "category_id": "epo",
        "difficulty": "easy",
        "question_count": 5,
    }


@pytest.fixture
def sample_answer_submission() -> dict[str, Any]:
    """Sample answer submission for testing."""
    return {
        "question_id": "easy_1",
        "selected_option": "A",
        "time_taken_seconds": 30,
    }
