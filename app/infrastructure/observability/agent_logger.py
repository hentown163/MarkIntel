"""Agent observability logger for tracking reasoning, decisions, and execution traces"""
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from app.infrastructure.observability.models import (
    AgentDecision,
    ExecutionTrace,
    ReasoningStep,
    DecisionType
)


class AgentObservabilityLogger:
    """
    Observability logger for autonomous agent
    
    This class provides comprehensive logging and monitoring capabilities
    for the agent's reasoning process, decisions, and execution traces.
    
    Supports both in-memory and database persistence for compliance and audit trails.
    """
    
    def __init__(
        self,
        log_level: int = logging.INFO,
        enable_database_logging: bool = False,
        db_repository=None
    ):
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
        
        # In-memory storage (always active for quick access)
        self.decisions: List[AgentDecision] = []
        self.execution_traces: List[ExecutionTrace] = []
        
        # Database persistence (opt-in via feature flag)
        self.enable_database_logging = enable_database_logging
        self.db_repository = db_repository
        
        if self.enable_database_logging and not self.db_repository:
            self.logger.warning(
                "Database logging enabled but no repository provided. "
                "Falling back to in-memory only."
            )
            self.enable_database_logging = False
    
    def log_decision(self, decision: AgentDecision):
        """
        Log an agent decision with full reasoning chain
        
        Stores in-memory and optionally persists to database for audit trail
        """
        # In-memory storage
        self.decisions.append(decision)
        
        # Console logging
        self.logger.info(
            f"Agent Decision | Type: {decision.decision_type.value} | "
            f"Confidence: {decision.confidence_score:.2%} | "
            f"Reasoning Steps: {len(decision.reasoning_chain)}"
        )
        self.logger.debug(f"Decision Details: {json.dumps(decision.to_dict(), indent=2)}")
        
        # Database persistence (async, non-blocking)
        if self.enable_database_logging and self.db_repository:
            try:
                asyncio.create_task(self._persist_decision_async(decision))
            except RuntimeError:
                # No event loop running, do sync persistence
                self._persist_decision_sync(decision)
    
    def log_reasoning_step(self, trace_id: str, step_name: str, reasoning: str, data_used: List[str]):
        """Log a single reasoning step in the agent's thought process"""
        self.logger.info(
            f"[{trace_id}] Reasoning Step: {step_name}"
        )
        self.logger.debug(f"Reasoning: {reasoning}")
        self.logger.debug(f"Data Sources: {', '.join(data_used)}")
    
    def start_execution_trace(self, trace_id: str, session_id: Optional[str] = None) -> ExecutionTrace:
        """Start a new execution trace"""
        trace = ExecutionTrace(
            trace_id=trace_id,
            start_time=datetime.now(),
            end_time=None,
            session_id=session_id
        )
        self.execution_traces.append(trace)
        self.logger.info(f"Started execution trace: {trace_id}")
        return trace
    
    def end_execution_trace(self, trace_id: str, success: bool = True, error_message: Optional[str] = None):
        """
        End an execution trace
        
        Persists to database if enabled for audit and performance tracking
        """
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
            
            # Database persistence (async, non-blocking)
            if self.enable_database_logging and self.db_repository:
                try:
                    asyncio.create_task(self._persist_trace_async(trace))
                except RuntimeError:
                    # No event loop running, do sync persistence
                    self._persist_trace_sync(trace)
    
    def get_decision_history(
        self,
        decision_type: Optional[DecisionType] = None,
        limit: int = 100,
        from_database: bool = False
    ) -> List[AgentDecision]:
        """
        Retrieve decision history, optionally filtered by type
        
        Args:
            decision_type: Filter by decision type
            limit: Maximum number of decisions to return
            from_database: If True and DB logging enabled, query from database instead of memory
        """
        if from_database and self.enable_database_logging and self.db_repository:
            if decision_type:
                return self.db_repository.find_decisions_by_type(decision_type, limit=limit)
            else:
                return self.db_repository.find_recent_decisions(limit=limit)
        
        # In-memory fallback
        decisions = self.decisions
        if decision_type:
            decisions = [d for d in decisions if d.decision_type == decision_type]
        return decisions[-limit:]
    
    def get_execution_metrics(self, from_database: bool = False, days: int = 7) -> Dict[str, Any]:
        """
        Get aggregate execution metrics
        
        Args:
            from_database: If True and DB logging enabled, query from database
            days: Number of days to include in stats (for database queries)
        """
        if from_database and self.enable_database_logging and self.db_repository:
            return self.db_repository.get_trace_stats(days=days)
        
        # In-memory calculation
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
    
    async def _persist_decision_async(self, decision: AgentDecision):
        """Async persistence of decision to database"""
        try:
            self.db_repository.save_decision(decision)
        except Exception as e:
            self.logger.error(f"Failed to persist decision to database: {e}")
    
    async def _persist_trace_async(self, trace: ExecutionTrace):
        """Async persistence of trace to database"""
        try:
            self.db_repository.save_trace(trace)
        except Exception as e:
            self.logger.error(f"Failed to persist trace to database: {e}")
    
    def _persist_decision_sync(self, decision: AgentDecision):
        """Sync persistence of decision to database"""
        try:
            self.db_repository.save_decision(decision)
        except Exception as e:
            self.logger.error(f"Failed to persist decision to database: {e}")
    
    def _persist_trace_sync(self, trace: ExecutionTrace):
        """Sync persistence of trace to database"""
        try:
            self.db_repository.save_trace(trace)
        except Exception as e:
            self.logger.error(f"Failed to persist trace to database: {e}")


# Global singleton instance (in-memory only by default)
_agent_logger = AgentObservabilityLogger()


def get_agent_logger() -> AgentObservabilityLogger:
    """Get the global agent logger instance"""
    return _agent_logger


def initialize_agent_logger_with_db(db_repository, enable_database_logging: bool = True):
    """
    Initialize the global agent logger with database persistence
    
    Call this at application startup to enable database logging
    """
    global _agent_logger
    _agent_logger = AgentObservabilityLogger(
        enable_database_logging=enable_database_logging,
        db_repository=db_repository
    )
    return _agent_logger
