"""Quiz Forge — FastAPI application entry point."""

import time
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import register_exception_handlers
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.api_version import APIVersionMiddleware
from app.middleware.rate_limiter import limiter
from app.api.v1.router import api_router

settings = get_settings()
root_logger = setup_logging()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler — startup and shutdown events."""
    logger.info("Starting Quiz Forge API v%s", settings.api_version)
    yield
    logger.info("Shutting down Quiz Forge API")


app = FastAPI(
    title="Quiz Forge API",
    description=(
        "Industry-grade backend API for the Quiz Forge MCQ Practice Platform. "
        "Provides quiz categories, questions, session management, and analytics."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "health", "description": "Health check and status"},
        {"name": "questions", "description": "Categories and questions"},
        {"name": "quiz", "description": "Quiz sessions and grading"},
        {"name": "user", "description": "User progress and analytics"},
        {"name": "admin", "description": "Admin management"},
    ],
)

# ============= Middleware =============

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Request ID
app.add_middleware(RequestIDMiddleware)

# API version
app.add_middleware(APIVersionMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Prometheus metrics (optional — import if available)
try:
    from prometheus_fastapi_instrumentator import Instrumentator

    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    logger.info("Prometheus metrics enabled at /metrics")
except ImportError:
    logger.debug("prometheus-fastapi-instrumentator not installed, skipping metrics")

# OpenTelemetry tracing (optional)
try:
    from app.core.tracing import setup_tracing

    setup_tracing(app)
except ImportError:
    logger.debug("OpenTelemetry packages not installed, skipping tracing")


# ============= Health Check =============

@app.get("/health", tags=["health"])
async def health_check() -> dict[str, Any]:
    """Health check endpoint.

    Returns service status, version, and uptime metadata.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_version": settings.api_version,
        "environment": "debug" if settings.debug else "production",
    }


# ============= Routes =============

app.include_router(api_router, prefix=f"/api/{settings.api_version}")


# ============= Main =============

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
