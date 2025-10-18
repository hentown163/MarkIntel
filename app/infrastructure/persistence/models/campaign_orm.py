"""Campaign SQLAlchemy models"""
from sqlalchemy import Column, String, Float, Date, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.infrastructure.config.database import Base
import enum


class CampaignStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignORM(Base):
    """Campaign ORM model"""
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(Enum(CampaignStatusEnum), nullable=False, default=CampaignStatusEnum.DRAFT)
    theme = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_budget = Column(Float, nullable=False)
    expected_roi = Column(Float, nullable=False)
    metrics_json = Column(JSON, nullable=True)
    service_id = Column(String, nullable=True)
    feedback_history = Column(JSON, nullable=True, default=[])
    
    ideas = relationship("CampaignIdeaORM", back_populates="campaign", cascade="all, delete-orphan")
    channel_mix = relationship("ChannelPlanORM", back_populates="campaign", cascade="all, delete-orphan")


class CampaignIdeaORM(Base):
    """Campaign idea ORM model"""
    __tablename__ = "campaign_ideas"
    
    id = Column(String, primary_key=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    theme = Column(String, nullable=False)
    core_message = Column(Text, nullable=False)
    target_segments = Column(JSON, nullable=False)
    competitive_angle = Column(Text, nullable=False)
    
    campaign = relationship("CampaignORM", back_populates="ideas")


class ChannelPlanORM(Base):
    """Channel plan ORM model"""
    __tablename__ = "channel_plans"
    
    id = Column(String, primary_key=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    channel = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    budget_allocation = Column(Float, nullable=False)
    success_metrics = Column(JSON, nullable=False)
    
    campaign = relationship("CampaignORM", back_populates="channel_mix")
