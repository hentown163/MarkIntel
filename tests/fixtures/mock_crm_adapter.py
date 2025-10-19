from typing import List, Dict, Any, Optional
from datetime import datetime


class MockCRMAdapter:
    def __init__(self):
        self.customers = [
            {
                "id": "cust_001",
                "name": "Acme Corp",
                "email": "contact@acme.com",
                "industry": "Technology",
                "size": "Enterprise",
                "lifetime_value": 50000.0,
                "engagement_score": 0.85,
                "last_interaction": datetime.now().isoformat()
            },
            {
                "id": "cust_002",
                "name": "TechStart Inc",
                "email": "hello@techstart.com",
                "industry": "Software",
                "size": "Startup",
                "lifetime_value": 10000.0,
                "engagement_score": 0.72,
                "last_interaction": datetime.now().isoformat()
            }
        ]
        self.get_customers_called = False
        self.get_customer_by_id_called = False
        
    async def get_customers(
        self,
        limit: int = 100,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        self.get_customers_called = True
        filtered = self.customers
        
        if filters:
            if "industry" in filters:
                filtered = [c for c in filtered if c["industry"] == filters["industry"]]
            if "min_value" in filters:
                filtered = [c for c in filtered if c["lifetime_value"] >= filters["min_value"]]
        
        return filtered[offset:offset + limit]
    
    async def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        self.get_customer_by_id_called = True
        for customer in self.customers:
            if customer["id"] == customer_id:
                return customer
        return None
    
    async def get_customer_insights(
        self,
        customer_ids: List[str]
    ) -> Dict[str, Any]:
        customers = [c for c in self.customers if c["id"] in customer_ids]
        return {
            "total_customers": len(customers),
            "total_value": sum(c["lifetime_value"] for c in customers),
            "avg_engagement": sum(c["engagement_score"] for c in customers) / len(customers) if customers else 0,
            "industries": list(set(c["industry"] for c in customers)),
            "segments": {
                "enterprise": len([c for c in customers if c["size"] == "Enterprise"]),
                "startup": len([c for c in customers if c["size"] == "Startup"])
            }
        }


class MockCRMError:
    @staticmethod
    async def get_customers(*args, **kwargs):
        raise Exception("CRM API Error: Authentication failed")
    
    @staticmethod
    async def get_customer_by_id(*args, **kwargs):
        raise Exception("CRM API Error: Service unavailable")
    
    @staticmethod
    async def get_customer_insights(*args, **kwargs):
        raise Exception("CRM API Error: Rate limit exceeded")


def create_mock_crm_adapter():
    return MockCRMAdapter()


def create_mock_crm_error_adapter():
    return MockCRMError()
