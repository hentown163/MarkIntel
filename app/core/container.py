"""Dependency Injection Container"""
from sqlalchemy.orm import Session

from app.infrastructure.config.database import SessionLocal
from app.infrastructure.persistence.repositories.sqlalchemy_campaign_repository import SQLAlchemyCampaignRepository
from app.infrastructure.persistence.repositories.sqlalchemy_service_repository import SQLAlchemyServiceRepository
from app.infrastructure.persistence.repositories.sqlalchemy_market_signal_repository import SQLAlchemyMarketSignalRepository
from app.infrastructure.llm.openai_campaign_ideation_adapter import OpenAICampaignIdeationAdapter
from app.application.use_cases.generate_campaign_use_case import GenerateCampaignUseCase
from app.application.use_cases.list_campaigns_use_case import ListCampaignsUseCase
from app.application.use_cases.get_campaign_detail_use_case import GetCampaignDetailUseCase
from app.application.use_cases.regenerate_ideas_use_case import RegenerateIdeasUseCase
from app.application.use_cases.regenerate_strategies_use_case import RegenerateStrategiesUseCase
from app.application.use_cases.record_feedback_use_case import RecordFeedbackUseCase
from app.application.use_cases.search_campaigns_use_case import SearchCampaignsUseCase
from app.application.use_cases.update_campaign_use_case import UpdateCampaignUseCase
from app.application.use_cases.delete_campaign_use_case import DeleteCampaignUseCase
from app.core.settings import settings


class Container:
    """
    Dependency Injection Container
    
    Following Dependency Inversion Principle - wires up dependencies
    """
    
    @staticmethod
    def get_db_session() -> Session:
        """Get database session"""
        return SessionLocal()
    
    @staticmethod
    def get_campaign_repository(session: Session):
        """Get campaign repository"""
        return SQLAlchemyCampaignRepository(session)
    
    @staticmethod
    def get_service_repository(session: Session):
        """Get service repository"""
        return SQLAlchemyServiceRepository(session)
    
    @staticmethod
    def get_market_signal_repository(session: Session):
        """Get market signal repository"""
        return SQLAlchemyMarketSignalRepository(session)
    
    @staticmethod
    def get_ideation_service():
        """Get campaign ideation service"""
        import os
        from app.infrastructure.llm.rule_based_ideation_adapter import RuleBasedCampaignIdeationAdapter
        
        if settings.use_ai_generation and os.getenv("OPENAI_API_KEY"):
            try:
                return OpenAICampaignIdeationAdapter()
            except Exception as e:
                print(f"WARNING: Failed to initialize OpenAI adapter: {e}. Falling back to rule-based.")
                return RuleBasedCampaignIdeationAdapter()
        else:
            return RuleBasedCampaignIdeationAdapter()
    
    @staticmethod
    def get_generate_campaign_use_case(session: Session):
        """Get generate campaign use case"""
        return GenerateCampaignUseCase(
            campaign_repo=Container.get_campaign_repository(session),
            service_repo=Container.get_service_repository(session),
            signal_repo=Container.get_market_signal_repository(session),
            ideation_service=Container.get_ideation_service()
        )
    
    @staticmethod
    def get_list_campaigns_use_case(session: Session):
        """Get list campaigns use case"""
        return ListCampaignsUseCase(
            campaign_repo=Container.get_campaign_repository(session)
        )
    
    @staticmethod
    def get_campaign_detail_use_case(session: Session):
        """Get campaign detail use case"""
        return GetCampaignDetailUseCase(
            campaign_repo=Container.get_campaign_repository(session)
        )
    
    @staticmethod
    def get_regenerate_ideas_use_case(session: Session):
        """Get regenerate ideas use case"""
        return RegenerateIdeasUseCase(
            campaign_repo=Container.get_campaign_repository(session),
            service_repo=Container.get_service_repository(session),
            signal_repo=Container.get_market_signal_repository(session),
            ideation_service=Container.get_ideation_service()
        )
    
    @staticmethod
    def get_regenerate_strategies_use_case(session: Session):
        """Get regenerate strategies use case"""
        return RegenerateStrategiesUseCase(
            campaign_repo=Container.get_campaign_repository(session),
            ideation_service=Container.get_ideation_service()
        )
    
    @staticmethod
    def get_record_feedback_use_case(session: Session):
        """Get record feedback use case"""
        return RecordFeedbackUseCase(
            campaign_repo=Container.get_campaign_repository(session)
        )
    
    @staticmethod
    def get_search_campaigns_use_case(session: Session):
        """Get search campaigns use case"""
        return SearchCampaignsUseCase(
            campaign_repo=Container.get_campaign_repository(session)
        )
    
    @staticmethod
    def get_update_campaign_use_case(session: Session):
        """Get update campaign use case"""
        return UpdateCampaignUseCase(
            campaign_repo=Container.get_campaign_repository(session)
        )
    
    @staticmethod
    def get_delete_campaign_use_case(session: Session):
        """Get delete campaign use case"""
        return DeleteCampaignUseCase(
            campaign_repo=Container.get_campaign_repository(session)
        )
