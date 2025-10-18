"""Service entity"""
from dataclasses import dataclass
from typing import List

from app.domain.value_objects import ServiceId
from app.core.exceptions import ValidationError


@dataclass
class Service:
    """
    Service entity
    
    Represents a product/service offered by the company
    """
    id: ServiceId
    name: str
    category: str
    description: str
    target_audience: List[str]
    key_benefits: List[str]
    market_mentions: int = 0
    active_campaigns: int = 0
    competitors: List[str] = None
    
    def __post_init__(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ValidationError("Service must have a name")
        if not self.category:
            raise ValidationError("Service must have a category")
        if not self.target_audience:
            raise ValidationError("Service must have target audience")
        if self.competitors is None:
            object.__setattr__(self, 'competitors', [])
        if self.market_mentions < 0:
            raise ValidationError("Market mentions cannot be negative")
    
    def add_competitor(self, competitor: str):
        """Add a competitor"""
        if competitor not in self.competitors:
            self.competitors.append(competitor)
    
    def increment_campaign_count(self):
        """Increment active campaigns count"""
        self.active_campaigns += 1
    
    def decrement_campaign_count(self):
        """Decrement active campaigns count"""
        if self.active_campaigns > 0:
            self.active_campaigns -= 1
