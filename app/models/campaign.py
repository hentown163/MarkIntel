from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class CampaignStatus(str, Enum):
    active = "active"
    draft = "draft"
    completed = "completed"

class CampaignIdea(BaseModel):
    id: str
    theme: str
    core_message: str
    target_segments: List[str]
    competitive_angle: str

class ChannelPlan(BaseModel):
    channel: str
    content_type: str
    frequency: str
    budget_allocation: float
    success_metrics: List[str]

class CampaignMetrics(BaseModel):
    engagement: Optional[str] = None
    leads: Optional[str] = None
    conversions: Optional[str] = None

class Campaign(BaseModel):
    id: str
    name: str
    status: CampaignStatus
    theme: str
    start_date: str
    end_date: str
    ideas: List[CampaignIdea]
    channel_mix: List[ChannelPlan]
    total_budget: int
    expected_roi: float
    metrics: Optional[CampaignMetrics] = None
