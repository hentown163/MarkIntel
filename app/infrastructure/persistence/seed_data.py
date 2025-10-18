"""Seed data for database"""
import uuid
from datetime import datetime, timedelta, date
from decimal import Decimal
from sqlalchemy.orm import Session

from app.domain.value_objects import ServiceId, SignalId, CampaignId, Money, DateRange
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal, ImpactLevel
from app.domain.entities.campaign import Campaign, CampaignStatus, CampaignIdea, ChannelPlan, CampaignMetrics
from app.infrastructure.persistence.repositories.sqlalchemy_service_repository import SQLAlchemyServiceRepository
from app.infrastructure.persistence.repositories.sqlalchemy_market_signal_repository import SQLAlchemyMarketSignalRepository
from app.infrastructure.persistence.repositories.sqlalchemy_campaign_repository import SQLAlchemyCampaignRepository


def seed_database(session: Session):
    """Seed the database with initial data"""
    service_repo = SQLAlchemyServiceRepository(session)
    signal_repo = SQLAlchemyMarketSignalRepository(session)
    campaign_repo = SQLAlchemyCampaignRepository(session)
    
    if len(service_repo.find_all()) > 0:
        print("Database already seeded, skipping...")
        return
    
    print("Seeding database...")
    
    # Seed Services (10 services)
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
        Service(
            id=ServiceId("svc-004"),
            name="Real-Time Analytics Engine",
            category="Data & Analytics",
            description="Process and analyze petabytes of data in real-time with ML-powered insights and automated reporting.",
            target_audience=["Data Engineers", "Business Analysts", "CDOs"],
            key_benefits=["Real-Time Processing", "ML Insights", "Scalability"],
            market_mentions=156,
            active_campaigns=4,
            competitors=["DataFlow Pro", "Analytics Cloud", "InsightStream"],
        ),
        Service(
            id=ServiceId("svc-005"),
            name="Edge Computing Platform",
            category="Edge & IoT",
            description="Deploy intelligence at the edge with low-latency processing for IoT devices and distributed systems.",
            target_audience=["IoT Architects", "Edge Engineers", "Technical Directors"],
            key_benefits=["Low Latency", "Edge Intelligence", "Distributed Computing"],
            market_mentions=98,
            active_campaigns=2,
            competitors=["EdgeMaster", "IoT Cloud", "SmartEdge"],
        ),
        Service(
            id=ServiceId("svc-006"),
            name="DevOps Automation Suite",
            category="DevOps",
            description="End-to-end CI/CD automation with intelligent testing, deployment, and monitoring capabilities.",
            target_audience=["DevOps Engineers", "Development Teams", "Engineering Managers"],
            key_benefits=["Automation", "Continuous Deployment", "Monitoring"],
            market_mentions=203,
            active_campaigns=5,
            competitors=["DevPipeline", "AutoDeploy", "CICloudOps"],
        ),
        Service(
            id=ServiceId("svc-007"),
            name="Compliance Management Platform",
            category="Governance & Compliance",
            description="Automated compliance monitoring and reporting for GDPR, HIPAA, SOC 2, and other regulations.",
            target_audience=["Compliance Officers", "Legal Teams", "CISOs"],
            key_benefits=["Automated Compliance", "Audit Ready", "Risk Management"],
            market_mentions=145,
            active_campaigns=3,
            competitors=["ComplianceHub", "RegulatoryPro", "AuditMaster"],
        ),
        Service(
            id=ServiceId("svc-008"),
            name="Customer Data Platform",
            category="Marketing Technology",
            description="Unified customer data platform for personalized marketing and customer experience optimization.",
            target_audience=["Marketing Directors", "CMOs", "Customer Success Teams"],
            key_benefits=["360° Customer View", "Personalization", "Marketing Automation"],
            market_mentions=178,
            active_campaigns=7,
            competitors=["CustomerCloud", "MarketHub", "PersonalizePro"],
        ),
        Service(
            id=ServiceId("svc-009"),
            name="Blockchain Infrastructure",
            category="Blockchain & Web3",
            description="Enterprise-grade blockchain infrastructure for secure, transparent, and decentralized applications.",
            target_audience=["Blockchain Architects", "CTOs", "Innovation Teams"],
            key_benefits=["Decentralization", "Security", "Transparency"],
            market_mentions=87,
            active_campaigns=2,
            competitors=["ChainMaster", "BlockCloud", "Web3Platform"],
        ),
        Service(
            id=ServiceId("svc-010"),
            name="API Management Platform",
            category="API & Integration",
            description="Comprehensive API lifecycle management with security, analytics, and developer portal.",
            target_audience=["API Architects", "Integration Teams", "Platform Engineers"],
            key_benefits=["API Security", "Developer Experience", "Analytics"],
            market_mentions=167,
            active_campaigns=4,
            competitors=["APIHub", "GatewayPro", "IntegrationCloud"],
        ),
    ]
    
    for service in services:
        service_repo.save(service)
    
    # Seed Market Signals (20 signals)
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
        MarketSignal(
            id=SignalId("sig-004"),
            source="Forrester Research",
            content="Multi-cloud adoption accelerates - 89% of enterprises now use multiple cloud providers.",
            timestamp=now - timedelta(hours=8),
            relevance_score=0.91,
            category="Cloud",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-005"),
            source="IDC Report",
            content="Edge computing market to reach $274B by 2025, driven by IoT and 5G expansion.",
            timestamp=now - timedelta(hours=10),
            relevance_score=0.79,
            category="Edge Computing",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-006"),
            source="LinkedIn Insights",
            content="DevOps job postings increase 43% YoY as automation becomes critical for digital transformation.",
            timestamp=now - timedelta(hours=12),
            relevance_score=0.75,
            category="DevOps",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-007"),
            source="Reuters",
            content="New GDPR enforcement leads to $2.3B in fines - compliance tech spending surges.",
            timestamp=now - timedelta(hours=14),
            relevance_score=0.86,
            category="Compliance",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-008"),
            source="Marketing Week",
            content="Customer data platforms see 67% adoption rate among Fortune 500 companies.",
            timestamp=now - timedelta(hours=16),
            relevance_score=0.82,
            category="Marketing Tech",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-009"),
            source="CoinDesk",
            content="Enterprise blockchain adoption grows 52% as companies seek transparent supply chains.",
            timestamp=now - timedelta(hours=18),
            relevance_score=0.71,
            category="Blockchain",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-010"),
            source="API Economy Report",
            content="API traffic grows 300% annually - API management becomes mission-critical.",
            timestamp=now - timedelta(hours=20),
            relevance_score=0.84,
            category="API",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-011"),
            source="Cybersecurity Today",
            content="Zero-trust architecture adoption increases to 61% following major security breaches.",
            timestamp=now - timedelta(days=1),
            relevance_score=0.89,
            category="Security",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-012"),
            source="Cloud Computing Magazine",
            content="Cost optimization tools see 78% ROI as cloud spending hits $500B globally.",
            timestamp=now - timedelta(days=1, hours=2),
            relevance_score=0.80,
            category="Cloud",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-013"),
            source="AI Trends",
            content="Generative AI market expected to grow from $40B to $1.3T by 2032.",
            timestamp=now - timedelta(days=1, hours=4),
            relevance_score=0.94,
            category="AI",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-014"),
            source="Data Science Central",
            content="Real-time analytics adoption reaches 82% as businesses demand instant insights.",
            timestamp=now - timedelta(days=1, hours=6),
            relevance_score=0.77,
            category="Data Analytics",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-015"),
            source="Industry Report",
            content="Remote work drives 54% increase in demand for secure cloud collaboration tools.",
            timestamp=now - timedelta(days=1, hours=8),
            relevance_score=0.73,
            category="Cloud",
            impact=ImpactLevel.LOW,
        ),
        MarketSignal(
            id=SignalId("sig-016"),
            source="Tech Leadership Summit",
            content="CIOs prioritize automation - 91% plan to increase automation budgets in 2025.",
            timestamp=now - timedelta(days=2),
            relevance_score=0.85,
            category="Automation",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-017"),
            source="Venture Capital Report",
            content="VC funding for cybersecurity startups reaches $12B, up 38% from last year.",
            timestamp=now - timedelta(days=2, hours=4),
            relevance_score=0.76,
            category="Security",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-018"),
            source="IoT World Congress",
            content="Smart manufacturing drives IoT device growth to 27B connected devices globally.",
            timestamp=now - timedelta(days=2, hours=8),
            relevance_score=0.78,
            category="IoT",
            impact=ImpactLevel.MEDIUM,
        ),
        MarketSignal(
            id=SignalId("sig-019"),
            source="Financial Times",
            content="Digital transformation spending projected to exceed $3.4T in 2026.",
            timestamp=now - timedelta(days=3),
            relevance_score=0.88,
            category="Digital Transformation",
            impact=ImpactLevel.HIGH,
        ),
        MarketSignal(
            id=SignalId("sig-020"),
            source="Industry Survey",
            content="87% of enterprises report data integration challenges - integration platforms in high demand.",
            timestamp=now - timedelta(days=3, hours=6),
            relevance_score=0.81,
            category="Integration",
            impact=ImpactLevel.MEDIUM,
        ),
    ]
    
    for signal in signals:
        signal_repo.save(signal)
    
    # Seed Campaigns (15 campaigns with different statuses)
    today = date.today()
    
    campaigns = [
        # Active Campaigns
        Campaign(
            id=CampaignId("cmp-001"),
            name="Zero Trust Security Initiative",
            status=CampaignStatus.ACTIVE,
            theme="Secure Your Future with Zero Trust",
            date_range=DateRange(
                start_date=today - timedelta(days=10),
                end_date=today + timedelta(days=20)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Zero Trust, Zero Compromise",
                    core_message="End-to-end security from code to cloud with AI-powered threat prevention",
                    target_segments=["CISO", "Security Teams", "IT Directors"],
                    competitive_angle="Unlike competitors who focus on detection, we prevent breaches at the source"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="LinkedIn", content_type="Thought Leadership", frequency="3x/week", budget_allocation=0.35, success_metrics=["Engagement Rate", "Lead Quality"]),
                ChannelPlan(channel="Webinars", content_type="Security Deep Dives", frequency="Bi-weekly", budget_allocation=0.25, success_metrics=["Attendee Count", "Demo Requests"]),
                ChannelPlan(channel="Industry Events", content_type="Conference Sponsorship", frequency="Quarterly", budget_allocation=0.25, success_metrics=["Booth Visits", "Meeting Bookings"]),
                ChannelPlan(channel="Email", content_type="Case Studies", frequency="Weekly", budget_allocation=0.15, success_metrics=["Open Rate", "Click-Through Rate"]),
            ],
            total_budget=Money(Decimal("250000.00")),
            expected_roi=3.2,
            metrics=CampaignMetrics(engagement="12.4K", leads="342", conversions="28")
        ),
        Campaign(
            id=CampaignId("cmp-002"),
            name="Multi-Cloud Mastery Campaign",
            status=CampaignStatus.ACTIVE,
            theme="Maximize Your Multi-Cloud Investment",
            date_range=DateRange(
                start_date=today - timedelta(days=15),
                end_date=today + timedelta(days=45)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Cloud Freedom, Unified Control",
                    core_message="Unified management across AWS, Azure, and GCP with automated cost optimization",
                    target_segments=["Cloud Architects", "DevOps Teams", "CTOs"],
                    competitive_angle="Only platform offering true multi-cloud orchestration with AI-powered cost optimization"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="YouTube", content_type="Technical Tutorials", frequency="2x/week", budget_allocation=0.30, success_metrics=["Views", "Watch Time", "Subscribers"]),
                ChannelPlan(channel="Developer Forums", content_type="Technical Content", frequency="Daily", budget_allocation=0.20, success_metrics=["Engagement", "Upvotes"]),
                ChannelPlan(channel="Webinars", content_type="Technical Demos", frequency="Weekly", budget_allocation=0.30, success_metrics=["Registration", "Attendance"]),
                ChannelPlan(channel="Podcasts", content_type="Thought Leadership", frequency="Monthly", budget_allocation=0.20, success_metrics=["Downloads", "Shares"]),
            ],
            total_budget=Money(Decimal("180000.00")),
            expected_roi=2.8,
            metrics=CampaignMetrics(engagement="8.7K", leads="215", conversions="19")
        ),
        Campaign(
            id=CampaignId("cmp-003"),
            name="Enterprise AI Transformation",
            status=CampaignStatus.ACTIVE,
            theme="Future-Proof Your AI Strategy",
            date_range=DateRange(
                start_date=today - timedelta(days=5),
                end_date=today + timedelta(days=55)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Governance-First AI",
                    core_message="Enterprise-grade AI with built-in governance, compliance, and security",
                    target_segments=["CDO", "AI Engineers", "Data Scientists"],
                    competitive_angle="SOC 2-compliant AI workflows with automated model governance"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="LinkedIn", content_type="Case Studies", frequency="Daily", budget_allocation=0.35, success_metrics=["Engagement", "Lead Gen"]),
                ChannelPlan(channel="Research Papers", content_type="Technical Whitepapers", frequency="Monthly", budget_allocation=0.25, success_metrics=["Downloads", "Citations"]),
                ChannelPlan(channel="Conferences", content_type="Keynote Sponsorship", frequency="Quarterly", budget_allocation=0.30, success_metrics=["Attendance", "Brand Recall"]),
                ChannelPlan(channel="Email", content_type="Newsletter", frequency="Weekly", budget_allocation=0.10, success_metrics=["Open Rate", "CTR"]),
            ],
            total_budget=Money(Decimal("320000.00")),
            expected_roi=4.1,
            metrics=CampaignMetrics(engagement="15.2K", leads="428", conversions="35")
        ),
        Campaign(
            id=CampaignId("cmp-004"),
            name="Real-Time Analytics Revolution",
            status=CampaignStatus.ACTIVE,
            theme="Insights at the Speed of Business",
            date_range=DateRange(
                start_date=today - timedelta(days=7),
                end_date=today + timedelta(days=23)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Real-Time Intelligence, Real Business Impact",
                    core_message="Process and analyze data 10x faster than traditional platforms",
                    target_segments=["Data Engineers", "Business Analysts", "CDOs"],
                    competitive_angle="ML-powered insights that surface trends before your competitors even collect the data"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="LinkedIn", content_type="Data Stories", frequency="3x/week", budget_allocation=0.30, success_metrics=["Engagement", "Shares"]),
                ChannelPlan(channel="Webinars", content_type="Live Demos", frequency="Bi-weekly", budget_allocation=0.35, success_metrics=["Registration", "Conversion"]),
                ChannelPlan(channel="Industry Reports", content_type="Benchmarks", frequency="Quarterly", budget_allocation=0.20, success_metrics=["Downloads", "Media Mentions"]),
                ChannelPlan(channel="Email", content_type="Use Cases", frequency="Weekly", budget_allocation=0.15, success_metrics=["CTR", "Demo Requests"]),
            ],
            total_budget=Money(Decimal("210000.00")),
            expected_roi=3.5,
            metrics=CampaignMetrics(engagement="9.8K", leads="267", conversions="22")
        ),
        
        # Draft Campaigns
        Campaign(
            id=CampaignId("cmp-005"),
            name="Edge Intelligence Campaign",
            status=CampaignStatus.DRAFT,
            theme="Bring Computing to the Edge",
            date_range=DateRange(
                start_date=today + timedelta(days=14),
                end_date=today + timedelta(days=74)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Intelligence Where It Matters",
                    core_message="Low-latency processing for IoT and edge devices with real-time decision-making",
                    target_segments=["IoT Architects", "Edge Engineers", "Technical Directors"],
                    competitive_angle="Deploy intelligence where your data is generated - reduce latency by 90%"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="IoT Forums", content_type="Technical Discussions", frequency="Daily", budget_allocation=0.25, success_metrics=["Engagement", "Reputation"]),
                ChannelPlan(channel="Technical Blogs", content_type="Architecture Patterns", frequency="2x/week", budget_allocation=0.30, success_metrics=["Reads", "Shares"]),
                ChannelPlan(channel="Webinars", content_type="Edge Computing 101", frequency="Monthly", budget_allocation=0.25, success_metrics=["Attendance", "Follow-up"]),
                ChannelPlan(channel="Trade Shows", content_type="Live Demos", frequency="Quarterly", budget_allocation=0.20, success_metrics=["Booth Traffic", "Leads"]),
            ],
            total_budget=Money(Decimal("165000.00")),
            expected_roi=2.9,
        ),
        Campaign(
            id=CampaignId("cmp-006"),
            name="DevOps Automation Excellence",
            status=CampaignStatus.DRAFT,
            theme="Deploy with Confidence",
            date_range=DateRange(
                start_date=today + timedelta(days=21),
                end_date=today + timedelta(days=81)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Automate Everything, Deploy Anything",
                    core_message="End-to-end CI/CD automation with intelligent testing and zero-downtime deployments",
                    target_segments=["DevOps Engineers", "Development Teams", "Engineering Managers"],
                    competitive_angle="Only platform with AI-powered rollback prediction and automated remediation"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="GitHub", content_type="Open Source Tools", frequency="Weekly", budget_allocation=0.35, success_metrics=["Stars", "Contributors"]),
                ChannelPlan(channel="YouTube", content_type="DevOps Tutorials", frequency="2x/week", budget_allocation=0.30, success_metrics=["Subscribers", "Views"]),
                ChannelPlan(channel="Conferences", content_type="Workshop Sponsorship", frequency="Quarterly", budget_allocation=0.20, success_metrics=["Attendance", "Leads"]),
                ChannelPlan(channel="Slack Communities", content_type="Community Support", frequency="Daily", budget_allocation=0.15, success_metrics=["Members", "Engagement"]),
            ],
            total_budget=Money(Decimal("195000.00")),
            expected_roi=3.3,
        ),
        Campaign(
            id=CampaignId("cmp-007"),
            name="Compliance Made Simple",
            status=CampaignStatus.DRAFT,
            theme="Compliance Without the Complexity",
            date_range=DateRange(
                start_date=today + timedelta(days=28),
                end_date=today + timedelta(days=88)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Automated Compliance, Effortless Audits",
                    core_message="Stay compliant with GDPR, HIPAA, SOC 2 through automated monitoring and reporting",
                    target_segments=["Compliance Officers", "Legal Teams", "CISOs"],
                    competitive_angle="Real-time compliance dashboards that prevent violations before they happen"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="LinkedIn", content_type="Regulatory Updates", frequency="Daily", budget_allocation=0.30, success_metrics=["Reach", "Engagement"]),
                ChannelPlan(channel="Webinars", content_type="Compliance Training", frequency="Monthly", budget_allocation=0.35, success_metrics=["Registration", "Certificates"]),
                ChannelPlan(channel="Whitepapers", content_type="Regulatory Guides", frequency="Quarterly", budget_allocation=0.25, success_metrics=["Downloads", "Shares"]),
                ChannelPlan(channel="Email", content_type="Compliance Alerts", frequency="Weekly", budget_allocation=0.10, success_metrics=["Open Rate", "Actions"]),
            ],
            total_budget=Money(Decimal("175000.00")),
            expected_roi=2.7,
        ),
        
        # Completed Campaigns
        Campaign(
            id=CampaignId("cmp-008"),
            name="Customer 360 Launch",
            status=CampaignStatus.COMPLETED,
            theme="Know Your Customers Like Never Before",
            date_range=DateRange(
                start_date=today - timedelta(days=90),
                end_date=today - timedelta(days=30)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="360° Customer Intelligence",
                    core_message="Unified customer data platform for personalized marketing at scale",
                    target_segments=["Marketing Directors", "CMOs", "Customer Success Teams"],
                    competitive_angle="Only CDP with real-time behavioral triggers and AI-powered segmentation"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="LinkedIn", content_type="Success Stories", frequency="Daily", budget_allocation=0.35, success_metrics=["Engagement", "Lead Gen"]),
                ChannelPlan(channel="Webinars", content_type="Personalization Masterclass", frequency="Weekly", budget_allocation=0.30, success_metrics=["Attendance", "Conversion"]),
                ChannelPlan(channel="Industry Events", content_type="Booth Presence", frequency="Monthly", budget_allocation=0.25, success_metrics=["Conversations", "Demos"]),
                ChannelPlan(channel="Email", content_type="ROI Calculator", frequency="Bi-weekly", budget_allocation=0.10, success_metrics=["CTR", "Tool Usage"]),
            ],
            total_budget=Money(Decimal("285000.00")),
            expected_roi=4.5,
            metrics=CampaignMetrics(engagement="24.5K", leads="687", conversions="89")
        ),
        Campaign(
            id=CampaignId("cmp-009"),
            name="Blockchain for Business",
            status=CampaignStatus.COMPLETED,
            theme="Trust Through Transparency",
            date_range=DateRange(
                start_date=today - timedelta(days=120),
                end_date=today - timedelta(days=60)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Enterprise Blockchain Made Easy",
                    core_message="Secure, transparent, and decentralized applications without the complexity",
                    target_segments=["Blockchain Architects", "CTOs", "Innovation Teams"],
                    competitive_angle="First enterprise blockchain platform with no-code smart contract builder"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="Crypto Forums", content_type="Technical Discussions", frequency="Daily", budget_allocation=0.25, success_metrics=["Reputation", "Mentions"]),
                ChannelPlan(channel="LinkedIn", content_type="Use Cases", frequency="3x/week", budget_allocation=0.30, success_metrics=["Reach", "Engagement"]),
                ChannelPlan(channel="Virtual Conferences", content_type="Panel Discussions", frequency="Monthly", budget_allocation=0.30, success_metrics=["Attendance", "Leads"]),
                ChannelPlan(channel="Technical Blogs", content_type="Architecture Posts", frequency="Weekly", budget_allocation=0.15, success_metrics=["Reads", "Comments"]),
            ],
            total_budget=Money(Decimal("145000.00")),
            expected_roi=2.4,
            metrics=CampaignMetrics(engagement="6.3K", leads="178", conversions="12")
        ),
        Campaign(
            id=CampaignId("cmp-010"),
            name="API Economy Leadership",
            status=CampaignStatus.COMPLETED,
            theme="APIs That Power the Digital Economy",
            date_range=DateRange(
                start_date=today - timedelta(days=75),
                end_date=today - timedelta(days=15)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Build Once, Connect Everywhere",
                    core_message="Comprehensive API lifecycle management with enterprise security and analytics",
                    target_segments=["API Architects", "Integration Teams", "Platform Engineers"],
                    competitive_angle="Only platform offering API versioning with zero-downtime migrations"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="Developer Portal", content_type="API Documentation", frequency="Continuous", budget_allocation=0.35, success_metrics=["Page Views", "API Keys"]),
                ChannelPlan(channel="YouTube", content_type="Integration Tutorials", frequency="2x/week", budget_allocation=0.25, success_metrics=["Views", "Subscribers"]),
                ChannelPlan(channel="Hackathons", content_type="API Challenges", frequency="Quarterly", budget_allocation=0.25, success_metrics=["Participants", "Submissions"]),
                ChannelPlan(channel="Technical Blogs", content_type="Best Practices", frequency="Weekly", budget_allocation=0.15, success_metrics=["Reads", "Shares"]),
            ],
            total_budget=Money(Decimal("198000.00")),
            expected_roi=3.7,
            metrics=CampaignMetrics(engagement="11.2K", leads="341", conversions="45")
        ),
        
        # Paused Campaign
        Campaign(
            id=CampaignId("cmp-011"),
            name="Sustainability Tech Initiative",
            status=CampaignStatus.PAUSED,
            theme="Green Technology for a Better Tomorrow",
            date_range=DateRange(
                start_date=today - timedelta(days=40),
                end_date=today + timedelta(days=20)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Carbon-Neutral Cloud Computing",
                    core_message="Reduce your carbon footprint while scaling your infrastructure",
                    target_segments=["Sustainability Officers", "CTOs", "Board Directors"],
                    competitive_angle="First cloud platform with carbon tracking and offset automation"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="ESG Reports", content_type="Impact Studies", frequency="Quarterly", budget_allocation=0.35, success_metrics=["Downloads", "Citations"]),
                ChannelPlan(channel="LinkedIn", content_type="Sustainability Stories", frequency="Weekly", budget_allocation=0.30, success_metrics=["Engagement", "Shares"]),
                ChannelPlan(channel="Industry Events", content_type="Green Tech Summit", frequency="Annual", budget_allocation=0.25, success_metrics=["Attendance", "Media Coverage"]),
                ChannelPlan(channel="Partnerships", content_type="NGO Collaborations", frequency="Ongoing", budget_allocation=0.10, success_metrics=["Partnerships", "Impact"]),
            ],
            total_budget=Money(Decimal("225000.00")),
            expected_roi=2.2,
            metrics=CampaignMetrics(engagement="5.1K", leads="89", conversions="7")
        ),
        
        # More Active Campaigns
        Campaign(
            id=CampaignId("cmp-012"),
            name="Hybrid Work Solutions",
            status=CampaignStatus.ACTIVE,
            theme="Work From Anywhere, Securely",
            date_range=DateRange(
                start_date=today - timedelta(days=20),
                end_date=today + timedelta(days=40)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Secure Collaboration for Distributed Teams",
                    core_message="Enterprise-grade security meets seamless remote collaboration",
                    target_segments=["IT Directors", "HR Leaders", "Remote Team Managers"],
                    competitive_angle="Zero-trust security with integrated productivity tools"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="LinkedIn", content_type="Remote Work Tips", frequency="Daily", budget_allocation=0.30, success_metrics=["Engagement", "Followers"]),
                ChannelPlan(channel="Webinars", content_type="Hybrid Work Best Practices", frequency="Weekly", budget_allocation=0.35, success_metrics=["Registration", "Attendance"]),
                ChannelPlan(channel="Email", content_type="Case Studies", frequency="Bi-weekly", budget_allocation=0.20, success_metrics=["Open Rate", "CTR"]),
                ChannelPlan(channel="Podcasts", content_type="Future of Work", frequency="Monthly", budget_allocation=0.15, success_metrics=["Downloads", "Engagement"]),
            ],
            total_budget=Money(Decimal("205000.00")),
            expected_roi=3.4,
            metrics=CampaignMetrics(engagement="13.7K", leads="389", conversions="31")
        ),
        Campaign(
            id=CampaignId("cmp-013"),
            name="FinTech Innovation Series",
            status=CampaignStatus.ACTIVE,
            theme="Banking on the Future",
            date_range=DateRange(
                start_date=today - timedelta(days=12),
                end_date=today + timedelta(days=48)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Next-Gen Financial Services",
                    core_message="AI-powered fraud detection and real-time payment processing",
                    target_segments=["FinTech CTOs", "Banking Executives", "Payment Processors"],
                    competitive_angle="Process 1M transactions per second with 99.999% uptime"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="Financial Conferences", content_type="Keynote Speaking", frequency="Quarterly", budget_allocation=0.40, success_metrics=["Audience Size", "Media Mentions"]),
                ChannelPlan(channel="LinkedIn", content_type="FinTech Insights", frequency="Daily", budget_allocation=0.30, success_metrics=["Engagement", "Lead Gen"]),
                ChannelPlan(channel="Research Reports", content_type="Industry Analysis", frequency="Quarterly", budget_allocation=0.20, success_metrics=["Downloads", "Press Pickup"]),
                ChannelPlan(channel="Email", content_type="Regulatory Updates", frequency="Weekly", budget_allocation=0.10, success_metrics=["Open Rate", "Forwards"]),
            ],
            total_budget=Money(Decimal("340000.00")),
            expected_roi=4.8,
            metrics=CampaignMetrics(engagement="18.9K", leads="521", conversions="67")
        ),
        
        # More Draft Campaigns
        Campaign(
            id=CampaignId("cmp-014"),
            name="Healthcare Digital Transformation",
            status=CampaignStatus.DRAFT,
            theme="Modernizing Patient Care",
            date_range=DateRange(
                start_date=today + timedelta(days=35),
                end_date=today + timedelta(days=95)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="HIPAA-Compliant Healthcare Cloud",
                    core_message="Secure patient data management with AI-powered diagnostics support",
                    target_segments=["Healthcare CIOs", "Hospital Administrators", "Medical IT Teams"],
                    competitive_angle="Only platform with built-in HIPAA compliance and automated audit trails"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="Healthcare Conferences", content_type="Product Demos", frequency="Quarterly", budget_allocation=0.35, success_metrics=["Booth Visits", "Demo Requests"]),
                ChannelPlan(channel="Medical Journals", content_type="Technical Articles", frequency="Monthly", budget_allocation=0.30, success_metrics=["Citations", "Reach"]),
                ChannelPlan(channel="Webinars", content_type="Compliance Training", frequency="Bi-weekly", budget_allocation=0.25, success_metrics=["Registration", "Completion"]),
                ChannelPlan(channel="Email", content_type="Compliance Updates", frequency="Weekly", budget_allocation=0.10, success_metrics=["Open Rate", "CTR"]),
            ],
            total_budget=Money(Decimal("275000.00")),
            expected_roi=3.1,
        ),
        Campaign(
            id=CampaignId("cmp-015"),
            name="Manufacturing 4.0 Revolution",
            status=CampaignStatus.DRAFT,
            theme="Smart Factories, Smarter Operations",
            date_range=DateRange(
                start_date=today + timedelta(days=42),
                end_date=today + timedelta(days=102)
            ),
            ideas=[
                CampaignIdea(
                    id=str(uuid.uuid4())[:8],
                    theme="Industrial IoT at Scale",
                    core_message="Connect, monitor, and optimize your entire manufacturing operation",
                    target_segments=["Manufacturing Engineers", "Plant Managers", "Operations Directors"],
                    competitive_angle="Predictive maintenance that reduces downtime by 60%"
                )
            ],
            channel_mix=[
                ChannelPlan(channel="Trade Shows", content_type="Live Factory Demos", frequency="Quarterly", budget_allocation=0.40, success_metrics=["Demos", "Leads"]),
                ChannelPlan(channel="LinkedIn", content_type="Industry Insights", frequency="3x/week", budget_allocation=0.25, success_metrics=["Engagement", "Reach"]),
                ChannelPlan(channel="Webinars", content_type="ROI Workshops", frequency="Monthly", budget_allocation=0.25, success_metrics=["Registration", "Pipeline"]),
                ChannelPlan(channel="Case Studies", content_type="Customer Stories", frequency="Quarterly", budget_allocation=0.10, success_metrics=["Downloads", "Shares"]),
            ],
            total_budget=Money(Decimal("235000.00")),
            expected_roi=3.6,
        ),
    ]
    
    for campaign in campaigns:
        campaign_repo.save(campaign)
    
    print("Database seeding completed!")
    print(f"Seeded {len(services)} services, {len(signals)} market signals, and {len(campaigns)} campaigns")
