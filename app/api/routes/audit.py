"""API routes for agent audit logs and observability"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.infrastructure.config.database import get_db
from app.infrastructure.persistence.repositories.agent_decision_repository import AgentDecisionRepository
from app.infrastructure.observability.models import DecisionType
from pydantic import BaseModel


router = APIRouter(prefix="/api/audit", tags=["audit"])


class DecisionResponse(BaseModel):
    """Decision response model"""
    decision_id: str
    timestamp: str
    decision_type: str
    reasoning_chain: List[str]
    data_sources: List[str]
    confidence_score: float
    session_id: Optional[str]
    metadata: dict


class TraceResponse(BaseModel):
    """Trace response model"""
    trace_id: str
    start_time: str
    end_time: Optional[str]
    total_duration_ms: Optional[float]
    steps: List[dict]
    success: bool
    error_message: Optional[str]
    session_id: Optional[str]


class DecisionStatsResponse(BaseModel):
    """Decision statistics response"""
    total_decisions: int
    by_type: dict
    average_confidence: float
    days: int


class TraceStatsResponse(BaseModel):
    """Trace statistics response"""
    total_traces: int
    successful: int
    failed: int
    success_rate: float
    average_duration_ms: float
    days: int


@router.get("/decisions/recent", response_model=List[DecisionResponse])
def get_recent_decisions(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get recent agent decisions
    
    Returns up to `limit` most recent decisions with full reasoning chains
    """
    repo = AgentDecisionRepository(db)
    decisions = repo.find_recent_decisions(limit=limit)
    
    return [
        DecisionResponse(
            decision_id=d.decision_id,
            timestamp=d.timestamp.isoformat(),
            decision_type=d.decision_type.value,
            reasoning_chain=d.reasoning_chain,
            data_sources=d.data_sources,
            confidence_score=d.confidence_score,
            session_id=d.session_id,
            metadata=d.metadata or {}
        )
        for d in decisions
    ]


@router.get("/decisions/by-type/{decision_type}", response_model=List[DecisionResponse])
def get_decisions_by_type(
    decision_type: str,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get decisions filtered by type
    
    Returns decisions of a specific type (campaign_generation, customer_targeting, etc.)
    """
    try:
        dt = DecisionType(decision_type)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Invalid decision type: {decision_type}")
    
    repo = AgentDecisionRepository(db)
    decisions = repo.find_decisions_by_type(dt, limit=limit)
    
    return [
        DecisionResponse(
            decision_id=d.decision_id,
            timestamp=d.timestamp.isoformat(),
            decision_type=d.decision_type.value,
            reasoning_chain=d.reasoning_chain,
            data_sources=d.data_sources,
            confidence_score=d.confidence_score,
            session_id=d.session_id,
            metadata=d.metadata or {}
        )
        for d in decisions
    ]


@router.get("/decisions/by-session/{session_id}", response_model=List[DecisionResponse])
def get_decisions_by_session(
    session_id: str,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get all decisions for a specific session
    
    Useful for debugging or understanding a specific user interaction
    """
    repo = AgentDecisionRepository(db)
    decisions = repo.find_decisions_by_session(session_id, limit=limit)
    
    return [
        DecisionResponse(
            decision_id=d.decision_id,
            timestamp=d.timestamp.isoformat(),
            decision_type=d.decision_type.value,
            reasoning_chain=d.reasoning_chain,
            data_sources=d.data_sources,
            confidence_score=d.confidence_score,
            session_id=d.session_id,
            metadata=d.metadata or {}
        )
        for d in decisions
    ]


@router.get("/decisions/{decision_id}", response_model=DecisionResponse)
def get_decision(
    decision_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific decision by ID
    
    Returns full details including reasoning chain and metadata
    """
    from fastapi import HTTPException
    
    repo = AgentDecisionRepository(db)
    decision = repo.find_decision_by_id(decision_id)
    
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return DecisionResponse(
        decision_id=decision.decision_id,
        timestamp=decision.timestamp.isoformat(),
        decision_type=decision.decision_type.value,
        reasoning_chain=decision.reasoning_chain,
        data_sources=decision.data_sources,
        confidence_score=decision.confidence_score,
        session_id=decision.session_id,
        metadata=decision.metadata or {}
    )


@router.get("/traces/recent", response_model=List[TraceResponse])
def get_recent_traces(
    limit: int = Query(50, ge=1, le=500),
    success_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get recent execution traces
    
    Returns execution traces with step-by-step details
    """
    repo = AgentDecisionRepository(db)
    traces = repo.find_recent_traces(limit=limit, success_only=success_only)
    
    return [
        TraceResponse(
            trace_id=t.trace_id,
            start_time=t.start_time.isoformat(),
            end_time=t.end_time.isoformat() if t.end_time else None,
            total_duration_ms=(t.end_time - t.start_time).total_seconds() * 1000 if t.end_time else None,
            steps=t.steps,
            success=t.success,
            error_message=t.error_message,
            session_id=t.session_id
        )
        for t in traces
    ]


@router.get("/traces/{trace_id}", response_model=TraceResponse)
def get_trace(
    trace_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific execution trace by ID
    
    Returns full trace with all steps and timing information
    """
    from fastapi import HTTPException
    
    repo = AgentDecisionRepository(db)
    trace = repo.find_trace_by_id(trace_id)
    
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    
    return TraceResponse(
        trace_id=trace.trace_id,
        start_time=trace.start_time.isoformat(),
        end_time=trace.end_time.isoformat() if trace.end_time else None,
        total_duration_ms=(trace.end_time - trace.start_time).total_seconds() * 1000 if trace.end_time else None,
        steps=trace.steps,
        success=trace.success,
        error_message=trace.error_message,
        session_id=trace.session_id
    )


@router.get("/stats/decisions", response_model=DecisionStatsResponse)
def get_decision_stats(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get decision statistics for the last N days
    
    Returns aggregated metrics for compliance and performance tracking
    """
    repo = AgentDecisionRepository(db)
    stats = repo.get_decision_stats(days=days)
    
    return DecisionStatsResponse(**stats)


@router.get("/stats/traces", response_model=TraceStatsResponse)
def get_trace_stats(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get execution trace statistics for the last N days
    
    Returns performance metrics including success rate and average duration
    """
    repo = AgentDecisionRepository(db)
    stats = repo.get_trace_stats(days=days)
    
    return TraceStatsResponse(**stats)


@router.post("/cleanup/decisions")
def cleanup_old_decisions(
    days: int = Query(90, ge=30, le=730),
    db: Session = Depends(get_db)
):
    """
    Delete decisions older than N days (retention policy)
    
    Use for compliance with data retention requirements
    """
    repo = AgentDecisionRepository(db)
    count = repo.delete_old_decisions(days=days)
    
    return {
        "deleted": count,
        "retention_days": days,
        "message": f"Deleted {count} decisions older than {days} days"
    }


@router.post("/cleanup/traces")
def cleanup_old_traces(
    days: int = Query(90, ge=30, le=730),
    db: Session = Depends(get_db)
):
    """
    Delete traces older than N days (retention policy)
    
    Use for compliance with data retention requirements
    """
    repo = AgentDecisionRepository(db)
    count = repo.delete_old_traces(days=days)
    
    return {
        "deleted": count,
        "retention_days": days,
        "message": f"Deleted {count} traces older than {days} days"
    }
