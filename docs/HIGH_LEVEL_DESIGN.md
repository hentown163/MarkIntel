# NexusPlanner - High-Level Design (HLD)

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagrams](#architecture-diagrams)
3. [Component Overview](#component-overview)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Deployment Architecture](#deployment-architecture)

---

## 1. System Overview

### 1.1 Purpose
NexusPlanner is an enterprise-grade AI-powered campaign intelligence platform that combines real-time market intelligence with advanced AI to generate data-driven marketing campaigns that respond to market opportunities instantly.

### 1.2 Key Capabilities
- **AI-Powered Campaign Generation**: Uses OpenAI GPT-4 or AWS Bedrock (Claude 3.5) for intelligent campaign ideation
- **Real-Time Market Intelligence**: Analyzes market signals and trends to inform campaign strategy
- **Multi-Channel Strategy**: Generates optimized channel mix across email, social, paid ads, events, etc.
- **RAG (Retrieval-Augmented Generation)**: Leverages CRM data and historical campaigns for context-aware generation
- **Agent Observability**: Full audit trail of AI decisions for compliance (GDPR, SOC 2, HIPAA)
- **Clean Architecture**: Maintainable, testable, and extensible design following SOLID principles

### 1.3 Target Users
- Marketing Directors
- CMOs
- Marketing Operations Teams
- Marketing Agencies
- Enterprise Marketing Teams

---

## 2. Architecture Diagrams

### 2.1 System Context Diagram (C4 Model - Level 1)

\`\`\`plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()

title System Context Diagram - NexusPlanner

Person(marketeer, "Marketing Team", "Marketing professionals creating campaigns")
Person(admin, "Administrator", "System administrators managing configuration")

System(nexusplanner, "NexusPlanner", "AI-powered campaign intelligence platform")

System_Ext(openai, "OpenAI API", "GPT-4 for campaign generation")
System_Ext(bedrock, "AWS Bedrock", "Claude 3.5 Sonnet for campaign generation")
System_Ext(db, "PostgreSQL Database", "Campaign, signal, and user data")
System_Ext(crm, "CRM System", "Customer data for RAG")
System_Ext(market_sources, "Market Data Sources", "Industry reports, social media, news")

Rel(marketeer, nexusplanner, "Creates campaigns, views insights", "HTTPS")
Rel(admin, nexusplanner, "Configures settings", "HTTPS")
Rel(nexusplanner, openai, "Generates campaigns", "HTTPS/API")
Rel(nexusplanner, bedrock, "Generates campaigns", "AWS SDK")
Rel(nexusplanner, db, "Reads/writes data", "PostgreSQL Protocol")
Rel(nexusplanner, crm, "Retrieves customer data", "API")
Rel(nexusplanner, market_sources, "Ingests market signals", "API/Webhooks")

@enduml
\`\`\`

### 2.2 Container Diagram (C4 Model - Level 2)

\`\`\`plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

title Container Diagram - NexusPlanner

Person(user, "Marketing User", "Creates and manages campaigns")

System_Boundary(nexusplanner, "NexusPlanner") {
    Container(spa, "React SPA", "React 19, Vite", "Provides campaign management UI")
    Container(api, "FastAPI Backend", "Python 3.11, FastAPI, SQLAlchemy", "Provides REST API, handles business logic")
    ContainerDb(db, "Database", "PostgreSQL", "Stores campaigns, signals, users, agent decisions")
    Container(rag, "RAG System", "Vector Store, Embeddings", "Provides context for AI generation")
    Container(agent, "Agent System", "Multi-agent coordinator", "Orchestrates specialized AI agents")
}

System_Ext(llm, "LLM Provider", "OpenAI GPT-4 or AWS Bedrock Claude")
System_Ext(crm_ext, "External CRM", "Salesforce, HubSpot, etc.")

Rel(user, spa, "Uses", "HTTPS")
Rel(spa, api, "Makes API calls", "JSON/HTTPS")
Rel(api, db, "Reads/writes", "SQL")
Rel(api, rag, "Retrieves context", "In-memory")
Rel(api, agent, "Coordinates agents", "In-memory")
Rel(agent, llm, "Generates content", "HTTPS/API")
Rel(rag, crm_ext, "Syncs customer data", "API")

@enduml
\`\`\`

### 2.3 Clean Architecture Layers

\`\`\`plantuml
@startuml
!define RECTANGLE class

skinparam backgroundColor #FEFEFE
skinparam handwritten false

package "Presentation Layer" #LightBlue {
  [FastAPI Routes] as routes
  [React Frontend] as frontend
}

package "Application Layer" #LightGreen {
  [Use Cases] as usecases
  [DTOs] as dtos
  [Mappers] as mappers
}

package "Domain Layer (Core)" #LightYellow {
  [Entities] as entities
  [Value Objects] as vo
  [Repository Interfaces] as repo_interfaces
  [Domain Services] as domain_services
}

package "Infrastructure Layer" #LightCoral {
  [SQLAlchemy ORM] as orm
  [Repository Implementations] as repo_impl
  [OpenAI Adapter] as openai
  [Bedrock Adapter] as bedrock
  [Database Config] as db_config
  [RAG System] as rag_infra
  [Agent Logger] as logger
}

routes --> usecases
frontend --> routes
usecases --> entities
usecases --> domain_services
usecases --> dtos
mappers --> entities
mappers --> dtos
repo_impl --|> repo_interfaces
openai --|> domain_services
bedrock --|> domain_services
orm --> db_config
usecases --> repo_interfaces
repo_impl --> orm

note right of entities
  **Dependency Rule:**
  Inner layers know nothing
  about outer layers.
  
  Domain is the core,
  independent of frameworks.
end note

@enduml
\`\`\`

### 2.4 Component Interaction Diagram

\`\`\`plantuml
@startuml
title Campaign Generation Flow - Component Interaction

actor User
participant "React SPA" as SPA
participant "FastAPI" as API
participant "GenerateCampaignUseCase" as UC
participant "CampaignRepository" as Repo
participant "AgentCoordinator" as Agent
participant "BedrockAdapter" as Bedrock
participant "VectorStore" as RAG
participant "AgentLogger" as Logger
database "PostgreSQL" as DB

User -> SPA: Request new campaign
SPA -> API: POST /api/campaigns/generate
API -> UC: execute(request)
UC -> Repo: find market signals
Repo -> DB: SELECT FROM market_signals
DB --> Repo: signals[]
Repo --> UC: signals[]

UC -> RAG: get_relevant_context(service_id)
RAG --> UC: crm_data, past_campaigns

UC -> Agent: generate_campaign(signals, context)
Agent -> Bedrock: generate_ideas(prompt, context)
Bedrock --> Agent: campaign_ideas[]

Agent -> Logger: log_decision(decision_data)
Logger -> DB: INSERT INTO agent_decisions

Agent -> Bedrock: generate_strategies(ideas, budget)
Bedrock --> Agent: channel_strategies[]

Agent -> Logger: log_decision(strategy_data)
Agent --> UC: campaign_entity

UC -> Repo: save(campaign)
Repo -> DB: INSERT INTO campaigns
DB --> Repo: campaign_id
Repo --> UC: saved_campaign

UC --> API: CampaignResponseDTO
API --> SPA: JSON response
SPA --> User: Display campaign

@enduml
\`\`\`

---

## 3. Component Overview

### 3.1 Frontend Components (React SPA)

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Dashboard** | Main overview | Active campaigns, metrics, market insights |
| **Campaigns** | Campaign management | List, create, edit, delete campaigns |
| **CampaignDetailModal** | Campaign details | View/edit campaign ideas and strategies |
| **MarketIntelligence** | Market signals | Real-time market data, filtering |
| **Services** | Product/service catalog | Manage offerings and target audiences |
| **Observability** | Agent decisions | Audit trail, decision reasoning |
| **AuthContext** | Authentication | JWT-based auth, protected routes |

### 3.2 Backend Components (FastAPI)

#### 3.2.1 Domain Layer
- **Entities**: Campaign, Service, MarketSignal, CampaignIdea, ChannelPlan
- **Value Objects**: CampaignId, ServiceId, Money, DateRange
- **Repository Interfaces**: Define data access contracts
- **Domain Services**: CampaignIdeationService (port for AI)

#### 3.2.2 Application Layer
- **Use Cases**: GenerateCampaign, ListCampaigns, UpdateCampaign, RecordFeedback
- **DTOs**: Request/Response validation and transformation
- **Mappers**: Domain ↔ DTO conversion

#### 3.2.3 Infrastructure Layer
- **ORM Models**: SQLAlchemy models for all entities
- **Repositories**: SQLAlchemy implementations
- **AI Adapters**: OpenAI, Bedrock, Rule-based
- **RAG System**: Vector store with CRM integration
- **Agent System**: Multi-agent coordinator with specialized agents

### 3.3 AI Agent System

| Agent | Responsibility |
|-------|---------------|
| **Strategy Agent** | Analyzes market signals, identifies opportunities |
| **Creative Agent** | Generates campaign ideas and messaging |
| **Optimization Agent** | Determines optimal channel mix and budget allocation |
| **Reasoning Engine** | Provides explainable decision-making |
| **Agent Coordinator** | Orchestrates multi-agent collaboration |

---

## 4. Data Flow

### 4.1 Campaign Generation Flow

1. **User Request** → React SPA submits campaign generation request
2. **API Gateway** → FastAPI receives and validates request
3. **Use Case Execution** → GenerateCampaignUseCase orchestrates workflow
4. **Context Retrieval** → RAG system fetches relevant CRM data and past campaigns
5. **Market Analysis** → Agent retrieves and analyzes market signals
6. **AI Generation** → Bedrock/OpenAI generates ideas and strategies
7. **Decision Logging** → Agent logger records all decisions with reasoning
8. **Persistence** → Repository saves campaign to database
9. **Response** → DTO mapper converts entity to API response
10. **UI Update** → React displays new campaign

### 4.2 Authentication Flow

1. User submits credentials → FastAPI `/auth/login`
2. Validate against database (or AWS AD via LDAP)
3. Generate JWT token with user claims
4. Return token to frontend
5. Frontend stores token in memory
6. Include token in Authorization header for protected routes
7. Backend validates token on each request

---

## 5. Technology Stack

### 5.1 Frontend
- **Framework**: React 19
- **Build Tool**: Vite 7
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Language**: JavaScript (ES6+)

### 5.2 Backend
- **Framework**: FastAPI 0.110+
- **Language**: Python 3.11
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Migration**: Alembic
- **Package Manager**: UV (fast Python package manager)

### 5.3 AI/LLM
- **Primary**: AWS Bedrock (Claude 3.5 Sonnet)
- **Alternative**: OpenAI (GPT-4)
- **Fallback**: Rule-based ideation adapter

### 5.4 Database
- **RDBMS**: PostgreSQL (Neon-hosted)
- **ORM**: SQLAlchemy 2.0
- **Migration Tool**: Alembic

### 5.5 Infrastructure
- **Container**: Docker (multi-stage builds)
- **Orchestration**: Kubernetes (EKS)
- **Package Manager**: Helm
- **CI/CD**: (Ready for GitHub Actions/GitLab CI)

---

## 6. Deployment Architecture

### 6.1 Kubernetes/EKS Deployment

\`\`\`plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Deployment.puml

title Deployment Diagram - AWS EKS

Deployment_Node(aws, "AWS Cloud", "Amazon Web Services") {
    Deployment_Node(eks, "EKS Cluster", "Managed Kubernetes") {
        Deployment_Node(namespace, "nexusplanner-prod", "Kubernetes Namespace") {
            Container(frontend_pod, "Frontend Pods", "Nginx + React SPA", "3 replicas with HPA")
            Container(backend_pod, "Backend Pods", "Uvicorn + FastAPI", "5 replicas with HPA")
            Container(ingress, "Ingress Controller", "AWS ALB", "HTTPS termination")
        }
    }
    
    Deployment_Node(rds, "RDS PostgreSQL", "Managed Database") {
        ContainerDb(db, "PostgreSQL", "Database", "Multi-AZ deployment")
    }
    
    Deployment_Node(bedrock, "AWS Bedrock", "Managed AI Service") {
        Container(claude, "Claude 3.5 Sonnet", "Foundation Model", "On-demand access")
    }
    
    Deployment_Node(secrets, "AWS Secrets Manager", "Secret Management") {
        Container(secret_store, "Secrets", "Credentials Storage", "JWT keys, API keys")
    }
}

Deployment_Node(user_env, "User Environment", "Browser") {
    Container(browser, "Web Browser", "Chrome/Firefox/Safari", "React application")
}

Rel(browser, ingress, "HTTPS requests", "443")
Rel(ingress, frontend_pod, "Routes /", "HTTP")
Rel(ingress, backend_pod, "Routes /api/*", "HTTP")
Rel(backend_pod, db, "SQL queries", "5432")
Rel(backend_pod, claude, "API calls", "HTTPS")
Rel(backend_pod, secret_store, "Retrieve secrets", "AWS SDK")

@enduml
\`\`\`

### 6.2 Container Architecture

\`\`\`plantuml
@startuml
title Docker Container Architecture

package "Frontend Container" {
  [Nginx] as nginx
  [React SPA] as react
  nginx --> react : serves
}

package "Backend Container" {
  [Uvicorn] as uvicorn
  [FastAPI App] as fastapi
  [Worker Pool] as workers
  uvicorn --> fastapi
  uvicorn --> workers
}

package "Database Container (External)" {
  [PostgreSQL] as postgres
}

react --> fastapi : API calls
fastapi --> postgres : SQL

note right of nginx
  **Frontend Image:**
  - Multi-stage build
  - Build with Node 20
  - Serve with Nginx
  - Size: ~50MB
end note

note right of uvicorn
  **Backend Image:**
  - Multi-stage build
  - Python 3.11 slim
  - 4 Uvicorn workers
  - Size: ~300MB
end note

@enduml
\`\`\`

### 6.3 Scaling Strategy

#### Horizontal Pod Autoscaling (HPA)
- **Frontend**: Scale 3-10 pods based on CPU (70% threshold)
- **Backend**: Scale 5-20 pods based on CPU/Memory (80% threshold)

#### Resource Limits
- **Frontend Pod**: 256Mi memory, 0.25 CPU (request), 512Mi memory, 0.5 CPU (limit)
- **Backend Pod**: 512Mi memory, 0.5 CPU (request), 1Gi memory, 1 CPU (limit)

#### Database Scaling
- **PostgreSQL**: Managed by Neon/AWS RDS with auto-scaling storage
- **Connection Pooling**: SQLAlchemy pool_size=10, max_overflow=20

---

## 7. Security Architecture

### 7.1 Authentication & Authorization
- **JWT-based authentication** with secure secret key rotation
- **Role-based access control** (RBAC): admin, user, viewer
- **AWS Active Directory integration** via LDAP (optional)

### 7.2 Data Security
- **Encryption at rest**: PostgreSQL encryption enabled
- **Encryption in transit**: TLS 1.3 for all API communication
- **Secret management**: AWS Secrets Manager / Kubernetes Secrets
- **SQL injection prevention**: SQLAlchemy ORM with parameterized queries

### 7.3 Compliance
- **GDPR**: User data deletion, audit trails
- **SOC 2**: Agent decision logging, access controls
- **HIPAA-ready**: Encryption, audit logs, access controls

---

## 8. Non-Functional Requirements

### 8.1 Performance
- **API Response Time**: < 200ms (p95)
- **Campaign Generation**: < 5 seconds (with AI)
- **Concurrent Users**: 1000+ simultaneous users
- **Database Queries**: < 100ms (p95)

### 8.2 Availability
- **Uptime SLA**: 99.9% (managed by Kubernetes)
- **Recovery Time Objective (RTO)**: < 5 minutes
- **Recovery Point Objective (RPO)**: < 1 hour

### 8.3 Scalability
- **Horizontal scaling**: Auto-scale pods based on load
- **Database scaling**: Managed PostgreSQL auto-scaling
- **Cost optimization**: Spot instances for non-critical workloads

---

## 9. Observability

### 9.1 Logging
- **Application Logs**: Structured JSON logs with correlation IDs
- **Agent Decision Logs**: Full audit trail in database
- **Access Logs**: All API requests logged

### 9.2 Monitoring (Planned)
- **Metrics**: Prometheus + Grafana
- **APM**: OpenTelemetry for distributed tracing
- **Alerts**: PagerDuty/Slack for critical issues

### 9.3 Health Checks
- **/health**: Liveness probe (is app running?)
- **/ready**: Readiness probe (can app serve traffic?)

---

## 10. Disaster Recovery

### 10.1 Backup Strategy
- **Database**: Daily automated backups (7-day retention)
- **Configuration**: Git-based version control
- **Secrets**: AWS Secrets Manager with versioning

### 10.2 Recovery Procedures
1. Deploy latest Helm chart
2. Restore database from backup
3. Verify health checks
4. Gradual traffic rollout

---

## Appendix: PlantUML Diagram Source Files

All PlantUML diagrams are embedded in this document and can be rendered using:
- PlantUML Online Server: http://www.plantuml.com/plantuml/uml/
- VS Code PlantUML Extension
- IntelliJ IDEA PlantUML Plugin

To regenerate diagrams, copy the PlantUML code blocks and paste into any PlantUML renderer.
