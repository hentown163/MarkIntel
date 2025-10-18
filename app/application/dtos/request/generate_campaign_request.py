"""Generate Campaign Request DTO"""
from pydantic import BaseModel, Field, validator


class GenerateCampaignRequestDTO(BaseModel):
    """
    Request DTO for campaign generation
    
    Following Single Responsibility Principle - only handles data validation
    """
    product_service: str = Field(..., min_length=1, description="Product or service name")
    target_audience: str = Field(..., min_length=1, description="Target audience")
    competitors: str = Field(default="", description="Competitors (comma-separated)")
    additional_context: str = Field(default="", description="Additional context")
    duration_days: int = Field(default=30, ge=1, le=365, description="Campaign duration in days")
    
    @validator('product_service')
    def validate_product_service(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Product/service name cannot be empty")
        return v.strip()
    
    @validator('target_audience')
    def validate_target_audience(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Target audience cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_service": "CloudScale AI Security Suite",
                "target_audience": "CISOs, Security Teams",
                "competitors": "Sentinel, ThreatGuard Pro",
                "additional_context": "Focus on zero-trust architecture",
                "duration_days": 60
            }
        }
