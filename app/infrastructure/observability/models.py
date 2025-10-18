"""Observability models for agent decisions and execution traces"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class DecisionType(str, Enum):
    """Types of agent decisions"""
    CAMPAIGN_GENERATION = "campaign_generation"
    CUSTOMER_TARGETING = "customer_targeting"
    CHANNEL_SELECTION = "channel_selection"
    CONTENT_OPTIMIZATION = "content_optimization"
    BUDGET_ALLOCATION = "budget_allocation"


class ReasoningStep(str, Enum):
    """Steps in agent reasoning process"""
    DATA_RETRIEVAL = "data_retrieval"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    EVALUATION = "evaluation"


@dataclass
class AgentDecision:
    """Represents a single decision made by the agent"""
    decision_id: str
    timestamp: datetime
    decision_type: DecisionType
    reasoning_chain: List[str]
    data_sources: List[str]
    confidence_score: float
    session_id: Optional[str] = None
    outcome: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert decision to dictionary for logging"""
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp.isoformat(),
            "decision_type": self.decision_type.value,
            "reasoning_chain": self.reasoning_chain,
            "data_sources": self.data_sources,
            "confidence_score": self.confidence_score,
            "session_id": self.session_id,
            "outcome": self.outcome,
            "metadata": self.metadata
        }


@dataclass
class ExecutionTrace:
    """Tracks agent execution flow and performance"""
    trace_id: str
    start_time: datetime
    end_time: Optional[datetime]
    steps: List[Dict[str, Any]] = field(default_factory=list)
    total_tokens_used: int = 0
    total_api_calls: int = 0
    success: bool = True
    error_message: Optional[str] = None
    session_id: Optional[str] = None
    
    def add_step(self, step_name: str, step_type: ReasoningStep, duration_ms: float, metadata: Optional[Dict] = None):
        """Add a step to the execution trace"""
        self.steps.append({
            "step_name": step_name,
            "step_type": step_type.value,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
    
    def to_dict(self) -> Dict:
        """Convert trace to dictionary for logging"""
        return {
            "trace_id": self.trace_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_duration_ms": (self.end_time - self.start_time).total_seconds() * 1000 if self.end_time else None,
            "steps": self.steps,
            "total_tokens_used": self.total_tokens_used,
            "total_api_calls": self.total_api_calls,
            "success": self.success,
            "error_message": self.error_message,
            "session_id": self.session_id
        }
