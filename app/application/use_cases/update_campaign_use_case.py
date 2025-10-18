"""Update Campaign Use Case"""
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.value_objects import CampaignId
from app.domain.entities.campaign import CampaignStatus
from app.application.dtos.request.update_campaign_request import UpdateCampaignRequestDTO
from app.application.dtos.response.campaign_response import CampaignResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper
from app.core.exceptions import EntityNotFoundError, UseCaseError


class UpdateCampaignUseCase:
    """
    Update Campaign Use Case
    
    Following Single Responsibility Principle - handles campaign updates
    Following Dependency Inversion Principle - depends on repository abstraction
    """
    
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo
    
    def execute(self, campaign_id: str, update_dto: UpdateCampaignRequestDTO) -> CampaignResponseDTO:
        """Execute the use case to update a campaign"""
        try:
            campaign = self.campaign_repo.find_by_id(CampaignId(campaign_id))
            if not campaign:
                raise EntityNotFoundError("Campaign", campaign_id)
            
            if update_dto.name is not None:
                campaign.name = update_dto.name
            
            if update_dto.status is not None:
                try:
                    campaign.status = CampaignStatus(update_dto.status.lower())
                except ValueError:
                    raise UseCaseError(f"Invalid status: {update_dto.status}")
            
            if update_dto.theme is not None:
                campaign.theme = update_dto.theme
            
            saved_campaign = self.campaign_repo.save(campaign)
            
            return CampaignMapper.to_response_dto(saved_campaign)
            
        except EntityNotFoundError:
            raise
        except UseCaseError:
            raise
        except Exception as e:
            raise UseCaseError(f"Failed to update campaign: {str(e)}")
