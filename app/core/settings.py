"""Application settings and configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration"""
    
    app_name: str = "NexusPlanner"
    app_version: str = "2.0.0"
    debug: bool = True
    
    database_url: str = "postgresql://localhost/nexusplanner"
    
    llm_provider: str = "openai"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    
    use_ai_generation: bool = True
    
    # Agent Observability Settings
    enable_database_logging: bool = True
    agent_log_retention_days: int = 90
    
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
