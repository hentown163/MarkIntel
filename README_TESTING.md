# Quick Start: Running Tests

## Prerequisites
- Python 3.11+
- uv (Python package manager)
- All dependencies installed (`uv sync`)

## Run All Tests
```bash
uv run pytest tests/
```

## Run with Coverage
```bash
uv run pytest tests/ --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

## Run Specific Tests
```bash
# Domain tests only
uv run pytest tests/unit/domain/

# Use case tests
uv run pytest tests/unit/use_cases/

# Security tests
uv run pytest tests/unit/security/
```

## Current Test Stats
- **Total Tests**: 60
- **Coverage**: 47%
- **Passing**: 100%

## Test Categories
1. **Domain Entity Tests** (41 tests) - Campaign, Service, MarketSignal
2. **Use Case Tests** (12 tests) - Generate campaigns, record feedback
3. **Security Tests** (7 tests) - JWT authentication

See [TEST_DOCUMENTATION.md](TEST_DOCUMENTATION.md) for complete details.
