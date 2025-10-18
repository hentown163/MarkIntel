"""Mock CRM data repository - simulates enterprise CRM data"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
from app.domain.entities.crm.customer import (
    Customer, CustomerSegment, EngagementLevel
)
from app.infrastructure.rag.vector_store import get_vector_store


class MockCRMRepository:
    """
    Mock CRM repository that simulates real enterprise customer data
    
    This will be replaced with actual CRM integration (HubSpot, Salesforce)
    but provides realistic data for RAG and agent development.
    """
    
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self._initialize_mock_data()
        self._index_in_vector_store()
    
    def _initialize_mock_data(self):
        """Initialize mock customer data representing various segments and engagement levels"""
        
        # Enterprise customers
        self.customers["cust_001"] = Customer(
            id="cust_001",
            name="Sarah Chen",
            email="sarah.chen@techcorp.com",
            company_id="comp_001",
            company_name="TechCorp Industries",
            segment=CustomerSegment.ENTERPRISE,
            engagement_level=EngagementLevel.HIGH,
            lifetime_value=250000.0,
            last_engagement_date=datetime.now() - timedelta(days=2),
            last_engagement_channel="Email",
            industry="Technology",
            company_size=5000,
            deal_stage="Negotiation",
            pain_points=["Scaling infrastructure", "Cloud migration", "Security compliance"],
            interests=["AI/ML platforms", "DevOps automation", "Enterprise security"],
            campaign_history=["Q1 2025 Cloud Migration", "AI Innovation Summit"]
        )
        
        self.customers["cust_002"] = Customer(
            id="cust_002",
            name="Michael Rodriguez",
            email="m.rodriguez@globalfinance.com",
            company_id="comp_002",
            company_name="Global Finance Corp",
            segment=CustomerSegment.ENTERPRISE,
            engagement_level=EngagementLevel.MEDIUM,
            lifetime_value=180000.0,
            last_engagement_date=datetime.now() - timedelta(days=15),
            last_engagement_channel="Webinar",
            industry="Financial Services",
            company_size=8000,
            deal_stage="Evaluation",
            pain_points=["Regulatory compliance", "Data analytics", "Risk management"],
            interests=["FinTech solutions", "Compliance automation", "Data governance"],
            campaign_history=["Financial Compliance Webinar 2024"]
        )
        
        # Mid-market customers
        self.customers["cust_003"] = Customer(
            id="cust_003",
            name="Emma Thompson",
            email="emma.t@healthtech.io",
            company_id="comp_003",
            company_name="HealthTech Solutions",
            segment=CustomerSegment.MID_MARKET,
            engagement_level=EngagementLevel.HIGH,
            lifetime_value=75000.0,
            last_engagement_date=datetime.now() - timedelta(days=5),
            last_engagement_channel="Product Demo",
            industry="Healthcare",
            company_size=500,
            deal_stage="Proposal",
            pain_points=["Patient data management", "HIPAA compliance", "Integration with legacy systems"],
            interests=["Healthcare AI", "Telemedicine", "Patient engagement"],
            campaign_history=["Healthcare Innovation Q4 2024", "HIPAA Compliance Guide"]
        )
        
        self.customers["cust_004"] = Customer(
            id="cust_004",
            name="James Park",
            email="jpark@retailpro.com",
            company_id="comp_004",
            company_name="RetailPro Systems",
            segment=CustomerSegment.MID_MARKET,
            engagement_level=EngagementLevel.LOW,
            lifetime_value=45000.0,
            last_engagement_date=datetime.now() - timedelta(days=45),
            last_engagement_channel="Newsletter",
            industry="Retail",
            company_size=300,
            deal_stage="Prospect",
            pain_points=["Inventory management", "Omnichannel experience", "Supply chain visibility"],
            interests=["E-commerce platforms", "Inventory optimization", "Customer analytics"],
            campaign_history=["Retail Trends Newsletter"]
        )
        
        # SMB customers
        self.customers["cust_005"] = Customer(
            id="cust_005",
            name="Lisa Wang",
            email="lisa@designstudio.co",
            company_id="comp_005",
            company_name="Creative Design Studio",
            segment=CustomerSegment.SMB,
            engagement_level=EngagementLevel.MEDIUM,
            lifetime_value=15000.0,
            last_engagement_date=datetime.now() - timedelta(days=10),
            last_engagement_channel="Chat",
            industry="Professional Services",
            company_size=25,
            deal_stage="Active Customer",
            pain_points=["Client collaboration", "Project management", "Time tracking"],
            interests=["Collaboration tools", "Design workflows", "Client portals"],
            campaign_history=["SMB Productivity Guide", "Design Tools Comparison"]
        )
        
        # Startups
        self.customers["cust_006"] = Customer(
            id="cust_006",
            name="Alex Kumar",
            email="alex@aistartup.ai",
            company_id="comp_006",
            company_name="AI Startup Inc",
            segment=CustomerSegment.STARTUP,
            engagement_level=EngagementLevel.HIGH,
            lifetime_value=8000.0,
            last_engagement_date=datetime.now() - timedelta(days=1),
            last_engagement_channel="Slack",
            industry="Technology",
            company_size=12,
            deal_stage="Trial",
            pain_points=["Rapid scaling", "Cost optimization", "MVP development"],
            interests=["Startup tools", "ML infrastructure", "Growth hacking"],
            campaign_history=["Startup Accelerator Program", "AI Tools for Startups"]
        )
        
        # Dormant customer
        self.customers["cust_007"] = Customer(
            id="cust_007",
            name="Robert Kim",
            email="rkim@legacy-corp.com",
            company_id="comp_007",
            company_name="Legacy Manufacturing",
            segment=CustomerSegment.MID_MARKET,
            engagement_level=EngagementLevel.DORMANT,
            lifetime_value=90000.0,
            last_engagement_date=datetime.now() - timedelta(days=180),
            last_engagement_channel="Email",
            industry="Manufacturing",
            company_size=600,
            deal_stage="Inactive",
            pain_points=["Digital transformation", "Legacy system modernization", "Workforce training"],
            interests=["Industry 4.0", "IoT sensors", "Predictive maintenance"],
            campaign_history=["Manufacturing Digital Summit 2024"]
        )
    
    def _index_in_vector_store(self):
        """Index all customers in the vector store for RAG retrieval"""
        vector_store = get_vector_store()
        
        for customer in self.customers.values():
            vector_store.add_document(
                doc_id=f"customer_{customer.id}",
                content=customer.to_context_string(),
                metadata={
                    "type": "customer",
                    "customer_id": customer.id,
                    "segment": customer.segment.value,
                    "engagement_level": customer.engagement_level.value,
                    "industry": customer.industry,
                    "icp_score": customer.get_icp_match_score()
                }
            )
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return list(self.customers.values())
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a specific customer by ID"""
        return self.customers.get(customer_id)
    
    def get_customers_by_segment(self, segment: CustomerSegment) -> List[Customer]:
        """Get customers filtered by segment"""
        return [c for c in self.customers.values() if c.segment == segment]
    
    def get_high_value_customers(self, min_ltv: float = 50000.0) -> List[Customer]:
        """Get high-value customers based on LTV"""
        return [c for c in self.customers.values() if c.lifetime_value >= min_ltv]
    
    def get_engaged_customers(self) -> List[Customer]:
        """Get currently engaged customers (high/medium engagement)"""
        return [
            c for c in self.customers.values()
            if c.engagement_level in [EngagementLevel.HIGH, EngagementLevel.MEDIUM]
        ]
    
    def search_customers_for_campaign(
        self,
        campaign_theme: str,
        target_segment: Optional[CustomerSegment] = None,
        min_engagement: Optional[EngagementLevel] = None,
        top_k: int = 5
    ) -> List[Customer]:
        """
        Search for customers relevant to a campaign using RAG
        
        This uses vector similarity to find customers whose profile,
        pain points, and interests match the campaign theme.
        """
        vector_store = get_vector_store()
        
        # Build metadata filter
        metadata_filter = {"type": "customer"}
        if target_segment:
            metadata_filter["segment"] = target_segment.value
        
        # Retrieve similar customers
        docs = vector_store.retrieve(
            query=campaign_theme,
            top_k=top_k,
            filter_metadata=metadata_filter
        )
        
        # Convert back to Customer objects and filter by engagement if needed
        customers = []
        for doc in docs:
            customer_id = doc.metadata.get("customer_id")
            customer = self.get_customer(customer_id)
            if customer:
                if min_engagement:
                    engagement_order = {
                        EngagementLevel.HIGH: 3,
                        EngagementLevel.MEDIUM: 2,
                        EngagementLevel.LOW: 1,
                        EngagementLevel.DORMANT: 0
                    }
                    if engagement_order[customer.engagement_level] >= engagement_order[min_engagement]:
                        customers.append(customer)
                else:
                    customers.append(customer)
        
        return customers
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the CRM data"""
        total = len(self.customers)
        return {
            "total_customers": total,
            "by_segment": {
                segment.value: len([c for c in self.customers.values() if c.segment == segment])
                for segment in CustomerSegment
            },
            "by_engagement": {
                level.value: len([c for c in self.customers.values() if c.engagement_level == level])
                for level in EngagementLevel
            },
            "total_ltv": sum(c.lifetime_value for c in self.customers.values()),
            "avg_ltv": sum(c.lifetime_value for c in self.customers.values()) / total if total > 0 else 0
        }


# Global singleton instance
_crm_repo = MockCRMRepository()


def get_crm_repository() -> MockCRMRepository:
    """Get the global CRM repository instance"""
    return _crm_repo
