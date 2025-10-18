"""Service SQLAlchemy model"""
from sqlalchemy import Column, String, Integer, JSON, Text
from app.infrastructure.config.database import Base


class ServiceORM(Base):
    """Service ORM model"""
    __tablename__ = "services"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    target_audience = Column(JSON, nullable=False)
    key_benefits = Column(JSON, nullable=False)
    market_mentions = Column(Integer, default=0)
    active_campaigns = Column(Integer, default=0)
    competitors = Column(JSON, nullable=True)
