"""Campaign repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.campaign import Campaign, CampaignStatus
from app.domain.value_objects import CampaignId


class CampaignRepository(ABC):
    """
    Campaign repository interface (port)
    
    Following Interface Segregation Principle - focused interface
    Following Dependency Inversion Principle - depends on abstraction
    """
    
    @abstractmethod
    def find_by_id(self, campaign_id: CampaignId) -> Optional[Campaign]:
        """Find campaign by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Campaign]:
        """Find all campaigns"""
        pass
    
    @abstractmethod
    def find_by_status(self, status: CampaignStatus) -> List[Campaign]:
        """Find campaigns by status"""
        pass
    
    @abstractmethod
    def find_recent(self, limit: int = 10) -> List[Campaign]:
        """Find recent campaigns"""
        pass
    
    @abstractmethod
    def save(self, campaign: Campaign) -> Campaign:
        """Save campaign (create or update)"""
        pass
    
    @abstractmethod
    def delete(self, campaign_id: CampaignId) -> bool:
        """Delete campaign"""
        pass
    
    @abstractmethod
    def count_by_status(self, status: CampaignStatus) -> int:
        """Count campaigns by status"""
        pass
