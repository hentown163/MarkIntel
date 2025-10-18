"""Search Campaigns Use Case"""
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.entities.campaign import CampaignStatus
from app.application.dtos.response.campaign_response import CampaignResponseDTO, CampaignListResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper


class SearchCampaignsUseCase:
    """
    Search Campaigns Use Case
    
    Following Single Responsibility Principle - handles campaign search
    """
    
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo
    
    def execute(self, query: str = None, status: str = None) -> CampaignListResponseDTO:
        """Execute the use case to search campaigns"""
        campaign_status = None
        if status:
            try:
                campaign_status = CampaignStatus(status.lower())
            except ValueError:
                campaign_status = None
        
        campaigns = self.campaign_repo.search(query=query, status=campaign_status)
        
        campaign_dtos = [CampaignMapper.to_response_dto(c) for c in campaigns]
        
        return CampaignListResponseDTO(
            campaigns=campaign_dtos,
            total=len(campaign_dtos)
        )
