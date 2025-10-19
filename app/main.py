"""
NexusPlanner API - Clean Architecture Implementation

This is the new main application file using Clean Architecture principles.
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import text
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
from app.models.request import LoginRequest, UserRegistrationRequest

from app.infrastructure.persistence.seed_data import seed_database
from app.api.routes import agent, audit
from app.api import auth
from app.core.auth_middleware import get_current_user, TokenData

# Import ORM models to register them with SQLAlchemy
from app.infrastructure.persistence.models.agent_decision_orm import (
    AgentDecisionORM,
    ExecutionTraceORM,
    ReasoningStepORM
)
from app.infrastructure.persistence.models.agent_memory_orm import (
    AgentMemoryORM,
    AgentLearningORM,
    AgentConversationORM,
    MultiAgentCoordinationORM,
    AgentFeedbackLoopORM
)
from app.infrastructure.persistence.models.campaign_template_orm import CampaignTemplateORM
from app.infrastructure.persistence.models.user_orm import UserORM

app = FastAPI(title="NexusPlanner API", version="2.0.0 - Agentic AI Edition")

# Include authentication routes
app.include_router(auth.router)
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


def run_migrations():
    """Run Alembic migrations programmatically"""
    from alembic.config import Config
    from alembic import command
    
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    print("Initializing database...")
    
    if settings.run_migrations_on_startup:
        print("Running database migrations...")
        try:
            run_migrations()
            print("Database migrations completed successfully")
        except Exception as e:
            print(f"Migration warning: {e}")
            print("Falling back to init_db()...")
            init_db()
    else:
        print("Skipping automatic migrations (RUN_MIGRATIONS_ON_STARTUP=False)")
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


@app.get("/health")
def health_check():
    """
    Kubernetes Liveness Probe
    
    Returns 200 OK if the application is alive and running.
    This endpoint should always return successfully unless the app is completely dead.
    """
    return {"status": "healthy", "service": "nexusplanner-api"}


@app.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Kubernetes Readiness Probe
    
    Returns 200 OK if the application is ready to serve traffic.
    Checks:
    - Database connectivity
    - Critical dependencies
    
    If this fails, Kubernetes will not route traffic to this pod.
    """
    try:
        # Use text() for SQLAlchemy 2.x compatibility
        db.execute(text("SELECT 1"))
        db.commit()
        
        return {
            "status": "ready",
            "service": "nexusplanner-api",
            "database": "connected",
            "ai_provider": settings.llm_provider,
            "version": settings.app_version
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service not ready: {str(e)}"
        )


