"""Agent Decision and Execution Trace SQLAlchemy models"""
from sqlalchemy import Column, String, Float, DateTime, Text, JSON, Integer, Boolean, Index
from app.infrastructure.config.database import Base
from datetime import datetime


class AgentDecisionORM(Base):
    """
    Agent Decision ORM model - stores all AI agent decisions with full audit trail
    
    Critical for compliance (GDPR, SOC 2, HIPAA) and observability
    """
    __tablename__ = "agent_decisions"
    
    id = Column(String, primary_key=True)
    decision_id = Column(String, nullable=False, unique=True, index=True)
    session_id = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    decision_type = Column(String, nullable=False, index=True)
    
    reasoning_chain = Column(JSON, nullable=False)
    data_sources = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=False)
    decision_metadata = Column(JSON, nullable=True)
    
    model_used = Column(String, nullable=True)
    latency_ms = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_decision_type_timestamp', 'decision_type', 'timestamp'),
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    )


class ExecutionTraceORM(Base):
    """
    Execution Trace ORM model - stores detailed step-by-step execution traces
    
    Enables debugging, performance analysis, and understanding agent behavior
    """
    __tablename__ = "execution_traces"
    
    id = Column(String, primary_key=True)
    trace_id = Column(String, nullable=False, unique=True, index=True)
    session_id = Column(String, nullable=True, index=True)
    
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=True)
    total_duration_ms = Column(Float, nullable=True)
    
    steps = Column(JSON, nullable=False)
    success = Column(Boolean, nullable=False, default=True)
    error_message = Column(Text, nullable=True)
    
    trace_metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_trace_start_time', 'start_time'),
        Index('idx_trace_success', 'success', 'start_time'),
    )


class ReasoningStepORM(Base):
    """
    Reasoning Step ORM model - stores individual reasoning steps within a trace
    
    Provides granular visibility into agent's thought process
    """
    __tablename__ = "reasoning_steps"
    
    id = Column(String, primary_key=True)
    trace_id = Column(String, nullable=False, index=True)
    step_number = Column(Integer, nullable=False)
    
    step_type = Column(String, nullable=False)
    step_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    duration_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    step_metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_step_trace_number', 'trace_id', 'step_number'),
    )
