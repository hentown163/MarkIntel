"""Market signal SQLAlchemy model"""
from sqlalchemy import Column, String, Float, DateTime, Enum, Text
from app.infrastructure.config.database import Base
import enum


class ImpactLevelEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MarketSignalORM(Base):
    """Market signal ORM model"""
    __tablename__ = "market_signals"
    
    id = Column(String, primary_key=True)
    source = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    relevance_score = Column(Float, nullable=False)
    category = Column(String, nullable=False, index=True)
    impact = Column(Enum(ImpactLevelEnum), nullable=False)
