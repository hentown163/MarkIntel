from typing import List, Dict, Any
from unittest.mock import AsyncMock, MagicMock


class MockOpenAIAdapter:
    def __init__(self):
        self.generate_campaign_ideas_called = False
        self.generate_channel_strategies_called = False
        self.analyze_market_signals_called = False
        
    async def generate_campaign_ideas(
        self,
        service_name: str,
        service_description: str,
        market_signals: List[Dict[str, Any]],
        crm_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        self.generate_campaign_ideas_called = True
        return {
            "campaigns": [
                {
                    "title": f"AI Generated Campaign for {service_name}",
                    "description": "Test campaign description",
                    "target_audience": "Tech professionals",
                    "key_messages": ["Innovation", "Efficiency"],
                    "channels": ["email", "social"],
                    "budget_recommendation": 5000.0
                }
            ],
            "rationale": "Based on market analysis"
        }
    
    async def generate_channel_strategies(
        self,
        campaign_title: str,
        campaign_description: str,
        channels: List[str],
        budget: float
    ) -> List[Dict[str, Any]]:
        self.generate_channel_strategies_called = True
        return [
            {
                "channel": channel,
                "tactics": [f"Tactic 1 for {channel}", f"Tactic 2 for {channel}"],
                "budget_allocation": budget / len(channels),
                "expected_reach": 5000,
                "kpis": ["Engagement", "Conversion"]
            }
            for channel in channels
        ]
    
    async def analyze_market_signals(
        self,
        signals: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        self.analyze_market_signals_called = True
        return {
            "summary": "Market analysis summary",
            "opportunities": ["Opportunity 1", "Opportunity 2"],
            "threats": ["Threat 1"],
            "recommendations": ["Recommendation 1", "Recommendation 2"]
        }


class MockOpenAIError:
    @staticmethod
    async def generate_campaign_ideas(*args, **kwargs):
        raise Exception("OpenAI API Error: Rate limit exceeded")
    
    @staticmethod
    async def generate_channel_strategies(*args, **kwargs):
        raise Exception("OpenAI API Error: Service unavailable")
    
    @staticmethod
    async def analyze_market_signals(*args, **kwargs):
        raise Exception("OpenAI API Error: Invalid request")


def create_mock_openai_adapter():
    return MockOpenAIAdapter()


def create_mock_openai_error_adapter():
    return MockOpenAIError()
