"""Delete Campaign Use Case"""
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.value_objects import CampaignId
from app.core.exceptions import EntityNotFoundError, UseCaseError


class DeleteCampaignUseCase:
    """
    Delete Campaign Use Case
    
    Following Single Responsibility Principle - handles campaign deletion
    Following Dependency Inversion Principle - depends on repository abstraction
    """
    
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo
    
    def execute(self, campaign_id: str) -> bool:
        """Execute the use case to delete a campaign"""
        try:
            campaign = self.campaign_repo.find_by_id(CampaignId(campaign_id))
            if not campaign:
                raise EntityNotFoundError("Campaign", campaign_id)
            
            success = self.campaign_repo.delete(CampaignId(campaign_id))
            
            if not success:
                raise UseCaseError(f"Failed to delete campaign {campaign_id}")
            
            return success
            
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise UseCaseError(f"Failed to delete campaign: {str(e)}")
