"""Custom exception classes and FastAPI exception handlers."""

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger("exceptions")


# ============= Custom Exceptions =============


class QuizForgeError(Exception):
    """Base exception for all Quiz Forge errors."""

    def __init__(self, message: str, status_code: int = 500, detail: Any = None) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class NotFoundError(QuizForgeError):
    """Resource not found."""

    def __init__(self, resource: str, resource_id: str) -> None:
        super().__init__(
            message=f"{resource} not found: {resource_id}",
            status_code=404,
        )


class ValidationError(QuizForgeError):
    """Validation error."""

    def __init__(self, message: str, detail: Any = None) -> None:
        super().__init__(message=message, status_code=422, detail=detail)


class QuizSessionError(QuizForgeError):
    """Quiz session error."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=400)


# ============= Exception Handlers =============


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app.

    Args:
        app: The FastAPI application instance.
    """

    @app.exception_handler(QuizForgeError)
    async def quiz_forge_exception_handler(request: Request, exc: QuizForgeError) -> JSONResponse:
        logger.error("QuizForgeError: %s (status=%d)", exc.message, exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "detail": None,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Internal server error",
                "detail": None,
            },
        )
