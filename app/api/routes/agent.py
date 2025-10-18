"""API routes for autonomous agent operations"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.domain.services.agent.reasoning_engine import get_reasoning_engine
from app.infrastructure.observability.agent_logger import get_agent_logger
from app.infrastructure.rag.mock_crm_repository import get_crm_repository
from app.infrastructure.rag.vector_store import get_vector_store


router = APIRouter(prefix="/api/agent", tags=["agent"])


class AgentPlanRequest(BaseModel):
    """Request to create an agent plan"""
    business_objective: str
    target_audience: Optional[str] = None
    budget_constraint: Optional[float] = None
    timeline: Optional[str] = None


class AgentPlanResponse(BaseModel):
    """Response containing the agent's plan"""
    plan_id: str
    objective: str
    steps: List[Dict[str, Any]]
    reasoning: str
    confidence: float
    estimated_duration_ms: float


class CampaignEvaluationRequest(BaseModel):
    """Request to evaluate campaign outcome"""
    campaign_id: str
    engagement_rate: Optional[float] = None
    conversion_rate: Optional[float] = None
    revenue_generated: Optional[float] = None
    cost: Optional[float] = None
    other_metrics: Optional[Dict[str, Any]] = None


@router.post("/plan", response_model=AgentPlanResponse)
def create_agent_plan(request: AgentPlanRequest):
    """
    Have the autonomous agent create a multi-step campaign plan
    
    This demonstrates agentic behavior:
    - Agent analyzes the objective
    - Retrieves relevant CRM data using RAG
    - Creates a multi-step execution plan
    - Logs all reasoning and decisions
    """
    try:
        engine = get_reasoning_engine()
        plan = engine.create_campaign_plan(
            business_objective=request.business_objective,
            target_audience=request.target_audience,
            budget_constraint=request.budget_constraint,
            timeline=request.timeline
        )
        
        return AgentPlanResponse(
            plan_id=plan.plan_id,
            objective=plan.objective,
            steps=plan.steps,
            reasoning=plan.reasoning,
            confidence=plan.confidence,
            estimated_duration_ms=plan.estimated_duration_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent planning failed: {str(e)}")


@router.post("/evaluate")
def evaluate_campaign(request: CampaignEvaluationRequest):
    """
    Evaluate campaign outcome and enable agent learning
    
    This enables closed-loop learning - the agent learns from
    campaign results to improve future recommendations.
    """
    try:
        engine = get_reasoning_engine()
        
        metrics = {}
        if request.engagement_rate is not None:
            metrics["engagement_rate"] = request.engagement_rate
        if request.conversion_rate is not None:
            metrics["conversion_rate"] = request.conversion_rate
        if request.revenue_generated is not None:
            metrics["revenue_generated"] = request.revenue_generated
        if request.cost is not None:
            metrics["cost"] = request.cost
        if request.other_metrics:
            metrics.update(request.other_metrics)
        
        evaluation = engine.evaluate_campaign_outcome(
            campaign_id=request.campaign_id,
            actual_metrics=metrics
        )
        
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@router.get("/observability/decisions")
def get_agent_decisions(decision_type: Optional[str] = None):
    """
    Get agent decision history for observability
    
    Shows what the agent decided, why, and with what confidence.
    """
    try:
        logger = get_agent_logger()
        decisions = logger.get_decision_history()
        
        return {
            "total_decisions": len(decisions),
            "decisions": [d.to_dict() for d in decisions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/observability/metrics")
def get_agent_metrics():
    """
    Get aggregate metrics about agent performance
    
    Provides insights into:
    - Execution times
    - Success rates
    - Token usage
    - API call counts
    """
    try:
        logger = get_agent_logger()
        return logger.get_execution_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/observability/export")
def export_observability_data():
    """
    Export all observability data for analysis
    
    Useful for debugging, auditing, and understanding agent behavior.
    """
    try:
        logger = get_agent_logger()
        return logger.export_observability_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crm/stats")
def get_crm_stats():
    """Get statistics about CRM data"""
    try:
        crm_repo = get_crm_repository()
        return crm_repo.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rag/stats")
def get_rag_stats():
    """Get statistics about RAG vector store"""
    try:
        vector_store = get_vector_store()
        return vector_store.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MULTI-AGENT COORDINATION ENDPOINTS (Agentic AI Features)
# ============================================================================

class MultiAgentCampaignRequest(BaseModel):
    """Request for multi-agent coordinated campaign generation"""
    objective: str
    service_name: str
    service_description: Optional[str] = None
    target_segment: Optional[str] = "Enterprise"
    budget: Optional[float] = 100000.0
    timeline: Optional[str] = "Q1 2026"


class MultiAgentCampaignResponse(BaseModel):
    """Response from multi-agent campaign generation"""
    workflow_id: str
    objective: str
    multi_agent_coordination: Dict[str, Any]
    campaign_plan: Dict[str, Any]
    agents_involved: List[str]
    coordination_complete: bool


class AgentEvaluationRequest(BaseModel):
    """Request for agent-powered evaluation with learning"""
    campaign_id: str
    campaign_data: Dict[str, Any]
    actual_metrics: Dict[str, Any]
    strategy: Dict[str, Any]


@router.post("/multi-agent/generate-campaign", response_model=MultiAgentCampaignResponse)
def generate_campaign_with_agents(request: MultiAgentCampaignRequest):
    """
    Generate a campaign using coordinated multi-agent workflow
    
    This demonstrates full Agentic AI capabilities:
    - ResearchAgent gathers market intelligence
    - StrategyAgent develops strategic approach
    - ExecutionAgent creates implementation plan
    - Coordinator synthesizes all results
    
    This is TRUE multi-agent coordination with autonomous agents
    working together!
    """
    try:
        from app.domain.services.agent.agent_coordinator import get_agent_coordinator
        from app.infrastructure.persistence.repositories.market_signal_repository import get_market_signal_repository
        from sqlalchemy.orm import Session
        from app.infrastructure.config.database import SessionLocal
        
        coordinator = get_agent_coordinator()
        
        # Get market signals for research
        db = SessionLocal()
        try:
            signal_repo = get_market_signal_repository(db)
            market_signals = signal_repo.find_all()
            market_signals_data = [
                {
                    "title": s.title,
                    "description": s.description,
                    "impact_score": s.impact_score,
                    "source": s.source
                }
                for s in market_signals
            ]
        finally:
            db.close()
        
        # Get customer data for segmentation
        crm_repo = get_crm_repository()
        customers = crm_repo.get_all_customers()
        customers_data = [
            {
                "name": c.company_name,
                "segment": c.segment.value,
                "engagement_level": c.engagement_level.value,
                "annual_revenue": c.annual_revenue
            }
            for c in customers
        ]
        
        # Prepare service details
        service_details = {
            "name": request.service_name,
            "description": request.service_description or f"Enterprise {request.service_name} solution"
        }
        
        # Prepare constraints
        constraints = {
            "budget": request.budget,
            "timeline": request.timeline,
            "target_segment": request.target_segment
        }
        
        # Execute multi-agent workflow
        result = coordinator.generate_campaign_with_agents(
            objective=request.objective,
            service_details=service_details,
            market_signals=market_signals_data,
            customers=customers_data,
            constraints=constraints
        )
        
        return MultiAgentCampaignResponse(
            workflow_id=result["workflow_id"],
            objective=result["objective"],
            multi_agent_coordination=result["multi_agent_coordination"],
            campaign_plan=result["campaign_plan"],
            agents_involved=result["agents_involved"],
            coordination_complete=result["coordination_complete"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-agent generation failed: {str(e)}")


@router.post("/multi-agent/evaluate-and-learn")
def evaluate_and_learn(request: AgentEvaluationRequest):
    """
    Evaluate campaign with EvaluationAgent and extract learnings
    
    This demonstrates self-correction and learning:
    - EvaluationAgent assesses performance
    - Extracts learnings from outcomes
    - Identifies needed corrections
    - Stores learnings for future use
    
    This is the self-correction loop that makes the agent smarter over time!
    """
    try:
        from app.domain.services.agent.agent_coordinator import get_agent_coordinator
        
        coordinator = get_agent_coordinator()
        
        result = coordinator.evaluate_and_learn(
            campaign_id=request.campaign_id,
            campaign_data=request.campaign_data,
            actual_metrics=request.actual_metrics,
            strategy=request.strategy
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@router.get("/multi-agent/workflows")
def list_agent_workflows():
    """
    List all active multi-agent workflows
    
    Shows what the agent system is currently working on
    """
    try:
        from app.domain.services.agent.agent_coordinator import get_agent_coordinator
        
        coordinator = get_agent_coordinator()
        workflows = coordinator.list_active_workflows()
        
        return {
            "total_workflows": len(workflows),
            "workflows": workflows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/multi-agent/workflow/{workflow_id}")
def get_workflow_status(workflow_id: str):
    """
    Get detailed status of a specific multi-agent workflow
    
    Track the progress of agent coordination in real-time
    """
    try:
        from app.domain.services.agent.agent_coordinator import get_agent_coordinator
        
        coordinator = get_agent_coordinator()
        status = coordinator.get_workflow_status(workflow_id)
        
        if not status:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
        return status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
def get_agent_capabilities():
    """
    Get information about agent capabilities
    
    Returns details about what the autonomous agents can do
    """
    return {
        "agentic_features": {
            "multi_step_reasoning": {
                "enabled": True,
                "description": "Agent can plan, execute, and adapt multi-step workflows",
                "endpoint": "/api/agent/plan"
            },
            "self_correction": {
                "enabled": True,
                "description": "Agent learns from outcomes and corrects future behavior",
                "endpoint": "/api/agent/multi-agent/evaluate-and-learn"
            },
            "persistent_memory": {
                "enabled": True,
                "description": "Agent remembers learnings and context across sessions",
                "storage": "PostgreSQL database"
            },
            "multi_agent_coordination": {
                "enabled": True,
                "description": "Multiple specialized agents work together",
                "agents": [
                    "ResearchAgent - Market intelligence gathering",
                    "StrategyAgent - Strategic planning",
                    "ExecutionAgent - Implementation planning",
                    "EvaluationAgent - Performance evaluation"
                ],
                "endpoint": "/api/agent/multi-agent/generate-campaign"
            }
        },
        "specialized_agents": [
            {
                "name": "ResearchAgent",
                "role": "Market research and customer intelligence",
                "capabilities": [
                    "Market trend analysis",
                    "Customer segment research",
                    "Competitive intelligence",
                    "Data validation"
                ]
            },
            {
                "name": "StrategyAgent",
                "role": "Campaign strategy development",
                "capabilities": [
                    "Strategic planning",
                    "Channel selection",
                    "Budget allocation",
                    "Risk assessment"
                ]
            },
            {
                "name": "ExecutionAgent",
                "role": "Campaign implementation",
                "capabilities": [
                    "Tactical execution planning",
                    "Content generation guidance",
                    "Timeline creation",
                    "Progress tracking"
                ]
            },
            {
                "name": "EvaluationAgent",
                "role": "Performance evaluation and learning",
                "capabilities": [
                    "Performance assessment",
                    "Learning extraction",
                    "Improvement recommendations",
                    "Self-correction triggers"
                ]
            }
        ],
        "coordination": {
            "orchestrator": "AgentCoordinator",
            "communication": "Inter-agent messaging",
            "workflow_management": "Multi-phase workflows",
            "result_synthesis": "Coordinated outputs"
        }
    }
