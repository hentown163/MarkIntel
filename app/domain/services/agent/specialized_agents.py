"""Specialized AI agents for multi-agent coordination"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
from enum import Enum
from openai import OpenAI

from app.core.settings import settings
from app.infrastructure.persistence.repositories.agent_memory_repository import AgentMemoryRepository


class AgentRole(Enum):
    """Different agent roles in the multi-agent system"""
    RESEARCH = "research"
    STRATEGY = "strategy"
    EXECUTION = "execution"
    EVALUATION = "evaluation"
    COORDINATOR = "coordinator"


@dataclass
class AgentMessage:
    """Message passed between agents"""
    from_agent: str
    to_agent: str
    message_type: str  # request, response, notification, question
    content: Dict[str, Any]
    timestamp: datetime
    priority: int = 1  # 1-5, 5 is highest


class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, agent_id: str, role: AgentRole, repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None):
        self.agent_id = agent_id
        self.role = role
        self.repository = repository
        self.session_id = session_id or f"session_{uuid.uuid4().hex[:12]}"
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.memory: List[Dict] = []
        self.learnings: List[Dict] = []
        
        if self.repository:
            self._load_historical_learnings()
    
    def _load_historical_learnings(self):
        """Load historical learnings from database"""
        if not self.repository:
            return
        
        db_learnings = self.repository.retrieve_learnings(
            agent_id=self.agent_id,
            min_confidence=0.6,
            status='active',
            limit=20
        )
        
        for learning in db_learnings:
            self.learnings.append({
                "learning_id": learning.learning_id,
                "category": learning.learning_category,
                "finding": learning.finding,
                "confidence": learning.confidence,
                "applied_count": learning.applied_count
            })
    
    def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Receive and process a message from another agent"""
        raise NotImplementedError
    
    def add_to_memory(self, content: str, importance: float = 0.5, memory_type: str = "observation"):
        """Add something to the agent's memory (persisted to database)"""
        memory_data = {
            "content": content,
            "timestamp": datetime.now(),
            "importance": importance,
            "memory_type": memory_type
        }
        
        self.memory.append(memory_data)
        if len(self.memory) > 50:
            self.memory = self.memory[-50:]
        
        if self.repository:
            self.repository.store_memory(
                agent_id=self.agent_id,
                memory_type=memory_type,
                content=content,
                importance_score=importance,
                session_id=self.session_id
            )
    
    def store_learning(self, learning_category: str, finding: str, evidence: Dict, confidence: float = 0.7):
        """Store a learning to database"""
        learning_data = {
            "category": learning_category,
            "finding": finding,
            "evidence": evidence,
            "confidence": confidence,
            "timestamp": datetime.now()
        }
        self.learnings.append(learning_data)
        
        if self.repository:
            learning_orm = self.repository.store_learning(
                agent_id=self.agent_id,
                source_type="agent_evaluation",
                learning_category=learning_category,
                finding=finding,
                evidence=evidence,
                confidence=confidence
            )
            learning_data["learning_id"] = learning_orm.learning_id


