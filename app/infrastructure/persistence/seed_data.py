"""Seed data for database"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.domain.value_objects import ServiceId, SignalId
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal, ImpactLevel
from app.infrastructure.persistence.repositories.sqlalchemy_service_repository import SQLAlchemyServiceRepository
from app.infrastructure.persistence.repositories.sqlalchemy_market_signal_repository import SQLAlchemyMarketSignalRepository


def seed_database(session: Session):
    """Seed the database with initial data"""
    service_repo = SQLAlchemyServiceRepository(session)
    signal_repo = SQLAlchemyMarketSignalRepository(session)
    
    if len(service_repo.find_all()) > 0:
        print("Database already seeded, skipping...")
        return
    
    print("Seeding database...")
    
    services = [
        Service(
            id=ServiceId("svc-001"),
            name="CloudScale AI Security Suite",
            category="Security",
            description="AI-powered threat detection, automated response, and zero-trust architecture implementation for enterprise security.",
            target_audience=["CISO", "Security Teams", "IT Directors"],
            key_benefits=["Zero Trust", "Threat Prevention", "Compliance"],
            market_mentions=234,
            active_campaigns=3,
            competitors=["Sentinel", "ThreatGuard Pro", "CyberShield"],
        ),
        Service(
            id=ServiceId("svc-002"),
            name="Multi-Cloud Infrastructure Platform",
            category="Cloud Infrastructure",
            description="Unified management across AWS, Azure, and GCP with automated provisioning, cost optimization, and security compliance monitoring.",
            target_audience=["Cloud Architects", "DevOps Teams", "CTOs"],
            key_benefits=["Unified View", "Cost Efficiency", "Automated Provisioning"],
            market_mentions=189,
            active_campaigns=6,
            competitors=["CloudMaster", "MultiCloud Pro", "Infralink"],
        ),
        Service(
            id=ServiceId("svc-003"),
            name="Enterprise AI Platform",
            category="Artificial Intelligence",
            description="End-to-end AI solution for predictive analytics, automation, and intelligent decision-making at enterprise scale.",
            target_audience=["CDO", "AI Engineers", "Data Scientists"],
            key_benefits=["Governance", "Scalability", "Compliance"],
            market_mentions=312,
            active_campaigns=12,
            competitors=["AI Enterprise", "SmartOps AI", "Neural Cloud"],
        ),
    ]
    
    for service in services:
        service_repo.save(service)
    
    now = datetime.utcnow()
    signals = [
        MarketSignal(
            id=SignalId("sig-001"),
            source="Gartner Report",
            content="AI security platforms surge 47%. The AI security market is projected to grow at 47% CAGR through 2026.",
            timestamp=now - timedelta(hours=2),
            relevance_score=0.92,
            category="AI",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-002"),
            source="TechCrunch",
            content="CompetitorX Launches Cloud Infrastructure Suite targeting enterprise customers.",
            timestamp=now - timedelta(hours=4),
            relevance_score=0.85,
            category="Competitor",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-003"),
            source="Social Media Analytics",
            content="Enterprise AI Adoption Reaches 73%. Latest industry survey reveals strong market opportunity.",
            timestamp=now - timedelta(hours=6),
            relevance_score=0.88,
            category="AI",
            impact=ImpactLevel.MEDIUM,
        ),
    ]
    
    for signal in signals:
        signal_repo.save(signal)
    
    print("Database seeding completed!")
