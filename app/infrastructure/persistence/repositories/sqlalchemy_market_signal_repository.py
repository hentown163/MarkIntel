"""SQLAlchemy implementation of Market Signal Repository"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.repositories.market_signal_repository import MarketSignalRepository
from app.domain.entities.market_signal import MarketSignal, ImpactLevel
from app.domain.value_objects import SignalId
from app.infrastructure.persistence.models.market_signal_orm import MarketSignalORM


class SQLAlchemyMarketSignalRepository(MarketSignalRepository):
    """SQLAlchemy implementation of MarketSignalRepository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_id(self, signal_id: SignalId) -> Optional[MarketSignal]:
        """Find signal by ID"""
        orm = self.session.query(MarketSignalORM).filter(
            MarketSignalORM.id == str(signal_id)
        ).first()
        return self._to_entity(orm) if orm else None
    
    def find_all(self) -> List[MarketSignal]:
        """Find all signals"""
        orms = self.session.query(MarketSignalORM).order_by(
            MarketSignalORM.timestamp.desc()
        ).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_recent(self, limit: int = 10) -> List[MarketSignal]:
        """Find recent signals"""
        orms = self.session.query(MarketSignalORM).order_by(
            MarketSignalORM.timestamp.desc()
        ).limit(limit).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_high_relevance(self, threshold: float = 0.7) -> List[MarketSignal]:
        """Find high relevance signals"""
        orms = self.session.query(MarketSignalORM).filter(
            MarketSignalORM.relevance_score >= threshold
        ).order_by(MarketSignalORM.relevance_score.desc()).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_by_category(self, category: str) -> List[MarketSignal]:
        """Find signals by category"""
        orms = self.session.query(MarketSignalORM).filter(
            MarketSignalORM.category == category
        ).all()
        return [self._to_entity(orm) for orm in orms]
    
    def save(self, signal: MarketSignal) -> MarketSignal:
        """Save signal (create or update)"""
        existing = self.session.query(MarketSignalORM).filter(
            MarketSignalORM.id == str(signal.id)
        ).first()
        
        if existing:
            self._update_orm(existing, signal)
        else:
            orm = self._to_orm(signal)
            self.session.add(orm)
        
        self.session.commit()
        return signal
    
    def delete(self, signal_id: SignalId) -> bool:
        """Delete signal"""
        result = self.session.query(MarketSignalORM).filter(
            MarketSignalORM.id == str(signal_id)
        ).delete()
        self.session.commit()
        return result > 0
    
    def _to_entity(self, orm: MarketSignalORM) -> MarketSignal:
        """Convert ORM to domain entity"""
        return MarketSignal(
            id=SignalId(orm.id),
            source=orm.source,
            content=orm.content,
            timestamp=orm.timestamp,
            relevance_score=orm.relevance_score,
            category=orm.category,
            impact=ImpactLevel(orm.impact)
        )
    
    def _to_orm(self, signal: MarketSignal) -> MarketSignalORM:
        """Convert domain entity to ORM"""
        return MarketSignalORM(
            id=str(signal.id),
            source=signal.source,
            content=signal.content,
            timestamp=signal.timestamp,
            relevance_score=signal.relevance_score,
            category=signal.category,
            impact=signal.impact.value
        )
    
    def _update_orm(self, orm: MarketSignalORM, signal: MarketSignal):
        """Update existing ORM from domain entity"""
        orm.source = signal.source
        orm.content = signal.content
        orm.timestamp = signal.timestamp
        orm.relevance_score = signal.relevance_score
        orm.category = signal.category
        orm.impact = signal.impact.value
    
    def find_with_filters(
        self,
        impact: Optional[str] = None,
        category: Optional[str] = None,
        source: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_relevance: Optional[float] = None
    ) -> List[MarketSignal]:
        """Find signals with advanced filters"""
        query = self.session.query(MarketSignalORM)
        
        if impact:
            query = query.filter(MarketSignalORM.impact == impact)
        
        if category:
            query = query.filter(MarketSignalORM.category == category)
        
        if source:
            query = query.filter(MarketSignalORM.source.ilike(f"%{source}%"))
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(MarketSignalORM.timestamp >= start_dt)
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(MarketSignalORM.timestamp <= end_dt)
        
        if min_relevance is not None:
            query = query.filter(MarketSignalORM.relevance_score >= min_relevance)
        
        orms = query.order_by(MarketSignalORM.timestamp.desc()).all()
        return [self._to_entity(orm) for orm in orms]
