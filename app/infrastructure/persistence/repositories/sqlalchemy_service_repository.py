"""SQLAlchemy implementation of Service Repository"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.service_repository import ServiceRepository
from app.domain.entities.service import Service
from app.domain.value_objects import ServiceId
from app.infrastructure.persistence.models.service_orm import ServiceORM


class SQLAlchemyServiceRepository(ServiceRepository):
    """SQLAlchemy implementation of ServiceRepository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_id(self, service_id: ServiceId) -> Optional[Service]:
        """Find service by ID"""
        orm = self.session.query(ServiceORM).filter(
            ServiceORM.id == str(service_id)
        ).first()
        return self._to_entity(orm) if orm else None
    
    def find_all(self) -> List[Service]:
        """Find all services"""
        orms = self.session.query(ServiceORM).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_by_category(self, category: str) -> List[Service]:
        """Find services by category"""
        orms = self.session.query(ServiceORM).filter(
            ServiceORM.category == category
        ).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_by_name(self, name: str) -> Optional[Service]:
        """Find service by name (exact or partial match)"""
        orm = self.session.query(ServiceORM).filter(
            ServiceORM.name.ilike(f"%{name}%")
        ).first()
        return self._to_entity(orm) if orm else None
    
    def save(self, service: Service) -> Service:
        """Save service (create or update)"""
        existing = self.session.query(ServiceORM).filter(
            ServiceORM.id == str(service.id)
        ).first()
        
        if existing:
            self._update_orm(existing, service)
        else:
            orm = self._to_orm(service)
            self.session.add(orm)
        
        self.session.commit()
        return service
    
    def delete(self, service_id: ServiceId) -> bool:
        """Delete service"""
        result = self.session.query(ServiceORM).filter(
            ServiceORM.id == str(service_id)
        ).delete()
        self.session.commit()
        return result > 0
    
    def _to_entity(self, orm: ServiceORM) -> Service:
        """Convert ORM to domain entity"""
        return Service(
            id=ServiceId(orm.id),
            name=orm.name,
            category=orm.category,
            description=orm.description,
            target_audience=orm.target_audience,
            key_benefits=orm.key_benefits,
            market_mentions=orm.market_mentions,
            active_campaigns=orm.active_campaigns,
            competitors=orm.competitors or []
        )
    
    def _to_orm(self, service: Service) -> ServiceORM:
        """Convert domain entity to ORM"""
        return ServiceORM(
            id=str(service.id),
            name=service.name,
            category=service.category,
            description=service.description,
            target_audience=service.target_audience,
            key_benefits=service.key_benefits,
            market_mentions=service.market_mentions,
            active_campaigns=service.active_campaigns,
            competitors=service.competitors
        )
    
    def _update_orm(self, orm: ServiceORM, service: Service):
        """Update existing ORM from domain entity"""
        orm.name = service.name
        orm.category = service.category
        orm.description = service.description
        orm.target_audience = service.target_audience
        orm.key_benefits = service.key_benefits
        orm.market_mentions = service.market_mentions
        orm.active_campaigns = service.active_campaigns
        orm.competitors = service.competitors
