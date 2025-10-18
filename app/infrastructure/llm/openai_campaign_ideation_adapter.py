"""OpenAI adapter for campaign ideation - implementing domain service port"""
import os
import json
import uuid
from typing import List
from openai import OpenAI

from app.domain.services.campaign_ideation_service import (
    CampaignIdeationService,
    CampaignGenerationRequest
)
from app.domain.entities.campaign import CampaignIdea, ChannelPlan
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal
from app.core.exceptions import ExternalServiceError


class OpenAICampaignIdeationAdapter(CampaignIdeationService):
    """
    OpenAI implementation of campaign ideation service
    
    Following Dependency Inversion Principle - implements domain service interface
    Following Open/Closed Principle - can be swapped with other implementations
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not found. AI generation will not work.")
            self.client = None
            self.model = None
        else:
            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-5"
    
    def generate_ideas(
        self,
        service: Service,
        market_signals: List[MarketSignal],
        request: CampaignGenerationRequest
    ) -> List[CampaignIdea]:
        """Generate campaign ideas using GPT-5"""
        if not self.client:
            raise ExternalServiceError("OpenAI client not initialized. Please set OPENAI_API_KEY environment variable.")
        
        try:
            prompt = self._build_ideation_prompt(service, market_signals, request)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert B2B marketing strategist specializing in enterprise technology campaigns. Generate creative, data-driven campaign ideas based on market intelligence and competitive analysis. Respond with JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_completion_tokens=2048
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._parse_ideas(result)
            
        except Exception as e:
            raise ExternalServiceError(f"Failed to generate campaign ideas: {str(e)}")
    
    def optimize_channel_mix(
        self,
        ideas: List[CampaignIdea],
        target_audience: List[str]
    ) -> List[ChannelPlan]:
        """Optimize channel mix using GPT-5"""
        if not self.client:
            raise ExternalServiceError("OpenAI client not initialized. Please set OPENAI_API_KEY environment variable.")
        
        try:
            prompt = self._build_channel_optimization_prompt(ideas, target_audience)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a B2B marketing channel optimization expert. Recommend the optimal mix of marketing channels with budget allocation and success metrics. Respond with JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_completion_tokens=1024
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._parse_channel_mix(result)
            
        except Exception as e:
            raise ExternalServiceError(f"Failed to optimize channel mix: {str(e)}")
    
    def _build_ideation_prompt(
        self,
        service: Service,
        market_signals: List[MarketSignal],
        request: CampaignGenerationRequest
    ) -> str:
        """Build prompt for campaign ideation"""
        relevant_signals = [s for s in market_signals if s.is_highly_relevant()][:5]
        
        signal_context = "\n".join([
            f"- [{s.source}] {s.content} (Impact: {s.impact.value}, Relevance: {s.relevance_score})"
            for s in relevant_signals
        ])
        
        return f"""Generate 1-2 creative B2B marketing campaign ideas for the following:

**Product/Service:** {service.name}
**Category:** {service.category}
**Description:** {service.description}
**Target Audience:** {', '.join(service.target_audience)}
**Key Benefits:** {', '.join(service.key_benefits)}
**Competitors:** {', '.join(service.competitors or [])}

**Market Intelligence:**
{signal_context or "No recent market signals available"}

**Additional Context:** {request.additional_context or "None"}

Generate campaign ideas that:
1. Address current market trends from the intelligence
2. Differentiate from competitors
3. Resonate with the target audience
4. Leverage the key benefits

Respond in this JSON format:
{{
  "ideas": [
    {{
      "theme": "Campaign theme (5-10 words)",
      "core_message": "Main value proposition (1-2 sentences)",
      "target_segments": ["segment1", "segment2"],
      "competitive_angle": "How we differentiate (1-2 sentences)"
    }}
  ]
}}"""
    
    def _build_channel_optimization_prompt(
        self,
        ideas: List[CampaignIdea],
        target_audience: List[str]
    ) -> str:
        """Build prompt for channel optimization"""
        idea_summary = " | ".join([idea.theme for idea in ideas])
        
        return f"""Recommend the optimal B2B marketing channel mix for:

**Campaign Themes:** {idea_summary}
**Target Audience:** {', '.join(target_audience)}

Consider these B2B channels:
- LinkedIn (Thought leadership, ads, engagement)
- Email (Newsletters, nurture sequences, campaigns)
- Webinars (Educational sessions, product demos)
- Events (Conferences, executive briefings)
- Content Marketing (Blog, whitepapers, case studies)
- Paid Search (Google Ads)

Recommend 3-4 channels with:
1. Budget allocation (must sum to 1.0)
2. Content type
3. Posting frequency
4. Success metrics

Respond in this JSON format:
{{
  "channels": [
    {{
      "channel": "Channel name",
      "content_type": "Type of content",
      "frequency": "Posting frequency (e.g., Weekly, 3x/week)",
      "budget_allocation": 0.35,
      "success_metrics": ["metric1", "metric2"]
    }}
  ]
}}"""
    
    def _parse_ideas(self, result: dict) -> List[CampaignIdea]:
        """Parse AI response into CampaignIdea entities"""
        ideas = []
        for idea_data in result.get("ideas", []):
            idea = CampaignIdea(
                id=str(uuid.uuid4())[:8],
                theme=idea_data.get("theme", "Campaign Theme"),
                core_message=idea_data.get("core_message", "Value proposition"),
                target_segments=idea_data.get("target_segments", []),
                competitive_angle=idea_data.get("competitive_angle", "Differentiation")
            )
            ideas.append(idea)
        return ideas
    
    def _parse_channel_mix(self, result: dict) -> List[ChannelPlan]:
        """Parse AI response into ChannelPlan entities"""
        channels = []
        for channel_data in result.get("channels", []):
            channel = ChannelPlan(
                channel=channel_data.get("channel", ""),
                content_type=channel_data.get("content_type", ""),
                frequency=channel_data.get("frequency", ""),
                budget_allocation=channel_data.get("budget_allocation", 0.25),
                success_metrics=channel_data.get("success_metrics", [])
            )
            channels.append(channel)
        return channels
