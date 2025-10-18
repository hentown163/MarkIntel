"""SQLAlchemy implementation of Campaign Template Repository"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.domain.repositories.campaign_template_repository import CampaignTemplateRepository
from app.domain.entities.campaign_template import CampaignTemplate
from app.infrastructure.persistence.models.campaign_template_orm import CampaignTemplateORM


class SQLAlchemyCampaignTemplateRepository(CampaignTemplateRepository):
    """SQLAlchemy implementation of CampaignTemplateRepository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_id(self, template_id: str) -> Optional[CampaignTemplate]:
        """Find template by ID"""
        orm = self.session.query(CampaignTemplateORM).filter(
            CampaignTemplateORM.id == template_id
        ).first()
        return self._to_entity(orm) if orm else None
    
    def find_all(self) -> List[CampaignTemplate]:
        """Find all templates"""
        orms = self.session.query(CampaignTemplateORM).order_by(
            CampaignTemplateORM.created_at.desc()
        ).all()
        return [self._to_entity(orm) for orm in orms]
    
    def search(self, query: str = None, tags: List[str] = None) -> List[CampaignTemplate]:
        """Search templates by query or tags"""
        q = self.session.query(CampaignTemplateORM)
        
        if query and query.strip():
            search_term = f"%{query.lower().strip()}%"
            q = q.filter(
                or_(
                    func.lower(CampaignTemplateORM.name).like(search_term),
                    func.lower(CampaignTemplateORM.theme).like(search_term),
                    func.lower(CampaignTemplateORM.description).like(search_term)
                )
            )
        
        orms = q.order_by(CampaignTemplateORM.created_at.desc()).all()
        templates = [self._to_entity(orm) for orm in orms]
        
        if tags:
            templates = [t for t in templates if t.tags and any(tag in t.tags for tag in tags)]
        
        return templates
    
    def save(self, template: CampaignTemplate) -> CampaignTemplate:
        """Save template (create or update)"""
        existing = self.session.query(CampaignTemplateORM).filter(
            CampaignTemplateORM.id == template.id
        ).first()
        
        if existing:
            self._update_orm(existing, template)
        else:
            orm = self._to_orm(template)
            self.session.add(orm)
        
        self.session.commit()
        return template
    
    def delete(self, template_id: str) -> bool:
        """Delete template"""
        result = self.session.query(CampaignTemplateORM).filter(
            CampaignTemplateORM.id == template_id
        ).delete()
        self.session.commit()
        return result > 0
    
    def _to_entity(self, orm: CampaignTemplateORM) -> CampaignTemplate:
        """Convert ORM to domain entity"""
        return CampaignTemplate(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            theme=orm.theme,
            ideas=orm.ideas or [],
            channel_mix=orm.channel_mix or [],
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            created_by=orm.created_by,
            tags=orm.tags or []
        )
    
    def _to_orm(self, template: CampaignTemplate) -> CampaignTemplateORM:
        """Convert domain entity to ORM"""
        return CampaignTemplateORM(
            id=template.id,
            name=template.name,
            description=template.description,
            theme=template.theme,
            ideas=template.ideas,
            channel_mix=template.channel_mix,
            created_at=template.created_at,
            updated_at=template.updated_at,
            created_by=template.created_by,
            tags=template.tags
        )
    
    def _update_orm(self, orm: CampaignTemplateORM, template: CampaignTemplate):
        """Update existing ORM from domain entity"""
        orm.name = template.name
        orm.description = template.description
        orm.theme = template.theme
        orm.ideas = template.ideas
        orm.channel_mix = template.channel_mix
        orm.updated_at = template.updated_at
        orm.created_by = template.created_by
        orm.tags = template.tags
