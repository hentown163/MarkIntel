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
