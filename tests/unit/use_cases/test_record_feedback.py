import pytest
from unittest.mock import Mock
from app.application.use_cases.record_feedback_use_case import RecordFeedbackUseCase
from app.application.dtos.request.campaign_feedback_request import CampaignFeedbackRequestDTO, FeedbackType, FeedbackTarget
from app.domain.value_objects.campaign_id import CampaignId
from app.core.exceptions import EntityNotFoundError, UseCaseError


@pytest.mark.unit
class TestRecordFeedbackUseCase:
    @pytest.fixture
    def mock_campaign_repo(self, mock_campaign):
        repo = Mock()
        repo.find_by_id = Mock(return_value=mock_campaign)
        repo.save = Mock(return_value=mock_campaign)
        return repo
    
    @pytest.fixture
    def use_case(self, mock_campaign_repo):
        return RecordFeedbackUseCase(campaign_repo=mock_campaign_repo)
    
    @pytest.fixture
    def valid_feedback_request(self):
        return CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.LIKE,
            target=FeedbackTarget.IDEAS,
            comment="Great campaign idea!"
        )
    
    def test_execute_success(self, use_case, valid_feedback_request, mock_campaign_repo, mock_campaign):
        result = use_case.execute(
            campaign_id="camp_test123",
            feedback_dto=valid_feedback_request
        )
        
        assert result.success is True
        assert result.campaign_id == "camp_test123"
        assert "recorded successfully" in result.message
        
        mock_campaign_repo.find_by_id.assert_called_once()
        mock_campaign_repo.save.assert_called_once()
        
        assert len(mock_campaign.feedback_history) == 1
        assert mock_campaign.feedback_history[0].feedback_type == "like"
        assert mock_campaign.feedback_history[0].target == "ideas"
    
    def test_execute_dislike_feedback(self, use_case, mock_campaign_repo, mock_campaign):
        feedback = CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.DISLIKE,
            target=FeedbackTarget.STRATEGIES,
            comment="Strategies need work"
        )
        
        result = use_case.execute("camp_test123", feedback)
        
        assert result.success is True
        assert len(mock_campaign.feedback_history) == 1
        assert mock_campaign.feedback_history[0].feedback_type == "dislike"
    
    def test_execute_without_comment(self, use_case, mock_campaign_repo, mock_campaign):
        feedback = CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.LIKE,
            target=FeedbackTarget.IDEAS
        )
        
        result = use_case.execute("camp_test123", feedback)
        
        assert result.success is True
        assert mock_campaign.feedback_history[0].comment is None
    
    def test_execute_campaign_not_found(self, mock_campaign_repo):
        mock_campaign_repo.find_by_id = Mock(return_value=None)
        use_case = RecordFeedbackUseCase(campaign_repo=mock_campaign_repo)
        
        feedback = CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.LIKE,
            target=FeedbackTarget.IDEAS
        )
        
        with pytest.raises(EntityNotFoundError, match="Campaign"):
            use_case.execute("nonexistent_campaign", feedback)
    
    def test_execute_repository_error(self, mock_campaign):
        mock_campaign_repo = Mock()
        mock_campaign_repo.find_by_id = Mock(return_value=mock_campaign)
        mock_campaign_repo.save = Mock(side_effect=Exception("Database error"))
        
        use_case = RecordFeedbackUseCase(campaign_repo=mock_campaign_repo)
        
        feedback = CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.LIKE,
            target=FeedbackTarget.IDEAS
        )
        
        with pytest.raises(UseCaseError, match="Failed to record feedback"):
            use_case.execute("camp_test123", feedback)
    
    def test_execute_multiple_feedbacks(self, use_case, mock_campaign_repo, mock_campaign):
        feedback1 = CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.LIKE,
            target=FeedbackTarget.IDEAS,
            comment="Great idea!"
        )
        feedback2 = CampaignFeedbackRequestDTO(
            feedback_type=FeedbackType.DISLIKE,
            target=FeedbackTarget.STRATEGIES,
            comment="Needs improvement"
        )
        
        use_case.execute("camp_test123", feedback1)
        use_case.execute("camp_test123", feedback2)
        
        assert len(mock_campaign.feedback_history) == 2
        assert mock_campaign.feedback_history[0].target == "ideas"
        assert mock_campaign.feedback_history[1].target == "strategies"
