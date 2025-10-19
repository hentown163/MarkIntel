# NexusPlanner Test Documentation

## Overview
This document describes the comprehensive unit test suite for NexusPlanner, covering both backend (Python/FastAPI) and frontend (React) components.

## Test Coverage Summary

**Current Backend Coverage: 47%**
- Total Tests: 60 passing
- Domain Entities: 41 tests
- Use Cases: 12 tests
- Security: 7 tests

## Backend Testing

### Test Structure
```
tests/
├── conftest.py                 # Common fixtures and test configuration
├── pytest.ini                  # Pytest configuration
├── fixtures/                   # Mock implementations
│   ├── mock_openai_adapter.py  # OpenAI service mock
│   ├── mock_vector_store.py    # Vector store mock
│   └── mock_crm_adapter.py     # CRM adapter mock
└── unit/
    ├── domain/                 # Domain entity tests
    │   ├── test_campaign.py    # Campaign, CampaignIdea, ChannelPlan tests
    │   ├── test_service.py     # Service entity tests
    │   └── test_market_signal.py # MarketSignal entity tests
    ├── use_cases/             # Application use case tests
    │   ├── test_generate_campaign.py  # Campaign generation tests
    │   └── test_record_feedback.py    # Feedback recording tests
    └── security/              # Security and authentication tests
        └── test_auth.py       # JWT authentication tests
```

### Running Tests

#### Run All Tests
```bash
uv run pytest tests/
```

#### Run Specific Test Categories
```bash
# Domain tests only
uv run pytest tests/unit/domain/ -v

# Use case tests only
uv run pytest tests/unit/use_cases/ -v

# Security tests only
uv run pytest tests/unit/security/ -v -m security
```

#### Run with Coverage Report
```bash
# Terminal report
uv run pytest tests/ --cov=app --cov-report=term-missing

# HTML report (opens in browser)
uv run pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

#### Run Tests by Marker
```bash
# Unit tests only
uv run pytest -m unit

# Security tests only
uv run pytest -m security

# Slow tests
uv run pytest -m slow
```

### Test Fixtures

#### Common Fixtures (conftest.py)
- `test_db`: In-memory SQLite database for testing
- `client`: FastAPI TestClient instance
- `mock_campaign_id`: Sample CampaignId value object
- `mock_service_id`: Sample ServiceId value object
- `mock_signal_id`: Sample SignalId value object
- `mock_service`: Complete Service entity
- `mock_market_signal`: Complete MarketSignal entity
- `mock_campaign`: Complete Campaign aggregate
- `mock_jwt_token`: Valid JWT token for auth tests
- `auth_headers`: Authorization headers with JWT token

#### Mock Adapters
1. **MockOpenAIAdapter** - Simulates OpenAI API
   - `generate_campaign_ideas()`: Returns mock campaign ideas
   - `generate_channel_strategies()`: Returns mock channel strategies
   - `analyze_market_signals()`: Returns mock market analysis

2. **MockVectorStore** - Simulates vector database
   - `add_document()`: Adds documents with embeddings
   - `search()`: Returns similarity search results
   - `get_document_count()`: Returns document count

3. **MockCRMAdapter** - Simulates CRM integrations
   - `get_customers()`: Returns mock customer data
   - `get_customer_by_id()`: Returns specific customer
   - `get_customer_insights()`: Returns aggregated insights

### Test Categories

#### 1. Domain Entity Tests (41 tests)

**CampaignIdea Tests**
- ✓ Create campaign idea successfully
- ✓ Validation failures (missing theme, message, segments)

**ChannelPlan Tests**
- ✓ Create channel plan successfully
- ✓ Budget allocation validation (0-1 range)

**Campaign Tests**
- ✓ Create campaign successfully
- ✓ Validation (name, ideas, channel mix, budget allocation)
- ✓ State transitions (activate, pause, complete, cancel)
- ✓ Update metrics
- ✓ Add feedback

**Service Tests**
- ✓ Create service successfully
- ✓ Validation (name, category, target audience)
- ✓ Competitor management
- ✓ Campaign count tracking

**MarketSignal Tests**
- ✓ Create market signal successfully
- ✓ Validation (source, content, relevance score, category)
- ✓ Relevance checking (is_highly_relevant)
- ✓ Impact checking (is_high_impact)

#### 2. Use Case Tests (12 tests)

**GenerateCampaignUseCase**
- ✓ Execute campaign generation successfully
- ✓ Use high relevance market signals
- ✓ Create service when not found
- ✓ Handle ideation service errors
- ✓ Handle repository errors
- ✓ Validate campaign structure

**RecordFeedbackUseCase**
- ✓ Record like feedback successfully
- ✓ Record dislike feedback successfully
- ✓ Handle feedback without comments
- ✓ Handle campaign not found error
- ✓ Handle repository errors
- ✓ Record multiple feedbacks

#### 3. Security Tests (7 tests)

**JWT Authentication**
- ✓ Create access token
- ✓ Create token with custom expiry
- ✓ Decode valid token
- ✓ Reject expired token
- ✓ Reject invalid token
- ✓ Reject tampered token
- ✓ Preserve custom claims

### Testing Best Practices

1. **Isolation**: Each test is independent and doesn't rely on other tests
2. **Mocking**: External services (OpenAI, CRM, Vector Store) are mocked
3. **Fixtures**: Common test data is defined in fixtures for reusability
4. **Markers**: Tests are tagged with markers (@pytest.mark.unit, @pytest.mark.security)
5. **Coverage**: Aim for 80%+ coverage on business logic (domain/use cases)
6. **Clear Naming**: Test names describe what they test (test_create_campaign_success)

### Error Handling Tests

Tests verify proper error handling for:
- Invalid input data (ValidationError)
- Missing entities (EntityNotFoundError)
- External service failures (UseCaseError)
- Authentication failures (JWT errors)
- Database errors

### Next Steps for Testing

#### Backend
- [ ] Repository/persistence tests (CRUD operations)
- [ ] Integration tests with real database
- [ ] API endpoint tests (FastAPI routes)
- [ ] Agent decision and observability tests
- [ ] Performance tests for high-volume scenarios

#### Frontend
- [ ] Component tests (Campaign list, modals, forms)
- [ ] Hook tests (useApi, useCampaigns, useDashboard)
- [ ] API client tests
- [ ] Routing tests
- [ ] Integration tests

### CI/CD Integration

#### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: uv run pytest tests/ --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Test Maintenance

- Review and update tests when requirements change
- Keep fixtures up-to-date with domain changes
- Add tests for new features before implementation (TDD)
- Regularly check coverage reports for gaps
- Refactor tests to reduce duplication

## Contact

For questions about the test suite, please refer to this documentation or check the inline comments in test files.
