"""
NexusPlanner API - Clean Architecture Implementation

This is the new main application file using Clean Architecture principles.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.core.settings import settings
from app.core.exceptions import EntityNotFoundError, UseCaseError
from app.infrastructure.config.database import get_db, init_db
from app.core.container import Container
from app.application.dtos.request.generate_campaign_request import GenerateCampaignRequestDTO
from app.application.dtos.response.campaign_response import CampaignResponseDTO, CampaignListResponseDTO

from app.infrastructure.persistence.seed_data import seed_database

app = FastAPI(title="NexusPlanner API", version="2.0.0")

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
    
    print(f"NexusPlanner v{settings.app_version} started!")
    print(f"AI Generation: {'ENABLED' if settings.use_ai_generation else 'DISABLED (using rule-based)'}")


@app.get("/")
def root():
    """API root"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "ai_enabled": settings.use_ai_generation,
        "endpoints": {
            "campaigns": "/api/campaigns",
            "services": "/api/services",
            "market_intelligence": "/api/market-intelligence",
            "dashboard": "/api/dashboard/metrics"
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
def get_campaigns(db: Session = Depends(get_db)):
    """Get all campaigns"""
    try:
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
