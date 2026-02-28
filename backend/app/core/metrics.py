"""Prometheus metrics setup.

Configures the ``prometheus-fastapi-instrumentator`` and exposes custom
business metrics (quiz sessions started, answers graded, etc.).
"""

from prometheus_client import Counter, Histogram

# ============= Custom Business Metrics =============

QUIZ_SESSIONS_STARTED = Counter(
    "quiz_sessions_started_total",
    "Total number of quiz sessions started",
    ["category_id", "difficulty"],
)

ANSWERS_GRADED = Counter(
    "answers_graded_total",
    "Total number of answers graded",
    ["is_correct"],
)

QUIZ_SCORE_DISTRIBUTION = Histogram(
    "quiz_score_percent",
    "Distribution of quiz scores (percent correct)",
    buckets=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
)

QUESTION_RESPONSE_TIME = Histogram(
    "question_response_time_seconds",
    "Time taken by users to answer a question",
    buckets=[5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 300],
)
