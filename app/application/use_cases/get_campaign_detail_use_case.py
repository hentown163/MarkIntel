"""Get Campaign Detail Use Case"""
from typing import Optional

from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.value_objects import CampaignId
from app.application.dtos.response.campaign_response import CampaignResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper
from app.core.exceptions import EntityNotFoundError


class GetCampaignDetailUseCase:
    """
    Get Campaign Detail Use Case
    
    Following Single Responsibility Principle
    """
    
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo
    
    def execute(self, campaign_id: str) -> CampaignResponseDTO:
        """Execute the use case"""
        campaign = self.campaign_repo.find_by_id(CampaignId(campaign_id))
        
        if not campaign:
            raise EntityNotFoundError("Campaign", campaign_id)
        
        return CampaignMapper.to_response_dto(campaign)
