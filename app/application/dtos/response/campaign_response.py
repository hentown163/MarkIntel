"""Campaign Response DTOs"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CampaignIdeaDTO(BaseModel):
    """Campaign idea DTO"""
    id: str
    theme: str
    core_message: str
    target_segments: List[str]
    competitive_angle: str


class ChannelPlanDTO(BaseModel):
    """Channel plan DTO"""
    channel: str
    content_type: str
    frequency: str
    budget_allocation: float
    success_metrics: List[str]


class CampaignMetricsDTO(BaseModel):
    """Campaign metrics DTO"""
    engagement: Optional[str] = None
    leads: Optional[str] = None
    conversions: Optional[str] = None


class FeedbackHistoryDTO(BaseModel):
    """Feedback history item DTO"""
    feedback_type: str
    target: str
    comment: Optional[str] = None
    timestamp: Optional[str] = None


class CampaignResponseDTO(BaseModel):
    """
    Campaign response DTO
    
    Following Single Responsibility Principle - only for API responses
    """
    id: str
    name: str
    status: str
    theme: str
    start_date: str
    end_date: str
    ideas: List[CampaignIdeaDTO]
    channel_mix: List[ChannelPlanDTO]
    total_budget: float
    expected_roi: float
    metrics: Optional[CampaignMetricsDTO] = None
    feedback_history: List[FeedbackHistoryDTO] = []
    
    class Config:
        from_attributes = True


class CampaignListResponseDTO(BaseModel):
    """List of campaigns response"""
    campaigns: List[CampaignResponseDTO]
    total: int
