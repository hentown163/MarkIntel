"""Regenerate Campaign Ideas Use Case"""
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.repositories.service_repository import ServiceRepository
from app.domain.repositories.market_signal_repository import MarketSignalRepository
from app.domain.services.campaign_ideation_service import CampaignIdeationService
from app.domain.value_objects import CampaignId
from app.application.dtos.response.campaign_response import CampaignResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper
from app.core.exceptions import EntityNotFoundError, UseCaseError


class RegenerateIdeasUseCase:
    """
    Regenerate Campaign Ideas Use Case
    
    Following Single Responsibility Principle - orchestrates idea regeneration
    Following Dependency Inversion Principle - depends on repository abstractions
    """
    
    def __init__(
        self,
        campaign_repo: CampaignRepository,
        service_repo: ServiceRepository,
        signal_repo: MarketSignalRepository,
        ideation_service: CampaignIdeationService
    ):
        self.campaign_repo = campaign_repo
        self.service_repo = service_repo
        self.signal_repo = signal_repo
        self.ideation_service = ideation_service
    
    def execute(self, campaign_id: str) -> CampaignResponseDTO:
        """Execute the use case to regenerate campaign ideas"""
        try:
            campaign = self.campaign_repo.find_by_id(CampaignId(campaign_id))
            if not campaign:
                raise EntityNotFoundError("Campaign", campaign_id)
            
            service = self.service_repo.find_by_name(campaign.name.split(":")[0].strip())
            if not service:
                services = self.service_repo.find_all()
                if not services:
                    raise UseCaseError(f"No services available to regenerate campaign ideas")
                service = services[0]
            
            market_signals = self.signal_repo.find_high_relevance(threshold=0.7)
            
            from app.domain.services.campaign_ideation_service import CampaignGenerationRequest
            domain_request = CampaignGenerationRequest(
                product_service=service.name,
                target_audience=", ".join(campaign.ideas[0].target_segments if campaign.ideas else service.target_audience),
                competitors=", ".join(service.competitors) if service.competitors else "",
                additional_context=campaign.theme,
                duration_days=(campaign.date_range.end_date - campaign.date_range.start_date).days
            )
            
            new_ideas = self.ideation_service.generate_ideas(
                service=service,
                market_signals=market_signals,
                request=domain_request
            )
            
            campaign.ideas = new_ideas
            campaign.theme = new_ideas[0].theme if new_ideas else campaign.theme
            
            saved_campaign = self.campaign_repo.save(campaign)
            
            return CampaignMapper.to_response_dto(saved_campaign)
            
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise UseCaseError(f"Failed to regenerate campaign ideas: {str(e)}")
