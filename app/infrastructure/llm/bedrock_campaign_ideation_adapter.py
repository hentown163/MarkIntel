"""
Amazon Bedrock adapter for campaign ideation - implementing domain service port

This adapter uses AWS Bedrock's Converse API for model-agnostic LLM integration.
Supports multiple foundation models including Claude 3.5 Sonnet, Llama, and others.

Enterprise features:
- VPC endpoint support for private deployments
- AWS IAM-based authentication (no hardcoded keys)
- Comprehensive error handling and logging
- Cost optimization through model selection
- Compliance-ready (GDPR, HIPAA, SOC 2)
"""
import os
import json
import uuid
from typing import List, Dict, Any, Optional
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError

from app.domain.services.campaign_ideation_service import (
    CampaignIdeationService,
    CampaignGenerationRequest
)
from app.domain.entities.campaign import CampaignIdea, ChannelPlan
from app.domain.entities.service import Service
from app.domain.entities.market_signal import MarketSignal
from app.core.exceptions import ExternalServiceError


class BedrockCampaignIdeationAdapter(CampaignIdeationService):
    """
    Amazon Bedrock implementation of campaign ideation service
    
    Following SOLID Principles:
    - Single Responsibility: Handles only Bedrock LLM interactions
    - Open/Closed: Can be extended without modifying existing code
    - Liskov Substitution: Can replace OpenAI adapter without breaking system
    - Interface Segregation: Implements only required CampaignIdeationService methods
    - Dependency Inversion: Depends on CampaignIdeationService abstraction
    """
    
    # Supported Bedrock models with metadata
    SUPPORTED_MODELS = {
        "claude-3-5-sonnet": {
            "id": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "max_tokens": 8192,
            "description": "Best for complex reasoning, enterprise use cases"
        },
        "claude-3-sonnet": {
            "id": "anthropic.claude-3-sonnet-20240229-v1:0",
            "max_tokens": 4096,
            "description": "Balanced performance and cost"
        },
        "claude-3-haiku": {
            "id": "anthropic.claude-3-haiku-20240307-v1:0",
            "max_tokens": 4096,
            "description": "Fastest, most cost-effective"
        },
        "llama-3-2-90b": {
            "id": "meta.llama3-2-90b-instruct-v1:0",
            "max_tokens": 2048,
            "description": "Open-source alternative"
        }
    }
    
    def __init__(
        self,
        model_name: str = "claude-3-5-sonnet",
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        endpoint_url: Optional[str] = None
    ):
        """
        Initialize Bedrock adapter with AWS configuration
        
        Args:
            model_name: Model to use (default: claude-3-5-sonnet)
            region_name: AWS region (default: from env or us-east-1)
            aws_access_key_id: AWS access key (default: from env or IAM role)
            aws_secret_access_key: AWS secret key (default: from env or IAM role)
            endpoint_url: Custom endpoint URL for VPC endpoints
        """
        self.model_name = model_name
        
        # Validate model selection
        if model_name not in self.SUPPORTED_MODELS:
            print(f"WARNING: Model '{model_name}' not in supported list. Using default.")
            self.model_name = "claude-3-5-sonnet"
        
        self.model_config = self.SUPPORTED_MODELS[self.model_name]
        self.model_id = self.model_config["id"]
        
        # AWS Configuration with retry and timeout settings
        config = Config(
            region_name=region_name or os.getenv("AWS_REGION", "us-east-1"),
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            },
            connect_timeout=10,
            read_timeout=60
        )
        
        # Initialize Bedrock Runtime client
        try:
            client_kwargs = {
                'service_name': 'bedrock-runtime',
                'config': config
            }
            
            # Support for VPC endpoints
            if endpoint_url:
                client_kwargs['endpoint_url'] = endpoint_url
            
            # Support for explicit credentials (non-production) or IAM roles (production)
            if aws_access_key_id and aws_secret_access_key:
                client_kwargs['aws_access_key_id'] = aws_access_key_id
                client_kwargs['aws_secret_access_key'] = aws_secret_access_key
            
            self.client = boto3.client(**client_kwargs)
            print(f"✓ Bedrock adapter initialized with model: {self.model_name} ({self.model_id})")
            
        except Exception as e:
            print(f"WARNING: Failed to initialize Bedrock client: {str(e)}")
            print("Bedrock AI generation will not work. Please configure AWS credentials.")
            self.client = None
    
    def generate_ideas(
        self,
        service: Service,
        market_signals: List[MarketSignal],
        request: CampaignGenerationRequest
    ) -> List[CampaignIdea]:
        """
        Generate campaign ideas using Amazon Bedrock
        
        Uses Converse API for model-agnostic interaction
        """
        if not self.client:
            raise ExternalServiceError(
                "Bedrock client not initialized. Please configure AWS credentials "
                "(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)."
            )
        
        try:
            prompt = self._build_ideation_prompt(service, market_signals, request)
            
            # Use Bedrock Converse API (model-agnostic)
            response = self._invoke_model_converse(
                system_prompt="You are an expert B2B marketing strategist specializing in enterprise technology campaigns. Generate creative, data-driven campaign ideas based on market intelligence and competitive analysis. Respond with JSON only.",
                user_message=prompt,
                max_tokens=2048
            )
            
            result = json.loads(response)
            return self._parse_ideas(result)
            
        except json.JSONDecodeError as e:
            raise ExternalServiceError(f"Failed to parse Bedrock response as JSON: {str(e)}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            raise ExternalServiceError(f"Bedrock API error ({error_code}): {error_msg}")
        except Exception as e:
            raise ExternalServiceError(f"Failed to generate campaign ideas with Bedrock: {str(e)}")
    
    def optimize_channel_mix(
        self,
        ideas: List[CampaignIdea],
        target_audience: List[str]
    ) -> List[ChannelPlan]:
        """
        Optimize channel mix using Amazon Bedrock
        """
        if not self.client:
            raise ExternalServiceError(
                "Bedrock client not initialized. Please configure AWS credentials."
            )
        
        try:
            prompt = self._build_channel_optimization_prompt(ideas, target_audience)
            
            response = self._invoke_model_converse(
                system_prompt="You are a B2B marketing channel optimization expert. Recommend the optimal mix of marketing channels with budget allocation and success metrics. Respond with JSON only.",
                user_message=prompt,
                max_tokens=1024
            )
            
            result = json.loads(response)
            return self._parse_channel_mix(result)
            
        except json.JSONDecodeError as e:
            raise ExternalServiceError(f"Failed to parse Bedrock response as JSON: {str(e)}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            raise ExternalServiceError(f"Bedrock API error ({error_code}): {error_msg}")
        except Exception as e:
            raise ExternalServiceError(f"Failed to optimize channel mix with Bedrock: {str(e)}")
    
    def _invoke_model_converse(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """
        Invoke Bedrock model using Converse API (model-agnostic)
        
        The Converse API provides a consistent interface across all Bedrock models,
        simplifying model switching and multi-model strategies.
        """
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_message}]
                    }
                ],
                system=[{"text": system_prompt}],
                inferenceConfig={
                    "maxTokens": min(max_tokens, self.model_config["max_tokens"]),
                    "temperature": temperature,
                    "topP": 0.9
                }
            )
            
            # Extract text from response
            output_message = response['output']['message']
            content_blocks = output_message['content']
            
            # Combine all text blocks
            text_response = ""
            for block in content_blocks:
                if 'text' in block:
                    text_response += block['text']
            
            return text_response
            
        except ClientError as e:
            raise ExternalServiceError(f"Bedrock Converse API error: {str(e)}")
    
    def _build_ideation_prompt(
        self,
        service: Service,
        market_signals: List[MarketSignal],
        request: CampaignGenerationRequest
    ) -> str:
        """Build prompt for campaign ideation (reuses OpenAI prompt structure)"""
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
        """Build prompt for channel optimization (reuses OpenAI prompt structure)"""
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
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration"""
        return {
            "model_name": self.model_name,
            "model_id": self.model_id,
            "description": self.model_config["description"],
            "max_tokens": self.model_config["max_tokens"],
            "provider": "Amazon Bedrock"
        }
