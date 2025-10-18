"""Record Campaign Feedback Use Case"""
from datetime import datetime
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.value_objects import CampaignId
from app.domain.entities.campaign import CampaignFeedback
from app.application.dtos.request.campaign_feedback_request import CampaignFeedbackRequestDTO
from app.application.dtos.response.feedback_response import FeedbackResponseDTO
from app.core.exceptions import EntityNotFoundError, UseCaseError


class RecordFeedbackUseCase:
    """
    Record Campaign Feedback Use Case
    
    Following Single Responsibility Principle - handles feedback recording
    Following Dependency Inversion Principle - depends on repository abstraction
    """
    
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo
    
    def execute(self, campaign_id: str, feedback_dto: CampaignFeedbackRequestDTO) -> FeedbackResponseDTO:
        """Execute the use case to record feedback"""
        try:
            campaign = self.campaign_repo.find_by_id(CampaignId(campaign_id))
            if not campaign:
                raise EntityNotFoundError("Campaign", campaign_id)
            
            feedback = CampaignFeedback(
                feedback_type=feedback_dto.feedback_type.value,
                target=feedback_dto.target.value,
                comment=feedback_dto.comment,
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            
            campaign.add_feedback(feedback)
            
            self.campaign_repo.save(campaign)
            
            print(f"Feedback persisted for campaign {campaign_id}: {feedback_dto.feedback_type} on {feedback_dto.target}")
            
            return FeedbackResponseDTO(
                success=True,
                message=f"Feedback recorded successfully for {feedback_dto.target}",
                campaign_id=campaign_id
            )
            
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise UseCaseError(f"Failed to record feedback: {str(e)}")
