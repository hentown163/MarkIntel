"""Campaign mapper - converts between domain entities and DTOs"""
from typing import List
from datetime import date as Date

from app.domain.entities.campaign import Campaign, CampaignIdea, ChannelPlan, CampaignMetrics
from app.domain.value_objects import CampaignId, Money, DateRange
from app.application.dtos.response.campaign_response import (
    CampaignResponseDTO,
    CampaignIdeaDTO,
    ChannelPlanDTO,
    CampaignMetricsDTO
)


class CampaignMapper:
    """
    Mapper for Campaign entity and DTOs
    
    Following Single Responsibility Principle - only handles mapping
    """
    
    @staticmethod
    def to_response_dto(campaign: Campaign) -> CampaignResponseDTO:
        """Convert domain Campaign to response DTO"""
        return CampaignResponseDTO(
            id=str(campaign.id),
            name=campaign.name,
            status=campaign.status.value,
            theme=campaign.theme,
            start_date=campaign.date_range.start_date.isoformat(),
            end_date=campaign.date_range.end_date.isoformat(),
            ideas=[CampaignMapper._idea_to_dto(idea) for idea in campaign.ideas],
            channel_mix=[CampaignMapper._channel_to_dto(ch) for ch in campaign.channel_mix],
            total_budget=float(campaign.total_budget.amount),
            expected_roi=campaign.expected_roi,
            metrics=CampaignMapper._metrics_to_dto(campaign.metrics) if campaign.metrics else None
        )
    
    @staticmethod
    def _idea_to_dto(idea: CampaignIdea) -> CampaignIdeaDTO:
        """Convert CampaignIdea to DTO"""
        return CampaignIdeaDTO(
            id=idea.id,
            theme=idea.theme,
            core_message=idea.core_message,
            target_segments=idea.target_segments,
            competitive_angle=idea.competitive_angle
        )
    
    @staticmethod
    def _channel_to_dto(channel: ChannelPlan) -> ChannelPlanDTO:
        """Convert ChannelPlan to DTO"""
        return ChannelPlanDTO(
            channel=channel.channel,
            content_type=channel.content_type,
            frequency=channel.frequency,
            budget_allocation=channel.budget_allocation,
            success_metrics=channel.success_metrics
        )
    
    @staticmethod
    def _metrics_to_dto(metrics: CampaignMetrics) -> CampaignMetricsDTO:
        """Convert CampaignMetrics to DTO"""
        return CampaignMetricsDTO(
            engagement=metrics.engagement,
            leads=metrics.leads,
            conversions=metrics.conversions
        )
