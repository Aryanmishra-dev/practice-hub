"""Session management using Redis for production scalability."""

import json
from typing import Any

import redis

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("session_manager")

settings = get_settings()


class SessionManager:
    """Manage quiz sessions using Redis."""

    def __init__(self) -> None:
        """Initialize Redis connection."""
        self.redis_client: redis.Redis[str] = redis.from_url(
            settings.redis_url, decode_responses=True
        )
        self.prefix = "quiz_session:"
        self.ttl = 3600  # 1 hour

    def create_session(self, session_id: str, session_data: dict[str, Any]) -> None:
        """Create a new quiz session in Redis."""
        try:
            self.redis_client.setex(
                f"{self.prefix}{session_id}",
                self.ttl,
                json.dumps(session_data),
            )
            logger.debug(f"Session {session_id} created in Redis")
        except redis.RedisError as e:
            logger.error(f"Failed to create session: {e}")
            raise

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve a quiz session from Redis."""
        try:
            data = self.redis_client.get(f"{self.prefix}{session_id}")
            if data:
                return json.loads(data)
            return None
        except redis.RedisError as e:
            logger.error(f"Failed to get session: {e}")
            raise

    def update_session(self, session_id: str, session_data: dict[str, Any]) -> None:
        """Update an existing quiz session in Redis."""
        try:
            self.redis_client.setex(
                f"{self.prefix}{session_id}",
                self.ttl,
                json.dumps(session_data),
            )
            logger.debug(f"Session {session_id} updated in Redis")
        except redis.RedisError as e:
            logger.error(f"Failed to update session: {e}")
            raise

    def delete_session(self, session_id: str) -> None:
        """Delete a quiz session from Redis."""
        try:
            self.redis_client.delete(f"{self.prefix}{session_id}")
            logger.debug(f"Session {session_id} deleted from Redis")
        except redis.RedisError as e:
            logger.error(f"Failed to delete session: {e}")
            raise

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists in Redis."""
        try:
            return self.redis_client.exists(f"{self.prefix}{session_id}") > 0
        except redis.RedisError as e:
            logger.error(f"Failed to check session existence: {e}")
            raise


# Global session manager instance
session_manager = SessionManager()
