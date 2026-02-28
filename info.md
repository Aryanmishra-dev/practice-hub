# 🏭 QUIZ-FORGE: Industry-Grade Repository Upgrade Prompt

> **Copy this entire prompt and use it with Claude (or any LLM) to upgrade your repository step by step.**

---

## 📋 MASTER PROMPT

```
You are a senior DevOps/MLOps engineer helping a data science student upgrade their full-stack project (QUIZ-FORGE) to industry-grade standards. The student only knows Python and Python-based frameworks — NO Node.js tooling for CI/CD or scripting. All automation, linting, and pipeline tooling must be Python-based.

The project stack is:
- Frontend: Next.js 14 (TypeScript) — linting handled by ESLint/Prettier (already configured)
- Backend: FastAPI (Python 3.11+) — this is where all Python tooling goes
- Database: Supabase (PostgreSQL)
- Container: Docker + Docker Compose
- CI/CD: GitHub Actions

Your job is to implement ALL of the following improvements, one section at a time, providing actual file contents (not pseudocode). Ask me which section to start with.

---

## SECTION 1: Python Backend — Code Quality Tooling

Set up the following tools for the FastAPI backend. Provide the exact config files.

### Tools to configure:
1. **Ruff** — ultra-fast Python linter + formatter (replaces flake8, isort, black)
2. **Pylint** — deep static analysis with a .pylintrc config
3. **Mypy** — strict type checking with mypy.ini
4. **pre-commit** — Git hooks that run all checks before every commit

### Deliverables:
- `backend/pyproject.toml` with [tool.ruff], [tool.mypy] sections
- `backend/.pylintrc` with sensible defaults (max-line-length=100, disable=C0114 for missing module docstrings, etc.)
- `.pre-commit-config.yaml` at repo root with hooks for: ruff, pylint, mypy, trailing-whitespace, end-of-file-fixer, check-yaml, check-json
- `backend/Makefile` with targets: lint, format, typecheck, test, all

---

## SECTION 2: Python Backend — Testing & Coverage

Set up a comprehensive test suite using pytest.

### Tools to configure:
1. **pytest** with pytest-asyncio for async FastAPI routes
2. **pytest-cov** for coverage reporting (aim for >80%)
3. **httpx** for async test client (AsyncClient)
4. **factory-boy or faker** for test data generation

### Deliverables:
- `backend/pytest.ini` or `[tool.pytest.ini_options]` in pyproject.toml
- `backend/tests/conftest.py` with fixtures: test app, async client, mock Supabase client
- `backend/tests/unit/test_quiz_service.py` — unit tests for quiz loading logic
- `backend/tests/integration/test_api_routes.py` — integration tests for /api/v1/categories and /api/v1/quiz endpoints
- `backend/tests/unit/test_models.py` — Pydantic model validation tests
- Coverage config: fail if coverage < 80%, generate HTML report

---

## SECTION 3: GitHub Actions CI Pipeline (Python-only tooling)

Create GitHub Actions workflows. All steps must use Python tools only (pip install, pytest, ruff, etc.). No npm/node steps for backend.

### Workflows to create:

#### `.github/workflows/backend-ci.yml`
Triggers: push/PR to main and develop
Jobs:
1. **lint** — checkout, setup Python 3.11, pip install ruff pylint mypy, run ruff check, pylint, mypy
2. **test** — checkout, setup Python 3.11, pip install -r requirements.txt -r requirements-dev.txt, run pytest with coverage, upload coverage report as artifact
3. **security** — run bandit (Python security linter) and safety (checks for vulnerable dependencies)
4. **docker-build** — build backend Docker image to verify it builds correctly

#### `.github/workflows/frontend-ci.yml`
Triggers: push/PR to main and develop
Jobs:
1. **lint** — setup Node.js, run npm ci, run eslint and prettier check
2. **typecheck** — run tsc --noEmit
3. **test** — run jest with coverage
4. **build** — run next build to verify production build succeeds

#### `.github/workflows/integration.yml`
Triggers: push to main only
Jobs:
1. Spin up full docker-compose stack
2. Run health check against backend /health endpoint (using Python requests or curl)
3. Run smoke tests using pytest against the running stack

---

## SECTION 4: Security Scanning

Add Python-based security tools.

### Tools:
1. **Bandit** — scans Python code for security issues (hardcoded passwords, SQL injection patterns, etc.)
2. **Safety** — checks all pip packages against known CVE database
3. **pip-audit** — alternative/complement to safety
4. **Trivy** (via GitHub Action) — scans Docker images for vulnerabilities

### Deliverables:
- `backend/.bandit` config file
- `backend/scripts/security_check.py` — Python script that runs bandit + safety and fails with non-zero exit if issues found
- GitHub Actions step using `aquasecurity/trivy-action` for Docker image scanning
- Add security job to backend-ci.yml

---

## SECTION 5: Docker & Docker Compose Hardening

Make Docker setup production-ready.

### Improvements:
1. **Multi-stage Dockerfile for backend** — builder stage (install deps) + runtime stage (minimal image)
2. **Non-root user** in both containers
3. **Health checks** in docker-compose.yml for both services
4. **Resource limits** (memory, CPU) in docker-compose.yml
5. **.dockerignore** files for both frontend and backend
6. **docker-compose.override.yml** for local dev (volume mounts, hot reload)
7. **docker-compose.prod.yml** for production (no volume mounts, restart policies)

### Deliverables:
- `backend/Dockerfile` (multi-stage, non-root)
- `frontend/Dockerfile` (multi-stage, non-root)  
- `docker-compose.yml` (base config)
- `docker-compose.override.yml` (dev)
- `docker-compose.prod.yml` (prod)
- `backend/.dockerignore`
- `frontend/.dockerignore`

---

## SECTION 6: Code Quality — Backend Architecture Improvements

Refactor the FastAPI backend to follow industry patterns.

### Patterns to implement:
1. **Repository Pattern** — separate data access layer from business logic
2. **Service Layer** — business logic separate from route handlers
3. **Dependency Injection** — use FastAPI's Depends() for services, config, DB clients
4. **Structured Logging** — replace print() with Python's logging module (JSON format for prod)
5. **Custom Exception Handlers** — global handlers returning consistent error schemas
6. **Environment-based config** — use pydantic-settings BaseSettings with .env.example

### Deliverables:
- `backend/app/core/config.py` — Settings class with pydantic-settings
- `backend/app/core/logging.py` — structured logger setup
- `backend/app/core/exceptions.py` — custom exception classes + FastAPI exception handlers
- `backend/app/repositories/quiz_repository.py` — data access layer
- `backend/app/services/quiz_service.py` — business logic
- Refactored `backend/app/api/v1/routes/quiz.py` using the service layer
- `.env.example` with all required environment variables documented

---

## SECTION 7: API Quality Improvements

Make the FastAPI API production-grade.

### Improvements:
1. **API versioning** — already have /api/v1, but add proper versioning headers
2. **Request/Response schemas** — strict Pydantic v2 models for all endpoints
3. **API rate limiting** — use slowapi (Python package, wraps limits library)
4. **Request ID middleware** — add X-Request-ID header to all responses
5. **Response caching** — use fastapi-cache2 with in-memory backend for quiz questions
6. **OpenAPI improvements** — add tags, descriptions, examples to all routes
7. **Health check endpoint** — /health returns version, uptime, dependency status

### Deliverables:
- `backend/app/middleware/request_id.py`
- `backend/app/middleware/rate_limiter.py` using slowapi
- Updated route files with full Pydantic schemas + OpenAPI docs
- `backend/app/api/v1/routes/health.py`
- `backend/requirements.txt` updated with: slowapi, fastapi-cache2, limits

---

## SECTION 8: Git Workflow & Branch Protection

Set up professional Git practices.

### Deliverables:
1. **`.github/PULL_REQUEST_TEMPLATE.md`** — PR template with checklist: tests added, linting passed, docs updated
2. **`.github/ISSUE_TEMPLATE/bug_report.md`** — structured bug report template
3. **`.github/ISSUE_TEMPLATE/feature_request.md`** — feature request template
4. **`.github/CODEOWNERS`** — define code ownership (use @yourusername for everything)
5. **`CONTRIBUTING.md`** — how to set up dev environment, run tests, submit PRs (Python-focused instructions)
6. **`CHANGELOG.md`** — initial changelog following Keep a Changelog format
7. **Branch naming convention** documented in CONTRIBUTING.md:
   - feature/description
   - fix/description  
   - chore/description

---

## SECTION 9: Documentation

Professional documentation setup.

### Deliverables:
1. **`README.md`** — full rewrite with: badges (CI status, coverage, Python version, license), architecture diagram (ASCII), quick start guide, API docs link, contributing section
2. **`docs/architecture.md`** — detailed architecture decisions
3. **`docs/api.md`** — API endpoints reference (auto-generated from OpenAPI if possible)
4. **`docs/development.md`** — full local setup guide (Python venv, Docker, env vars)
5. **`docs/deployment.md`** — production deployment guide
6. **Docstrings** — add Google-style docstrings to all Python functions/classes (mypy will enforce)

---

## SECTION 10: Monitoring & Observability (Bonus)

Add observability to the backend.

### Tools (all Python):
1. **prometheus-fastapi-instrumentator** — expose /metrics endpoint for Prometheus
2. **Python logging** with structlog — structured JSON logs
3. **Sentry SDK** — error tracking (free tier available)
4. **OpenTelemetry** — distributed tracing setup

### Deliverables:
- `backend/app/core/metrics.py` — Prometheus metrics setup
- `backend/app/core/tracing.py` — OpenTelemetry setup
- Updated `backend/app/main.py` with all middleware and instrumentation registered
- `docker-compose.monitoring.yml` — optional Prometheus + Grafana stack for local dev

---

## HOW TO USE THIS PROMPT

Start with Section 1 (Code Quality Tooling) and work your way through. Each section builds on the previous.

For each section, say:
"Implement Section X for my QUIZ-FORGE project"

And provide any additional context about your specific file structure if needed.
```