class ResearchAgent(BaseAgent):
    """
    Research Agent - gathers intelligence and data
    
    Responsibilities:
    - Market research and competitive analysis
    - Customer data gathering and analysis
    - Trend identification
    - Data validation
    """
    
    def __init__(self, repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None):
        super().__init__(agent_id="research_agent", role=AgentRole.RESEARCH, repository=repository, session_id=session_id)
    
    def research_market_trends(self, topic: str, market_signals: List[Dict]) -> Dict[str, Any]:
        """Research market trends for a given topic"""
        self.add_to_memory(f"Researching market trends for: {topic}", importance=0.7)
        
        # Analyze market signals
        relevant_signals = [
            signal for signal in market_signals
            if any(keyword in signal.get('title', '').lower() or 
                   keyword in signal.get('description', '').lower() 
                   for keyword in topic.lower().split())
        ]
        
        trends = {
            "topic": topic,
            "signals_analyzed": len(market_signals),
            "relevant_signals": len(relevant_signals),
            "trends_identified": [],
            "confidence": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        if relevant_signals:
            # Extract trend patterns
            impact_scores = [s.get('impact_score', 'medium') for s in relevant_signals]
            high_impact = impact_scores.count('high')
            
            if high_impact >= 2:
                trends["trends_identified"].append({
                    "trend": f"High market activity in {topic}",
                    "evidence": f"{high_impact} high-impact signals detected",
                    "confidence": 0.8
                })
                trends["confidence"] = 0.8
            elif relevant_signals:
                trends["trends_identified"].append({
                    "trend": f"Emerging interest in {topic}",
                    "evidence": f"{len(relevant_signals)} relevant market signals",
                    "confidence": 0.6
                })
                trends["confidence"] = 0.6
        
        self.add_to_memory(f"Identified {len(trends['trends_identified'])} trends", importance=0.8)
        return trends
    
    def research_customer_segment(self, segment: str, customers: List[Dict]) -> Dict[str, Any]:
        """Deep dive research on a customer segment"""
        self.add_to_memory(f"Researching customer segment: {segment}", importance=0.7)
        
        segment_customers = [c for c in customers if c.get('segment') == segment]
        
        analysis = {
            "segment": segment,
            "total_customers": len(segment_customers),
            "characteristics": [],
            "opportunities": [],
            "challenges": [],
            "recommendation": ""
        }
        
        if segment_customers:
            # Analyze engagement levels
            high_engagement = sum(1 for c in segment_customers 
                                 if c.get('engagement_level') == 'high')
            engagement_rate = high_engagement / len(segment_customers)
            
            analysis["characteristics"].append(
                f"Engagement rate: {engagement_rate:.1%}"
            )
            
            # Analyze revenue potential
            avg_revenue = sum(c.get('annual_revenue', 0) for c in segment_customers) / len(segment_customers)
            analysis["characteristics"].append(
                f"Average annual revenue: ${avg_revenue:,.0f}"
            )
            
            if engagement_rate > 0.5:
                analysis["opportunities"].append("High engagement segment - ready for upsell campaigns")
            else:
                analysis["challenges"].append("Low engagement - need re-engagement strategies")
            
            analysis["recommendation"] = self._generate_segment_recommendation(
                segment, engagement_rate, avg_revenue
            )
        
        return analysis
    
    def _generate_segment_recommendation(self, segment: str, engagement: float, revenue: float) -> str:
        """Generate strategic recommendation for a segment"""
        if engagement > 0.6 and revenue > 500000:
            return f"Prime target: {segment} shows high engagement and revenue potential"
        elif engagement > 0.4:
            return f"Opportunity: {segment} is moderately engaged, focus on value demonstration"
        else:
            return f"Challenge: {segment} needs re-engagement before campaign targeting"
    
    def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process research requests from other agents"""
        if message.message_type == "request":
            request_type = message.content.get("type")
            
            if request_type == "market_research":
                result = self.research_market_trends(
                    message.content.get("topic", ""),
                    message.content.get("market_signals", [])
                )
                return AgentMessage(
                    from_agent=self.agent_id,
                    to_agent=message.from_agent,
                    message_type="response",
                    content={"result": result},
                    timestamp=datetime.now()
                )
            elif request_type == "segment_research":
                result = self.research_customer_segment(
                    message.content.get("segment", ""),
                    message.content.get("customers", [])
                )
                return AgentMessage(
                    from_agent=self.agent_id,
                    to_agent=message.from_agent,
                    message_type="response",
                    content={"result": result},
                    timestamp=datetime.now()
                )
        
        return None


class StrategyAgent(BaseAgent):
    """
    Strategy Agent - creates strategic plans and recommendations
    
    Responsibilities:
    - Campaign strategy development
    - Channel selection and optimization
    - Budget allocation
    - Risk assessment
    """
    
    def __init__(self, repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None):
        super().__init__(agent_id="strategy_agent", role=AgentRole.STRATEGY, repository=repository, session_id=session_id)
    
    def develop_campaign_strategy(
        self,
        objective: str,
        research_findings: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Develop strategic campaign plan based on research"""
        self.add_to_memory(f"Developing strategy for: {objective}", importance=0.9)
        
        strategy = {
            "objective": objective,
            "strategic_approach": [],
            "channel_recommendations": [],
            "budget_allocation": {},
            "risk_factors": [],
            "success_criteria": [],
            "confidence": 0.0
        }
        
        # Analyze research findings
        trends = research_findings.get("trends_identified", [])
        
        if trends:
            high_conf_trends = [t for t in trends if t.get("confidence", 0) > 0.7]
            if high_conf_trends:
                strategy["strategic_approach"].append(
                    "Capitalize on high-confidence market trends"
                )
                strategy["confidence"] = 0.8
        
        # Channel selection based on objective
        objective_lower = objective.lower()
        if "awareness" in objective_lower or "brand" in objective_lower:
            strategy["channel_recommendations"] = [
                {"channel": "LinkedIn", "priority": "high", "rationale": "Professional visibility"},
                {"channel": "Webinars", "priority": "high", "rationale": "Thought leadership"},
                {"channel": "Content Marketing", "priority": "medium", "rationale": "SEO and reach"}
            ]
        elif "conversion" in objective_lower or "sales" in objective_lower:
            strategy["channel_recommendations"] = [
                {"channel": "Email", "priority": "high", "rationale": "Direct conversion path"},
                {"channel": "Retargeting", "priority": "high", "rationale": "Capture interested leads"},
                {"channel": "Demo Events", "priority": "medium", "rationale": "High-intent prospects"}
            ]
        else:
            strategy["channel_recommendations"] = [
                {"channel": "LinkedIn", "priority": "high", "rationale": "B2B reach"},
                {"channel": "Email", "priority": "medium", "rationale": "Direct communication"},
                {"channel": "Events", "priority": "medium", "rationale": "Relationship building"}
            ]
        
        # Budget allocation
        budget = constraints.get("budget", 100000)
        strategy["budget_allocation"] = self._allocate_budget(
            budget,
            strategy["channel_recommendations"]
        )
        
        # Risk assessment
        if not trends:
            strategy["risk_factors"].append("Limited market intelligence - monitor closely")
        if budget < 50000:
            strategy["risk_factors"].append("Limited budget may restrict channel diversity")
        
        # Success criteria
        strategy["success_criteria"] = [
            "Engagement rate > 5%",
            "Conversion rate > 2%",
            "ROI > 3x"
        ]
        
        return strategy
    
    def _allocate_budget(self, total_budget: float, channels: List[Dict]) -> Dict[str, float]:
        """Allocate budget across recommended channels"""
        allocation = {}
        
        high_priority = [c for c in channels if c.get("priority") == "high"]
        medium_priority = [c for c in channels if c.get("priority") == "medium"]
        
        # 60% to high priority, 40% to medium
        if high_priority:
            high_budget = total_budget * 0.6
            per_high = high_budget / len(high_priority)
            for channel in high_priority:
                allocation[channel["channel"]] = per_high
        
        if medium_priority:
            medium_budget = total_budget * 0.4
            per_medium = medium_budget / len(medium_priority)
            for channel in medium_priority:
                allocation[channel["channel"]] = per_medium
        
        return allocation
    
    def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process strategy requests from other agents"""
        if message.message_type == "request" and message.content.get("type") == "develop_strategy":
            result = self.develop_campaign_strategy(
                message.content.get("objective", ""),
                message.content.get("research_findings", {}),
                message.content.get("constraints", {})
            )
            return AgentMessage(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                message_type="response",
                content={"result": result},
                timestamp=datetime.now()
            )
        return None


class ExecutionAgent(BaseAgent):
    """
    Execution Agent - implements campaigns and strategies
    
    Responsibilities:
    - Campaign implementation
    - Content generation
    - Tactical execution
    - Progress tracking
    """
    
    def __init__(self, repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None):
        super().__init__(agent_id="execution_agent", role=AgentRole.EXECUTION, repository=repository, session_id=session_id)
    
    def execute_campaign_plan(
        self,
        strategy: Dict[str, Any],
        service_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the campaign based on strategy"""
        self.add_to_memory("Executing campaign plan", importance=0.9)
        
        execution_result = {
            "status": "executed",
            "campaign_elements": [],
            "timeline": [],
            "deliverables": [],
            "next_steps": []
        }
        
        # Generate campaign elements based on channels
        for channel_rec in strategy.get("channel_recommendations", []):
            channel = channel_rec["channel"]
            budget = strategy.get("budget_allocation", {}).get(channel, 0)
            
            element = {
                "channel": channel,
                "budget": budget,
                "tactics": self._get_channel_tactics(channel),
                "timeline_weeks": self._estimate_timeline(channel)
            }
            execution_result["campaign_elements"].append(element)
        
        # Create timeline
        total_weeks = max(
            (e.get("timeline_weeks", 4) for e in execution_result["campaign_elements"]),
            default=4
        )
        execution_result["timeline"] = [
            {"week": i+1, "activities": f"Week {i+1} execution"}
            for i in range(total_weeks)
        ]
        
        # Define deliverables
        execution_result["deliverables"] = [
            "Campaign creative assets",
            "Channel-specific content",
            "Performance dashboard",
            "Weekly status reports"
        ]
        
        # Next steps
        execution_result["next_steps"] = [
            "Monitor campaign performance daily",
            "Collect feedback and metrics",
            "Prepare for optimization cycle"
        ]
        
        return execution_result
    
    def _get_channel_tactics(self, channel: str) -> List[str]:
        """Get specific tactics for a channel"""
        tactics_map = {
            "LinkedIn": ["Sponsored posts", "InMail campaigns", "Company page updates"],
            "Email": ["Drip campaigns", "Newsletter series", "Personalized outreach"],
            "Webinars": ["Live events", "Q&A sessions", "Recorded replays"],
            "Events": ["Trade shows", "User conferences", "Networking sessions"],
            "Content Marketing": ["Blog posts", "Whitepapers", "Case studies"]
        }
        return tactics_map.get(channel, ["Standard campaign tactics"])
    
    def _estimate_timeline(self, channel: str) -> int:
        """Estimate timeline in weeks for channel setup"""
        timeline_map = {
            "LinkedIn": 2,
            "Email": 3,
            "Webinars": 4,
            "Events": 6,
            "Content Marketing": 4
        }
        return timeline_map.get(channel, 4)
    
    def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process execution requests from other agents"""
        if message.message_type == "request" and message.content.get("type") == "execute_campaign":
            result = self.execute_campaign_plan(
                message.content.get("strategy", {}),
                message.content.get("service_details", {})
            )
            return AgentMessage(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                message_type="response",
                content={"result": result},
                timestamp=datetime.now()
            )
        return None


class EvaluationAgent(BaseAgent):
    """
    Evaluation Agent - assesses outcomes and generates learnings
    
    Responsibilities:
    - Performance evaluation
    - Learning extraction
    - Improvement recommendations
    - Self-correction triggers
    """
    
    def __init__(self, repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None):
        super().__init__(agent_id="evaluation_agent", role=AgentRole.EVALUATION, repository=repository, session_id=session_id)
    
    def evaluate_campaign_performance(
        self,
        campaign_data: Dict[str, Any],
        actual_metrics: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate campaign and extract learnings"""
        self.add_to_memory("Evaluating campaign performance", importance=0.9)
        
        evaluation = {
            "overall_assessment": "",
            "performance_score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "learnings": [],
            "corrections_needed": [],
            "confidence": 0.8
        }
        
        # Evaluate against success criteria
        success_criteria = strategy.get("success_criteria", [])
        metrics_met = 0
        total_criteria = len(success_criteria)
        
        engagement_rate = actual_metrics.get("engagement_rate", 0)
        conversion_rate = actual_metrics.get("conversion_rate", 0)
        roi = actual_metrics.get("roi", 0)
        
        # Check engagement
        if engagement_rate > 0.05:
            metrics_met += 1
            evaluation["strengths"].append(
                f"Strong engagement: {engagement_rate:.1%} exceeded target"
            )
        else:
            evaluation["weaknesses"].append(
                f"Low engagement: {engagement_rate:.1%} below target"
            )
            evaluation["corrections_needed"].append({
                "area": "engagement",
                "issue": "Low engagement rate",
                "recommendation": "Revise messaging and targeting"
            })
        
        # Check conversion
        if conversion_rate > 0.02:
            metrics_met += 1
            evaluation["strengths"].append(
                f"Good conversion: {conversion_rate:.1%}"
            )
        elif conversion_rate < 0.01:
            evaluation["weaknesses"].append(
                f"Weak conversion: {conversion_rate:.1%}"
            )
            evaluation["corrections_needed"].append({
                "area": "conversion",
                "issue": "Low conversion rate",
                "recommendation": "Optimize call-to-action and landing pages"
            })
        
        # Check ROI
        if roi > 3.0:
            metrics_met += 1
            evaluation["strengths"].append(f"Excellent ROI: {roi:.1f}x")
        
        # Calculate performance score
        if total_criteria > 0:
            evaluation["performance_score"] = metrics_met / total_criteria
        else:
            evaluation["performance_score"] = 0.5
        
        # Generate learnings
        if engagement_rate > 0.1:
            learning = {
                "finding": "High engagement indicates strong product-market fit",
                "evidence": f"Engagement rate: {engagement_rate:.1%}",
                "confidence": 0.9,
                "category": "targeting"
            }
            evaluation["learnings"].append(learning)
            self.store_learning(
                learning_category="targeting",
                finding=learning["finding"],
                evidence={"engagement_rate": engagement_rate, "metrics": actual_metrics},
                confidence=0.9
            )
        
        if len(evaluation["corrections_needed"]) > 0:
            learning = {
                "finding": "Campaign requires optimization in multiple areas",
                "evidence": f"{len(evaluation['corrections_needed'])} areas identified",
                "confidence": 0.8,
                "category": "strategy"
            }
            evaluation["learnings"].append(learning)
            self.store_learning(
                learning_category="strategy",
                finding=learning["finding"],
                evidence={"corrections_needed": evaluation["corrections_needed"]},
                confidence=0.8
            )
        
        # Overall assessment
        if evaluation["performance_score"] >= 0.8:
            evaluation["overall_assessment"] = "Excellent performance - continue and scale"
        elif evaluation["performance_score"] >= 0.6:
            evaluation["overall_assessment"] = "Good performance with room for optimization"
        else:
            evaluation["overall_assessment"] = "Requires significant improvements"
        
        return evaluation
    
    def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process evaluation requests from other agents"""
        if message.message_type == "request" and message.content.get("type") == "evaluate_campaign":
            result = self.evaluate_campaign_performance(
                message.content.get("campaign_data", {}),
                message.content.get("actual_metrics", {}),
                message.content.get("strategy", {})
            )
            return AgentMessage(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                message_type="response",
                content={"result": result},
                timestamp=datetime.now()
            )
        return None


# Global agent instances
_research_agent = ResearchAgent()
_strategy_agent = StrategyAgent()
_execution_agent = ExecutionAgent()
_evaluation_agent = EvaluationAgent()


def get_research_agent(repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None) -> ResearchAgent:
    """Get a research agent instance (with optional repository for persistence)"""
    if repository:
        return ResearchAgent(repository=repository, session_id=session_id)
    return _research_agent


def get_strategy_agent(repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None) -> StrategyAgent:
    """Get a strategy agent instance (with optional repository for persistence)"""
    if repository:
        return StrategyAgent(repository=repository, session_id=session_id)
    return _strategy_agent


def get_execution_agent(repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None) -> ExecutionAgent:
    """Get an execution agent instance (with optional repository for persistence)"""
    if repository:
        return ExecutionAgent(repository=repository, session_id=session_id)
    return _execution_agent


def get_evaluation_agent(repository: Optional[AgentMemoryRepository] = None, session_id: Optional[str] = None) -> EvaluationAgent:
    """Get an evaluation agent instance (with optional repository for persistence)"""
    if repository:
        return EvaluationAgent(repository=repository, session_id=session_id)
    return _evaluation_agent
