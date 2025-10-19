"""Alembic environment configuration for NexusPlanner database migrations"""
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.infrastructure.config.database import Base

from app.infrastructure.persistence.models.campaign_orm import (
    CampaignORM,
    CampaignIdeaORM,
    ChannelPlanORM,
)
from app.infrastructure.persistence.models.service_orm import ServiceORM
from app.infrastructure.persistence.models.market_signal_orm import MarketSignalORM
from app.infrastructure.persistence.models.user_orm import UserORM
from app.infrastructure.persistence.models.campaign_template_orm import CampaignTemplateORM
from app.infrastructure.persistence.models.agent_decision_orm import (
    AgentDecisionORM,
    ExecutionTraceORM,
    ReasoningStepORM,
)
from app.infrastructure.persistence.models.agent_memory_orm import (
    AgentMemoryORM,
    AgentLearningORM,
    AgentConversationORM,
    MultiAgentCoordinationORM,
    AgentFeedbackLoopORM,
)

target_metadata = Base.metadata


def get_url():
    """Get database URL from environment variable"""
    return os.getenv("DATABASE_URL", "postgresql://localhost/nexusplanner")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
