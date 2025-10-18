"""Agent observability logger for tracking reasoning, decisions, and execution traces"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import json


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
            "error_message": self.error_message
        }


class AgentObservabilityLogger:
    """
    Observability logger for autonomous agent
    
    This class provides comprehensive logging and monitoring capabilities
    for the agent's reasoning process, decisions, and execution traces.
    """
    
    def __init__(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger("nexus_agent")
        self.logger.setLevel(log_level)
        
        # Configure handler if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.decisions: List[AgentDecision] = []
        self.execution_traces: List[ExecutionTrace] = []
    
    def log_decision(self, decision: AgentDecision):
        """Log an agent decision with full reasoning chain"""
        self.decisions.append(decision)
        self.logger.info(
            f"Agent Decision | Type: {decision.decision_type.value} | "
            f"Confidence: {decision.confidence_score:.2%} | "
            f"Reasoning Steps: {len(decision.reasoning_chain)}"
        )
        self.logger.debug(f"Decision Details: {json.dumps(decision.to_dict(), indent=2)}")
    
    def log_reasoning_step(self, trace_id: str, step_name: str, reasoning: str, data_used: List[str]):
        """Log a single reasoning step in the agent's thought process"""
        self.logger.info(
            f"[{trace_id}] Reasoning Step: {step_name}"
        )
        self.logger.debug(f"Reasoning: {reasoning}")
        self.logger.debug(f"Data Sources: {', '.join(data_used)}")
    
    def start_execution_trace(self, trace_id: str) -> ExecutionTrace:
        """Start a new execution trace"""
        trace = ExecutionTrace(
            trace_id=trace_id,
            start_time=datetime.now(),
            end_time=None
        )
        self.execution_traces.append(trace)
        self.logger.info(f"Started execution trace: {trace_id}")
        return trace
    
    def end_execution_trace(self, trace_id: str, success: bool = True, error_message: Optional[str] = None):
        """End an execution trace"""
        trace = next((t for t in self.execution_traces if t.trace_id == trace_id), None)
        if trace:
            trace.end_time = datetime.now()
            trace.success = success
            trace.error_message = error_message
            
            duration = (trace.end_time - trace.start_time).total_seconds() * 1000
            self.logger.info(
                f"Completed execution trace: {trace_id} | "
                f"Duration: {duration:.2f}ms | "
                f"Steps: {len(trace.steps)} | "
                f"Success: {success}"
            )
    
    def get_decision_history(self, decision_type: Optional[DecisionType] = None) -> List[AgentDecision]:
        """Retrieve decision history, optionally filtered by type"""
        if decision_type:
            return [d for d in self.decisions if d.decision_type == decision_type]
        return self.decisions
    
    def get_execution_metrics(self) -> Dict[str, Any]:
        """Get aggregate execution metrics"""
        if not self.execution_traces:
            return {}
        
        completed_traces = [t for t in self.execution_traces if t.end_time]
        if not completed_traces:
            return {}
        
        total_duration = sum((t.end_time - t.start_time).total_seconds() * 1000 for t in completed_traces)
        avg_duration = total_duration / len(completed_traces)
        
        return {
            "total_executions": len(completed_traces),
            "successful_executions": sum(1 for t in completed_traces if t.success),
            "failed_executions": sum(1 for t in completed_traces if not t.success),
            "avg_duration_ms": avg_duration,
            "total_tokens_used": sum(t.total_tokens_used for t in completed_traces),
            "total_api_calls": sum(t.total_api_calls for t in completed_traces)
        }
    
    def export_observability_data(self) -> Dict[str, Any]:
        """Export all observability data for analysis"""
        return {
            "decisions": [d.to_dict() for d in self.decisions],
            "execution_traces": [t.to_dict() for t in self.execution_traces],
            "metrics": self.get_execution_metrics()
        }


# Global singleton instance
_agent_logger = AgentObservabilityLogger()


def get_agent_logger() -> AgentObservabilityLogger:
    """Get the global agent logger instance"""
    return _agent_logger
