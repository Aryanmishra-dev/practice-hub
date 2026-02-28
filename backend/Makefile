.PHONY: install lint format typecheck test security clean all dev

# ============= Setup =============
install:
	pip install -e ".[dev]"
	pre-commit install

# ============= Code Quality =============
lint:
	ruff check app/ tests/
	pylint app/ --rcfile=.pylintrc --score=yes

format:
	ruff format app/ tests/
	ruff check app/ tests/ --fix

typecheck:
	mypy app/ --config-file=pyproject.toml

# ============= Testing =============
test:
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=80

test-unit:
	pytest tests/unit/ -v -m unit

test-integration:
	pytest tests/integration/ -v -m integration

test-quick:
	pytest tests/ -x -q

# ============= Security =============
security:
	bandit -r app/ -c .bandit
	pip-audit

# ============= Combined =============
all: lint typecheck test security
	@echo "All checks passed!"

# ============= Development =============
dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete 2>/dev/null || true
