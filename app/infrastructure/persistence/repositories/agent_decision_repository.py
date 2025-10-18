"""Repository for persisting and querying agent decisions and execution traces"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_

from app.infrastructure.persistence.models.agent_decision_orm import (
    AgentDecisionORM,
    ExecutionTraceORM,
    ReasoningStepORM
)
from app.infrastructure.observability.models import (
    AgentDecision,
    ExecutionTrace,
    ReasoningStep as ReasoningStepEnum,
    DecisionType
)


class AgentDecisionRepository:
    """
    Repository for agent decisions and execution traces
    
    Provides persistent storage with query capabilities for audit trails
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def save_decision(self, decision: AgentDecision) -> None:
        """Save agent decision to database"""
        orm = AgentDecisionORM(
            id=str(uuid.uuid4()),
            decision_id=decision.decision_id,
            session_id=decision.session_id,
            timestamp=decision.timestamp,
            decision_type=decision.decision_type.value,
            reasoning_chain=decision.reasoning_chain,
            data_sources=decision.data_sources,
            confidence_score=decision.confidence_score,
            decision_metadata=decision.metadata or {},
            model_used=decision.metadata.get("model_used") if decision.metadata else None,
            latency_ms=decision.metadata.get("latency_ms") if decision.metadata else None,
            error_message=decision.metadata.get("error_message") if decision.metadata else None,
            created_at=datetime.utcnow()
        )
        
        self.session.add(orm)
        self.session.commit()
    
    def save_trace(self, trace: ExecutionTrace) -> None:
        """Save execution trace to database"""
        total_duration_ms = None
        if trace.end_time and trace.start_time:
            total_duration_ms = (trace.end_time - trace.start_time).total_seconds() * 1000
        
        orm = ExecutionTraceORM(
            id=str(uuid.uuid4()),
            trace_id=trace.trace_id,
            session_id=getattr(trace, 'session_id', None),
            start_time=trace.start_time,
            end_time=trace.end_time,
            total_duration_ms=total_duration_ms,
            steps=[self._step_to_dict(step) for step in trace.steps],
            success=trace.success,
            error_message=trace.error_message,
            trace_metadata={},
            created_at=datetime.utcnow()
        )
        
        self.session.add(orm)
        self.session.commit()
    
    def find_decision_by_id(self, decision_id: str) -> Optional[AgentDecision]:
        """Find decision by ID"""
        orm = self.session.query(AgentDecisionORM).filter(
            AgentDecisionORM.decision_id == decision_id
        ).first()
        
        return self._orm_to_decision(orm) if orm else None
    
    def find_decisions_by_session(self, session_id: str, limit: int = 100) -> List[AgentDecision]:
        """Find all decisions for a session"""
        orms = self.session.query(AgentDecisionORM).filter(
            AgentDecisionORM.session_id == session_id
        ).order_by(desc(AgentDecisionORM.timestamp)).limit(limit).all()
        
        return [self._orm_to_decision(orm) for orm in orms]
    
    def find_decisions_by_type(self, decision_type: DecisionType, limit: int = 100) -> List[AgentDecision]:
        """Find decisions by type"""
        orms = self.session.query(AgentDecisionORM).filter(
            AgentDecisionORM.decision_type == decision_type.value
        ).order_by(desc(AgentDecisionORM.timestamp)).limit(limit).all()
        
        return [self._orm_to_decision(orm) for orm in orms]
    
    def find_recent_decisions(self, limit: int = 50) -> List[AgentDecision]:
        """Find recent decisions"""
        orms = self.session.query(AgentDecisionORM).order_by(
            desc(AgentDecisionORM.timestamp)
        ).limit(limit).all()
        
        return [self._orm_to_decision(orm) for orm in orms]
    
    def find_decisions_in_range(
        self,
        start_date: datetime,
        end_date: datetime,
        decision_type: Optional[DecisionType] = None
    ) -> List[AgentDecision]:
        """Find decisions within date range"""
        query = self.session.query(AgentDecisionORM).filter(
            and_(
                AgentDecisionORM.timestamp >= start_date,
                AgentDecisionORM.timestamp <= end_date
            )
        )
        
        if decision_type:
            query = query.filter(AgentDecisionORM.decision_type == decision_type.value)
        
        orms = query.order_by(desc(AgentDecisionORM.timestamp)).all()
        return [self._orm_to_decision(orm) for orm in orms]
    
    def find_trace_by_id(self, trace_id: str) -> Optional[ExecutionTrace]:
        """Find execution trace by ID"""
        orm = self.session.query(ExecutionTraceORM).filter(
            ExecutionTraceORM.trace_id == trace_id
        ).first()
        
        return self._orm_to_trace(orm) if orm else None
    
    def find_recent_traces(self, limit: int = 50, success_only: bool = False) -> List[ExecutionTrace]:
        """Find recent execution traces"""
        query = self.session.query(ExecutionTraceORM)
        
        if success_only:
            query = query.filter(ExecutionTraceORM.success.is_(True))
        
        orms = query.order_by(desc(ExecutionTraceORM.start_time)).limit(limit).all()
        return [self._orm_to_trace(orm) for orm in orms]
    
    def get_decision_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get decision statistics for the last N days"""
        since = datetime.utcnow() - timedelta(days=days)
        
        total = self.session.query(AgentDecisionORM).filter(
            AgentDecisionORM.timestamp >= since
        ).count()
        
        by_type = {}
        for decision_type in DecisionType:
            count = self.session.query(AgentDecisionORM).filter(
                and_(
                    AgentDecisionORM.timestamp >= since,
                    AgentDecisionORM.decision_type == decision_type.value
                )
            ).count()
            by_type[decision_type.value] = count
        
        avg_confidence = self.session.query(AgentDecisionORM).filter(
            AgentDecisionORM.timestamp >= since
        ).with_entities(AgentDecisionORM.confidence_score).all()
        
        avg_conf_score = sum(c[0] for c in avg_confidence) / len(avg_confidence) if avg_confidence else 0.0
        
        return {
            "total_decisions": total,
            "by_type": by_type,
            "average_confidence": avg_conf_score,
            "days": days
        }
    
    def get_trace_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get trace statistics for the last N days"""
        since = datetime.utcnow() - timedelta(days=days)
        
        total = self.session.query(ExecutionTraceORM).filter(
            ExecutionTraceORM.start_time >= since
        ).count()
        
        successful = self.session.query(ExecutionTraceORM).filter(
            and_(
                ExecutionTraceORM.start_time >= since,
                ExecutionTraceORM.success == True
            )
        ).count()
        
        failed = total - successful
        
        durations = self.session.query(ExecutionTraceORM).filter(
            and_(
                ExecutionTraceORM.start_time >= since,
                ExecutionTraceORM.total_duration_ms.isnot(None)
            )
        ).with_entities(ExecutionTraceORM.total_duration_ms).all()
        
        avg_duration_ms = sum(d[0] for d in durations) / len(durations) if durations else 0.0
        
        return {
            "total_traces": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0.0,
            "average_duration_ms": avg_duration_ms,
            "days": days
        }
    
    def delete_old_decisions(self, days: int = 90) -> int:
        """Delete decisions older than N days (for retention policy)"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        count = self.session.query(AgentDecisionORM).filter(
            AgentDecisionORM.timestamp < cutoff
        ).delete()
        
        self.session.commit()
        return count
    
    def delete_old_traces(self, days: int = 90) -> int:
        """Delete traces older than N days (for retention policy)"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        count = self.session.query(ExecutionTraceORM).filter(
            ExecutionTraceORM.start_time < cutoff
        ).delete()
        
        self.session.commit()
        return count
    
    def _orm_to_decision(self, orm: AgentDecisionORM) -> AgentDecision:
        """Convert ORM to domain model"""
        return AgentDecision(
            decision_id=orm.decision_id,
            timestamp=orm.timestamp,
            decision_type=DecisionType(orm.decision_type),
            reasoning_chain=orm.reasoning_chain,
            data_sources=orm.data_sources,
            confidence_score=orm.confidence_score,
            session_id=orm.session_id,
            metadata=orm.decision_metadata or {}
        )
    
    def _orm_to_trace(self, orm: ExecutionTraceORM) -> ExecutionTrace:
        """Convert ORM to domain model"""
        trace = ExecutionTrace(
            trace_id=orm.trace_id,
            start_time=orm.start_time,
            end_time=orm.end_time
        )
        trace.steps = orm.steps if orm.steps else []
        trace.success = orm.success
        trace.error_message = orm.error_message
        trace.session_id = orm.session_id
        
        return trace
    
    def _step_to_dict(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Convert step dict - pass through since it's already a dict"""
        return step
