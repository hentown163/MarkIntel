import uuid
import random
from datetime import datetime, timedelta
from typing import List, Optional
from ..models import (
    Service,
    MarketSignal,
    CampaignIdea,
    ChannelPlan,
    Campaign,
    CampaignGenerationRequest,
    CampaignStatus,
)

class CampaignGenerator:
    def __init__(self, services: List[Service], market_signals: List[MarketSignal]):
        self.services = services
        self.market_signals = market_signals

    def _generate_ideas(self, service: Service) -> List[CampaignIdea]:
        relevant_signals = [s for s in self.market_signals if s.relevance_score > 0.7]

        category = service.category
        if category in ["AI Platform", "Artificial Intelligence"]:
            theme = "Future-Proof Your AI Strategy"
            message = "Enterprise-grade AI with built-in governance and compliance"
            angle = "Unlike competitors, we offer SOC 2-compliant AI workflows"
        elif category in ["Cloud Security", "Security"]:
            theme = "Zero Trust, Zero Compromise"
            message = "End-to-end security from code to cloud"
            angle = "While others focus on detection, we prevent breaches at the source"
        elif category == "Cloud Infrastructure":
            theme = "Maximize Your Multi-Cloud Investment"
            message = "Unified management across all major cloud providers"
            angle = "Seamless integration with your existing tech stack"
        elif category in ["Data & Analytics", "Data Platform"]:
            theme = "Real-Time Intelligence, Real Business Impact"
            message = "Transform data into actionable insights at enterprise scale"
            angle = "Process and analyze data 10x faster than traditional platforms"
        elif category == "Edge & IoT":
            theme = "Bring Computing to the Edge"
            message = "Low-latency processing for IoT and edge devices"
            angle = "Deploy intelligence where your data is generated"
        else:
            theme = f"Maximize Your {category} Investment"
            message = "Integrated solutions for complex enterprise needs"
            angle = "Seamless integration with your existing tech stack"

        idea = CampaignIdea(
            id=str(uuid.uuid4())[:8],
            theme=theme,
            core_message=message,
            target_segments=service.target_audience,
            competitive_angle=angle,
        )
        return [idea]

    def _optimize_channel_mix(self, ideas: List[CampaignIdea]) -> List[ChannelPlan]:
        audiences = set()
        for idea in ideas:
            audiences.update(idea.target_segments)

        audience_list = list(audiences)
        is_security = any(
            "CISO" in a or "Security" in a or "Security Teams" in a for a in audience_list
        )

        if is_security:
            return [
                ChannelPlan(channel="LinkedIn", content_type="Thought Leadership", frequency="Weekly", budget_allocation=0.35, success_metrics=["Engagement Rate", "Lead Quality"]),
                ChannelPlan(channel="Webinars", content_type="Deep Dives", frequency="Bi-weekly", budget_allocation=0.25, success_metrics=["Attendee Count", "Conversion Rate"]),
                ChannelPlan(channel="Email", content_type="Nurture Sequences", frequency="Daily", budget_allocation=0.20, success_metrics=["Open Rate", "Click-Through"]),
                ChannelPlan(channel="Events", content_type="Executive Briefings", frequency="Monthly", budget_allocation=0.20, success_metrics=["Attendance", "Pipeline Generated"]),
            ]
        else:
            return [
                ChannelPlan(channel="LinkedIn", content_type="Product Updates", frequency="3x/week", budget_allocation=0.30, success_metrics=["Engagement Rate", "Follower Growth"]),
                ChannelPlan(channel="Email", content_type="Newsletter", frequency="Weekly", budget_allocation=0.25, success_metrics=["Open Rate", "Click-Through"]),
                ChannelPlan(channel="Blog", content_type="Technical Content", frequency="2x/week", budget_allocation=0.20, success_metrics=["Page Views", "Time on Page"]),
                ChannelPlan(channel="Webinars", content_type="How-To Sessions", frequency="Weekly", budget_allocation=0.25, success_metrics=["Registration", "Attendance"]),
            ]

    def generate_campaign_plan(
        self, request: CampaignGenerationRequest, service: Optional[Service] = None
    ) -> Campaign:
        target_service = service
        if not target_service:
            for s in self.services:
                if request.product_service.lower() in s.name.lower() or s.name.lower() in request.product_service.lower():
                    target_service = s
                    break

        if not target_service:
            target_service = Service(
                id=str(uuid.uuid4())[:8],
                name=request.product_service,
                category="Enterprise Solution",
                target_audience=[a.strip() for a in request.target_audience.split(",")],
                key_benefits=["Innovation", "Scalability", "Reliability"],
                competitors=[c.strip() for c in request.competitors.split(",")] if request.competitors else [],
            )

        ideas = self._generate_ideas(target_service)
        channel_mix = self._optimize_channel_mix(ideas)

        total_budget = round(50000 + random.random() * 50000)
        expected_roi = round(3.0 + random.random() * 2.0, 1)

        now = datetime.utcnow()
        duration = request.duration_days or 30
        end_date = now + timedelta(days=duration)

        campaign = Campaign(
            id=str(uuid.uuid4())[:8],
            name=f"{target_service.name} Campaign",
            status=CampaignStatus.draft,
            theme=ideas[0].theme if ideas else "Enterprise Campaign",
            start_date=now.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            ideas=ideas,
            channel_mix=channel_mix,
            total_budget=total_budget,
            expected_roi=expected_roi,
        )
        return campaign
