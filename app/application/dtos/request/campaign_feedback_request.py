"""Campaign Feedback Request DTO"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class FeedbackType(str, Enum):
    """Feedback type enumeration"""
    LIKE = "like"
    DISLIKE = "dislike"


class FeedbackTarget(str, Enum):
    """Feedback target enumeration"""
    IDEAS = "ideas"
    STRATEGIES = "strategies"
    OVERALL = "overall"


class CampaignFeedbackRequestDTO(BaseModel):
    """
    Request DTO for campaign feedback
    
    Following Single Responsibility Principle - only handles data validation
    """
    feedback_type: FeedbackType = Field(..., description="Type of feedback (like/dislike)")
    target: FeedbackTarget = Field(..., description="What the feedback is for")
    comment: Optional[str] = Field(None, max_length=500, description="Optional feedback comment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feedback_type": "like",
                "target": "ideas",
                "comment": "Great campaign themes!"
            }
        }
