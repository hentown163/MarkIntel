"""Feedback Response DTO"""
from pydantic import BaseModel


class FeedbackResponseDTO(BaseModel):
    """
    Response DTO for feedback submission
    """
    success: bool
    message: str
    campaign_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Feedback recorded successfully",
                "campaign_id": "camp-123"
            }
        }
