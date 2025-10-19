"""Application settings and configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration"""
    
    app_name: str = "NexusPlanner"
    app_version: str = "2.0.0"
    debug: bool = True
    
    database_url: str = "postgresql://localhost/nexusplanner"
    
    # AI Provider Selection ("openai", "bedrock", "anthropic")
    llm_provider: str = "openai"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-5"
    
    # Anthropic Configuration (for direct Anthropic API, not Bedrock)
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # AWS Bedrock Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_bedrock_endpoint_url: Optional[str] = None  # For VPC endpoints
    bedrock_model_name: str = "claude-3-5-sonnet"  # Options: claude-3-5-sonnet, claude-3-sonnet, claude-3-haiku, llama-3-2-90b
    
    # General LLM Settings
    llm_model: str = "gpt-4"  # Legacy field for backward compatibility
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    
    use_ai_generation: bool = True
    
    # Agent Observability Settings
    enable_database_logging: bool = True
    agent_log_retention_days: int = 90
    
    # Database Migration Settings
    run_migrations_on_startup: bool = True
    
    # Authentication Settings
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 480  # 8 hours
    
    # AWS Active Directory Settings
    aws_ad_server: Optional[str] = None
    aws_ad_domain: Optional[str] = None
    aws_ad_base_dn: Optional[str] = None
    aws_ad_use_ssl: bool = True
    
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