@app.post("/api/campaigns/generate", response_model=CampaignResponseDTO)
def generate_campaign(
    request: GenerateCampaignRequestDTO,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    """Get all campaigns with optional search and filtering"""
    try:
        if query or status:
            use_case = Container.get_search_campaigns_use_case(db)
            return use_case.execute(query=query or "", status=status or "")
        else:
            use_case = Container.get_list_campaigns_use_case(db)
            return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/recent", response_model=CampaignListResponseDTO)
def get_recent_campaigns(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    """Get recent campaigns"""
    try:
        use_case = Container.get_list_campaigns_use_case(db)
        return use_case.execute(limit=3)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/{campaign_id}", response_model=CampaignResponseDTO)
def get_campaign(
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
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
def get_services(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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
def get_service(
    service_id: str,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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
def get_market_intelligence(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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
def get_recent_market_intelligence(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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


@app.get("/api/market-intelligence/filter")
def filter_market_intelligence(
    impact: Optional[str] = Query(None, description="Filter by impact level: low, medium, high"),
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source (partial match)"),
    start_date: Optional[str] = Query(None, description="Filter by start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="Filter by end date (ISO format)"),
    min_relevance: Optional[float] = Query(None, description="Minimum relevance score (0-1)"),
    db: Session = Depends(get_db)
):
    """Get market signals with advanced filters"""
    signal_repo = Container.get_market_signal_repository(db)
    signals = signal_repo.find_with_filters(
        impact=impact,
        category=category,
        source=source,
        start_date=start_date,
        end_date=end_date,
        min_relevance=min_relevance
    )
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
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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


@app.get("/api/export/campaigns")
def export_campaigns(
    format: str = Query("csv", description="Export format: csv or json"),
    db: Session = Depends(get_db)
):
    """Export all campaigns"""
    from app.utils.export_helpers import dict_to_csv, dict_to_json, flatten_campaign_for_export
    
    use_case = Container.get_list_campaigns_use_case(db)
    result = use_case.execute()
    campaigns = result.campaigns
    
    campaign_dicts = [
        {
            "id": str(c.id),
            "name": c.name,
            "theme": c.theme,
            "status": c.status.value,
            "start_date": c.start_date,
            "end_date": c.end_date,
            "created_at": c.created_at.isoformat() if hasattr(c, 'created_at') else "",
            "ideas": [{"description": idea.description, "target_kpi": idea.target_kpi} for idea in c.ideas],
            "channel_mix": [{"channel": ch.channel, "allocation": ch.budget_allocation} for ch in c.channel_strategies],
            "metrics": c.metrics
        }
        for c in campaigns
    ]
    
    if format.lower() == "csv":
        flat_campaigns = [flatten_campaign_for_export(c) for c in campaign_dicts]
        content, media_type = dict_to_csv(flat_campaigns)
        return Response(content=content, media_type=media_type, headers={"Content-Disposition": "attachment; filename=campaigns.csv"})
    else:
        content, media_type = dict_to_json(campaign_dicts)
        return Response(content=content, media_type=media_type, headers={"Content-Disposition": "attachment; filename=campaigns.json"})


@app.get("/api/export/market-intelligence")
def export_market_intelligence(
    format: str = Query("csv", description="Export format: csv or json"),
    db: Session = Depends(get_db)
):
    """Export all market intelligence signals"""
    from app.utils.export_helpers import dict_to_csv, dict_to_json, flatten_signal_for_export
    
    signal_repo = Container.get_market_signal_repository(db)
    signals = signal_repo.find_all()
    
    signal_dicts = [
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
    
    if format.lower() == "csv":
        flat_signals = [flatten_signal_for_export(s) for s in signal_dicts]
        content, media_type = dict_to_csv(flat_signals)
        return Response(content=content, media_type=media_type, headers={"Content-Disposition": "attachment; filename=market_intelligence.csv"})
    else:
        content, media_type = dict_to_json(signal_dicts)
        return Response(content=content, media_type=media_type, headers={"Content-Disposition": "attachment; filename=market_intelligence.json"})


@app.post("/api/campaigns/bulk-delete")
def bulk_delete_campaigns(
    campaign_ids: List[str],
    db: Session = Depends(get_db)
):
    """Bulk delete campaigns"""
    deleted_count = 0
    errors = []
    
    for campaign_id in campaign_ids:
        try:
            use_case = Container.get_delete_campaign_use_case(db)
            success = use_case.execute(campaign_id)
            if success:
                deleted_count += 1
        except EntityNotFoundError:
            errors.append(f"Campaign {campaign_id} not found")
        except Exception as e:
            errors.append(f"Error deleting {campaign_id}: {str(e)}")
    
    return {
        "deleted_count": deleted_count,
        "total_requested": len(campaign_ids),
        "errors": errors
    }


@app.patch("/api/campaigns/bulk-update")
def bulk_update_campaigns(
    updates: List[dict],
    db: Session = Depends(get_db)
):
    """Bulk update campaigns"""
    from app.application.dtos.request.update_campaign_request import UpdateCampaignRequestDTO
    
    updated_count = 0
    errors = []
    
    for update in updates:
        try:
            campaign_id = update.get("id")
            if not campaign_id:
                errors.append("Missing campaign ID")
                continue
            
            request = UpdateCampaignRequestDTO(
                name=update.get("name"),
                status=update.get("status"),
                theme=update.get("theme")
            )
            use_case = Container.get_update_campaign_use_case(db)
            use_case.execute(campaign_id, request)
            updated_count += 1
        except EntityNotFoundError:
            errors.append(f"Campaign {campaign_id} not found")
        except Exception as e:
            errors.append(f"Error updating {campaign_id}: {str(e)}")
    
    return {
        "updated_count": updated_count,
        "total_requested": len(updates),
        "errors": errors
    }


@app.get("/api/templates")
def get_templates(
    query: Optional[str] = Query(None, description="Search query"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    db: Session = Depends(get_db)
):
    """Get all campaign templates"""
    from app.infrastructure.persistence.repositories.campaign_template_repository import SQLAlchemyCampaignTemplateRepository
    
    template_repo = SQLAlchemyCampaignTemplateRepository(db)
    
    if query or tags:
        templates = template_repo.search(query=query, tags=tags)
    else:
        templates = template_repo.find_all()
    
    return [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "theme": t.theme,
            "ideas": t.ideas,
            "channel_mix": t.channel_mix,
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat(),
            "tags": t.tags
        }
        for t in templates
    ]


@app.get("/api/templates/{template_id}")
def get_template(template_id: str, db: Session = Depends(get_db)):
    """Get a specific template"""
    from app.infrastructure.persistence.repositories.campaign_template_repository import SQLAlchemyCampaignTemplateRepository
    
    template_repo = SQLAlchemyCampaignTemplateRepository(db)
    template = template_repo.find_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "theme": template.theme,
        "ideas": template.ideas,
        "channel_mix": template.channel_mix,
        "created_at": template.created_at.isoformat(),
        "updated_at": template.updated_at.isoformat(),
        "tags": template.tags
    }


@app.post("/api/templates")
def create_template(template_data: dict, db: Session = Depends(get_db)):
    """Create a new campaign template from a campaign or scratch"""
    from app.infrastructure.persistence.repositories.campaign_template_repository import SQLAlchemyCampaignTemplateRepository
    from app.domain.entities.campaign_template import CampaignTemplate
    from datetime import datetime
    import uuid
    
    template_repo = SQLAlchemyCampaignTemplateRepository(db)
    
    template = CampaignTemplate(
        id=str(uuid.uuid4()),
        name=template_data.get("name"),
        description=template_data.get("description"),
        theme=template_data.get("theme"),
        ideas=template_data.get("ideas", []),
        channel_mix=template_data.get("channel_mix", []),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        tags=template_data.get("tags", [])
    )
    
    saved_template = template_repo.save(template)
    
    return {
        "id": saved_template.id,
        "name": saved_template.name,
        "description": saved_template.description,
        "theme": saved_template.theme,
        "ideas": saved_template.ideas,
        "channel_mix": saved_template.channel_mix,
        "created_at": saved_template.created_at.isoformat(),
        "updated_at": saved_template.updated_at.isoformat(),
        "tags": saved_template.tags
    }


@app.delete("/api/templates/{template_id}")
def delete_template(template_id: str, db: Session = Depends(get_db)):
    """Delete a template"""
    from app.infrastructure.persistence.repositories.campaign_template_repository import SQLAlchemyCampaignTemplateRepository
    
    template_repo = SQLAlchemyCampaignTemplateRepository(db)
    success = template_repo.delete(template_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {"success": True, "message": "Template deleted successfully"}


@app.post("/api/campaigns/from-template/{template_id}")
def create_campaign_from_template(
    template_id: str,
    campaign_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new campaign from a template"""
    from app.infrastructure.persistence.repositories.campaign_template_repository import SQLAlchemyCampaignTemplateRepository
    from app.application.dtos.request.generate_campaign_request import GenerateCampaignRequestDTO
    
    template_repo = SQLAlchemyCampaignTemplateRepository(db)
    template = template_repo.find_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    request = GenerateCampaignRequestDTO(
        service_id=campaign_data.get("service_id"),
        target_audience=campaign_data.get("target_audience", "Enterprise decision-makers"),
        budget=campaign_data.get("budget", 50000.0)
    )
    
    use_case = Container.get_generate_campaign_use_case(db)
    campaign = use_case.execute(request)
    
    return campaign


@app.get("/api/analytics/campaigns")
def get_campaign_analytics(db: Session = Depends(get_db)):
    """Get campaign performance analytics"""
    from app.domain.entities.campaign import CampaignStatus
    campaign_repo = Container.get_campaign_repository(db)
    
    all_campaigns = campaign_repo.find_all()
    
    status_breakdown = {
        "draft": campaign_repo.count_by_status(CampaignStatus.DRAFT),
        "active": campaign_repo.count_by_status(CampaignStatus.ACTIVE),
        "completed": campaign_repo.count_by_status(CampaignStatus.COMPLETED)
    }
    
    total_budget = sum([c.metrics.get("budget_allocated", 0) for c in all_campaigns if c.metrics])
    total_conversions = sum([c.metrics.get("conversions", 0) for c in all_campaigns if c.metrics])
    total_leads = sum([c.metrics.get("leads", 0) for c in all_campaigns if c.metrics])
    
    recent_performance = []
    for campaign in all_campaigns[:10]:
        if campaign.metrics:
            recent_performance.append({
                "id": str(campaign.id),
                "name": campaign.name,
                "status": campaign.status.value,
                "conversions": campaign.metrics.get("conversions", 0),
                "leads": campaign.metrics.get("leads", 0),
                "engagement": campaign.metrics.get("engagement", 0),
                "roi": campaign.metrics.get("roi", 0)
            })
    
    return {
        "total_campaigns": len(all_campaigns),
        "status_breakdown": status_breakdown,
        "total_budget": total_budget,
        "total_conversions": total_conversions,
        "total_leads": total_leads,
        "avg_conversion_rate": total_conversions / max(total_leads, 1) * 100 if total_leads > 0 else 0,
        "recent_performance": recent_performance
    }


@app.get("/api/analytics/trends")
def get_trends_analytics(db: Session = Depends(get_db)):
    """Get market intelligence trends"""
    signal_repo = Container.get_market_signal_repository(db)
    signals = signal_repo.find_all()
    
    impact_breakdown = {"low": 0, "medium": 0, "high": 0}
    category_breakdown = {}
    
    for signal in signals:
        impact_breakdown[signal.impact.value] = impact_breakdown.get(signal.impact.value, 0) + 1
        category_breakdown[signal.category] = category_breakdown.get(signal.category, 0) + 1
    
    return {
        "total_signals": len(signals),
        "impact_breakdown": impact_breakdown,
        "category_breakdown": category_breakdown,
        "high_impact_count": impact_breakdown["high"],
        "categories": list(category_breakdown.keys())
    }


@app.post("/api/notifications/webhook")
def register_webhook(webhook_data: dict):
    """Register a webhook URL for notifications"""
    return {
        "success": True,
        "webhook_id": "webhook_123",
        "url": webhook_data.get("url"),
        "events": webhook_data.get("events", ["high_impact_signal", "campaign_status_change"]),
        "message": "Webhook registered successfully"
    }


@app.post("/api/notifications/test")
def test_notification(notification_data: dict):
    """Test webhook notification"""
    from app.infrastructure.notifications.webhook_service import WebhookService
    
    url = notification_data.get("webhook_url")
    if not url:
        raise HTTPException(status_code=400, detail="webhook_url required")
    
    test_payload = {
        "event": "test",
        "message": "Test notification from NexusPlanner",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    success = WebhookService.send_webhook(url, test_payload)
    
    return {
        "success": success,
        "message": "Test notification sent" if success else "Failed to send notification"
    }


@app.post("/api/auth/register")
def register_user(user_data: UserRegistrationRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    from app.utils.auth_helpers import get_password_hash
    from app.infrastructure.persistence.models.user_orm import UserORM
    import uuid
    
    existing = db.query(UserORM).filter(
        (UserORM.email == user_data.email) | 
        (UserORM.username == user_data.username)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    user = UserORM(
        id=str(uuid.uuid4()),
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role="user"
    )
    
    db.add(user)
    db.commit()
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role
    }


@app.post("/api/auth/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    from app.utils.auth_helpers import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
    from app.infrastructure.persistence.models.user_orm import UserORM
    from datetime import timedelta, datetime
    
    user = db.query(UserORM).filter(UserORM.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is inactive")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role
        }
    }


@app.get("/api/auth/me")
def get_current_user(authorization: Optional[str] = None, db: Session = Depends(get_db)):
    """Get current user from token"""
    from app.utils.auth_helpers import decode_token
    from app.infrastructure.persistence.models.user_orm import UserORM
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(UserORM).filter(UserORM.id == payload.get("user_id")).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
