"""Repository for agent memory and learnings persistence"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from app.infrastructure.persistence.models.agent_memory_orm import (
    AgentMemoryORM,
    AgentLearningORM,
    AgentConversationORM,
    MultiAgentCoordinationORM,
    AgentFeedbackLoopORM
)


class AgentMemoryRepository:
    """Repository for managing agent memory persistence"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def store_memory(
        self,
        agent_id: str,
        memory_type: str,
        content: str,
        importance_score: float = 0.5,
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> AgentMemoryORM:
        """Store a new memory"""
        memory = AgentMemoryORM(
            id=str(uuid.uuid4()),
            memory_id=f"mem_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            session_id=session_id,
            memory_type=memory_type,
            content=content,
            context=context or {},
            importance_score=importance_score,
            tags=tags or [],
            relevance_decay=1.0,
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            access_count=0
        )
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory
    
    def retrieve_memories(
        self,
        agent_id: str,
        memory_type: Optional[str] = None,
        min_importance: float = 0.0,
        limit: int = 50
    ) -> List[AgentMemoryORM]:
        """Retrieve memories for an agent"""
        query = self.db.query(AgentMemoryORM).filter(
            AgentMemoryORM.agent_id == agent_id,
            AgentMemoryORM.importance_score >= min_importance
        )
        
        if memory_type:
            query = query.filter(AgentMemoryORM.memory_type == memory_type)
        
        memories = query.order_by(
            desc(AgentMemoryORM.importance_score),
            desc(AgentMemoryORM.created_at)
        ).limit(limit).all()
        
        # Update access tracking
        for memory in memories:
            memory.last_accessed = datetime.utcnow()
            memory.access_count += 1
        self.db.commit()
        
        return memories
    
    def store_learning(
        self,
        agent_id: str,
        source_type: str,
        learning_category: str,
        finding: str,
        evidence: Dict,
        confidence: float = 0.5,
        impact_score: Optional[float] = None,
        source_id: Optional[str] = None
    ) -> AgentLearningORM:
        """Store a new learning"""
        learning = AgentLearningORM(
            id=str(uuid.uuid4()),
            learning_id=f"learn_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            source_type=source_type,
            source_id=source_id,
            learning_category=learning_category,
            finding=finding,
            evidence=evidence,
            confidence=confidence,
            impact_score=impact_score,
            validation_count=0,
            applied_count=0,
            status='active',
            created_at=datetime.utcnow()
        )
        self.db.add(learning)
        self.db.commit()
        self.db.refresh(learning)
        return learning
    
    def retrieve_learnings(
        self,
        agent_id: Optional[str] = None,
        learning_category: Optional[str] = None,
        min_confidence: float = 0.0,
        status: str = 'active',
        limit: int = 100
    ) -> List[AgentLearningORM]:
        """Retrieve learnings"""
        query = self.db.query(AgentLearningORM).filter(
            AgentLearningORM.confidence >= min_confidence,
            AgentLearningORM.status == status
        )
        
        if agent_id:
            query = query.filter(AgentLearningORM.agent_id == agent_id)
        
        if learning_category:
            query = query.filter(AgentLearningORM.learning_category == learning_category)
        
        return query.order_by(
            desc(AgentLearningORM.confidence),
            desc(AgentLearningORM.created_at)
        ).limit(limit).all()
    
    def update_learning_validation(self, learning_id: str, validated: bool):
        """Update learning validation count"""
        learning = self.db.query(AgentLearningORM).filter(
            AgentLearningORM.learning_id == learning_id
        ).first()
        
        if learning:
            if validated:
                learning.validation_count += 1
            else:
                learning.confidence = max(0.0, learning.confidence - 0.1)
            self.db.commit()
    
    def record_learning_application(self, learning_id: str):
        """Record that a learning was applied"""
        learning = self.db.query(AgentLearningORM).filter(
            AgentLearningORM.learning_id == learning_id
        ).first()
        
        if learning:
            learning.applied_count += 1
            learning.last_applied = datetime.utcnow()
            self.db.commit()
    
    def store_coordination_workflow(
        self,
        coordinator_agent: str,
        participant_agents: List[str],
        task_type: str,
        task_description: str,
        total_steps: int,
        agent_assignments: Dict,
        session_id: Optional[str] = None
    ) -> MultiAgentCoordinationORM:
        """Store a new multi-agent coordination workflow"""
        workflow = MultiAgentCoordinationORM(
            id=str(uuid.uuid4()),
            coordination_id=f"coord_{uuid.uuid4().hex[:8]}",
            session_id=session_id,
            coordinator_agent=coordinator_agent,
            participant_agents=participant_agents,
            task_type=task_type,
            task_description=task_description,
            workflow_state='initiated',
            current_step=0,
            total_steps=total_steps,
            agent_assignments=agent_assignments,
            communication_log=[],
            start_time=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow
    
    def update_workflow_progress(
        self,
        coordination_id: str,
        current_step: int,
        workflow_state: str,
        communication_entry: Optional[Dict] = None
    ):
        """Update workflow progress"""
        workflow = self.db.query(MultiAgentCoordinationORM).filter(
            MultiAgentCoordinationORM.coordination_id == coordination_id
        ).first()
        
        if workflow:
            workflow.current_step = current_step
            workflow.workflow_state = workflow_state
            
            if communication_entry:
                comm_log = workflow.communication_log or []
                comm_log.append(communication_entry)
                workflow.communication_log = comm_log
            
            self.db.commit()
    
    def complete_workflow(
        self,
        coordination_id: str,
        result: Dict,
        success: bool
    ):
        """Mark workflow as completed"""
        workflow = self.db.query(MultiAgentCoordinationORM).filter(
            MultiAgentCoordinationORM.coordination_id == coordination_id
        ).first()
        
        if workflow:
            workflow.workflow_state = 'completed' if success else 'failed'
            workflow.end_time = datetime.utcnow()
            workflow.duration_ms = (workflow.end_time - workflow.start_time).total_seconds() * 1000
            workflow.result = result
            workflow.success = success
            self.db.commit()
    
    def get_active_workflows(self) -> List[MultiAgentCoordinationORM]:
        """Get all active coordination workflows"""
        return self.db.query(MultiAgentCoordinationORM).filter(
            MultiAgentCoordinationORM.workflow_state.in_(['initiated', 'in_progress'])
        ).order_by(desc(MultiAgentCoordinationORM.start_time)).all()
    
    def store_feedback_loop(
        self,
        agent_id: str,
        initial_decision_id: str,
        context: Dict,
        expected_outcome: Dict,
        actual_outcome: Optional[Dict] = None
    ) -> AgentFeedbackLoopORM:
        """Store a new feedback loop for self-correction"""
        loop = AgentFeedbackLoopORM(
            id=str(uuid.uuid4()),
            loop_id=f"loop_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id,
            initial_decision_id=initial_decision_id,
            context=context,
            expected_outcome=expected_outcome,
            actual_outcome=actual_outcome,
            deviation_score=None,
            correction_needed=False,
            cycle_number=1,
            status='monitoring',
            created_at=datetime.utcnow()
        )
        self.db.add(loop)
        self.db.commit()
        self.db.refresh(loop)
        return loop
    
    def update_feedback_loop(
        self,
        loop_id: str,
        actual_outcome: Dict,
        deviation_score: float,
        correction_needed: bool,
        correction_applied: Optional[Dict] = None,
        learning_id: Optional[str] = None
    ):
        """Update feedback loop with actual results"""
        loop = self.db.query(AgentFeedbackLoopORM).filter(
            AgentFeedbackLoopORM.loop_id == loop_id
        ).first()
        
        if loop:
            loop.actual_outcome = actual_outcome
            loop.deviation_score = deviation_score
            loop.correction_needed = correction_needed
            loop.correction_applied = correction_applied
            loop.learning_generated = learning_id
            loop.status = 'correcting' if correction_needed else 'completed'
            loop.completed_at = datetime.utcnow() if not correction_needed else None
            self.db.commit()


def get_agent_memory_repository(db: Session) -> AgentMemoryRepository:
    """Factory function to get agent memory repository"""
    return AgentMemoryRepository(db)
