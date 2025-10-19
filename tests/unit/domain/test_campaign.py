import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from app.domain.entities.campaign import (
    Campaign, CampaignStatus, CampaignIdea, ChannelPlan, CampaignMetrics, CampaignFeedback
)
from app.domain.value_objects.campaign_id import CampaignId
from app.domain.value_objects.money import Money
from app.domain.value_objects.date_range import DateRange
from app.core.exceptions import ValidationError


@pytest.mark.unit
class TestCampaignIdea:
    def test_create_campaign_idea_success(self):
        idea = CampaignIdea(
            id="idea_001",
            theme="Innovation",
            core_message="Transform your business",
            target_segments=["Tech Leaders"],
            competitive_angle="AI-powered solutions"
        )
        assert idea.theme == "Innovation"
        assert idea.core_message == "Transform your business"
        assert len(idea.target_segments) == 1
    
    def test_create_campaign_idea_no_theme_fails(self):
        with pytest.raises(ValidationError, match="must have a theme"):
            CampaignIdea(
                id="idea_001",
                theme="",
                core_message="Transform your business",
                target_segments=["Tech Leaders"],
                competitive_angle="AI-powered"
            )
    
    def test_create_campaign_idea_no_message_fails(self):
        with pytest.raises(ValidationError, match="must have a core message"):
            CampaignIdea(
                id="idea_001",
                theme="Innovation",
                core_message="",
                target_segments=["Tech Leaders"],
                competitive_angle="AI-powered"
            )
    
    def test_create_campaign_idea_no_segments_fails(self):
        with pytest.raises(ValidationError, match="must have target segments"):
            CampaignIdea(
                id="idea_001",
                theme="Innovation",
                core_message="Transform your business",
                target_segments=[],
                competitive_angle="AI-powered"
            )


@pytest.mark.unit
class TestChannelPlan:
    def test_create_channel_plan_success(self):
        plan = ChannelPlan(
            channel="email",
            content_type="newsletter",
            frequency="weekly",
            budget_allocation=0.4,
            success_metrics=["Open rate", "CTR"]
        )
        assert plan.channel == "email"
        assert plan.budget_allocation == 0.4
        assert len(plan.success_metrics) == 2
    
    def test_create_channel_plan_invalid_allocation_fails(self):
        with pytest.raises(ValidationError, match="must be between 0 and 1"):
            ChannelPlan(
                channel="email",
                content_type="newsletter",
                frequency="weekly",
                budget_allocation=1.5,
                success_metrics=["Open rate"]
            )
    
    def test_create_channel_plan_negative_allocation_fails(self):
        with pytest.raises(ValidationError, match="must be between 0 and 1"):
            ChannelPlan(
                channel="email",
                content_type="newsletter",
                frequency="weekly",
                budget_allocation=-0.2,
                success_metrics=["Open rate"]
            )


