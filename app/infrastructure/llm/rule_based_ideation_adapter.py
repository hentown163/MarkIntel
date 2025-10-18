"""Rule-based fallback adapter for campaign ideation"""
import uuid
from typing import List

from app.domain.services.campaign_ideation_service import (
    CampaignIdeationService,
    CampaignGenerationRequest
)
from app.domain.entities.campaign import CampaignIdea, ChannelPlan
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal


class RuleBasedCampaignIdeationAdapter(CampaignIdeationService):
    """
    Rule-based fallback implementation (for when AI is disabled)
    
    This uses the old hardcoded logic as a fallback
    """
    
    def generate_ideas(
        self,
        service: Service,
        market_signals: List[MarketSignal],
        request: CampaignGenerationRequest
    ) -> List[CampaignIdea]:
        """Generate campaign ideas using rules"""
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
        else:
            theme = f"Maximize Your {category} Investment"
            message = "Integrated solutions for complex enterprise needs"
            angle = "Seamless integration with your existing tech stack"
        
        idea = CampaignIdea(
            id=str(uuid.uuid4())[:8],
            theme=theme,
            core_message=message,
            target_segments=service.target_audience,
            competitive_angle=angle
        )
        return [idea]
    
    def optimize_channel_mix(
        self,
        ideas: List[CampaignIdea],
        target_audience: List[str]
    ) -> List[ChannelPlan]:
        """Optimize channel mix using rules"""
        is_security = any("CISO" in a or "Security" in a for a in target_audience)
        
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
