"""Update Campaign Request DTO"""
from pydantic import BaseModel, Field
from typing import Optional


class UpdateCampaignRequestDTO(BaseModel):
    """
    Request DTO for campaign updates
    
    Following Single Responsibility Principle - only handles data validation
    """
    name: Optional[str] = Field(None, min_length=1, description="Campaign name")
    status: Optional[str] = Field(None, description="Campaign status (draft, active, paused, completed, cancelled)")
    theme: Optional[str] = Field(None, min_length=1, description="Campaign theme")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Campaign Name",
                "status": "active",
                "theme": "New Theme"
            }
        }
