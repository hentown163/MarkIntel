"""Campaign Template Repository Interface"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.campaign_template import CampaignTemplate


class CampaignTemplateRepository(ABC):
    """Campaign template repository interface"""
    
    @abstractmethod
    def find_by_id(self, template_id: str) -> Optional[CampaignTemplate]:
        """Find template by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[CampaignTemplate]:
        """Find all templates"""
        pass
    
    @abstractmethod
    def search(self, query: str = None, tags: List[str] = None) -> List[CampaignTemplate]:
        """Search templates by query or tags"""
        pass
    
    @abstractmethod
    def save(self, template: CampaignTemplate) -> CampaignTemplate:
        """Save template (create or update)"""
        pass
    
    @abstractmethod
    def delete(self, template_id: str) -> bool:
        """Delete template"""
        pass
