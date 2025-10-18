"""Repository interfaces (ports) - following Dependency Inversion Principle"""
from .campaign_repository import CampaignRepository
from .service_repository import ServiceRepository
from .market_signal_repository import MarketSignalRepository

__all__ = ["CampaignRepository", "ServiceRepository", "MarketSignalRepository"]
