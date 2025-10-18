"""List Campaigns Use Case"""
from typing import List

from app.domain.repositories.campaign_repository import CampaignRepository
from app.application.dtos.response.campaign_response import CampaignResponseDTO, CampaignListResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper


class ListCampaignsUseCase:
    """
    List Campaigns Use Case
    
    Following Single Responsibility Principle
    """
    
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo
    
    def execute(self, limit: int = None) -> CampaignListResponseDTO:
        """Execute the use case"""
        if limit:
            campaigns = self.campaign_repo.find_recent(limit)
        else:
            campaigns = self.campaign_repo.find_all()
        
        campaign_dtos = [CampaignMapper.to_response_dto(c) for c in campaigns]
        
        return CampaignListResponseDTO(
            campaigns=campaign_dtos,
            total=len(campaign_dtos)
        )
