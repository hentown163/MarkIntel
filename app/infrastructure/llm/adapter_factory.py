"""
AI Adapter Factory - Strategy Pattern Implementation

This factory provides runtime selection of AI adapters (OpenAI, Bedrock, Rule-based)
based on configuration, enabling:
- Multi-model strategies
- Graceful fallback
- A/B testing
- Cost optimization

Enterprise Features:
- Zero-downtime model switching
- Configuration-driven selection
- Failover support
- Telemetry and monitoring hooks

SOLID Principles:
- Single Responsibility: Only creates and configures adapters
- Open/Closed: New adapters can be added without modifying factory
- Dependency Inversion: Returns abstraction (CampaignIdeationService)
"""
from typing import Optional, Literal
import os

from app.domain.services.campaign_ideation_service import CampaignIdeationService
from app.core.settings import settings
from app.core.exceptions import ExternalServiceError


AdapterType = Literal["openai", "bedrock", "anthropic", "rule-based"]


class AdapterFactory:
    """
    Factory for creating AI adapters based on configuration
    
    Usage:
        # Single adapter
        adapter = AdapterFactory.create_adapter()
        
        # Explicit selection
        adapter = AdapterFactory.create_adapter(provider="bedrock")
        
        # With fallback
        adapter = AdapterFactory.create_with_fallback(
            primary="bedrock",
            fallback="openai"
        )
    """
    
    @staticmethod
    def create_adapter(
        provider: Optional[str] = None,
        **kwargs
    ) -> CampaignIdeationService:
        """
        Create an AI adapter based on configuration
        
        Args:
            provider: Provider name ("openai", "bedrock", "rule-based")
                     If None, uses settings.llm_provider
            **kwargs: Additional provider-specific configuration
        
        Returns:
            CampaignIdeationService implementation
        
        Raises:
            ExternalServiceError: If provider is invalid or initialization fails
        """
        provider = provider or settings.llm_provider
        provider = provider.lower()
        
        try:
            if provider == "openai":
                return AdapterFactory._create_openai_adapter(**kwargs)
            
            elif provider == "bedrock":
                return AdapterFactory._create_bedrock_adapter(**kwargs)
            
            elif provider == "anthropic":
                return AdapterFactory._create_anthropic_adapter(**kwargs)
            
            elif provider == "rule-based":
                return AdapterFactory._create_rule_based_adapter(**kwargs)
            
            else:
                raise ExternalServiceError(
                    f"Unknown AI provider: {provider}. "
                    f"Supported: openai, bedrock, anthropic, rule-based"
                )
        
        except ImportError as e:
            raise ExternalServiceError(
                f"Failed to import {provider} adapter: {str(e)}. "
                f"Ensure required dependencies are installed."
            )
        except Exception as e:
            raise ExternalServiceError(
                f"Failed to initialize {provider} adapter: {str(e)}"
            )
    
    @staticmethod
    def _create_openai_adapter(**kwargs) -> CampaignIdeationService:
        """Create OpenAI adapter"""
        from app.infrastructure.llm.openai_campaign_ideation_adapter import (
            OpenAICampaignIdeationAdapter
        )
        
        print(f"✓ Initializing OpenAI adapter (model: {settings.openai_model})")
        return OpenAICampaignIdeationAdapter()
    
    @staticmethod
    def _create_bedrock_adapter(**kwargs) -> CampaignIdeationService:
        """Create Amazon Bedrock adapter"""
        from app.infrastructure.llm.bedrock_campaign_ideation_adapter import (
            BedrockCampaignIdeationAdapter
        )
        
        # Build adapter configuration from settings
        adapter_config = {
            "model_name": kwargs.get("model_name", settings.bedrock_model_name),
            "region_name": kwargs.get("region_name", settings.aws_region),
        }
        
        # Add credentials if provided (prefer IAM roles in production)
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            adapter_config["aws_access_key_id"] = settings.aws_access_key_id
            adapter_config["aws_secret_access_key"] = settings.aws_secret_access_key
        
        # Support VPC endpoints
        if settings.aws_bedrock_endpoint_url:
            adapter_config["endpoint_url"] = settings.aws_bedrock_endpoint_url
        
        print(f"✓ Initializing Bedrock adapter (model: {adapter_config['model_name']}, region: {adapter_config['region_name']})")
        return BedrockCampaignIdeationAdapter(**adapter_config)
    
    @staticmethod
    def _create_anthropic_adapter(**kwargs) -> CampaignIdeationService:
        """
        Create Anthropic direct API adapter (future implementation)
        
        Note: This is for direct Anthropic API access, not Bedrock.
        For most enterprise use cases, prefer Bedrock for better compliance.
        """
        raise NotImplementedError(
            "Direct Anthropic adapter not yet implemented. "
            "Use 'bedrock' provider with Claude models instead."
        )
    
    @staticmethod
    def _create_rule_based_adapter(**kwargs) -> CampaignIdeationService:
        """Create rule-based fallback adapter"""
        from app.infrastructure.llm.rule_based_ideation_adapter import (
            RuleBasedIdeationAdapter
        )
        
        print("✓ Initializing rule-based adapter (no AI, template-based)")
        return RuleBasedIdeationAdapter()
    
    @staticmethod
    def create_with_fallback(
        primary: str = "bedrock",
        fallback: str = "rule-based"
    ) -> CampaignIdeationService:
        """
        Create adapter with automatic fallback
        
        If primary adapter fails to initialize, falls back to secondary.
        Useful for:
        - Development environments without cloud access
        - Handling API key expiration
        - Cost optimization (use rule-based when budget exceeded)
        
        Args:
            primary: Primary provider to attempt
            fallback: Fallback provider if primary fails
        
        Returns:
            Successfully initialized adapter
        
        Example:
            # Try Bedrock, fall back to rule-based if credentials missing
            adapter = AdapterFactory.create_with_fallback(
                primary="bedrock",
                fallback="rule-based"
            )
        """
        try:
            print(f"Attempting to initialize primary adapter: {primary}")
            return AdapterFactory.create_adapter(provider=primary)
        
        except Exception as e:
            print(f"⚠ Primary adapter ({primary}) failed: {str(e)}")
            print(f"Falling back to: {fallback}")
            
            try:
                return AdapterFactory.create_adapter(provider=fallback)
            except Exception as fallback_error:
                raise ExternalServiceError(
                    f"Both primary ({primary}) and fallback ({fallback}) adapters failed. "
                    f"Primary error: {str(e)}. Fallback error: {str(fallback_error)}"
                )
    
    @staticmethod
    def get_available_providers() -> dict:
        """
        Get list of available providers and their status
        
        Returns:
            Dictionary of provider names and availability status
            
        Example:
            {
                "openai": {"available": True, "reason": "API key configured"},
                "bedrock": {"available": False, "reason": "Missing AWS credentials"},
                "rule-based": {"available": True, "reason": "Always available"}
            }
        """
        status = {}
        
        # Check OpenAI
        if settings.openai_api_key or os.getenv("OPENAI_API_KEY"):
            status["openai"] = {"available": True, "reason": "API key configured"}
        else:
            status["openai"] = {"available": False, "reason": "Missing OPENAI_API_KEY"}
        
        # Check Bedrock (IAM role or credentials)
        has_credentials = (
            (settings.aws_access_key_id and settings.aws_secret_access_key) or
            os.getenv("AWS_ACCESS_KEY_ID")
        )
        if has_credentials:
            status["bedrock"] = {"available": True, "reason": "AWS credentials configured"}
        else:
            status["bedrock"] = {
                "available": True,  # Might work with IAM role
                "reason": "No explicit credentials (will attempt IAM role)"
            }
        
        # Rule-based always available
        status["rule-based"] = {"available": True, "reason": "Always available (no external dependencies)"}
        
        return status


def get_campaign_ideation_adapter() -> CampaignIdeationService:
    """
    Convenience function to get the configured campaign ideation adapter
    
    This is the recommended way to obtain an adapter instance.
    Uses settings.llm_provider to determine which adapter to create.
    
    Returns:
        CampaignIdeationService implementation
    
    Usage:
        from app.infrastructure.llm.adapter_factory import get_campaign_ideation_adapter
        
        adapter = get_campaign_ideation_adapter()
        ideas = adapter.generate_ideas(service, signals, request)
    """
    if not settings.use_ai_generation:
        print("AI generation disabled, using rule-based adapter")
        return AdapterFactory.create_adapter(provider="rule-based")
    
    return AdapterFactory.create_adapter()
