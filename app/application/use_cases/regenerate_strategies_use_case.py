"""Regenerate Campaign Strategies Use Case"""
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.services.campaign_ideation_service import CampaignIdeationService
from app.domain.value_objects import CampaignId
from app.application.dtos.response.campaign_response import CampaignResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper
from app.core.exceptions import EntityNotFoundError, UseCaseError


class RegenerateStrategiesUseCase:
    """
    Regenerate Campaign Channel Strategies Use Case
    
    Following Single Responsibility Principle - orchestrates strategy regeneration
    Following Dependency Inversion Principle - depends on repository abstractions
    """
    
    def __init__(
        self,
        campaign_repo: CampaignRepository,
        ideation_service: CampaignIdeationService
    ):
        self.campaign_repo = campaign_repo
        self.ideation_service = ideation_service
    
    def execute(self, campaign_id: str) -> CampaignResponseDTO:
        """Execute the use case to regenerate channel strategies"""
        try:
            campaign = self.campaign_repo.find_by_id(CampaignId(campaign_id))
            if not campaign:
                raise EntityNotFoundError("Campaign", campaign_id)
            
            target_audience_list = []
            if campaign.ideas:
                for idea in campaign.ideas:
                    target_audience_list.extend(idea.target_segments)
                target_audience_list = list(set(target_audience_list))
            
            new_channel_mix = self.ideation_service.optimize_channel_mix(
                ideas=campaign.ideas,
                target_audience=target_audience_list if target_audience_list else ["General Audience"]
            )
            
            campaign.channel_mix = new_channel_mix
            
            saved_campaign = self.campaign_repo.save(campaign)
            
            return CampaignMapper.to_response_dto(saved_campaign)
            
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise UseCaseError(f"Failed to regenerate channel strategies: {str(e)}")
