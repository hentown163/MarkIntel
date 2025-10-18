"""
NexusPlanner API - Clean Architecture Implementation

This is the new main application file using Clean Architecture principles.
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.settings import settings
from app.core.exceptions import EntityNotFoundError, UseCaseError
from app.infrastructure.config.database import get_db, init_db
from app.core.container import Container
from app.application.dtos.request.generate_campaign_request import GenerateCampaignRequestDTO
from app.application.dtos.request.campaign_feedback_request import CampaignFeedbackRequestDTO
from app.application.dtos.request.update_campaign_request import UpdateCampaignRequestDTO
from app.application.dtos.response.campaign_response import CampaignResponseDTO, CampaignListResponseDTO
from app.application.dtos.response.feedback_response import FeedbackResponseDTO

from app.infrastructure.persistence.seed_data import seed_database
from app.api.routes import agent, audit

# Import ORM models to register them with SQLAlchemy
from app.infrastructure.persistence.models.agent_decision_orm import (
    AgentDecisionORM,
    ExecutionTraceORM,
    ReasoningStepORM
)

app = FastAPI(title="NexusPlanner API", version="2.0.0 - Agentic AI Edition")

# Include agent routes
app.include_router(agent.router)
# Include audit routes for observability
app.include_router(audit.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    print("Initializing database...")
    init_db()
    
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()
    
    # Initialize RAG and agent systems
    from app.infrastructure.rag.mock_crm_repository import get_crm_repository
    from app.infrastructure.rag.vector_store import get_vector_store
    crm_repo = get_crm_repository()
    vector_store = get_vector_store()
    
    # Initialize agent observability logger with database persistence
    if settings.enable_database_logging:
        from app.infrastructure.observability.agent_logger import initialize_agent_logger_with_db
        from app.infrastructure.persistence.repositories.agent_decision_repository import AgentDecisionRepository
        
        db_session = next(get_db())
        try:
            repo = AgentDecisionRepository(db_session)
            initialize_agent_logger_with_db(repo, enable_database_logging=True)
            print(f"Agent Observability: Database logging ENABLED (retention: {settings.agent_log_retention_days} days)")
        finally:
            db_session.close()
    else:
        print("Agent Observability: In-memory logging only")
    
    print(f"NexusPlanner v{settings.app_version} - Agentic AI Edition started!")
    print(f"AI Generation: {'ENABLED' if settings.use_ai_generation else 'DISABLED (using rule-based)'}")
    print(f"RAG System: Initialized with {vector_store.get_stats()['total_documents']} documents")
    print(f"CRM Data: {crm_repo.get_stats()['total_customers']} customers indexed")


@app.get("/")
def root():
    """API root"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "ai_enabled": settings.use_ai_generation,
        "agent_enabled": True,
        "rag_enabled": True,
        "endpoints": {
            "campaigns": "/api/campaigns",
            "services": "/api/services",
            "market_intelligence": "/api/market-intelligence",
            "dashboard": "/api/dashboard/metrics",
            "agent": "/api/agent",
            "agent_observability": "/api/agent/observability",
            "audit_logs": "/api/audit"
        }
    }


@app.post("/api/campaigns/generate", response_model=CampaignResponseDTO)
def generate_campaign(
    request: GenerateCampaignRequestDTO,
    db: Session = Depends(get_db)
):
    """
    Generate a new campaign using AI (or rule-based fallback)
    
    This endpoint demonstrates Clean Architecture:
    - Request validated by DTO (Pydantic)
    - Use case orchestrates the business logic
    - Dependencies injected via container
    - Response mapped back to DTO
    """
    try:
        use_case = Container.get_generate_campaign_use_case(db)
        return use_case.execute(request)
    except UseCaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/campaigns", response_model=CampaignListResponseDTO)