---

## 🗂️ RECOMMENDED IMPLEMENTATION ORDER

| Priority | Section | Time Estimate | Impact |
|----------|---------|---------------|--------|
| 🔴 Must | 1 — Python Linting (Ruff + Pylint + pre-commit) | 1-2 hours | High |
| 🔴 Must | 3 — GitHub Actions CI | 2-3 hours | High |
| 🔴 Must | 2 — pytest + Coverage | 2-3 hours | High |
| 🟡 Should | 5 — Docker Hardening | 1-2 hours | Medium |
| 🟡 Should | 6 — Backend Architecture | 3-4 hours | Medium |
| 🟡 Should | 4 — Security Scanning | 1 hour | Medium |
| 🟢 Nice | 7 — API Quality | 2-3 hours | Medium |
| 🟢 Nice | 8 — Git Workflow | 1 hour | Low |
| 🟢 Nice | 9 — Documentation | 2-3 hours | Medium |
| ⭐ Bonus | 10 — Monitoring | 2-3 hours | Low |

---

## 🐍 KEY PYTHON PACKAGES YOU'LL NEED

```bash
# Add to backend/requirements-dev.txt
ruff>=0.3.0           # Linter + formatter (replaces black, isort, flake8)
pylint>=3.0.0         # Deep static analysis
mypy>=1.8.0           # Type checking
pre-commit>=3.6.0     # Git hooks
bandit>=1.7.0         # Security scanning
safety>=3.0.0         # Dependency vulnerability check
pip-audit>=2.7.0      # Another dep vulnerability checker
pytest>=8.0.0         # Test runner
pytest-asyncio>=0.23.0 # Async test support
pytest-cov>=4.1.0     # Coverage
httpx>=0.26.0         # Async HTTP client for tests
faker>=22.0.0         # Test data generation
slowapi>=0.1.9        # Rate limiting for FastAPI
fastapi-cache2>=0.2.1 # Response caching
prometheus-fastapi-instrumentator>=6.1.0  # Metrics
```

