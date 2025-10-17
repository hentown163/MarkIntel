from pydantic import BaseModel
from typing import List, Optional

class Service(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None
    target_audience: List[str]
    key_benefits: List[str]
    market_mentions: Optional[int] = None
    active_campaigns: Optional[int] = None
    backed_competitors: Optional[int] = None
    competitors: Optional[List[str]] = None
