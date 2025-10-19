from pydantic import BaseModel, EmailStr
from typing import Optional

class CampaignGenerationRequest(BaseModel):
    product_service: str
    target_audience: str
    competitors: Optional[str] = None
    additional_context: Optional[str] = None
    duration_days: Optional[int] = 30


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegistrationRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