def get_campaigns(
    query: Optional[str] = Query(None, description="Search query for campaign name or theme"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get all campaigns with optional search and filtering"""
    try:
        if query or status:
            use_case = Container.get_search_campaigns_use_case(db)
            return use_case.execute(query=query, status=status)
        else:
            use_case = Container.get_list_campaigns_use_case(db)
            return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/recent", response_model=CampaignListResponseDTO)
def get_recent_campaigns(db: Session = Depends(get_db)):
    """Get recent campaigns"""
    try:
        use_case = Container.get_list_campaigns_use_case(db)
        return use_case.execute(limit=3)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/{campaign_id}", response_model=CampaignResponseDTO)
def get_campaign(campaign_id: str, db: Session = Depends(get_db)):
    """Get a specific campaign"""
    try:
        use_case = Container.get_campaign_detail_use_case(db)
        return use_case.execute(campaign_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/campaigns/{campaign_id}", response_model=CampaignResponseDTO)
def update_campaign(
    campaign_id: str,
    request: UpdateCampaignRequestDTO,
    db: Session = Depends(get_db)
):
    """
    Update a campaign
    
    Allows updating campaign name, status, and theme.
    """
    try:
        use_case = Container.get_update_campaign_use_case(db)
        return use_case.execute(campaign_id, request)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except UseCaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.delete("/api/campaigns/{campaign_id}")
def delete_campaign(campaign_id: str, db: Session = Depends(get_db)):
    """
    Delete a campaign
    
    Permanently removes a campaign from the system.
    """
    try:
        use_case = Container.get_delete_campaign_use_case(db)
        success = use_case.execute(campaign_id)
        return {"success": success, "message": f"Campaign {campaign_id} deleted successfully"}
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except UseCaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.patch("/api/campaigns/{campaign_id}/regenerate-ideas", response_model=CampaignResponseDTO)
def regenerate_campaign_ideas(campaign_id: str, db: Session = Depends(get_db)):
    """
    Regenerate campaign ideas using AI (or rule-based fallback)
    
    This endpoint allows users to get fresh campaign ideas while keeping
    the same campaign structure and channel strategies.
    """
    try:
        use_case = Container.get_regenerate_ideas_use_case(db)
        return use_case.execute(campaign_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except UseCaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.patch("/api/campaigns/{campaign_id}/regenerate-strategies", response_model=CampaignResponseDTO)
def regenerate_channel_strategies(campaign_id: str, db: Session = Depends(get_db)):
    """
    Regenerate channel strategies using AI (or rule-based fallback)
    
    This endpoint allows users to get optimized channel mix and strategies
    while keeping the same campaign ideas.
    """
    try:
        use_case = Container.get_regenerate_strategies_use_case(db)
        return use_case.execute(campaign_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except UseCaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/campaigns/{campaign_id}/feedback", response_model=FeedbackResponseDTO)
def submit_campaign_feedback(
    campaign_id: str,
    feedback: CampaignFeedbackRequestDTO,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a campaign
    
    Allows users to provide like/dislike feedback on campaign ideas,
    strategies, or overall campaign. This helps track user preferences
    and improve future campaign generation.
    """
    try:
        use_case = Container.get_record_feedback_use_case(db)
        return use_case.execute(campaign_id, feedback)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except UseCaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/services")
def get_services(db: Session = Depends(get_db)):
    """Get all services"""
    service_repo = Container.get_service_repository(db)
    services = service_repo.find_all()
    return [
        {
            "id": str(s.id),
            "name": s.name,
            "category": s.category,
            "description": s.description,
            "target_audience": s.target_audience,
            "key_benefits": s.key_benefits,
            "market_mentions": s.market_mentions,
            "active_campaigns": s.active_campaigns,
            "competitors": s.competitors
        }
        for s in services
    ]


@app.get("/api/services/{service_id}")
def get_service(service_id: str, db: Session = Depends(get_db)):
    """Get a specific service"""
    from app.domain.value_objects import ServiceId
    service_repo = Container.get_service_repository(db)
    service = service_repo.find_by_id(ServiceId(service_id))
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {
        "id": str(service.id),
        "name": service.name,
        "category": service.category,
        "description": service.description,
        "target_audience": service.target_audience,
        "key_benefits": service.key_benefits,
        "market_mentions": service.market_mentions,
        "active_campaigns": service.active_campaigns,
        "competitors": service.competitors
    }


@app.get("/api/market-intelligence")
def get_market_intelligence(db: Session = Depends(get_db)):
    """Get all market signals"""
    signal_repo = Container.get_market_signal_repository(db)
    signals = signal_repo.find_all()
    return [
        {
            "id": str(s.id),
            "source": s.source,
            "content": s.content,
            "timestamp": s.timestamp.isoformat() + "Z",
            "relevance_score": s.relevance_score,
            "category": s.category,
            "impact": s.impact.value
        }
        for s in signals
    ]


@app.get("/api/market-intelligence/recent")
def get_recent_market_intelligence(db: Session = Depends(get_db)):
    """Get recent market signals"""
    signal_repo = Container.get_market_signal_repository(db)
    signals = signal_repo.find_recent(limit=4)
    return [
        {
            "id": str(s.id),
            "source": s.source,
            "content": s.content,
            "timestamp": s.timestamp.isoformat() + "Z",
            "relevance_score": s.relevance_score,
            "category": s.category,
            "impact": s.impact.value
        }
        for s in signals
    ]


@app.get("/api/dashboard/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Get dashboard metrics"""
    from app.domain.entities.campaign import CampaignStatus
    campaign_repo = Container.get_campaign_repository(db)
    signal_repo = Container.get_market_signal_repository(db)
    
    active_campaigns = campaign_repo.count_by_status(CampaignStatus.ACTIVE)
    total_signals = len(signal_repo.find_all())
    
    return {
        "active_campaigns": {"count": active_campaigns, "change": "+3 this week"},
        "market_insights": {"count": total_signals, "change": "+127 today"},
        "competitor_tracking": {"count": 23, "change": "5 active alerts"},
        "ai_generations": {"count": 156, "change": "+42 this month"},
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
