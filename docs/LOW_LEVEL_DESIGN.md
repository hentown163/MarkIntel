# NexusPlanner - Low-Level Design (LLD)

## 📋 Table of Contents
1. [Module Architecture](#module-architecture)
2. [Domain Layer Details](#domain-layer-details)
3. [Application Layer Details](#application-layer-details)
4. [Infrastructure Layer Details](#infrastructure-layer-details)
5. [API Specifications](#api-specifications)
6. [Sequence Diagrams](#sequence-diagrams)
7. [Class Diagrams](#class-diagrams)
8. [Error Handling](#error-handling)

---

## 1. Module Architecture

### 1.1 Directory Structure

\`\`\`
nexusplanner/
├── app/
│   ├── domain/                    # Core business logic
│   │   ├── entities/              # Business entities
│   │   │   ├── campaign.py        # Campaign aggregate root
│   │   │   ├── service.py         # Service entity
│   │   │   ├── market_signal.py   # Market signal entity
│   │   │   └── crm/              # CRM-related entities
│   │   │       └── customer.py
│   │   ├── value_objects/         # Immutable value objects
│   │   │   ├── campaign_id.py
│   │   │   ├── service_id.py
│   │   │   ├── money.py
│   │   │   └── date_range.py
│   │   ├── repositories/          # Repository interfaces
│   │   │   ├── campaign_repository.py
│   │   │   ├── service_repository.py
│   │   │   └── market_signal_repository.py
│   │   └── services/              # Domain services
│   │       ├── campaign_ideation_service.py  # Port for AI
│   │       └── agent/            # Multi-agent system
│   │           ├── agent_coordinator.py
│   │           ├── reasoning_engine.py
│   │           └── specialized_agents.py
│   ├── application/               # Application logic
│   │   ├── use_cases/             # Business workflows
│   │   │   ├── generate_campaign_use_case.py
│   │   │   ├── list_campaigns_use_case.py
│   │   │   ├── update_campaign_use_case.py
│   │   │   └── record_feedback_use_case.py
│   │   ├── dtos/                  # Data transfer objects
│   │   │   ├── request/
│   │   │   └── response/
│   │   └── mappers/               # Entity ↔ DTO conversion
│   ├── infrastructure/            # External integrations
│   │   ├── persistence/           # Database layer
│   │   │   ├── models/            # SQLAlchemy ORM models
│   │   │   └── repositories/      # Repository implementations
│   │   ├── llm/                   # AI adapters
│   │   │   ├── openai_campaign_ideation_adapter.py
│   │   │   ├── bedrock_campaign_ideation_adapter.py
│   │   │   └── rule_based_ideation_adapter.py
│   │   ├── rag/                   # RAG system
│   │   │   ├── vector_store.py
│   │   │   └── mock_crm_repository.py
│   │   ├── observability/         # Agent logging
│   │   │   └── agent_logger.py
│   │   └── config/                # Configuration
│   │       └── database.py
│   ├── core/                      # Shared kernel
│   │   ├── settings.py            # Configuration
│   │   ├── exceptions.py          # Custom exceptions
│   │   ├── container.py           # DI container
│   │   └── auth_middleware.py     # Authentication
│   ├── api/                       # API layer
│   │   ├── routes/                # Route handlers
│   │   │   ├── agent.py
│   │   │   └── audit.py
│   │   └── auth.py                # Auth endpoints
│   └── main.py                    # FastAPI application
├── frontend/                      # React SPA
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── pages/                 # Page components
│   │   ├── hooks/                 # Custom hooks
│   │   ├── context/               # React context
│   │   └── api/                   # API client
│   └── public/
├── tests/                         # Test suite
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── fixtures/                  # Test fixtures
├── alembic/                       # Database migrations
├── kubernetes/                    # K8s manifests
├── helm/                          # Helm charts
└── docs/                          # Documentation
\`\`\`

---

## 2. Domain Layer Details

### 2.1 Campaign Entity (Aggregate Root)

\`\`\`plantuml
@startuml
class Campaign {
  - id: CampaignId
  - name: str
  - theme: str
  - status: CampaignStatus
  - start_date: date
  - end_date: date
  - ideas: List[CampaignIdea]
  - channel_strategies: List[ChannelPlan]
  - metrics: CampaignMetrics
  - feedback_history: List[dict]
  
  + __init__(...)
  + add_idea(idea: CampaignIdea)
  + add_channel_strategy(strategy: ChannelPlan)
  + activate()
  + pause()
  + complete()
  + cancel()
  + update_metrics(metrics: CampaignMetrics)
  + record_feedback(feedback: dict)
}

class CampaignIdea {
  - theme: str
  - description: str
  - target_kpi: str
  - core_message: str
  - target_segments: List[str]
  - competitive_angle: str
  
  + __init__(...)
  + validate()
}

class ChannelPlan {
  - channel: str
  - budget_allocation: float
  - strategy: str
  - expected_reach: int
  - expected_engagement: float
  - kpis: List[str]
  
  + __init__(...)
  + validate()
}

enum CampaignStatus {
  DRAFT
  ACTIVE
  PAUSED
  COMPLETED
  CANCELLED
}

Campaign "1" *-- "many" CampaignIdea
Campaign "1" *-- "many" ChannelPlan
Campaign --> CampaignStatus

@enduml
\`\`\`

### 2.2 Value Objects

\`\`\`plantuml
@startuml
class CampaignId {
  - value: str
  + __init__(value: Optional[str] = None)
  + __str__(): str
  + __eq__(other): bool
  + __hash__(): int
}

class Money {
  - amount: Decimal
  - currency: str
  + __init__(amount: Decimal, currency: str = "USD")
  + __add__(other: Money): Money
  + __sub__(other: Money): Money
  + validate()
}

class DateRange {
  - start_date: date
  - end_date: date
  + __init__(start_date: date, end_date: date)
  + validate()
  + days(): int
  + contains(date: date): bool
}

note right of CampaignId
  **Immutable**
  Type-safe identifier
  Prevents primitive obsession
end note

note right of Money
  **Immutable**
  Currency-aware
  Prevents precision errors
end note

@enduml
\`\`\`

### 2.3 Repository Interfaces (Ports)

\`\`\`plantuml
@startuml
interface CampaignRepository {
  + save(campaign: Campaign): Campaign
  + find_by_id(campaign_id: CampaignId): Optional[Campaign]
  + find_all(): List[Campaign]
  + delete(campaign_id: CampaignId): bool
  + count_by_status(status: CampaignStatus): int
  + search(query: str, status: str): List[Campaign]
}

interface ServiceRepository {
  + save(service: Service): Service
  + find_by_id(service_id: ServiceId): Optional[Service]
  + find_all(): List[Service]
  + find_by_category(category: str): List[Service]
}

interface MarketSignalRepository {
  + save(signal: MarketSignal): MarketSignal
  + find_all(): List[MarketSignal]
  + find_recent(limit: int): List[MarketSignal]
  + find_with_filters(...): List[MarketSignal]
}

note top of CampaignRepository
  **Dependency Inversion Principle**
  Domain defines the contract,
  Infrastructure provides implementation
end note

@enduml
\`\`\`

### 2.4 Domain Service (Port for AI)

\`\`\`plantuml
@startuml
abstract class CampaignIdeationService {
  {abstract} + generate_campaign_ideas(...): List[CampaignIdea]
  {abstract} + generate_channel_strategies(...): List[ChannelPlan]
  {abstract} + regenerate_ideas(...): List[CampaignIdea]
  {abstract} + regenerate_strategies(...): List[ChannelPlan]
}

class OpenAICampaignIdeationAdapter {
  - client: OpenAI
  - model: str
  + generate_campaign_ideas(...): List[CampaignIdea]
  + generate_channel_strategies(...): List[ChannelPlan]
}

class BedrockCampaignIdeationAdapter {
  - client: BedrockRuntime
  - model_id: str
  + generate_campaign_ideas(...): List[CampaignIdea]
  + generate_channel_strategies(...): List[ChannelPlan]
}

class RuleBasedIdeationAdapter {
  + generate_campaign_ideas(...): List[CampaignIdea]
  + generate_channel_strategies(...): List[ChannelPlan]
}

CampaignIdeationService <|-- OpenAICampaignIdeationAdapter
CampaignIdeationService <|-- BedrockCampaignIdeationAdapter
CampaignIdeationService <|-- RuleBasedIdeationAdapter

note right of CampaignIdeationService
  **Liskov Substitution Principle**
  Any adapter can be swapped
  without breaking the system
end note

@enduml
\`\`\`

---

## 3. Application Layer Details

### 3.1 Use Case Pattern

\`\`\`plantuml
@startuml
class GenerateCampaignUseCase {
  - campaign_repository: CampaignRepository
  - service_repository: ServiceRepository
  - signal_repository: MarketSignalRepository
  - ideation_service: CampaignIdeationService
  - vector_store: VectorStore
  - agent_coordinator: AgentCoordinator
  
  + __init__(dependencies...)
  + execute(request: GenerateCampaignRequestDTO): CampaignResponseDTO
  - _retrieve_context(service_id: str): dict
  - _analyze_signals(): List[MarketSignal]
  - _coordinate_agents(...): Campaign
}

class UpdateCampaignUseCase {
  - campaign_repository: CampaignRepository
  
  + execute(campaign_id: str, request: UpdateCampaignRequestDTO): CampaignResponseDTO
}

class RecordFeedbackUseCase {
  - campaign_repository: CampaignRepository
  - agent_memory_repo: AgentMemoryRepository
  
  + execute(campaign_id: str, feedback: CampaignFeedbackRequestDTO): FeedbackResponseDTO
  - _store_learning(feedback: dict)
}

note right of GenerateCampaignUseCase
  **Single Responsibility**
  Orchestrates one business workflow
  Dependencies injected via constructor
end note

@enduml
\`\`\`

### 3.2 DTO Layer

\`\`\`plantuml
@startuml
class GenerateCampaignRequestDTO {
  + service_id: str
  + theme: str
  + start_date: date
  + end_date: date
  + total_budget: float
  + target_audience: List[str]
  + key_objectives: List[str]
  + model_config: ConfigDict
}

class CampaignResponseDTO {
  + id: str
  + name: str
  + theme: str
  + status: str
  + start_date: date
  + end_date: date
  + ideas: List[CampaignIdeaDTO]
  + channel_strategies: List[ChannelPlanDTO]
  + metrics: CampaignMetricsDTO
}

class CampaignMapper {
  + {static} to_dto(campaign: Campaign): CampaignResponseDTO
  + {static} to_entity(dto: CampaignResponseDTO): Campaign
}

GenerateCampaignRequestDTO ..> CampaignMapper : validates
CampaignMapper ..> CampaignResponseDTO : creates

note right of CampaignMapper
  **Separation of Concerns**
  Domain entities ≠ API contracts
  DTOs prevent API coupling
end note

@enduml
\`\`\`

---

## 4. Infrastructure Layer Details

### 4.1 Repository Implementation

\`\`\`plantuml
@startuml
class SQLAlchemyCampaignRepository {
  - session: Session
  
  + save(campaign: Campaign): Campaign
  + find_by_id(campaign_id: CampaignId): Optional[Campaign]
  + find_all(): List[Campaign]
  + delete(campaign_id: CampaignId): bool
  + count_by_status(status: CampaignStatus): int
  + search(query: str, status: str): List[Campaign]
  
  - _to_orm(campaign: Campaign): CampaignORM
  - _to_entity(orm: CampaignORM): Campaign
}

class CampaignORM {
  + id: str
  + name: str
  + status: CampaignStatusEnum
  + theme: str
  + start_date: date
  + end_date: date
  + total_budget: float
  + metrics_json: JSON
  + ideas: List[CampaignIdeaORM]
  + channel_mix: List[ChannelPlanORM]
}

interface CampaignRepository <<interface>>

CampaignRepository <|.. SQLAlchemyCampaignRepository
SQLAlchemyCampaignRepository --> CampaignORM : uses

@enduml
\`\`\`

### 4.2 AI Adapter Implementation

\`\`\`python
# BedrockCampaignIdeationAdapter - Key Methods

class BedrockCampaignIdeationAdapter(CampaignIdeationService):
    """AWS Bedrock adapter using Converse API"""
    
    def __init__(self, model_name: str = "claude-3-5-sonnet", ...):
        self.model_id = self.SUPPORTED_MODELS[model_name]["id"]
        self.bedrock = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url
        )
    
    def generate_campaign_ideas(
        self,
        request: CampaignGenerationRequest
    ) -> List[CampaignIdea]:
        """
        Generate campaign ideas using Claude 3.5 Sonnet
        
        Flow:
        1. Build context from RAG data
        2. Construct prompt with market signals
        3. Call Bedrock Converse API
        4. Parse JSON response
        5. Validate and create CampaignIdea entities
        """
        # Build prompt
        prompt = self._build_campaign_prompt(request)
        
        # Call Bedrock
        response = self.bedrock.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.7, "maxTokens": 2000}
        )
        
        # Parse and validate
        ideas_data = self._parse_ideas_response(response)
        return [CampaignIdea(**idea) for idea in ideas_data]
\`\`\`

### 4.3 Agent System Architecture

\`\`\`plantuml
@startuml
class AgentCoordinator {
  - strategy_agent: StrategyAgent
  - creative_agent: CreativeAgent
  - optimization_agent: OptimizationAgent
  - reasoning_engine: ReasoningEngine
  - agent_logger: AgentLogger
  
  + generate_campaign(...): Campaign
  - _coordinate_workflow(...): dict
  - _log_decision(decision_data: dict)
}

class StrategyAgent {
  - llm_adapter: CampaignIdeationService
  
  + analyze_market_signals(signals: List[MarketSignal]): dict
  + identify_opportunities(analysis: dict): List[str]
}

class CreativeAgent {
  - llm_adapter: CampaignIdeationService
  
  + generate_ideas(theme: str, context: dict): List[CampaignIdea]
  + refine_messaging(ideas: List[CampaignIdea]): List[CampaignIdea]
}

class OptimizationAgent {
  - llm_adapter: CampaignIdeationService
  
  + determine_channel_mix(budget: float, ...): List[ChannelPlan]
  + optimize_allocation(channels: List[ChannelPlan]): List[ChannelPlan]
}

class ReasoningEngine {
  + explain_decision(decision_data: dict): str
  + calculate_confidence(reasoning_chain: List[dict]): float
}

AgentCoordinator --> StrategyAgent
AgentCoordinator --> CreativeAgent
AgentCoordinator --> OptimizationAgent
AgentCoordinator --> ReasoningEngine

@enduml
\`\`\`

---

## 5. API Specifications

### 5.1 Campaign Endpoints

\`\`\`yaml
POST /api/campaigns/generate
  Description: Generate new campaign using AI
  Request:
    {
      "service_id": "svc-001",
      "theme": "Q4 Product Launch",
      "start_date": "2024-10-01",
      "end_date": "2024-12-31",
      "total_budget": 50000.0,
      "target_audience": ["CISOs", "Security Teams"],
      "key_objectives": ["Increase awareness", "Generate leads"]
    }
  Response: 201 Created
    {
      "id": "camp-12345",
      "name": "Q4 Product Launch Campaign",
      "status": "draft",
      "ideas": [...],
      "channel_strategies": [...],
      "metrics": {...}
    }

GET /api/campaigns
  Description: List all campaigns with optional filters
  Query Params:
    - query: string (search campaigns)
    - status: string (filter by status)
  Response: 200 OK
    {
      "campaigns": [...],
      "total": 42
    }

GET /api/campaigns/{campaign_id}
  Description: Get campaign details
  Response: 200 OK / 404 Not Found

PATCH /api/campaigns/{campaign_id}
  Description: Update campaign
  Request:
    {
      "name": "Updated Name",
      "status": "active"
    }
  Response: 200 OK

DELETE /api/campaigns/{campaign_id}
  Description: Delete campaign
  Response: 200 OK / 404 Not Found

POST /api/campaigns/{campaign_id}/feedback
  Description: Submit feedback for campaign
  Request:
    {
      "feedback_type": "like",
      "target": "idea",
      "target_id": "idea-1",
      "comment": "Great messaging!"
    }
  Response: 201 Created
\`\`\`

### 5.2 Authentication Endpoints

\`\`\`yaml
POST /auth/register
  Description: Register new user
  Request:
    {
      "email": "user@example.com",
      "username": "user123",
      "password": "SecureP@ss123",
      "full_name": "John Doe"
    }
  Response: 201 Created

POST /auth/login
  Description: Login and get JWT token
  Request:
    {
      "username": "user123",
      "password": "SecureP@ss123"
    }
  Response: 200 OK
    {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "token_type": "bearer",
      "expires_in": 28800
    }

GET /auth/me
  Description: Get current user
  Headers: Authorization: Bearer <token>
  Response: 200 OK
    {
      "id": "user-123",
      "email": "user@example.com",
      "username": "user123",
      "role": "user"
    }
\`\`\`

---

## 6. Sequence Diagrams

### 6.1 Campaign Generation Sequence

\`\`\`plantuml
@startuml
title Detailed Campaign Generation Sequence

actor User
participant UI as "React SPA"
participant API as "FastAPI"
participant UC as "GenerateCampaignUseCase"
participant RAG as "VectorStore"
participant Agent as "AgentCoordinator"
participant Strategy as "StrategyAgent"
participant Creative as "CreativeAgent"
participant Optim as "OptimizationAgent"
participant LLM as "Bedrock/OpenAI"
participant Repo as "CampaignRepository"
participant Logger as "AgentLogger"
participant DB as "PostgreSQL"

User -> UI: Fill campaign form
User -> UI: Click "Generate Campaign"
UI -> API: POST /api/campaigns/generate

API -> UC: execute(request_dto)

UC -> RAG: get_relevant_context(service_id)
RAG -> RAG: Retrieve CRM data, past campaigns
RAG --> UC: context_data

UC -> Agent: generate_campaign(request, context)

Agent -> Strategy: analyze_market_signals(signals)
Strategy -> LLM: "Analyze market trends..."
LLM --> Strategy: analysis_result
Strategy --> Agent: opportunities[]

Agent -> Logger: log_decision("market_analysis", ...)
Logger -> DB: INSERT INTO agent_decisions

Agent -> Creative: generate_ideas(theme, opportunities)
Creative -> LLM: "Generate campaign ideas..."
LLM --> Creative: ideas_json
Creative --> Agent: campaign_ideas[]

Agent -> Logger: log_decision("idea_generation", ...)

Agent -> Optim: determine_channel_mix(budget, ideas)
Optim -> LLM: "Optimize channel allocation..."
LLM --> Optim: channels_json
Optim --> Agent: channel_strategies[]

Agent -> Logger: log_decision("channel_optimization", ...)
Agent --> UC: campaign_entity

UC -> Repo: save(campaign)
Repo -> DB: BEGIN TRANSACTION
Repo -> DB: INSERT INTO campaigns
Repo -> DB: INSERT INTO campaign_ideas
Repo -> DB: INSERT INTO channel_plans
Repo -> DB: COMMIT
Repo --> UC: saved_campaign

UC --> API: campaign_response_dto
API --> UI: JSON response (201 Created)
UI --> User: Display campaign

@enduml
\`\`\`

### 6.2 Authentication Flow

\`\`\`plantuml
@startuml
title JWT Authentication Flow

actor User
participant UI as "React"
participant API as "FastAPI"
participant Auth as "AuthService"
participant DB as "PostgreSQL"

User -> UI: Enter credentials
UI -> API: POST /auth/login
API -> Auth: authenticate(username, password)

Auth -> DB: SELECT FROM users WHERE username=?
DB --> Auth: user_record

Auth -> Auth: verify_password(password, hashed_password)

alt Password Valid
    Auth -> Auth: create_access_token(user_data)
    Auth --> API: JWT token
    API --> UI: {"access_token": "...", "token_type": "bearer"}
    UI -> UI: Store token in memory
    UI --> User: Show dashboard
else Password Invalid
    Auth --> API: Invalid credentials error
    API --> UI: 401 Unauthorized
    UI --> User: Show error message
end

note right of UI
  **Protected Route Access:**
  1. UI sends token in Authorization header
  2. API validates token signature
  3. API extracts user claims
  4. API processes request with user context
end note

@enduml
\`\`\`

---

## 7. Class Diagrams

### 7.1 Complete Domain Model

\`\`\`plantuml
@startuml
!define ENTITY class
!define VO class

package "Value Objects" {
  VO CampaignId {
    - value: str
  }
  VO ServiceId {
    - value: str
  }
  VO Money {
    - amount: Decimal
    - currency: str
  }
  VO DateRange {
    - start_date: date
    - end_date: date
  }
}

package "Entities" {
  ENTITY Campaign {
    - id: CampaignId
    - name: str
    - theme: str
    - status: CampaignStatus
    - date_range: DateRange
    - ideas: List[CampaignIdea]
    - channel_strategies: List[ChannelPlan]
    + activate()
    + pause()
  }
  
  ENTITY CampaignIdea {
    - theme: str
    - description: str
    - core_message: str
    - target_segments: List[str]
  }
  
  ENTITY ChannelPlan {
    - channel: str
    - budget: Money
    - strategy: str
    - expected_reach: int
  }
  
  ENTITY Service {
    - id: ServiceId
    - name: str
    - category: str
    - target_audience: List[str]
  }
  
  ENTITY MarketSignal {
    - id: SignalId
    - source: str
    - content: str
    - timestamp: datetime
    - impact: ImpactLevel
  }
}

Campaign --> CampaignId
Campaign --> DateRange
Campaign "1" *-- "many" CampaignIdea
Campaign "1" *-- "many" ChannelPlan
ChannelPlan --> Money
Service --> ServiceId

@enduml
\`\`\`

---

## 8. Error Handling

### 8.1 Exception Hierarchy

\`\`\`plantuml
@startuml
class Exception

class ApplicationError {
  + message: str
  + code: str
}

class DomainError {
  + entity: str
}

class EntityNotFoundError {
  + entity_id: str
}

class ValidationError {
  + field: str
  + constraint: str
}

class UseCaseError {
  + use_case: str
}

class ExternalServiceError {
  + service: str
  + status_code: int
}

Exception <|-- ApplicationError
ApplicationError <|-- DomainError
ApplicationError <|-- UseCaseError
ApplicationError <|-- ExternalServiceError
DomainError <|-- EntityNotFoundError
DomainError <|-- ValidationError

@enduml
\`\`\`

### 8.2 Error Response Format

\`\`\`json
{
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "Campaign with ID 'camp-999' not found",
    "details": {
      "entity_type": "Campaign",
      "entity_id": "camp-999"
    },
    "timestamp": "2024-10-19T18:30:00Z"
  }
}
\`\`\`

---

## 9. Data Validation

### 9.1 Request Validation (Pydantic)

\`\`\`python
class GenerateCampaignRequestDTO(BaseModel):
    service_id: str = Field(..., min_length=1, max_length=100)
    theme: str = Field(..., min_length=3, max_length=200)
    start_date: date
    end_date: date
    total_budget: float = Field(..., gt=0, le=1000000)
    target_audience: List[str] = Field(..., min_length=1)
    key_objectives: List[str] = Field(..., min_length=1)
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
\`\`\`

---

## 10. Performance Optimizations

### 10.1 Database Query Optimization

- **Eager Loading**: Use SQLAlchemy `joinedload()` for related entities
- **Connection Pooling**: pool_size=10, max_overflow=20
- **Indexing**: Indexes on frequently queried fields (status, created_at, etc.)
- **Query Caching**: Cache frequently accessed reference data (services, templates)

### 10.2 API Response Optimization

- **Pagination**: Default page_size=20, max_size=100
- **Field Selection**: Support `fields` query param to return subset
- **Compression**: GZip compression for large responses
- **Caching**: HTTP cache headers for static data

### 10.3 LLM Call Optimization

- **Prompt Caching**: Cache common prompt patterns
- **Batch Processing**: Group multiple requests when possible
- **Timeout Handling**: 30-second timeout with fallback to rule-based
- **Rate Limiting**: Respect API rate limits with exponential backoff

---

## 11. Security Considerations

### 11.1 Input Sanitization
- SQL Injection: Parameterized queries via SQLAlchemy ORM
- XSS Prevention: React auto-escapes user input
- CSRF Protection: SameSite cookie attribute
- Request Size Limit: Max 10MB payload

### 11.2 Authentication Security
- Password Hashing: bcrypt with salt
- JWT Expiration: 8 hours default
- Token Refresh: Planned (not yet implemented)
- Rate Limiting: 100 requests/minute per user

---

## Appendix: Code Examples

### A1. Complete Use Case Implementation

\`\`\`python
from app.application.use_cases.base import UseCase
from app.domain.repositories.campaign_repository import CampaignRepository
from app.domain.services.campaign_ideation_service import CampaignIdeationService

class GenerateCampaignUseCase(UseCase):
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        ideation_service: CampaignIdeationService,
        # ... other dependencies
    ):
        self.campaign_repository = campaign_repository
        self.ideation_service = ideation_service
    
    def execute(self, request: GenerateCampaignRequestDTO) -> CampaignResponseDTO:
        # 1. Retrieve context
        context = self._retrieve_context(request.service_id)
        
        # 2. Generate ideas
        generation_request = CampaignGenerationRequest(
            theme=request.theme,
            service=context['service'],
            market_signals=context['signals'],
            crm_insights=context['crm_data']
        )
        ideas = self.ideation_service.generate_campaign_ideas(generation_request)
        
        # 3. Generate strategies
        strategies = self.ideation_service.generate_channel_strategies(
            generation_request, ideas
        )
        
        # 4. Create campaign entity
        campaign = Campaign(
            id=CampaignId(),
            name=f"{request.theme} Campaign",
            theme=request.theme,
            date_range=DateRange(request.start_date, request.end_date),
            ideas=ideas,
            channel_strategies=strategies
        )
        
        # 5. Persist
        saved_campaign = self.campaign_repository.save(campaign)
        
        # 6. Return DTO
        return CampaignMapper.to_dto(saved_campaign)
\`\`\`

---

**Document Version**: 1.0  
**Last Updated**: 2024-10-19  
**Authors**: NexusPlanner Development Team
