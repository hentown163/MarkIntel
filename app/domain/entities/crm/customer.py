"""CRM Customer entity - represents a customer/contact in the CRM system"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum


class CustomerSegment(str, Enum):
    """Customer segmentation categories"""
    ENTERPRISE = "enterprise"
    MID_MARKET = "mid_market"
    SMB = "smb"
    STARTUP = "startup"


class EngagementLevel(str, Enum):
    """Customer engagement levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DORMANT = "dormant"


@dataclass
class Customer:
    """
    Domain entity representing a customer from CRM
    
    This entity stores enriched customer data that will be used
    for RAG-powered campaign generation and agent reasoning.
    """
    id: str
    name: str
    email: str
    company_id: str
    company_name: str
    segment: CustomerSegment
    engagement_level: EngagementLevel
    lifetime_value: float
    last_engagement_date: Optional[datetime]
    last_engagement_channel: Optional[str]
    industry: str
    company_size: int
    deal_stage: Optional[str]
    pain_points: List[str]
    interests: List[str]
    campaign_history: List[str]
    
    def get_icp_match_score(self) -> float:
        """
        Calculate Ideal Customer Profile (ICP) match score
        
        This score helps the agent prioritize high-value customers
        for campaign targeting.
        """
        score = 0.0
        
        # Segment weight
        if self.segment == CustomerSegment.ENTERPRISE:
            score += 40
        elif self.segment == CustomerSegment.MID_MARKET:
            score += 30
        elif self.segment == CustomerSegment.SMB:
            score += 20
        else:
            score += 10
            
        # Engagement weight
        if self.engagement_level == EngagementLevel.HIGH:
            score += 30
        elif self.engagement_level == EngagementLevel.MEDIUM:
            score += 20
        elif self.engagement_level == EngagementLevel.LOW:
            score += 10
            
        # LTV weight
        if self.lifetime_value > 100000:
            score += 30
        elif self.lifetime_value > 50000:
            score += 20
        elif self.lifetime_value > 10000:
            score += 10
            
        return min(score, 100.0)
    
    def to_context_string(self) -> str:
        """
        Convert customer data to context string for RAG retrieval
        
        This creates a rich text representation that can be embedded
        and retrieved for campaign generation.
        """
        return f"""
        Customer: {self.name} ({self.email})
        Company: {self.company_name} | Industry: {self.industry} | Size: {self.company_size} employees
        Segment: {self.segment.value} | Engagement: {self.engagement_level.value}
        Lifetime Value: ${self.lifetime_value:,.2f}
        ICP Match Score: {self.get_icp_match_score()}/100
        Last Engagement: {self.last_engagement_channel} on {self.last_engagement_date}
        Deal Stage: {self.deal_stage or 'Not in pipeline'}
        Pain Points: {', '.join(self.pain_points)}
        Interests: {', '.join(self.interests)}
        Campaign History: {', '.join(self.campaign_history) if self.campaign_history else 'No previous campaigns'}
        """
