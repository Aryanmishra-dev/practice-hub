"""API version header middleware.

Adds an ``API-Version`` response header to every request.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import get_settings

settings = get_settings()


class APIVersionMiddleware(BaseHTTPMiddleware):
    """Attach ``API-Version`` header to all responses."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["API-Version"] = settings.api_version
        return response
