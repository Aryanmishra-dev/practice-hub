# Quiz Forge

[![Backend CI](https://github.com/theogengineer/QUIZ-FORGE/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/theogengineer/QUIZ-FORGE/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/theogengineer/QUIZ-FORGE/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/theogengineer/QUIZ-FORGE/actions/workflows/frontend-ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![License](https://img.shields.io/badge/license-MIT-green)

> Industry-grade MCQ Practice Platform for Trellix ePO Server Administration certification prep.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│        Next.js 14 · React 18 · Tailwind CSS             │
│        TypeScript · TanStack Query · Radix UI           │
│                  http://localhost:3000                   │
└────────────────────────┬────────────────────────────────┘
                         │  REST / JSON
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      Backend                            │
│            FastAPI · Python 3.11+ · Pydantic v2         │
│                  http://localhost:8000                   │
│                                                         │
│   ┌──────────┐   ┌───────────┐   ┌──────────────────┐  │
│   │  Routes   │──▶│  Service  │──▶│   Repository     │  │
│   │  (API)    │   │  (Logic)  │   │  (Data Access)   │  │
│   └──────────┘   └───────────┘   └──────────────────┘  │
│                                         │               │
│   Middleware: CORS · Rate Limit ·       │               │
│   Request ID · API Version · Metrics    ▼               │
│                                  ┌─────────────┐       │
│                                  │  JSON Files  │       │
│                                  │  (quiz data) │       │
│                                  └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Clone & configure

```bash
git clone https://github.com/theogengineer/QUIZ-FORGE.git
cd QUIZ-FORGE
cp .env.example backend/.env
```

### 2. Start the backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000** to use the app and **http://localhost:8000/docs** for the interactive API docs.

### Docker (alternative)

```bash
docker compose up --build
```

---

## API Documentation

Interactive docs are available when the backend is running:

| URL             | Format    |
|-----------------|-----------|
| `/docs`         | Swagger UI |
| `/redoc`        | ReDoc      |
| `/openapi.json` | OpenAPI 3  |
| `/metrics`      | Prometheus |
| `/health`       | Health check |

See [docs/api.md](docs/api.md) for a written reference.

---

## Development

```bash
cd backend

make lint         # Ruff + Pylint
make format       # Auto-format with Ruff
make typecheck    # Mypy strict mode
make test         # Pytest with coverage
make security     # Bandit + pip-audit
make all          # Run everything
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## Project Structure

```
backend/
  app/
    api/v1/          # Route handlers (questions, quiz, user, admin)
    core/            # Config, logging, security, exceptions
    middleware/       # Request ID, rate limiting, API versioning
    models/          # Pydantic v2 schemas
    repositories/    # Data access layer
    services/        # Business logic layer
  tests/             # Unit + integration tests

frontend/
  src/
    app/             # Next.js App Router pages
    components/      # UI and quiz components
    lib/             # API client, utilities
```

---

## Tech Stack

| Layer        | Technology                                    |
|------------- |-----------------------------------------------|
| Frontend     | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend      | FastAPI, Python 3.11+, Pydantic v2, Uvicorn   |
| Data         | JSON quiz files, Supabase PostgreSQL (optional)|
| Testing      | Pytest, Jest, httpx                           |
| Linting      | Ruff, Pylint, Mypy, ESLint, Prettier          |
| CI/CD        | GitHub Actions (lint, test, security, Docker)  |
| Security     | Bandit, pip-audit, Trivy, slowapi rate limiting|
| Monitoring   | Prometheus metrics, structured logging         |
| Containers   | Docker multi-stage builds, Docker Compose      |

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
