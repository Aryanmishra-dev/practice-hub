# Contributing to Quiz Forge

Thank you for your interest in contributing! This guide will help you set up the project locally and follow our development practices.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Branch Naming](#branch-naming)
- [Submitting a Pull Request](#submitting-a-pull-request)

---

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Backend

```bash
cd backend

# Install dependencies
pip install -e ".[dev]"

# Copy environment variables
cp .env.example .env

# Start the development server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend runs at `http://localhost:3000` and the backend at `http://localhost:8000`.

---

## Project Structure

```
backend/
  app/
    api/v1/          # Route handlers
    core/            # Config, logging, security
    middleware/       # Request ID, rate limiting, versioning
    models/          # Pydantic schemas
    repositories/    # Data access layer
    services/        # Business logic
  tests/
    unit/            # Unit tests
    integration/     # API integration tests

frontend/
  src/
    app/             # Next.js pages (App Router)
    components/      # React components
    lib/             # Utilities and API client
```

---

## Running Tests

### Backend

```bash
cd backend

# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run linting
make lint

# Run type checking
make typecheck

# Run everything
make all
```

### Frontend

```bash
cd frontend
npm run lint
npm test
```

---

## Code Style

### Python

- **Formatter**: Ruff (replaces Black + isort)
- **Linter**: Ruff + Pylint
- **Type checker**: Mypy (strict mode)
- **Line length**: 100 characters

Run `make format` to auto-format and `make lint` to check.

### TypeScript

- **Linter**: ESLint
- **Formatter**: Prettier
- Follow the existing patterns in the codebase

### Pre-commit Hooks

Install pre-commit hooks to automatically lint before committing:

```bash
pip install pre-commit
pre-commit install
```

---

## Branch Naming

Use the following conventions:

| Prefix       | Purpose                       | Example                         |
|------------- |-------------------------------|---------------------------------|
| `feature/`   | New features                  | `feature/quiz-timer`            |
| `fix/`       | Bug fixes                     | `fix/score-calculation`         |
| `chore/`     | Maintenance / tooling         | `chore/update-dependencies`     |
| `docs/`      | Documentation changes         | `docs/api-reference`            |
| `refactor/`  | Code refactoring              | `refactor/service-layer`        |

---

## Submitting a Pull Request

1. Fork the repo and create your branch from `main`.
2. Follow the branch naming convention above.
3. Write or update tests for your changes.
4. Ensure all checks pass: `make all` (backend) and `npm run lint` (frontend).
5. Fill out the PR template completely.
6. Request a review.

### Commit Messages

Use conventional commit style:

```
feat: add quiz timer component
fix: correct score calculation for mixed difficulty
docs: update API reference
chore: upgrade FastAPI to 0.110
```

---

## Questions?

Open an issue or reach out to the maintainers. We're happy to help!
