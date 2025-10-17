from pydantic import BaseModel
from typing import Optional

class CampaignGenerationRequest(BaseModel):
    product_service: str
    target_audience: str
    competitors: Optional[str] = None
    additional_context: Optional[str] = None
    duration_days: Optional[int] = 30
