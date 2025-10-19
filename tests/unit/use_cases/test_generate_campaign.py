import pytest
from unittest.mock import Mock, MagicMock
from decimal import Decimal

from app.application.use_cases.generate_campaign_use_case import GenerateCampaignUseCase
from app.application.dtos.request.generate_campaign_request import GenerateCampaignRequestDTO
from app.domain.entities.campaign import CampaignIdea, ChannelPlan
from app.core.exceptions import UseCaseError


@pytest.mark.unit
class TestGenerateCampaignUseCase:
    @pytest.fixture
    def mock_campaign_repo(self):
        repo = Mock()
        repo.save = Mock(side_effect=lambda campaign: campaign)
        return repo
    
    @pytest.fixture
    def mock_service_repo(self, mock_service):
        repo = Mock()
        repo.find_by_name = Mock(return_value=mock_service)
        repo.find_all = Mock(return_value=[mock_service])
        return repo
    
    @pytest.fixture
    def mock_signal_repo(self, mock_market_signal):
        repo = Mock()
        repo.find_high_relevance = Mock(return_value=[mock_market_signal])
        return repo
    
    @pytest.fixture
    def mock_ideation_service(self):
        service = Mock()
        service.generate_ideas = Mock(return_value=[
            CampaignIdea(
                id="idea_001",
                theme="Innovation Excellence",
                core_message="Transform your business with AI",
                target_segments=["Tech Leaders", "Decision Makers"],
                competitive_angle="Industry-leading AI solutions"
            )
        ])
        service.optimize_channel_mix = Mock(return_value=[
            ChannelPlan(
                channel="email",
                content_type="newsletter",
                frequency="weekly",
                budget_allocation=0.5,
                success_metrics=["Open rate", "CTR"]
            ),
            ChannelPlan(
                channel="social",
                content_type="posts",
                frequency="daily",
                budget_allocation=0.5,
                success_metrics=["Engagement", "Reach"]
            )
        ])
        return service
    
    @pytest.fixture
    def use_case(self, mock_campaign_repo, mock_service_repo, mock_signal_repo, mock_ideation_service):
        return GenerateCampaignUseCase(
            campaign_repo=mock_campaign_repo,
            service_repo=mock_service_repo,
            signal_repo=mock_signal_repo,
            ideation_service=mock_ideation_service
        )
    
    @pytest.fixture
    def valid_request(self):
        return GenerateCampaignRequestDTO(
            product_service="AI Analytics Platform",
            target_audience="Tech Leaders, Data Scientists",
            competitors="Competitor A, Competitor B",
            additional_context="Focus on enterprise customers",
            duration_days=60
        )
    
    def test_execute_success(self, use_case, valid_request, mock_campaign_repo, mock_ideation_service):
        result = use_case.execute(valid_request)
        
        assert result is not None
        assert result.name is not None
        assert result.status == "draft"
        
        mock_ideation_service.generate_ideas.assert_called_once()
        mock_ideation_service.optimize_channel_mix.assert_called_once()
        mock_campaign_repo.save.assert_called_once()
    
    def test_execute_with_high_relevance_signals(
        self, use_case, valid_request, mock_signal_repo, mock_ideation_service
    ):
        result = use_case.execute(valid_request)
        
        mock_signal_repo.find_high_relevance.assert_called_once_with(threshold=0.7)
        assert result is not None
    
    def test_execute_creates_service_when_not_found(
        self, mock_campaign_repo, mock_signal_repo, mock_ideation_service, valid_request
    ):
        mock_service_repo = Mock()
        mock_service_repo.find_by_name = Mock(return_value=None)
        mock_service_repo.find_all = Mock(return_value=[])
        
        use_case = GenerateCampaignUseCase(
            campaign_repo=mock_campaign_repo,
            service_repo=mock_service_repo,
            signal_repo=mock_signal_repo,
            ideation_service=mock_ideation_service
        )
        
        result = use_case.execute(valid_request)
        
        assert result is not None
        mock_service_repo.find_by_name.assert_called_once()
    
    def test_execute_handles_ideation_service_error(
        self, mock_campaign_repo, mock_service_repo, mock_signal_repo, valid_request
    ):
        mock_ideation_service = Mock()
        mock_ideation_service.generate_ideas = Mock(side_effect=Exception("Ideation failed"))
        
        use_case = GenerateCampaignUseCase(
            campaign_repo=mock_campaign_repo,
            service_repo=mock_service_repo,
            signal_repo=mock_signal_repo,
            ideation_service=mock_ideation_service
        )
        
        with pytest.raises(UseCaseError, match="Failed to generate campaign"):
            use_case.execute(valid_request)
    
    def test_execute_handles_repository_error(
        self, mock_service_repo, mock_signal_repo, mock_ideation_service, valid_request
    ):
        mock_campaign_repo = Mock()
        mock_campaign_repo.save = Mock(side_effect=Exception("Database error"))
        
        use_case = GenerateCampaignUseCase(
            campaign_repo=mock_campaign_repo,
            service_repo=mock_service_repo,
            signal_repo=mock_signal_repo,
            ideation_service=mock_ideation_service
        )
        
        with pytest.raises(UseCaseError):
            use_case.execute(valid_request)
    
    def test_campaign_has_correct_structure(
        self, use_case, valid_request
    ):
        result = use_case.execute(valid_request)
        
        assert result.id is not None
        assert result.name is not None
        assert result.theme is not None
        assert result.ideas is not None
        assert len(result.ideas) > 0
        assert result.channel_mix is not None
        assert len(result.channel_mix) > 0
        assert result.total_budget is not None
        assert result.expected_roi is not None
