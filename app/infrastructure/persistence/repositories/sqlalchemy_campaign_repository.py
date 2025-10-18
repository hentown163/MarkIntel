"""SQLAlchemy implementation of Campaign Repository"""
import uuid
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.entities.campaign import Campaign, CampaignIdea, ChannelPlan, CampaignMetrics, CampaignStatus, CampaignFeedback
from app.domain.value_objects import CampaignId, Money, DateRange
from app.infrastructure.persistence.models.campaign_orm import CampaignORM, CampaignIdeaORM, ChannelPlanORM


class SQLAlchemyCampaignRepository(CampaignRepository):
    """
    SQLAlchemy implementation of CampaignRepository
    
    Following Dependency Inversion Principle - implements domain interface
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_id(self, campaign_id: CampaignId) -> Optional[Campaign]:
        """Find campaign by ID"""
        orm = self.session.query(CampaignORM).filter(
            CampaignORM.id == str(campaign_id)
        ).first()
        return self._to_entity(orm) if orm else None
    
    def find_all(self) -> List[Campaign]:
        """Find all campaigns"""
        orms = self.session.query(CampaignORM).order_by(
            CampaignORM.start_date.desc()
        ).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_by_status(self, status: CampaignStatus) -> List[Campaign]:
        """Find campaigns by status"""
        orms = self.session.query(CampaignORM).filter(
            CampaignORM.status == status.value
        ).all()
        return [self._to_entity(orm) for orm in orms]
    
    def find_recent(self, limit: int = 10) -> List[Campaign]:
        """Find recent campaigns"""
        orms = self.session.query(CampaignORM).order_by(
            CampaignORM.start_date.desc()
        ).limit(limit).all()
        return [self._to_entity(orm) for orm in orms]
    
    def search(self, query: str = None, status: CampaignStatus = None) -> List[Campaign]:
        """Search campaigns by query and/or status using SQL"""
        q = self.session.query(CampaignORM)
        
        if status:
            q = q.filter(CampaignORM.status == status.value)
        
        if query and query.strip():
            search_term = f"%{query.lower().strip()}%"
            from sqlalchemy import or_, func
            q = q.filter(
                or_(
                    func.lower(CampaignORM.name).like(search_term),
                    func.lower(CampaignORM.theme).like(search_term)
                )
            )
        
        orms = q.order_by(CampaignORM.start_date.desc()).all()
        return [self._to_entity(orm) for orm in orms]
    
    def save(self, campaign: Campaign) -> Campaign:
        """Save campaign (create or update)"""
        existing = self.session.query(CampaignORM).filter(
            CampaignORM.id == str(campaign.id)
        ).first()
        
        if existing:
            self._update_orm(existing, campaign)
        else:
            orm = self._to_orm(campaign)
            self.session.add(orm)
        
        self.session.commit()
        return campaign
    
    def delete(self, campaign_id: CampaignId) -> bool:
        """Delete campaign with proper cascade"""
        orm = self.session.query(CampaignORM).filter(
            CampaignORM.id == str(campaign_id)
        ).first()
        
        if not orm:
            return False
        
        self.session.delete(orm)
        self.session.commit()
        return True
    
    def count_by_status(self, status: CampaignStatus) -> int:
        """Count campaigns by status"""
        return self.session.query(CampaignORM).filter(
            CampaignORM.status == status.value
        ).count()
    
    def _to_entity(self, orm: CampaignORM) -> Campaign:
        """Convert ORM to domain entity"""
        ideas = [
            CampaignIdea(
                id=idea_orm.id,
                theme=idea_orm.theme,
                core_message=idea_orm.core_message,
                target_segments=idea_orm.target_segments,
                competitive_angle=idea_orm.competitive_angle
            )
            for idea_orm in orm.ideas
        ]
        
        channel_mix = [
            ChannelPlan(
                channel=ch_orm.channel,
                content_type=ch_orm.content_type,
                frequency=ch_orm.frequency,
                budget_allocation=ch_orm.budget_allocation,
                success_metrics=ch_orm.success_metrics
            )
            for ch_orm in orm.channel_mix
        ]
        
        metrics = None
        if orm.metrics_json:
            metrics = CampaignMetrics(**orm.metrics_json)
        
        feedback_history = []
        if orm.feedback_history:
            feedback_history = [CampaignFeedback(**fb) for fb in orm.feedback_history]
        
        return Campaign(
            id=CampaignId(orm.id),
            name=orm.name,
            status=CampaignStatus(orm.status),
            theme=orm.theme,
            date_range=DateRange(orm.start_date, orm.end_date),
            ideas=ideas,
            channel_mix=channel_mix,
            total_budget=Money(orm.total_budget),
            expected_roi=orm.expected_roi,
            metrics=metrics,
            service_id=orm.service_id,
            feedback_history=feedback_history
        )
    
    def _to_orm(self, campaign: Campaign) -> CampaignORM:
        """Convert domain entity to ORM"""
        orm = CampaignORM(
            id=str(campaign.id),
            name=campaign.name,
            status=campaign.status.value,
            theme=campaign.theme,
            start_date=campaign.date_range.start_date,
            end_date=campaign.date_range.end_date,
            total_budget=float(campaign.total_budget.amount),
            expected_roi=campaign.expected_roi,
            metrics_json=self._metrics_to_json(campaign.metrics) if campaign.metrics else None,
            service_id=campaign.service_id,
            feedback_history=self._feedback_to_json(campaign.feedback_history) if campaign.feedback_history else []
        )
        
        for idea in campaign.ideas:
            idea_orm = CampaignIdeaORM(
                id=idea.id,
                campaign_id=str(campaign.id),
                theme=idea.theme,
                core_message=idea.core_message,
                target_segments=idea.target_segments,
                competitive_angle=idea.competitive_angle
            )
            orm.ideas.append(idea_orm)
        
        for channel in campaign.channel_mix:
            ch_orm = ChannelPlanORM(
                id=str(uuid.uuid4())[:8],
                campaign_id=str(campaign.id),
                channel=channel.channel,
                content_type=channel.content_type,
                frequency=channel.frequency,
                budget_allocation=channel.budget_allocation,
                success_metrics=channel.success_metrics
            )
            orm.channel_mix.append(ch_orm)
        
        return orm
    
    def _update_orm(self, orm: CampaignORM, campaign: Campaign):
        """Update existing ORM from domain entity"""
        orm.name = campaign.name
        orm.status = campaign.status.value
        orm.theme = campaign.theme
        orm.start_date = campaign.date_range.start_date
        orm.end_date = campaign.date_range.end_date
        orm.total_budget = float(campaign.total_budget.amount)
        orm.expected_roi = campaign.expected_roi
        orm.metrics_json = self._metrics_to_json(campaign.metrics) if campaign.metrics else None
        orm.service_id = campaign.service_id
        orm.feedback_history = self._feedback_to_json(campaign.feedback_history) if campaign.feedback_history else []
        
        orm.ideas.clear()
        for idea in campaign.ideas:
            idea_orm = CampaignIdeaORM(
                id=idea.id,
                campaign_id=str(campaign.id),
                theme=idea.theme,
                core_message=idea.core_message,
                target_segments=idea.target_segments,
                competitive_angle=idea.competitive_angle
            )
            orm.ideas.append(idea_orm)
        
        orm.channel_mix.clear()
        for channel in campaign.channel_mix:
            ch_orm = ChannelPlanORM(
                id=str(uuid.uuid4())[:8],
                campaign_id=str(campaign.id),
                channel=channel.channel,
                content_type=channel.content_type,
                frequency=channel.frequency,
                budget_allocation=channel.budget_allocation,
                success_metrics=channel.success_metrics
            )
            orm.channel_mix.append(ch_orm)
    
    def _metrics_to_json(self, metrics: CampaignMetrics) -> dict:
        """Convert metrics to JSON"""
        return {
            "engagement": metrics.engagement,
            "leads": metrics.leads,
            "conversions": metrics.conversions
        }
    
    def _feedback_to_json(self, feedback_list: List[CampaignFeedback]) -> list:
        """Convert feedback list to JSON"""
        return [
            {
                "feedback_type": fb.feedback_type,
                "target": fb.target,
                "comment": fb.comment,
                "timestamp": fb.timestamp
            }
            for fb in feedback_list
        ]
