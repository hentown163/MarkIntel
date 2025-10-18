"""Campaign Template Entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from app.core.exceptions import ValidationError


@dataclass
class CampaignTemplate:
    """
    Campaign Template entity
    
    Represents a reusable campaign structure that can be used to quickly create new campaigns
    """
    id: str
    name: str
    description: Optional[str]
    theme: str
    ideas: List[dict]
    channel_mix: List[dict]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate template invariants"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValidationError("Template must have a name")
        if not self.theme or len(self.theme.strip()) == 0:
            raise ValidationError("Template must have a theme")
        if not self.ideas or len(self.ideas) == 0:
            raise ValidationError("Template must have at least one idea")
        if not self.channel_mix or len(self.channel_mix) == 0:
            raise ValidationError("Template must have at least one channel")
