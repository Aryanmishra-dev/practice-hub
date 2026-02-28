# Development Guide

Complete guide to setting up Quiz Forge for local development.

---

## Prerequisites

| Tool       | Version   | Purpose           |
|------------|-----------|-------------------|
| Python     | 3.11+     | Backend runtime   |
| Node.js    | 18+       | Frontend runtime  |
| Git        | Latest    | Version control   |
| Docker     | Optional  | Containerized run |

---

## Backend Setup

### 1. Create a virtual environment (recommended)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

This installs the project in editable mode with all development tools (Ruff, Mypy, Pytest, Bandit, etc.).

### 3. Configure environment variables

```bash
cp ../.env.example .env
```

Edit `.env` and fill in your Supabase credentials if using the database. For local development without Supabase, the app works with JSON file data only.

Key variables:

| Variable             | Required | Description                    |
|----------------------|----------|--------------------------------|
| `SECRET_KEY`         | Yes      | Random string for JWT signing  |
| `SUPABASE_URL`       | No       | Supabase project URL           |
| `SUPABASE_KEY`       | No       | Supabase anon key              |
| `DEBUG`              | No       | Enable hot reload (default: false) |
| `LOG_LEVEL`          | No       | Logging level (default: INFO)  |

### 4. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for the interactive API docs.

---

## Frontend Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure environment

Create `frontend/.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start the dev server

```bash
npm run dev
```

Visit `http://localhost:3000`.

---

## Docker Setup

### Development

```bash
docker compose up --build
```

This uses `docker-compose.yml` + `docker-compose.override.yml` (dev overrides with hot reload).

### Production

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

---

## Running Tests

### Backend

```bash
cd backend

# All tests with coverage
make test

# Unit tests only
make test-unit

# Integration tests only
make test-integration
```

Coverage reports are generated in `htmlcov/`. Open `htmlcov/index.html` in a browser.

### Frontend

```bash
cd frontend
npm test
```

---

## Code Quality Tools

### Linting & Formatting

```bash
make lint      # Ruff + Pylint
make format    # Auto-format with Ruff
```

### Type Checking

```bash
make typecheck   # Mypy in strict mode
```

### Security Scanning

```bash
make security   # Bandit + pip-audit
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

Hooks run automatically on `git commit` and check:
- Trailing whitespace, YAML/JSON syntax
- Ruff linting and formatting
- Mypy type checking
- Bandit security scanning

---

## Makefile Targets

| Target           | Description                        |
|------------------|------------------------------------|
| `make install`   | Install all dependencies           |
| `make lint`      | Run Ruff + Pylint                  |
| `make format`    | Auto-format with Ruff              |
| `make typecheck` | Run Mypy                           |
| `make test`      | Run all tests with coverage        |
| `make test-unit` | Run unit tests only                |
| `make test-integration` | Run integration tests only  |
| `make security`  | Run Bandit + pip-audit             |
| `make all`       | Run lint + typecheck + test + security |
| `make dev`       | Start dev server (uvicorn --reload)|
| `make clean`     | Remove build artifacts             |
