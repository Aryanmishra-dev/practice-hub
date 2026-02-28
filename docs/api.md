# API Reference

Base URL: `http://localhost:8000`

All quiz endpoints are prefixed with `/api/v1`. Interactive docs are available at `/docs` (Swagger) and `/redoc`.

---

## Health & Monitoring

| Method | Endpoint   | Description                     |
|--------|------------|---------------------------------|
| GET    | `/health`  | Service status and version      |
| GET    | `/metrics` | Prometheus metrics (if enabled) |

---

## Categories

| Method | Endpoint                              | Description                |
|--------|---------------------------------------|----------------------------|
| GET    | `/api/v1/categories`                  | List all active categories |
| GET    | `/api/v1/categories/{category_id}`    | Get a single category      |
| GET    | `/api/v1/categories/{id}/questions`   | Get questions for a category |

### Query Parameters — `/categories/{id}/questions`

| Param      | Type   | Default | Description               |
|------------|--------|---------|---------------------------|
| difficulty | string | null    | Filter: easy, medium, hard, expert |
| limit      | int    | 50      | Max questions (1–100)     |

---

## Questions

| Method | Endpoint                        | Description                      |
|--------|---------------------------------|----------------------------------|
| GET    | `/api/v1/questions/{question_id}` | Get a question with correct answer |

---

## Quiz Sessions

| Method | Endpoint                            | Description                    |
|--------|-------------------------------------|--------------------------------|
| POST   | `/api/v1/quiz/start`                | Start a new quiz session       |
| POST   | `/api/v1/quiz/submit`               | Submit an answer               |
| POST   | `/api/v1/quiz/{session_id}/complete`| Complete and get results       |
| GET    | `/api/v1/quiz/{session_id}/result`  | Get results for a completed quiz |

### Request Body — `POST /quiz/start`

```json
{
  "category_id": "epo",
  "difficulty": "medium",
  "question_count": 10,
  "time_limit_seconds": 600,
  "exclude_answered": false
}
```

### Request Body — `POST /quiz/submit`

```json
{
  "question_id": "q_001",
  "selected_option": "B",
  "time_taken_seconds": 25
}
```

### Response — `POST /quiz/submit`

```json
{
  "is_correct": true,
  "correct_option": "B",
  "explanation": "The correct answer is B because..."
}
```

---

## User (Mock Data)

| Method | Endpoint                               | Description                  |
|--------|----------------------------------------|------------------------------|
| GET    | `/api/v1/user/progress`                | Progress overview            |
| GET    | `/api/v1/user/analytics/{category_id}` | Category-level analytics     |
| GET    | `/api/v1/user/history`                 | Paginated quiz history       |
| GET    | `/api/v1/user/recommendations`         | Practice recommendations     |

---

## Admin (Requires Auth)

| Method | Endpoint                           | Description                |
|--------|------------------------------------|----------------------------|
| GET    | `/api/v1/admin/stats`              | Dashboard statistics       |
| POST   | `/api/v1/admin/categories/bulk`    | Bulk upload categories     |
| POST   | `/api/v1/admin/questions/bulk`     | Bulk upload questions      |
| GET    | `/api/v1/admin/questions`          | Paginated question list    |
| PUT    | `/api/v1/admin/questions/{id}`     | Update a question          |
| DELETE | `/api/v1/admin/questions/{id}`     | Soft-delete a question     |

Admin endpoints require a valid JWT token via the `Authorization: Bearer <token>` header.

---

## Response Headers

Every response includes:

| Header         | Description                           |
|----------------|---------------------------------------|
| `X-Request-ID` | Unique request identifier (UUID)      |
| `API-Version`  | Current API version (e.g. `v1`)       |

---

## Rate Limiting

All endpoints are rate-limited to **60 requests per minute** per IP address. When exceeded, a `429 Too Many Requests` response is returned.

---

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "NOT_FOUND"
}
```

| Status | Error Code      | Description                 |
|--------|------------------|-----------------------------|
| 400    | QUIZ_SESSION_ERROR | Invalid quiz session state |
| 404    | NOT_FOUND        | Resource not found          |
| 422    | VALIDATION_ERROR | Input validation failed     |
| 429    | —                | Rate limit exceeded         |
