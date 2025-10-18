from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from .models import (
    Campaign,
    MarketSignal,
    Service,
    CampaignGenerationRequest,
    ImpactLevel,
)
from .storage import storage
from .services import CampaignGenerator

app = FastAPI(title="NexusPlanner API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard/metrics")
def get_dashboard_metrics():
    return storage.get_dashboard_metrics()

@app.get("/api/campaigns", response_model=List[Campaign])
def get_campaigns():
    return storage.get_campaigns()

@app.get("/api/campaigns/recent", response_model=List[Campaign])
def get_recent_campaigns():
    return storage.get_recent_campaigns()

@app.get("/api/campaigns/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: str):
    campaign = storage.get_campaign_by_id(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.post("/api/campaigns/generate", response_model=Campaign)
def generate_campaign(request: CampaignGenerationRequest):
    services = storage.get_services()
    market_signals = storage.get_market_signals()
    generator = CampaignGenerator(services, market_signals)
    campaign = generator.generate_campaign_plan(request)
    saved = storage.create_campaign(campaign)

    storage.add_market_signal(
        MarketSignal(
            id="",
            source="Campaign Generator",
            content=f'New campaign generated: "{saved.name}" targeting {request.target_audience}',
            timestamp=datetime.utcnow().isoformat() + "Z",
            relevance_score=0.85,
            category="AI",
            impact=ImpactLevel.medium,
        )
    )
    return saved

@app.get("/api/market-intelligence", response_model=List[MarketSignal])
def get_market_intelligence():
    return storage.get_market_signals()

@app.get("/api/market-intelligence/recent", response_model=List[MarketSignal])
def get_recent_market_intelligence():
    return storage.get_recent_market_signals()

@app.get("/api/services", response_model=List[Service])
def get_services():
    return storage.get_services()

@app.get("/api/services/{service_id}", response_model=Service)
def get_service(service_id: str):
    service = storage.get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