@pytest.mark.unit
class TestCampaign:
    def test_create_campaign_success(self, mock_campaign_id, mock_campaign_idea, mock_channel_plan, mock_date_range):
        campaign = Campaign(
            id=mock_campaign_id,
            name="Test Campaign",
            status=CampaignStatus.DRAFT,
            theme="AI Innovation",
            date_range=mock_date_range,
            ideas=[mock_campaign_idea],
            channel_mix=[mock_channel_plan, ChannelPlan(
                channel="social",
                content_type="posts",
                frequency="daily",
                budget_allocation=0.6,
                success_metrics=["Engagement"]
            )],
            total_budget=Money(amount=Decimal("5000.00"), currency="USD"),
            expected_roi=2.5
        )
        assert campaign.name == "Test Campaign"
        assert campaign.status == CampaignStatus.DRAFT
        assert len(campaign.ideas) == 1
        assert len(campaign.channel_mix) == 2
    
    def test_create_campaign_no_name_fails(self, mock_campaign_id, mock_campaign_idea, mock_channel_plan, mock_date_range):
        with pytest.raises(ValidationError, match="must have a name"):
            Campaign(
                id=mock_campaign_id,
                name="",
                status=CampaignStatus.DRAFT,
                theme="AI Innovation",
                date_range=mock_date_range,
                ideas=[mock_campaign_idea],
                channel_mix=[mock_channel_plan, ChannelPlan(
                    channel="social", content_type="posts",
                    frequency="daily", budget_allocation=0.6,
                    success_metrics=["Engagement"]
                )],
                total_budget=Money(amount=Decimal("5000.00"), currency="USD"),
                expected_roi=2.5
            )
    
    def test_create_campaign_no_ideas_fails(self, mock_campaign_id, mock_channel_plan, mock_date_range):
        with pytest.raises(ValidationError, match="must have at least one idea"):
            Campaign(
                id=mock_campaign_id,
                name="Test Campaign",
                status=CampaignStatus.DRAFT,
                theme="AI Innovation",
                date_range=mock_date_range,
                ideas=[],
                channel_mix=[mock_channel_plan, ChannelPlan(
                    channel="social", content_type="posts",
                    frequency="daily", budget_allocation=0.6,
                    success_metrics=["Engagement"]
                )],
                total_budget=Money(amount=Decimal("5000.00"), currency="USD"),
                expected_roi=2.5
            )
    
    def test_create_campaign_invalid_budget_allocation_fails(self, mock_campaign_id, mock_campaign_idea, mock_date_range):
        with pytest.raises(ValidationError, match="must sum to 1.0"):
            Campaign(
                id=mock_campaign_id,
                name="Test Campaign",
                status=CampaignStatus.DRAFT,
                theme="AI Innovation",
                date_range=mock_date_range,
                ideas=[mock_campaign_idea],
                channel_mix=[
                    ChannelPlan(
                        channel="email", content_type="newsletter",
                        frequency="weekly", budget_allocation=0.4,
                        success_metrics=["Open rate"]
                    ),
                    ChannelPlan(
                        channel="social", content_type="posts",
                        frequency="daily", budget_allocation=0.4,
                        success_metrics=["Engagement"]
                    )
                ],
                total_budget=Money(amount=Decimal("5000.00"), currency="USD"),
                expected_roi=2.5
            )
    
    def test_activate_campaign_success(self, mock_campaign):
        assert mock_campaign.status == CampaignStatus.DRAFT
        mock_campaign.activate()
        assert mock_campaign.status == CampaignStatus.ACTIVE
    
    def test_activate_non_draft_campaign_fails(self, mock_campaign):
        mock_campaign.status = CampaignStatus.ACTIVE
        with pytest.raises(ValidationError, match="Cannot activate"):
            mock_campaign.activate()
    
    def test_pause_campaign_success(self, mock_campaign):
        mock_campaign.status = CampaignStatus.ACTIVE
        mock_campaign.pause()
        assert mock_campaign.status == CampaignStatus.PAUSED
    
    def test_pause_non_active_campaign_fails(self, mock_campaign):
        with pytest.raises(ValidationError, match="Cannot pause"):
            mock_campaign.pause()
    
    def test_complete_campaign_success(self, mock_campaign):
        mock_campaign.status = CampaignStatus.ACTIVE
        mock_campaign.complete()
        assert mock_campaign.status == CampaignStatus.COMPLETED
    
    def test_complete_paused_campaign_success(self, mock_campaign):
        mock_campaign.status = CampaignStatus.PAUSED
        mock_campaign.complete()
        assert mock_campaign.status == CampaignStatus.COMPLETED
    
    def test_cancel_campaign_success(self, mock_campaign):
        mock_campaign.cancel()
        assert mock_campaign.status == CampaignStatus.CANCELLED
    
    def test_cancel_completed_campaign_fails(self, mock_campaign):
        mock_campaign.status = CampaignStatus.COMPLETED
        with pytest.raises(ValidationError, match="Cannot cancel completed"):
            mock_campaign.cancel()
    
    def test_update_metrics_success(self, mock_campaign):
        metrics = CampaignMetrics(
            engagement="80%",
            leads="150",
            conversions="25"
        )
        mock_campaign.update_metrics(metrics)
        assert mock_campaign.metrics.engagement == "80%"
        assert mock_campaign.metrics.leads == "150"
    
    def test_add_feedback_success(self, mock_campaign):
        feedback = CampaignFeedback(
            feedback_type="like",
            target="idea",
            comment="Great campaign idea!"
        )
        assert len(mock_campaign.feedback_history) == 0
        mock_campaign.add_feedback(feedback)
        assert len(mock_campaign.feedback_history) == 1
        assert mock_campaign.feedback_history[0].feedback_type == "like"
