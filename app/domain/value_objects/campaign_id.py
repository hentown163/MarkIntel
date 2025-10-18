"""Campaign ID value object"""
from dataclasses import dataclass
from app.core.exceptions import ValidationError


@dataclass(frozen=True)
class CampaignId:
    """Immutable campaign identifier"""
    value: str
    
    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValidationError("Campaign ID must be a non-empty string")
        
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CampaignId):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
