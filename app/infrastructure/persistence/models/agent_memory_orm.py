"""Agent Memory and Learning SQLAlchemy models for persistent memory across sessions"""
from sqlalchemy import Column, String, DateTime, Text, JSON, Float, Integer, Boolean, Index, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.config.database import Base
from datetime import datetime


class AgentMemoryORM(Base):
    """
    Agent Memory ORM - stores persistent context and learnings across sessions
    
    Enables the agent to:
    - Remember past interactions and decisions
    - Build context over time
    - Reference historical learnings
    - Maintain continuity across sessions
    """
    __tablename__ = "agent_memory"
    
    id = Column(String, primary_key=True)
    memory_id = Column(String, nullable=False, unique=True, index=True)
    agent_id = Column(String, nullable=False, index=True)  # Which agent owns this memory
    session_id = Column(String, nullable=True, index=True)
    
    memory_type = Column(String, nullable=False, index=True)  # conversation, learning, insight, pattern
    content = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)
    
    importance_score = Column(Float, nullable=False, default=0.5)  # 0.0-1.0
    relevance_decay = Column(Float, nullable=False, default=1.0)  # Decreases over time
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    last_accessed = Column(DateTime, nullable=False, default=datetime.utcnow)
    access_count = Column(Integer, nullable=False, default=0)
    
    tags = Column(JSON, nullable=True)  # For easy retrieval
    metadata = Column(JSON, nullable=True)
    
    __table_args__ = (
        Index('idx_agent_type_importance', 'agent_id', 'memory_type', 'importance_score'),
        Index('idx_session_created', 'session_id', 'created_at'),
    )


class AgentLearningORM(Base):
    """
    Agent Learning ORM - stores feedback and learnings from campaign outcomes
    
    Enables self-correction and continuous improvement by:
    - Recording what worked and what didn't
    - Tracking patterns of success and failure
    - Adjusting future behavior based on past outcomes
    """
    __tablename__ = "agent_learnings"
    
    id = Column(String, primary_key=True)
    learning_id = Column(String, nullable=False, unique=True, index=True)
    agent_id = Column(String, nullable=False, index=True)
    
    source_type = Column(String, nullable=False, index=True)  # campaign_outcome, user_feedback, self_evaluation
    source_id = Column(String, nullable=True)  # Campaign ID, decision ID, etc.
    
    learning_category = Column(String, nullable=False, index=True)  # strategy, channel_selection, messaging, targeting
    finding = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=False)  # Metrics, data that support this learning
    
    confidence = Column(Float, nullable=False, default=0.5)  # How confident are we in this learning?
    validation_count = Column(Integer, nullable=False, default=0)  # How many times has this been validated?
    
    impact_score = Column(Float, nullable=True)  # Measured impact (e.g., +10% conversion)
    applied_count = Column(Integer, nullable=False, default=0)  # How many times has this been applied?
    
    status = Column(String, nullable=False, default='active')  # active, deprecated, invalidated
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    last_applied = Column(DateTime, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    __table_args__ = (
        Index('idx_category_confidence', 'learning_category', 'confidence'),
        Index('idx_status_impact', 'status', 'impact_score'),
    )


class AgentConversationORM(Base):
    """
    Agent Conversation ORM - stores conversation history for context continuity
    
    Enables multi-turn interactions with memory of what was discussed
    """
    __tablename__ = "agent_conversations"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    
    turn_number = Column(Integer, nullable=False)
    role = Column(String, nullable=False)  # user, agent, system
    agent_id = Column(String, nullable=True)  # Which agent spoke
    
    content = Column(Text, nullable=False)
    intent = Column(String, nullable=True)  # Detected user intent
    entities = Column(JSON, nullable=True)  # Extracted entities
    
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    metadata = Column(JSON, nullable=True)
    
    __table_args__ = (
        Index('idx_conversation_turn', 'conversation_id', 'turn_number'),
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    )


class MultiAgentCoordinationORM(Base):
    """
    Multi-Agent Coordination ORM - tracks coordination between multiple agents
    
    Enables:
    - Agent-to-agent communication
    - Task delegation and handoffs
    - Collaborative decision-making
    - Coordinated workflows
    """
    __tablename__ = "multi_agent_coordination"
    
    id = Column(String, primary_key=True)
    coordination_id = Column(String, nullable=False, unique=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    
    coordinator_agent = Column(String, nullable=False)  # Which agent is coordinating
    participant_agents = Column(JSON, nullable=False)  # List of participating agents
    
    task_type = Column(String, nullable=False, index=True)  # campaign_generation, research, optimization
    task_description = Column(Text, nullable=False)
    
    workflow_state = Column(String, nullable=False, default='initiated')  # initiated, in_progress, completed, failed
    current_step = Column(Integer, nullable=False, default=0)
    total_steps = Column(Integer, nullable=False)
    
    agent_assignments = Column(JSON, nullable=False)  # Which agent does what
    communication_log = Column(JSON, nullable=False, default=list)  # Agent-to-agent messages
    
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_ms = Column(Float, nullable=True)
    
    result = Column(JSON, nullable=True)
    success = Column(Boolean, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_task_state', 'task_type', 'workflow_state'),
        Index('idx_coordinator_time', 'coordinator_agent', 'start_time'),
    )


class AgentFeedbackLoopORM(Base):
    """
    Agent Feedback Loop ORM - tracks self-correction cycles
    
    Records:
    - Initial decisions
    - Observed outcomes
    - Corrections made
    - Learning updates
    """
    __tablename__ = "agent_feedback_loops"
    
    id = Column(String, primary_key=True)
    loop_id = Column(String, nullable=False, unique=True, index=True)
    agent_id = Column(String, nullable=False, index=True)
    
    initial_decision_id = Column(String, nullable=False)
    context = Column(JSON, nullable=False)
    
    expected_outcome = Column(JSON, nullable=False)
    actual_outcome = Column(JSON, nullable=True)
    
    deviation_score = Column(Float, nullable=True)  # How far off were we?
    correction_needed = Column(Boolean, nullable=False, default=False)
    correction_applied = Column(JSON, nullable=True)
    
    learning_generated = Column(String, nullable=True)  # Foreign key to agent_learnings
    
    cycle_number = Column(Integer, nullable=False, default=1)  # How many correction cycles?
    status = Column(String, nullable=False, default='monitoring')  # monitoring, correcting, completed
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    __table_args__ = (
        Index('idx_agent_status', 'agent_id', 'status'),
        Index('idx_correction_needed', 'correction_needed', 'created_at'),
    )
