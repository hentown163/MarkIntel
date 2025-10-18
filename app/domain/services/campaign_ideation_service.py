"""Campaign ideation service interface (port for AI integration)"""
from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.campaign import CampaignIdea, ChannelPlan
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal


class CampaignGenerationRequest:
    """Request for campaign generation"""
    def __init__(
        self,
        product_service: str,
        target_audience: str,
        competitors: str = "",
        additional_context: str = "",
        duration_days: int = 30
    ):
        self.product_service = product_service
        self.target_audience = target_audience
        self.competitors = competitors
        self.additional_context = additional_context
        self.duration_days = duration_days


class CampaignIdeationService(ABC):
    """
    Campaign ideation service interface (port)
    
    This is the abstraction for AI-powered campaign generation.
    Implementations can use LLM (OpenAI, Anthropic) or rule-based logic.
    
    Following Open/Closed Principle - new implementations can be added
    Following Dependency Inversion Principle - clients depend on this abstraction
    """
    
    @abstractmethod
    def generate_ideas(
        self,
        service: Service,
        market_signals: List[MarketSignal],
        request: CampaignGenerationRequest
    ) -> List[CampaignIdea]:
        """Generate campaign ideas based on service and market signals"""
        pass
    
    @abstractmethod
    def optimize_channel_mix(
        self,
        ideas: List[CampaignIdea],
        target_audience: List[str]
    ) -> List[ChannelPlan]:
        """Optimize channel mix based on ideas and audience"""
        pass
