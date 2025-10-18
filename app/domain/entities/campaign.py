"""Campaign aggregate root and related entities"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import date

from app.domain.value_objects import CampaignId, Money, DateRange
from app.core.exceptions import ValidationError


class CampaignStatus(str, Enum):
    """Campaign status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class CampaignIdea:
    """Campaign idea entity - part of Campaign aggregate"""
    id: str
    theme: str
    core_message: str
    target_segments: List[str]
    competitive_angle: str
    
    def __post_init__(self):
        if not self.theme or len(self.theme.strip()) == 0:
            raise ValidationError("Campaign idea must have a theme")
        if not self.core_message:
            raise ValidationError("Campaign idea must have a core message")
        if not self.target_segments:
            raise ValidationError("Campaign idea must have target segments")


@dataclass
class ChannelPlan:
    """Channel plan entity - part of Campaign aggregate"""
    channel: str
    content_type: str
    frequency: str
    budget_allocation: float
    success_metrics: List[str]
    
    def __post_init__(self):
        if not self.channel:
            raise ValidationError("Channel plan must specify a channel")
        if self.budget_allocation < 0 or self.budget_allocation > 1:
            raise ValidationError("Budget allocation must be between 0 and 1")


@dataclass
class CampaignMetrics:
    """Campaign metrics value object"""
    engagement: Optional[str] = None
    leads: Optional[str] = None
    conversions: Optional[str] = None


@dataclass
class CampaignFeedback:
    """Campaign feedback value object"""
    feedback_type: str
    target: str
    comment: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class Campaign:
    """
    Campaign aggregate root
    
    Follows SOLID principles:
    - Single Responsibility: Manages campaign lifecycle
    - Encapsulation: Protects internal state
    """
    id: CampaignId
    name: str
    status: CampaignStatus
    theme: str
    date_range: DateRange
    ideas: List[CampaignIdea]
    channel_mix: List[ChannelPlan]
    total_budget: Money
    expected_roi: float
    metrics: Optional[CampaignMetrics] = None
    service_id: Optional[str] = None
    feedback_history: List[CampaignFeedback] = field(default_factory=list)
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate campaign invariants"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValidationError("Campaign must have a name")
        if not self.theme:
            raise ValidationError("Campaign must have a theme")
        if self.expected_roi < 0:
            raise ValidationError("Expected ROI cannot be negative")
        if not self.ideas:
            raise ValidationError("Campaign must have at least one idea")
        if not self.channel_mix:
            raise ValidationError("Campaign must have at least one channel")
        
        total_allocation = sum(ch.budget_allocation for ch in self.channel_mix)
        if abs(total_allocation - 1.0) > 0.01:
            raise ValidationError(f"Channel budget allocations must sum to 1.0, got {total_allocation}")
    
    def activate(self):
        """Activate campaign - domain logic"""
        if self.status != CampaignStatus.DRAFT:
            raise ValidationError(f"Cannot activate campaign in {self.status} status")
        self.status = CampaignStatus.ACTIVE
    
    def pause(self):
        """Pause active campaign"""
        if self.status != CampaignStatus.ACTIVE:
            raise ValidationError(f"Cannot pause campaign in {self.status} status")
        self.status = CampaignStatus.PAUSED
    
    def complete(self):
        """Mark campaign as completed"""
        if self.status not in [CampaignStatus.ACTIVE, CampaignStatus.PAUSED]:
            raise ValidationError(f"Cannot complete campaign in {self.status} status")
        self.status = CampaignStatus.COMPLETED
    
    def cancel(self):
        """Cancel campaign"""
        if self.status == CampaignStatus.COMPLETED:
            raise ValidationError("Cannot cancel completed campaign")
        self.status = CampaignStatus.CANCELLED
    
    def update_metrics(self, metrics: CampaignMetrics):
        """Update campaign metrics"""
        self.metrics = metrics
    
    def add_feedback(self, feedback: CampaignFeedback):
        """Add feedback to campaign"""
        self.feedback_history.append(feedback)
