import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.infrastructure.config.database import Base, get_db
from app.domain.entities.campaign import Campaign, CampaignStatus, CampaignIdea, ChannelPlan, CampaignMetrics
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal, ImpactLevel
from app.domain.value_objects.campaign_id import CampaignId
from app.domain.value_objects.service_id import ServiceId
from app.domain.value_objects.signal_id import SignalId
from app.domain.value_objects.money import Money
from app.domain.value_objects.date_range import DateRange


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = None
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            if db:
                db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_db):
    """
    FastAPI TestClient with test database dependency override.
    The test_db fixture ensures all API tests use the isolated test database.
    """
    return TestClient(app)


@pytest.fixture
def mock_campaign_id():
    return CampaignId("camp_test123")


@pytest.fixture
def mock_service_id():
    return ServiceId("svc_test456")


@pytest.fixture
def mock_signal_id():
    return SignalId("sig_test789")


@pytest.fixture
def mock_date_range():
    start = datetime.now().date()
    end = (datetime.now() + timedelta(days=30)).date()
    return DateRange(start_date=start, end_date=end)


@pytest.fixture
def mock_service(mock_service_id):
    return Service(
        id=mock_service_id,
        name="Test Service",
        description="A test service for unit tests",
        category="Software",
        target_audience=["Tech professionals", "Developers"],
        key_benefits=["Innovation", "Efficiency", "Scalability"]
    )


@pytest.fixture
def mock_market_signal(mock_signal_id):
    return MarketSignal(
        id=mock_signal_id,
        source="Test Source",
        content="Test market signal content",
        timestamp=datetime.now(),
        relevance_score=0.85,
        category="Technology",
        impact=ImpactLevel.HIGH
    )


@pytest.fixture
def mock_campaign_idea():
    return CampaignIdea(
        id="idea_test123",
        theme="Innovation Leadership",
        core_message="Transform your business with AI",
        target_segments=["Tech Leaders", "Decision Makers"],
        competitive_angle="First to market with AI-powered solutions"
    )


@pytest.fixture
def mock_channel_plan():
    return ChannelPlan(
        channel="email",
        content_type="newsletter",
        frequency="weekly",
        budget_allocation=0.4,
        success_metrics=["Open rate", "Click-through rate"]
    )


@pytest.fixture
def mock_campaign(mock_campaign_id, mock_campaign_idea, mock_channel_plan, mock_date_range):
    return Campaign(
        id=mock_campaign_id,
        name="Test Campaign",
        status=CampaignStatus.DRAFT,
        theme="AI Innovation",
        date_range=mock_date_range,
        ideas=[mock_campaign_idea],
        channel_mix=[
            mock_channel_plan,
            ChannelPlan(
                channel="social",
                content_type="posts",
                frequency="daily",
                budget_allocation=0.6,
                success_metrics=["Engagement", "Reach"]
            )
        ],
        total_budget=Money(amount=Decimal("5000.00"), currency="USD"),
        expected_roi=2.5,
        service_id="svc_test456"
    )


@pytest.fixture
def mock_jwt_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6OTk5OTk5OTk5OX0.test_signature"


@pytest.fixture
def mock_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "disabled": False
    }


@pytest.fixture
def auth_headers(mock_jwt_token):
    return {"Authorization": f"Bearer {mock_jwt_token}"}
