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
        if status:
            try:
                campaign_status = CampaignStatus(status.lower())
                campaigns = self.campaign_repo.find_by_status(campaign_status)
            except ValueError:
                campaigns = []
        else:
            campaigns = self.campaign_repo.find_all()
        
        if query and query.strip():
            query_lower = query.lower().strip()
            campaigns = [
                c for c in campaigns
                if query_lower in c.name.lower() or query_lower in c.theme.lower()
            ]
        
        campaign_dtos = [CampaignMapper.to_response_dto(c) for c in campaigns]
        
        return CampaignListResponseDTO(
            campaigns=campaign_dtos,
            total=len(campaign_dtos)
        )
