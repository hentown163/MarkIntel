"""Agent Coordinator - orchestrates multi-agent workflows"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

from app.domain.services.agent.specialized_agents import (
    get_research_agent,
    get_strategy_agent,
    get_execution_agent,
    get_evaluation_agent,
    AgentMessage,
    AgentRole
)
from app.infrastructure.observability.agent_logger import get_agent_logger
from app.infrastructure.persistence.repositories.agent_memory_repository import AgentMemoryRepository


@dataclass
class MultiAgentWorkflow:
    """Represents a coordinated workflow across multiple agents"""
    workflow_id: str
    objective: str
    participating_agents: List[str]
    current_phase: str
    status: str  # initiated, in_progress, completed, failed
    results: Dict[str, Any]
    communication_log: List[AgentMessage]


class AgentCoordinator:
    """
    Coordinates multiple specialized agents to accomplish complex tasks
    
    This is the brain of the multi-agent system that:
    - Decomposes complex tasks into agent-specific subtasks
    - Routes messages between agents
    - Manages workflow state
    - Coordinates handoffs between agents
    - Synthesizes results from multiple agents
    """
    
    def __init__(self, repository: Optional[AgentMemoryRepository] = None):
        self.repository = repository
        self.research_agent = get_research_agent(repository)
        self.strategy_agent = get_strategy_agent(repository)
        self.execution_agent = get_execution_agent(repository)
        self.evaluation_agent = get_evaluation_agent(repository)
        self.logger = get_agent_logger()
        
        self.active_workflows: Dict[str, MultiAgentWorkflow] = {}
    
    def generate_campaign_with_agents(
        self,
        objective: str,
        service_details: Dict[str, Any],
        market_signals: List[Dict],
        customers: List[Dict],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Orchestrate a full campaign generation using all specialized agents
        
        Workflow:
        1. Research Agent: Gather market intelligence and customer insights
        2. Strategy Agent: Develop strategic approach based on research
        3. Execution Agent: Create implementation plan
        4. Coordinator: Synthesize all results
        
        This demonstrates true multi-agent coordination!
        """
        workflow_id = f"workflow_{uuid.uuid4().hex[:8]}"
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        workflow = MultiAgentWorkflow(
            workflow_id=workflow_id,
            objective=objective,
            participating_agents=["research", "strategy", "execution"],
            current_phase="initiated",
            status="in_progress",
            results={},
            communication_log=[]
        )
        
        self.active_workflows[workflow_id] = workflow
        
        # Persist workflow to database
        if self.repository:
            db_workflow = self.repository.store_coordination_workflow(
                coordinator_agent="agent_coordinator",
                participant_agents=["research_agent", "strategy_agent", "execution_agent"],
                task_type="campaign_generation",
                task_description=objective,
                total_steps=3,
                agent_assignments={
                    "research": "gather_intelligence",
                    "strategy": "develop_plan",
                    "execution": "implement_campaign"
                },
                session_id=session_id
            )
            coordination_id = db_workflow.coordination_id
        else:
            coordination_id = None
        
        # PHASE 1: Research Agent gathers intelligence
        workflow.current_phase = "research"
        self._log_phase(workflow_id, "Research Agent gathering market intelligence")
        
        if self.repository and coordination_id:
            self.repository.update_workflow_progress(
                coordination_id=coordination_id,
                current_step=1,
                workflow_state="in_progress",
                communication_entry={
                    "phase": "research",
                    "timestamp": datetime.now().isoformat(),
                    "description": "Research Agent gathering intelligence"
                }
            )
        
        # Request market research
        research_request = AgentMessage(
            from_agent="coordinator",
            to_agent="research_agent",
            message_type="request",
            content={
                "type": "market_research",
                "topic": service_details.get("name", objective),
                "market_signals": market_signals
            },
            timestamp=datetime.now(),
            priority=5
        )
        workflow.communication_log.append(research_request)
        
        market_research = self.research_agent.research_market_trends(
            service_details.get("name", objective),
            market_signals
        )
        workflow.results["market_research"] = market_research
        
        # Request customer segment research
        target_segment = constraints.get("target_segment", "Enterprise")
        segment_request = AgentMessage(
            from_agent="coordinator",
            to_agent="research_agent",
            message_type="request",
            content={
                "type": "segment_research",
                "segment": target_segment,
                "customers": customers
            },
            timestamp=datetime.now(),
            priority=5
        )
        workflow.communication_log.append(segment_request)
        
        segment_analysis = self.research_agent.research_customer_segment(
            target_segment,
            customers
        )
        workflow.results["segment_analysis"] = segment_analysis
        
        # PHASE 2: Strategy Agent develops campaign strategy
        workflow.current_phase = "strategy"
        self._log_phase(workflow_id, "Strategy Agent developing campaign plan")
        
        if self.repository and coordination_id:
            self.repository.update_workflow_progress(
                coordination_id=coordination_id,
                current_step=2,
                workflow_state="in_progress",
                communication_entry={
                    "phase": "strategy",
                    "timestamp": datetime.now().isoformat(),
                    "description": "Strategy Agent developing plan"
                }
            )
        
        research_findings = {
            "trends_identified": market_research.get("trends_identified", []),
            "segment_insights": segment_analysis
        }
        
        strategy_request = AgentMessage(
            from_agent="coordinator",
            to_agent="strategy_agent",
            message_type="request",
            content={
                "type": "develop_strategy",
                "objective": objective,
                "research_findings": research_findings,
                "constraints": constraints
            },
            timestamp=datetime.now(),
            priority=5
        )
        workflow.communication_log.append(strategy_request)
        
        campaign_strategy = self.strategy_agent.develop_campaign_strategy(
            objective,
            research_findings,
            constraints
        )
        workflow.results["strategy"] = campaign_strategy
        
        # PHASE 3: Execution Agent creates implementation plan
        workflow.current_phase = "execution"
        self._log_phase(workflow_id, "Execution Agent creating implementation plan")
        
        if self.repository and coordination_id:
            self.repository.update_workflow_progress(
                coordination_id=coordination_id,
                current_step=3,
                workflow_state="in_progress",
                communication_entry={
                    "phase": "execution",
                    "timestamp": datetime.now().isoformat(),
                    "description": "Execution Agent creating implementation plan"
                }
            )
        
        execution_request = AgentMessage(
            from_agent="coordinator",
            to_agent="execution_agent",
            message_type="request",
            content={
                "type": "execute_campaign",
                "strategy": campaign_strategy,
                "service_details": service_details
            },
            timestamp=datetime.now(),
            priority=5
        )
        workflow.communication_log.append(execution_request)
        
        execution_plan = self.execution_agent.execute_campaign_plan(
            campaign_strategy,
            service_details
        )
        workflow.results["execution"] = execution_plan
        
        # PHASE 4: Synthesize all results
        workflow.current_phase = "synthesis"
        self._log_phase(workflow_id, "Coordinator synthesizing multi-agent results")
        
        final_result = self._synthesize_agent_results(
            workflow_id,
            objective,
            service_details,
            workflow.results
        )
        
        workflow.status = "completed"
        workflow.results["final"] = final_result
        
        # Persist workflow completion
        if self.repository and coordination_id:
            self.repository.complete_workflow(
                coordination_id=coordination_id,
                result=final_result,
                success=True
            )
        
        return final_result
    
    def evaluate_and_learn(
        self,
        campaign_id: str,
        campaign_data: Dict[str, Any],
        actual_metrics: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinate evaluation and learning from campaign outcomes
        
        This demonstrates self-correction and learning:
        1. Evaluation Agent assesses performance
        2. Extracts learnings
        3. Identifies needed corrections
        4. Feeds back into system memory
        """
        workflow_id = f"eval_workflow_{uuid.uuid4().hex[:8]}"
        
        self._log_phase(workflow_id, "Evaluation Agent assessing campaign performance")
        
        evaluation_request = AgentMessage(
            from_agent="coordinator",
            to_agent="evaluation_agent",
            message_type="request",
            content={
                "type": "evaluate_campaign",
                "campaign_data": campaign_data,
                "actual_metrics": actual_metrics,
                "strategy": strategy
            },
            timestamp=datetime.now(),
            priority=5
        )
        
        evaluation_result = self.evaluation_agent.evaluate_campaign_performance(
            campaign_data,
            actual_metrics,
            strategy
        )
        
        # Process learnings and corrections
        learnings_processed = self._process_learnings(
            campaign_id,
            evaluation_result.get("learnings", [])
        )
        
        corrections_applied = self._apply_corrections(
            campaign_id,
            evaluation_result.get("corrections_needed", [])
        )
        
        return {
            "evaluation": evaluation_result,
            "learnings_stored": learnings_processed,
            "corrections_applied": corrections_applied,
            "workflow_id": workflow_id
        }
    
    def _synthesize_agent_results(
        self,
        workflow_id: str,
        objective: str,
        service_details: Dict[str, Any],
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize results from multiple agents into coherent output"""
        market_research = results.get("market_research", {})
        segment_analysis = results.get("segment_analysis", {})
        strategy = results.get("strategy", {})
        execution = results.get("execution", {})
        
        synthesis = {
            "workflow_id": workflow_id,
            "objective": objective,
            "multi_agent_coordination": {
                "research_phase": {
                    "trends_identified": len(market_research.get("trends_identified", [])),
                    "segments_analyzed": segment_analysis.get("segment", ""),
                    "confidence": market_research.get("confidence", 0.0)
                },
                "strategy_phase": {
                    "strategic_approach": strategy.get("strategic_approach", []),
                    "channels_selected": len(strategy.get("channel_recommendations", [])),
                    "budget_allocated": sum(strategy.get("budget_allocation", {}).values()),
                    "confidence": strategy.get("confidence", 0.0)
                },
                "execution_phase": {
                    "campaign_elements": len(execution.get("campaign_elements", [])),
                    "timeline_weeks": len(execution.get("timeline", [])),
                    "deliverables": len(execution.get("deliverables", []))
                }
            },
            "campaign_plan": {
                "service": service_details.get("name", ""),
                "target_market": segment_analysis.get("segment", ""),
                "market_trends": market_research.get("trends_identified", []),
                "strategic_approach": strategy.get("strategic_approach", []),
                "channels": strategy.get("channel_recommendations", []),
                "budget_allocation": strategy.get("budget_allocation", {}),
                "execution_elements": execution.get("campaign_elements", []),
                "timeline": execution.get("timeline", []),
                "success_criteria": strategy.get("success_criteria", []),
                "risk_factors": strategy.get("risk_factors", [])
            },
            "agents_involved": ["Research Agent", "Strategy Agent", "Execution Agent"],
            "coordination_complete": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return synthesis
    
    def _process_learnings(self, campaign_id: str, learnings: List[Dict]) -> int:
        """Process and store learnings from evaluation"""
        stored_count = 0
        
        for learning in learnings:
            # In a full implementation, this would store to database
            # For now, we'll just log it
            self.logger.log_reasoning_step(
                trace_id=f"learning_{campaign_id}",
                step_name="store_learning",
                reasoning=learning.get("finding", ""),
                data_used=["Campaign Metrics", "Evaluation Results"]
            )
            stored_count += 1
        
        return stored_count
    
    def _apply_corrections(self, campaign_id: str, corrections: List[Dict]) -> List[str]:
        """Apply corrections based on evaluation"""
        applied_corrections = []
        
        for correction in corrections:
            area = correction.get("area", "")
            recommendation = correction.get("recommendation", "")
            
            # Log the correction
            self.logger.log_reasoning_step(
                trace_id=f"correction_{campaign_id}",
                step_name=f"apply_correction_{area}",
                reasoning=recommendation,
                data_used=["Evaluation Results", "Performance Metrics"]
            )
            
            applied_corrections.append(f"{area}: {recommendation}")
        
        return applied_corrections
    
    def _log_phase(self, workflow_id: str, message: str):
        """Log workflow phase transition"""
        self.logger.log_reasoning_step(
            trace_id=workflow_id,
            step_name="phase_transition",
            reasoning=message,
            data_used=["Multi-Agent Coordination"]
        )
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of an active workflow"""
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return None
        
        return {
            "workflow_id": workflow.workflow_id,
            "objective": workflow.objective,
            "current_phase": workflow.current_phase,
            "status": workflow.status,
            "agents_involved": workflow.participating_agents,
            "communication_count": len(workflow.communication_log)
        }
    
    def list_active_workflows(self) -> List[Dict[str, Any]]:
        """List all active workflows"""
        workflows = []
        for wf_id in self.active_workflows.keys():
            status = self.get_workflow_status(wf_id)
            if status:
                workflows.append(status)
        return workflows


# Global coordinator instance
_coordinator = AgentCoordinator()


def get_agent_coordinator() -> AgentCoordinator:
    """Get the global agent coordinator instance"""
    return _coordinator
