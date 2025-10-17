import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from ..models import Campaign, MarketSignal, Service, CampaignMetrics, CampaignIdea, ChannelPlan, CampaignStatus, ImpactLevel

class MemStorage:
    def __init__(self):
        self.campaigns: dict[str, Campaign] = {}
        self.market_signals: dict[str, MarketSignal] = {}
        self.services: dict[str, Service] = {}
        self._seed_data()

    def _id(self):
        return str(uuid.uuid4())

    def _seed_data(self):
        services = [
            Service(
                id="svc-001",
                name="CloudScale AI Security Suite",
                category="Security",
                description="AI-powered threat detection, automated response, and zero-trust architecture implementation for enterprise security.",
                target_audience=["CISO", "Security Teams", "IT Directors"],
                key_benefits=["Zero Trust", "Threat Prevention", "Compliance"],
                market_mentions=234,
                active_campaigns=3,
                backed_competitors=3,
                competitors=["Sentinel", "ThreatGuard Pro", "CyberShield"],
            ),
            Service(
                id="svc-002",
                name="Multi-Cloud Infrastructure Platform",
                category="Cloud Infrastructure",
                description="Unified management across AWS, Azure, and GCP with automated provisioning, cost optimization, and security compliance monitoring.",
                target_audience=["Cloud Architects", "DevOps Teams", "CTOs"],
                key_benefits=["Unified View", "Cost Efficiency", "Automated Provisioning"],
                market_mentions=189,
                active_campaigns=6,
                backed_competitors=3,
                competitors=["CloudMaster", "MultiCloud Pro", "Infralink"],
            ),
            Service(
                id="svc-003",
                name="Enterprise AI Platform",
                category="Artificial Intelligence",
                description="End-to-end AI solution for predictive analytics, automation, and intelligent decision-making at enterprise scale.",
                target_audience=["CDO", "AI Engineers", "Data Scientists"],
                key_benefits=["Governance", "Scalability", "Compliance"],
                market_mentions=312,
                active_campaigns=12,
                backed_competitors=3,
                competitors=["AI Enterprise", "SmartOps AI", "Neural Cloud"],
            ),
            Service(
                id="svc-004",
                name="Real-Time Analytics Engine",
                category="Data & Analytics",
                description="High-performance data processing and analytics platform with real-time insights and predictive modeling capabilities.",
                target_audience=["Data Architects", "Analysts", "Business Intelligence Teams"],
                key_benefits=["Real-time Processing", "Predictive Modeling", "Cost Efficiency"],
                market_mentions=156,
                active_campaigns=5,
                backed_competitors=3,
                competitors=["DataFlow Pro", "Analytics Hub", "InsightEngine"],
            ),
            Service(
                id="svc-005",
                name="Edge Computing Platform",
                category="Edge & IoT",
                description="Distributed computing solution for IoT devices, edge analytics, and low-latency processing at the network edge.",
                target_audience=["IoT Architects", "Manufacturing Teams", "Smart City Planners"],
                key_benefits=["Low Latency", "Edge Analytics", "IoT Integration"],
                market_mentions=143,
                active_campaigns=4,
                backed_competitors=3,
                competitors=["EdgeFlex", "IoT Cloud", "Edge Master"],
            ),
            Service(
                id="svc-006",
                name="Zero-Trust Security Framework",
                category="Security",
                description="Comprehensive zero-trust implementation with identity verification, micro-segmentation, and continuous authentication.",
                target_audience=["CISO", "Security Architects", "Compliance Officers"],
                key_benefits=["Identity Verification", "Micro-segmentation", "Compliance"],
                market_mentions=278,
                active_campaigns=9,
                backed_competitors=3,
                competitors=["ZeroGuard", "TrustNet", "SecureAccess"],
            ),
        ]
        for s in services:
            self.services[s.id] = s

        now = datetime.utcnow()
        signals = [
            MarketSignal(
                id="sig-001",
                source="Gartner Report",
                content="AI security platforms surge 47%. The AI security market is projected to grow at 47% CAGR through 2026. Key drivers include increasing cyber threats, regulatory compliance requirements, and enterprise digital transformation initiatives. CloudScale's AI Security Suite is well-positioned to capture market share.",
                timestamp=(now - timedelta(hours=2)).isoformat() + "Z",
                relevance_score=0.92,
                category="AI",
                impact=ImpactLevel.high,
            ),
            MarketSignal(
                id="sig-002",
                source="TechCrunch",
                content="CompetitorX Launches Cloud Infrastructure Suite. Major competitor launched comprehensive multi-cloud infrastructure management suite targeting enterprise customers. Feature set includes automated provisioning, cost optimization, and security compliance. Pricing positioned 15% below market average.",
                timestamp=(now - timedelta(hours=4)).isoformat() + "Z",
                relevance_score=0.85,
                category="Competitor",
                impact=ImpactLevel.high,
            ),
            MarketSignal(
                id="sig-003",
                source="Social Media Analytics",
                content="Enterprise AI Adoption Reaches 73%. Latest industry survey reveals 73% of Fortune 500 companies have deployed AI solutions in production. Primary use cases: predictive analytics (45%), automation (38%), and customer intelligence (32%). Indicates strong market opportunity for CloudScale's AI platform.",
                timestamp=(now - timedelta(hours=6)).isoformat() + "Z",
                relevance_score=0.88,
                category="AI",
                impact=ImpactLevel.medium,
            ),
            MarketSignal(
                id="sig-004",
                source="Social Media Analytics",
                content="Zero-Trust Architecture Keyword Surge: +250%. Social media mentions of 'zero-trust architecture' increased 250% in past week. LinkedIn discussions show strong interest from CISOs and security teams. Opportunity to position CloudScale's security framework as industry-leading zero-trust solution.",
                timestamp=(now - timedelta(hours=8)).isoformat() + "Z",
                relevance_score=0.78,
                category="Security",
                impact=ImpactLevel.medium,
            ),
            MarketSignal(
                id="sig-005",
                source="IDC Industry Report",
                content="Edge Computing Demand Spike in Manufacturing Sector. Manufacturing enterprises increasing edge computing adoption by 62% YoY. Primary drivers: IoT integration, real-time analytics, and reduced latency requirements. CloudScale's Edge Platform can address this vertical market opportunity.",
                timestamp=(now - timedelta(hours=12)).isoformat() + "Z",
                relevance_score=0.81,
                category="Cloud",
                impact=ImpactLevel.medium,
            ),
        ]
        for sig in signals:
            self.market_signals[sig.id] = sig

        campaigns = [
            Campaign(
                id="camp-001",
                name="Q4 Cloud Security Leadership Push",
                status=CampaignStatus.active,
                theme="Zero-Trust Architecture Excellence",
                start_date="2024-10-15",
                end_date="2024-12-31",
                ideas=[
                    CampaignIdea(
                        id="idea-001",
                        theme="Zero Trust, Zero Compromise",
                        core_message="End-to-end security from code to cloud",
                        target_segments=["CISO", "Security Teams"],
                        competitive_angle="While others focus on detection, we prevent breaches at the source",
                    )
                ],
                channel_mix=[
                    ChannelPlan(channel="LinkedIn", content_type="Thought Leadership", frequency="Weekly", budget_allocation=0.35, success_metrics=["Engagement Rate", "Lead Quality"]),
                    ChannelPlan(channel="Webinar", content_type="Deep Dives", frequency="Bi-weekly", budget_allocation=0.25, success_metrics=["Attendee Count", "Conversion Rate"]),
                    ChannelPlan(channel="Email", content_type="Nurture Sequences", frequency="Daily", budget_allocation=0.20, success_metrics=["Open Rate", "Click-Through"]),
                    ChannelPlan(channel="Events", content_type="Executive Briefings", frequency="Monthly", budget_allocation=0.20, success_metrics=["Attendance", "Pipeline Generated"]),
                ],
                total_budget=50000,
                expected_roi=3.5,
                metrics=CampaignMetrics(engagement="+34% engagement"),
            ),
            Campaign(
                id="camp-002",
                name="AI Platform Launch Campaign",
                status=CampaignStatus.active,
                theme="Enterprise AI Transformation",
                start_date="2024-11-01",
                end_date="2024-11-30",
                ideas=[
                    CampaignIdea(
                        id="idea-002",
                        theme="Future-Proof Your AI Strategy",
                        core_message="Enterprise-grade AI with built-in governance and compliance",
                        target_segments=["CDO", "AI Engineers"],
                        competitive_angle="Unlike competitors, we offer SOC 2-compliant AI workflows",
                    )
                ],
                channel_mix=[
                    ChannelPlan(channel="LinkedIn", content_type="Product Updates", frequency="3x/week", budget_allocation=0.30, success_metrics=["Engagement Rate", "Follower Growth"]),
                    ChannelPlan(channel="Email", content_type="Newsletter", frequency="Weekly", budget_allocation=0.25, success_metrics=["Open Rate", "Click-Through"]),
                    ChannelPlan(channel="Blog", content_type="Technical Content", frequency="2x/week", budget_allocation=0.20, success_metrics=["Page Views", "Time on Page"]),
                    ChannelPlan(channel="Events", content_type="How-To Sessions", frequency="Weekly", budget_allocation=0.25, success_metrics=["Registration", "Attendance"]),
                ],
                total_budget=75000,
                expected_roi=4.2,
                metrics=CampaignMetrics(leads="+28% leads"),
            ),
            Campaign(
                id="camp-003",
                name="Multi-Cloud Excellence Campaign",
                status=CampaignStatus.completed,
                theme="Hybrid Cloud Infrastructure",
                start_date="2024-09-15",
                end_date="2024-10-15",
                ideas=[
                    CampaignIdea(
                        id="idea-003",
                        theme="Maximize Your Cloud Investment",
                        core_message="Unified management across AWS, Azure, and GCP",
                        target_segments=["Cloud Architects", "DevOps Teams"],
                        competitive_angle="Seamless integration with your existing tech stack",
                    )
                ],
                channel_mix=[
                    ChannelPlan(channel="LinkedIn", content_type="Case Studies", frequency="Weekly", budget_allocation=0.30, success_metrics=["Engagement Rate", "Lead Quality"]),
                    ChannelPlan(channel="Webinar", content_type="Product Demos", frequency="Weekly", budget_allocation=0.30, success_metrics=["Attendee Count", "Demo Requests"]),
                    ChannelPlan(channel="Email", content_type="Campaign Series", frequency="2x/week", budget_allocation=0.20, success_metrics=["Open Rate", "Conversion Rate"]),
                    ChannelPlan(channel="PR", content_type="Press Releases", frequency="Monthly", budget_allocation=0.20, success_metrics=["Media Pickup", "Brand Mentions"]),
                ],
                total_budget=60000,
                expected_roi=3.8,
                metrics=CampaignMetrics(conversions="+42% conversions"),
            ),
        ]
        for c in campaigns:
            self.campaigns[c.id] = c

    def get_campaigns(self) -> List[Campaign]:
        return sorted(self.campaigns.values(), key=lambda c: c.start_date, reverse=True)

    def get_recent_campaigns(self, limit: int = 3) -> List[Campaign]:
        return self.get_campaigns()[:limit]

    def get_campaign_by_id(self, cid: str) -> Optional[Campaign]:
        return self.campaigns.get(cid)

    def create_campaign(self, campaign: Campaign) -> Campaign:
        campaign.id = self._id()
        self.campaigns[campaign.id] = campaign
        return campaign

    def get_market_signals(self) -> List[MarketSignal]:
        return sorted(self.market_signals.values(), key=lambda s: s.timestamp, reverse=True)

    def get_recent_market_signals(self, limit: int = 4) -> List[MarketSignal]:
        return self.get_market_signals()[:limit]

    def add_market_signal(self, signal: MarketSignal) -> MarketSignal:
        signal.id = self._id()
        self.market_signals[signal.id] = signal
        return signal

    def get_services(self) -> List[Service]:
        return list(self.services.values())

    def get_service_by_id(self, sid: str) -> Optional[Service]:
        return self.services.get(sid)

    def get_dashboard_metrics(self):
        active = len([c for c in self.campaigns.values() if c.status == "active"])
        return {
            "active_campaigns": {"count": active, "change": "+3 this week"},
            "market_insights": {"count": len(self.market_signals), "change": "+127 today"},
            "competitor_tracking": {"count": 23, "change": "5 active alerts"},
            "ai_generations": {"count": 156, "change": "+42 this month"},
        }

storage = MemStorage()
