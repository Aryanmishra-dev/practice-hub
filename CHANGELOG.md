# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-28

### Added

- FastAPI backend with quiz session management and grading
- Next.js 14 frontend with App Router and Tailwind CSS
- Quiz categories, difficulty selection, and timed quiz sessions
- Real-time answer grading with explanations
- User progress dashboard with mock analytics
- Admin endpoints with authentication
- Repository + Service layer architecture
- Structured logging with request ID tracing
- Rate limiting via slowapi
- Prometheus metrics at `/metrics`
- Comprehensive test suite (unit + integration)
- GitHub Actions CI/CD (backend, frontend, integration)
- Security scanning (Bandit, pip-audit, Trivy)
- Multi-stage Docker builds with non-root users
- Docker Compose configurations (dev, prod, monitoring)
- Pre-commit hooks (Ruff, Mypy, Bandit)
- PR and issue templates
- CONTRIBUTING guide and CODEOWNERS

### Security

- Non-root Docker containers
- Dependency vulnerability scanning in CI
- Rate limiting on all API endpoints
- Input validation via Pydantic v2
