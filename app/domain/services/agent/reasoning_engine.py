"""Autonomous agent reasoning engine for multi-step task planning and execution"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
from openai import OpenAI

from app.core.settings import settings
from app.infrastructure.observability.agent_logger import (
    get_agent_logger, AgentDecision, DecisionType, ReasoningStep
)
from app.infrastructure.rag.vector_store import get_vector_store
from app.infrastructure.rag.mock_crm_repository import get_crm_repository
from app.domain.entities.crm.customer import CustomerSegment, EngagementLevel


@dataclass
class ReasoningTask:
    """Represents a task for the agent to reason about"""
    task_id: str
    objective: str
    context: Dict[str, Any]
    constraints: List[str]
    expected_outcome: str


@dataclass
class AgentPlan:
    """Multi-step plan created by the agent"""
    plan_id: str
    objective: str
    steps: List[Dict[str, Any]]
    reasoning: str
    confidence: float
    estimated_duration_ms: float


class AgentReasoningEngine:
    """
    Autonomous reasoning engine for the GenAI agent
    
    This engine enables agentic behavior by:
    1. Analyzing objectives and creating multi-step plans
    2. Retrieving relevant data using RAG
    3. Making autonomous decisions with reasoning trails
    4. Adapting plans based on outcomes
    5. Learning from feedback
    """
    
    def __init__(self):
        self.logger = get_agent_logger()
        self.vector_store = get_vector_store()
        self.crm_repo = get_crm_repository()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    def create_campaign_plan(
        self,
        business_objective: str,
        target_audience: Optional[str] = None,
        budget_constraint: Optional[float] = None,
        timeline: Optional[str] = None
    ) -> AgentPlan:
        """
        Create an autonomous multi-step plan for campaign generation
        
        This is the core agentic behavior - the agent reasons about the
        objective and creates a plan without explicit instructions.
        """
        trace_id = f"plan_{uuid.uuid4().hex[:8]}"
        trace = self.logger.start_execution_trace(trace_id)
        
        reasoning_chain = []
        
        # Step 1: Analyze objective
        analysis_reasoning = self._analyze_objective(business_objective)
        reasoning_chain.append(f"Objective Analysis: {analysis_reasoning}")
        trace.add_step("analyze_objective", ReasoningStep.ANALYSIS, 50.0)
        
        # Step 2: Retrieve relevant customer data using RAG
        relevant_customers = self._retrieve_relevant_customers(
            business_objective,
            target_audience
        )
        reasoning_chain.append(
            f"Retrieved {len(relevant_customers)} relevant customers from CRM using RAG. "
            f"Segments: {', '.join(set(c.segment.value for c in relevant_customers))}"
        )
        trace.add_step("retrieve_customers", ReasoningStep.DATA_RETRIEVAL, 150.0)
        
        # Step 3: Determine target segments based on data
        target_segments = self._determine_target_segments(relevant_customers)
        reasoning_chain.append(
            f"Target Segments Identified: {', '.join(s.value for s in target_segments)} "
            f"based on ICP scores and engagement levels"
        )
        trace.add_step("determine_segments", ReasoningStep.ANALYSIS, 75.0)
        
        # Step 4: Create multi-step execution plan
        steps = self._create_execution_steps(
            business_objective,
            target_segments,
            relevant_customers,
            budget_constraint,
            timeline
        )
        reasoning_chain.append(f"Created {len(steps)}-step execution plan")
        trace.add_step("create_plan", ReasoningStep.PLANNING, 100.0)
        
        # Step 5: Calculate confidence
        confidence = self._calculate_plan_confidence(
            relevant_customers,
            target_segments,
            budget_constraint
        )
        reasoning_chain.append(f"Plan confidence: {confidence:.2%}")
        
        self.logger.end_execution_trace(trace_id, success=True)
        
        # Log the decision
        decision = AgentDecision(
            decision_id=f"decision_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            decision_type=DecisionType.CAMPAIGN_GENERATION,
            reasoning_chain=reasoning_chain,
            data_sources=["CRM", "Vector Store", "Business Rules"],
            confidence_score=confidence,
            metadata={
                "objective": business_objective,
                "target_segments": [s.value for s in target_segments],
                "customer_count": len(relevant_customers)
            }
        )
        self.logger.log_decision(decision)
        
        return AgentPlan(
            plan_id=trace_id,
            objective=business_objective,
            steps=steps,
            reasoning="\n".join(reasoning_chain),
            confidence=confidence,
            estimated_duration_ms=sum(s.get("estimated_duration_ms", 0) for s in steps)
        )
    
    def _analyze_objective(self, objective: str) -> str:
        """Analyze business objective to understand intent"""
        keywords = objective.lower()
        
        analysis_parts = []
        
        if any(word in keywords for word in ["increase", "grow", "boost", "expand"]):
            analysis_parts.append("Growth-focused objective")
        if any(word in keywords for word in ["engagement", "retention", "loyalty"]):
            analysis_parts.append("Engagement/retention goal")
        if any(word in keywords for word in ["awareness", "brand", "visibility"]):
            analysis_parts.append("Brand awareness initiative")
        if any(word in keywords for word in ["revenue", "sales", "conversion"]):
            analysis_parts.append("Revenue-driven campaign")
        
        return "; ".join(analysis_parts) if analysis_parts else "General marketing objective"
    
    def _retrieve_relevant_customers(
        self,
        objective: str,
        target_audience: Optional[str] = None
    ) -> List:
        """Use RAG to retrieve customers relevant to the campaign objective"""
        query = f"{objective}"
        if target_audience:
            query += f" targeting {target_audience}"
        
        # Use RAG to find relevant customers
        relevant_customers = self.crm_repo.search_customers_for_campaign(
            campaign_theme=query,
            top_k=10
        )
        
        self.logger.log_reasoning_step(
            trace_id="current",
            step_name="customer_retrieval",
            reasoning=f"Using RAG to find customers matching: '{query}'",
            data_used=["Vector Store", "CRM Data"]
        )
        
        return relevant_customers
    
    def _determine_target_segments(self, customers: List) -> List[CustomerSegment]:
        """Autonomously determine which customer segments to target"""
        if not customers:
            return [CustomerSegment.ENTERPRISE, CustomerSegment.MID_MARKET]
        
        segment_scores = {}
        for customer in customers:
            segment = customer.segment
            icp_score = customer.get_icp_match_score()
            engagement_bonus = 20 if customer.engagement_level == EngagementLevel.HIGH else 10
            
            score = icp_score + engagement_bonus
            segment_scores[segment] = segment_scores.get(segment, 0) + score
        
        # Sort segments by score and take top 2-3
        sorted_segments = sorted(
            segment_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [seg for seg, _ in sorted_segments[:3]]
    
    def _create_execution_steps(
        self,
        objective: str,
        target_segments: List[CustomerSegment],
        customers: List,
        budget: Optional[float],
        timeline: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Create multi-step execution plan"""
        steps = []
        
        # Step 1: Data enrichment
        steps.append({
            "step_number": 1,
            "action": "enrich_customer_data",
            "description": f"Enrich CRM data for {len(customers)} target customers",
            "reasoning": "Ensure we have complete customer profiles for personalization",
            "estimated_duration_ms": 500.0,
            "dependencies": []
        })
        
        # Step 2: Segment analysis
        steps.append({
            "step_number": 2,
            "action": "analyze_segments",
            "description": f"Deep analysis of {len(target_segments)} target segments",
            "reasoning": "Understand segment-specific pain points and preferences",
            "estimated_duration_ms": 300.0,
            "dependencies": [1]
        })
        
        # Step 3: Content generation
        steps.append({
            "step_number": 3,
            "action": "generate_campaign_content",
            "description": "Generate personalized campaign ideas and messaging",
            "reasoning": "Create resonant content using RAG-enhanced LLM generation",
            "estimated_duration_ms": 2000.0,
            "dependencies": [2]
        })
        
        # Step 4: Channel selection
        steps.append({
            "step_number": 4,
            "action": "optimize_channel_mix",
            "description": "Determine optimal channel strategy",
            "reasoning": f"Select channels based on customer engagement history",
            "estimated_duration_ms": 400.0,
            "dependencies": [2]
        })
        
        # Step 5: Budget allocation (if budget provided)
        if budget:
            steps.append({
                "step_number": 5,
                "action": "allocate_budget",
                "description": f"Optimize ${budget:,.2f} budget allocation",
                "reasoning": "Distribute budget across channels for maximum ROI",
                "estimated_duration_ms": 300.0,
                "dependencies": [4]
            })
        
        # Step 6: Campaign assembly
        steps.append({
            "step_number": 6,
            "action": "assemble_campaign",
            "description": "Assemble final campaign with all components",
            "reasoning": "Combine all elements into cohesive campaign",
            "estimated_duration_ms": 200.0,
            "dependencies": [3, 4]
        })
        
        return steps
    
    def _calculate_plan_confidence(
        self,
        customers: List,
        segments: List[CustomerSegment],
        budget: Optional[float]
    ) -> float:
        """Calculate confidence score for the plan"""
        confidence = 0.5  # Base confidence
        
        # More customers = higher confidence
        if len(customers) >= 5:
            confidence += 0.2
        elif len(customers) >= 3:
            confidence += 0.1
        
        # More targeted segments = higher confidence
        if len(segments) <= 2:
            confidence += 0.15
        
        # Budget provided = higher confidence
        if budget and budget > 0:
            confidence += 0.15
        
        return min(confidence, 1.0)
    
    def evaluate_campaign_outcome(
        self,
        campaign_id: str,
        actual_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate campaign outcome and learn from results
        
        This enables closed-loop learning for the agent.
        """
        trace_id = f"eval_{uuid.uuid4().hex[:8]}"
        trace = self.logger.start_execution_trace(trace_id)
        
        evaluation = {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": actual_metrics,
            "learnings": []
        }
        
        # Analyze engagement rate
        if "engagement_rate" in actual_metrics:
            eng_rate = actual_metrics["engagement_rate"]
            if eng_rate > 0.15:
                evaluation["learnings"].append(
                    "High engagement achieved - campaign resonated well with target audience"
                )
            elif eng_rate < 0.05:
                evaluation["learnings"].append(
                    "Low engagement - consider revising messaging or targeting"
                )
        
        # Analyze conversion rate
        if "conversion_rate" in actual_metrics:
            conv_rate = actual_metrics["conversion_rate"]
            if conv_rate > 0.05:
                evaluation["learnings"].append(
                    "Strong conversion performance - channel mix was effective"
                )
            elif conv_rate < 0.01:
                evaluation["learnings"].append(
                    "Weak conversions - optimize channel strategy or call-to-action"
                )
        
        # Log the evaluation
        decision = AgentDecision(
            decision_id=f"eval_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            decision_type=DecisionType.CONTENT_OPTIMIZATION,
            reasoning_chain=evaluation["learnings"],
            data_sources=["Campaign Metrics", "Historical Data"],
            confidence_score=0.8,
            outcome="evaluation_complete",
            metadata=actual_metrics
        )
        self.logger.log_decision(decision)
        
        self.logger.end_execution_trace(trace_id, success=True)
        
        return evaluation


# Global singleton instance
_reasoning_engine = AgentReasoningEngine()


def get_reasoning_engine() -> AgentReasoningEngine:
    """Get the global reasoning engine instance"""
    return _reasoning_engine
