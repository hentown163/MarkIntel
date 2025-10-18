"""Generate Campaign Use Case"""
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
import random

from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.repositories.service_repository import ServiceRepository
from app.domain.repositories.market_signal_repository import MarketSignalRepository
from app.domain.services.campaign_ideation_service import CampaignIdeationService, CampaignGenerationRequest
from app.domain.entities.campaign import Campaign, CampaignStatus
from app.domain.value_objects import CampaignId, Money, DateRange, ServiceId
from app.application.dtos.request.generate_campaign_request import GenerateCampaignRequestDTO
from app.application.dtos.response.campaign_response import CampaignResponseDTO
from app.application.mappers.campaign_mapper import CampaignMapper
from app.core.exceptions import UseCaseError, EntityNotFoundError


class GenerateCampaignUseCase:
    """
    Generate Campaign Use Case
    
    Following Single Responsibility Principle - orchestrates campaign generation
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
    
    def execute(self, request_dto: GenerateCampaignRequestDTO) -> CampaignResponseDTO:
        """Execute the use case"""
        try:
            service = self._find_or_create_service(request_dto)
            
            market_signals = self.signal_repo.find_high_relevance(threshold=0.7)
            
            domain_request = CampaignGenerationRequest(
                product_service=request_dto.product_service,
                target_audience=request_dto.target_audience,
                competitors=request_dto.competitors,
                additional_context=request_dto.additional_context,
                duration_days=request_dto.duration_days
            )
            
            ideas = self.ideation_service.generate_ideas(
                service=service,
                market_signals=market_signals,
                request=domain_request
            )
            
            target_audience_list = [s.strip() for s in request_dto.target_audience.split(",")]
            channel_mix = self.ideation_service.optimize_channel_mix(
                ideas=ideas,
                target_audience=target_audience_list
            )
            
            campaign = self._create_campaign_entity(
                service=service,
                ideas=ideas,
                channel_mix=channel_mix,
                duration_days=request_dto.duration_days
            )
            
            saved_campaign = self.campaign_repo.save(campaign)
            
            return CampaignMapper.to_response_dto(saved_campaign)
            
        except Exception as e:
            raise UseCaseError(f"Failed to generate campaign: {str(e)}")
    
    def _find_or_create_service(self, request_dto: GenerateCampaignRequestDTO):
        """Find existing service or create a temporary one"""
        service = self.service_repo.find_by_name(request_dto.product_service)
        
        if not service:
            all_services = self.service_repo.find_all()
            for s in all_services:
                if (request_dto.product_service.lower() in s.name.lower() or 
                    s.name.lower() in request_dto.product_service.lower()):
                    service = s
                    break
        
        if not service:
            from app.domain.entities.service import Service
            service = Service(
                id=ServiceId(str(uuid.uuid4())[:8]),
                name=request_dto.product_service,
                category="Enterprise Solution",
                description=f"Enterprise solution for {request_dto.target_audience}",
                target_audience=[s.strip() for s in request_dto.target_audience.split(",")],
                key_benefits=["Innovation", "Scalability", "Reliability"],
                competitors=[c.strip() for c in request_dto.competitors.split(",")] if request_dto.competitors else []
            )
        
        return service
    
    def _create_campaign_entity(self, service, ideas, channel_mix, duration_days: int) -> Campaign:
        """Create campaign domain entity"""
        from datetime import date
        
        start_date = date.today()
        end_date = start_date + timedelta(days=duration_days)
        
        total_budget = Decimal(50000 + random.random() * 50000)
        expected_roi = round(3.0 + random.random() * 2.0, 1)
        
        campaign = Campaign(
            id=CampaignId(str(uuid.uuid4())[:8]),
            name=f"{service.name} Campaign",
            status=CampaignStatus.DRAFT,
            theme=ideas[0].theme if ideas else "Enterprise Campaign",
            date_range=DateRange(start_date, end_date),
            ideas=ideas,
            channel_mix=channel_mix,
            total_budget=Money(total_budget),
            expected_roi=expected_roi
        )
        
        return campaign
