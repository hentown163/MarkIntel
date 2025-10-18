"""Market signal entity"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.value_objects import SignalId
from app.core.exceptions import ValidationError


class ImpactLevel(str, Enum):
    """Impact level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class MarketSignal:
    """
    Market Signal entity
    
    Represents intelligence gathered from market sources
    """
    id: SignalId
    source: str
    content: str
    timestamp: datetime
    relevance_score: float
    category: str
    impact: ImpactLevel
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate market signal invariants"""
        if not self.source:
            raise ValidationError("Market signal must have a source")
        if not self.content or len(self.content.strip()) == 0:
            raise ValidationError("Market signal must have content")
        if not (0 <= self.relevance_score <= 1):
            raise ValidationError("Relevance score must be between 0 and 1")
        if not self.category:
            raise ValidationError("Market signal must have a category")
    
    def is_highly_relevant(self) -> bool:
        """Check if signal is highly relevant"""
        return self.relevance_score >= 0.7
    
    def is_high_impact(self) -> bool:
        """Check if signal is high impact"""
        return self.impact == ImpactLevel.HIGH
