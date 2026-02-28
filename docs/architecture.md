# Architecture

This document describes the architecture decisions behind Quiz Forge.

---

## Design Principles

1. **Separation of Concerns** — Routes handle HTTP, services handle logic, repositories handle data.
2. **Dependency Injection** — Services and repositories are injected via FastAPI `Depends()`.
3. **Fail Fast** — Pydantic v2 validates all input at the boundary; custom exceptions produce clean error responses.
4. **Observability First** — Every request gets a unique ID, structured logs, and Prometheus metrics.

---

## Backend Layers

```
Request
  │
  ▼
┌─────────────────────────────────┐
│  Middleware                      │
│  - CORS                         │
│  - Rate Limiting (slowapi)      │
│  - Request ID (X-Request-ID)    │
│  - API Version header           │
│  - Prometheus instrumentation   │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│  Route Handlers (api/v1/)       │
│  - questions.py                 │
│  - quiz.py                      │
│  - user.py                      │
│  - admin.py                     │
│  Thin layer: parse request,     │
│  call service, return response  │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│  Service Layer (services/)      │
│  - QuizService                  │
│  Business logic: session mgmt,  │
│  grading, result calculation    │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│  Repository Layer (repos/)      │
│  - QuizRepository               │
│  Data access: load JSON files,  │
│  transform questions, query     │
└─────────────┬───────────────────┘
              ▼
        ┌───────────┐
        │ JSON Files │
        └───────────┘
```

---

## Data Flow — Quiz Session

1. **Start** — `POST /api/v1/quiz/start` creates an in-memory session with shuffled questions.
2. **Answer** — `POST /api/v1/quiz/submit` grades each answer and stores it in the session.
3. **Complete** — `POST /api/v1/quiz/{session_id}/complete` calculates score, difficulty breakdown, and recommendations.

Sessions are stored in-memory (`dict`). For production, swap to Redis or a database-backed store.

---

## Error Handling

Custom exception classes in `core/exceptions.py`:

| Exception           | HTTP Status | Use Case                       |
|---------------------|-------------|--------------------------------|
| `NotFoundError`     | 404         | Resource not found             |
| `ValidationError`   | 422         | Business rule violation        |
| `QuizSessionError`  | 400         | Invalid session state          |

All exceptions return a consistent JSON envelope:

```json
{
  "detail": "Category not found: xyz",
  "error_code": "NOT_FOUND"
}
```

---

## Middleware Stack

Middleware executes in reverse registration order (last registered = first to execute):

1. **CORS** — Allow frontend origin
2. **APIVersionMiddleware** — Add `API-Version` header
3. **RequestIDMiddleware** — Add `X-Request-ID` header
4. **Rate Limiter** — 60 req/min per IP (slowapi)
5. **Prometheus** — Request duration, count, size metrics

---

## Frontend Architecture

- **Next.js 14 App Router** — File-based routing under `src/app/`
- **Server Components** — Default; client components marked with `"use client"`
- **TanStack Query** — Data fetching with caching and revalidation
- **Tailwind CSS + Radix UI** — Styling with accessible primitives
- **Recharts** — Progress analytics visualization

---

## Future Improvements

- Redis-backed quiz sessions
- PostgreSQL question storage (Supabase schema exists in `database/`)
- WebSocket real-time quiz mode
- OpenTelemetry distributed tracing
- Sentry error tracking integration
