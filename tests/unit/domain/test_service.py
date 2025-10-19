import pytest

from app.domain.entities.service import Service
from app.domain.value_objects.service_id import ServiceId
from app.core.exceptions import ValidationError


@pytest.mark.unit
class TestService:
    def test_create_service_success(self, mock_service_id):
        service = Service(
            id=mock_service_id,
            name="Test Service",
            category="Software",
            description="A test service",
            target_audience=["Developers", "Tech Leaders"],
            key_benefits=["Fast", "Reliable", "Scalable"]
        )
        assert service.name == "Test Service"
        assert service.category == "Software"
        assert len(service.target_audience) == 2
        assert len(service.key_benefits) == 3
        assert service.market_mentions == 0
        assert service.active_campaigns == 0
    
    def test_create_service_no_name_fails(self, mock_service_id):
        with pytest.raises(ValidationError, match="must have a name"):
            Service(
                id=mock_service_id,
                name="",
                category="Software",
                description="A test service",
                target_audience=["Developers"],
                key_benefits=["Fast"]
            )
    
    def test_create_service_no_category_fails(self, mock_service_id):
        with pytest.raises(ValidationError, match="must have a category"):
            Service(
                id=mock_service_id,
                name="Test Service",
                category="",
                description="A test service",
                target_audience=["Developers"],
                key_benefits=["Fast"]
            )
    
    def test_create_service_no_target_audience_fails(self, mock_service_id):
        with pytest.raises(ValidationError, match="must have target audience"):
            Service(
                id=mock_service_id,
                name="Test Service",
                category="Software",
                description="A test service",
                target_audience=[],
                key_benefits=["Fast"]
            )
    
    def test_create_service_negative_mentions_fails(self, mock_service_id):
        with pytest.raises(ValidationError, match="cannot be negative"):
            Service(
                id=mock_service_id,
                name="Test Service",
                category="Software",
                description="A test service",
                target_audience=["Developers"],
                key_benefits=["Fast"],
                market_mentions=-5
            )
    
    def test_add_competitor_success(self, mock_service):
        assert len(mock_service.competitors) == 0
        mock_service.add_competitor("Competitor A")
        assert len(mock_service.competitors) == 1
        assert "Competitor A" in mock_service.competitors
    
    def test_add_duplicate_competitor_ignored(self, mock_service):
        mock_service.add_competitor("Competitor A")
        mock_service.add_competitor("Competitor A")
        assert len(mock_service.competitors) == 1
    
    def test_increment_campaign_count(self, mock_service):
        assert mock_service.active_campaigns == 0
        mock_service.increment_campaign_count()
        assert mock_service.active_campaigns == 1
        mock_service.increment_campaign_count()
        assert mock_service.active_campaigns == 2
    
    def test_decrement_campaign_count(self, mock_service):
        mock_service.active_campaigns = 3
        mock_service.decrement_campaign_count()
        assert mock_service.active_campaigns == 2
    
    def test_decrement_campaign_count_at_zero(self, mock_service):
        assert mock_service.active_campaigns == 0
        mock_service.decrement_campaign_count()
        assert mock_service.active_campaigns == 0
