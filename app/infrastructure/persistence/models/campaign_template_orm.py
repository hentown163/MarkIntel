"""Campaign Template ORM Model"""
from sqlalchemy import Column, String, Text, DateTime, JSON
from datetime import datetime

from app.infrastructure.config.database import Base


class CampaignTemplateORM(Base):
    """Campaign template ORM model for reusable campaign structures"""
    __tablename__ = "campaign_templates"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    theme = Column(String, nullable=False)
    ideas = Column(JSON, nullable=False)
    channel_mix = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String)
    tags = Column(JSON)