---

## 📁 FINAL REPOSITORY STRUCTURE (Target)

```
quiz-forge/
├── .github/
│   ├── workflows/
│   │   ├── backend-ci.yml        ← Python lint + test + security
│   │   ├── frontend-ci.yml       ← ESLint + Jest + Next.js build
│   │   └── integration.yml       ← Full stack smoke tests
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/
│   │   ├── core/
│   │   │   ├── config.py         ← pydantic-settings
│   │   │   ├── logging.py        ← structured logging
│   │   │   ├── exceptions.py     ← custom exceptions
│   │   │   └── metrics.py        ← Prometheus
│   │   ├── middleware/
│   │   │   ├── request_id.py
│   │   │   └── rate_limiter.py
│   │   ├── repositories/         ← data access layer
│   │   └── services/             ← business logic
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── unit/
│   │   └── integration/
│   ├── pyproject.toml            ← ruff + mypy config
│   ├── .pylintrc
│   ├── pytest.ini
│   ├── Makefile                  ← make lint, make test, make all
│   └── Dockerfile                ← multi-stage, non-root
├── frontend/
│   └── Dockerfile                ← multi-stage, non-root
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── development.md
│   └── deployment.md
├── .pre-commit-config.yaml       ← Git hooks
├── .env.example                  ← documented env vars
├── docker-compose.yml
├── docker-compose.override.yml   ← dev
├── docker-compose.prod.yml       ← prod
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md                     ← badges + architecture diagram
```

---

## ✅ INDUSTRY-GRADE CHECKLIST

When complete, your repo should pass all of these:

- [ ] `pre-commit run --all-files` passes with zero errors
- [ ] `pytest --cov=app --cov-fail-under=80` passes
- [ ] `pylint app/` scores >= 8.0/10
- [ ] `mypy app/` shows no errors
- [ ] `bandit -r app/` shows no HIGH severity issues
- [ ] `safety check` shows no critical CVEs
- [ ] GitHub Actions: all 3 workflows pass on `main`
- [ ] Docker images build successfully with no root user
- [ ] `/health` endpoint returns 200 with dependency status
- [ ] OpenAPI docs at `/docs` are fully documented with examples
- [ ] README has CI badge showing green
- [ ] Coverage badge showing >= 80%
- [ ] All PRs require CI to pass before merge (branch protection rule)