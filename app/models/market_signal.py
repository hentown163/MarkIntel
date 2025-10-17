from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ImpactLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class MarketSignal(BaseModel):
    id: str
    source: str
    content: str
    timestamp: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    category: Optional[str] = None
    impact: Optional[ImpactLevel] = None
