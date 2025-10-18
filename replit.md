# NexusPlanner - Enterprise GenAI Agent Platform

## Overview
NexusPlanner is an **enterprise-grade GenAI Agent platform** that autonomously plans, generates, and optimizes marketing campaigns using advanced AI capabilities. Unlike traditional Gen AI tools, NexusPlanner features **autonomous reasoning**, **RAG (Retrieval-Augmented Generation)**, **observability**, and **closed-loop learning** to deliver revenue-aware, data-driven campaign strategies.

**Transformation (October 2025):** Evolved from a simple GenAI campaign generator into a full **Agentic AI system** capable of:
- **Autonomous Multi-Step Planning**: The agent analyzes objectives and creates execution plans without explicit instructions
- **RAG-Powered Intelligence**: Retrieves relevant customer data to inform campaign decisions
- **Observability & Reasoning Trails**: Complete visibility into agent decisions and reasoning process
- **Closed-Loop Learning**: Learns from campaign outcomes to improve future recommendations
- **Enterprise Integration Ready**: Built to connect with CRM systems (HubSpot, Salesforce)

## User Preferences
**Communication Style:** Simple, everyday language - avoid technical jargon when talking to users.

**Development Approach:** Fast iteration with working features first, then refinement.

## Agentic AI Capabilities (New - October 2025)

### Autonomous Agent Features
- **Reasoning Engine**: Multi-step task planning with autonomous decision-making
- **RAG System**: Vector store with OpenAI embeddings for knowledge retrieval
- **CRM Integration**: Mock CRM repository with 7 enterprise customer profiles (ready for HubSpot/Salesforce)
- **Observability Layer**: Complete logging of agent decisions, reasoning chains, and execution traces
- **Closed-Loop Learning**: Campaign outcome evaluation for continuous improvement

### Agent Architecture
1. **Reasoning Engine** (`app/domain/services/agent/reasoning_engine.py`)
   - Creates multi-step execution plans
   - Analyzes business objectives
   - Retrieves relevant CRM data using RAG
   - Makes autonomous decisions with confidence scoring
   
2. **RAG Vector Store** (`app/infrastructure/rag/vector_store.py`)
   - OpenAI embedding generation (text-embedding-3-small)
   - Cosine similarity-based retrieval
   - Metadata filtering for targeted search
   
3. **Observability Logger** (`app/infrastructure/observability/agent_logger.py`)
   - **Production-Ready Database Logging** (October 2025)
   - Decision tracking with full reasoning chains
   - Execution traces with step-by-step performance metrics
   - Dual-mode: in-memory + PostgreSQL persistence
   - Async logging to avoid blocking agent operations
   - Configurable via feature flags and retention policies
   - Export capabilities for compliance and analysis
   
4. **Mock CRM Repository** (`app/infrastructure/rag/mock_crm_repository.py`)
   - 7 realistic customer profiles across segments (Enterprise, Mid-Market, SMB, Startup)
   - ICP (Ideal Customer Profile) scoring
   - Engagement level tracking
   - Ready to replace with real CRM API integration

## System Architecture

### UI/UX Decisions
The frontend is built with React, focusing on an interactive and responsive user interface. Key UI/UX features include:
- **Real-Time Progress Indicator:** A 5-step visual guide for AI campaign generation.
- **Interactive Campaign Details:** Modals for detailed campaign views, including regeneration and feedback options.
- **Status Filtering:** Campaigns can be filtered by 'All', 'Active', 'Draft', and 'Completed'.
- **Observability Dashboard:** (NEW - October 2025) Complete visibility into agent reasoning and decision-making
  - **Agent Decisions Tab:** View all agent decisions with confidence scores, reasoning chains, and data sources
  - **Execution Traces Tab:** Monitor step-by-step execution traces with performance metrics
  - **Performance Tab:** Track overall statistics, success rates, and decision patterns
  - **Real-time Filtering:** Search and filter decisions by type, status, and session
  - **Interactive Details View:** Click any decision or trace to see full details including reasoning steps
- **Dark Theme:** A responsive design with a default dark theme for improved user experience.
- **Styling:** Pure CSS with CSS Custom Properties for a clean and maintainable design.
- **State Management:** Utilizes custom React hooks for localized and efficient state management.

### Technical Implementations
The system adheres to **Clean Architecture** principles, incorporating **Domain-Driven Design (DDD)** and **SOLID** patterns. It comprises a React frontend and a FastAPI backend, communicating via RESTful APIs.

**Frontend (React):**
- **Framework:** React 19.1.1 with Vite for fast development.
- **Routing:** React Router DOM v7.9.4.
- **HTTP Client:** Axios 1.12.2.
- **Component Design:** Employs presentational components for reusability and maintainability.
- **API Client:** Centralized API client for all backend interactions.

**Backend (FastAPI):**
- **Framework:** FastAPI 0.115.0 for high performance and automatic validation.
- **ORM:** SQLAlchemy 2.x for PostgreSQL database interaction.
- **Validation:** Pydantic 2.9.2 for robust data validation.
- **Layered Architecture:**
    - **Domain Layer:** Contains core business logic, entities (Campaign, MarketSignal, Service), value objects (Money, DateRange), and domain services (CampaignIdeationService).
    - **Application Layer:** Orchestrates domain logic through use cases (e.g., GenerateCampaignUseCase).
    - **Infrastructure Layer:** Handles external concerns like database persistence (SQLAlchemy repositories) and AI integration (OpenAI adapter).
    - **API Layer:** FastAPI routes exposing use cases and defining request/response schemas.

### Feature Specifications

**Core GenAI Features:**
- **AI-Powered Campaign Generation:** Generates campaign ideas and strategies using OpenAI GPT-5.
- **Campaign Management:** View, filter, and interact with generated campaigns.
  - **Search:** Real-time campaign search by name, theme, or channel
  - **Delete:** Remove campaigns with confirmation dialog
  - **Status Filtering:** Filter by All, Active, Draft, and Completed statuses
- **Regeneration and Feedback:** Fully functional interactive features
  - **Regenerate Campaign Ideas:** Uses AI to generate fresh campaign ideas while preserving channel strategies
  - **Regenerate Channel Strategies:** Uses AI to optimize the channel mix while preserving campaign ideas
  - **Like/Dislike Feedback:** Allows users to provide feedback on campaigns with full history tracking
  - **Real-time Updates:** Modal displays fresh data immediately after regeneration without requiring reload

**Agentic AI Features (New):**
- **Autonomous Planning** (`POST /api/agent/plan`): Agent creates multi-step execution plans based on business objectives
- **Campaign Evaluation** (`POST /api/agent/evaluate`): Closed-loop learning from campaign outcomes
- **Observability APIs:**
  - `GET /api/agent/observability/decisions` - View all agent decisions with reasoning chains
  - `GET /api/agent/observability/metrics` - Agent performance metrics (execution time, success rate, token usage)
  - `GET /api/agent/observability/export` - Export complete observability data for analysis
- **RAG Statistics** (`GET /api/agent/rag/stats`): Vector store metrics and document counts
- **CRM Statistics** (`GET /api/agent/crm/stats`): Customer data insights and segmentation breakdown
- **Market Intelligence:** Tracks and displays market signals to inform campaign strategies.
- **Service Catalog:** Manages and displays available services with associated metrics.

**Enterprise Audit & Compliance Features (Production-Ready - October 2025):**
- **Database-Persisted Audit Logs**: All agent decisions and execution traces saved to PostgreSQL for compliance
  - Tables: `agent_decisions`, `execution_traces`, `reasoning_steps`
  - Indexed by timestamp, session_id, decision_type for efficient querying
  - JSONB columns for flexible metadata storage
- **Audit Trail APIs** (`/api/audit`):
  - `GET /api/audit/decisions/recent` - Recent agent decisions with reasoning chains
  - `GET /api/audit/decisions/by-type/{type}` - Filter decisions by type
  - `GET /api/audit/decisions/by-session/{session_id}` - Session-specific audit trail
  - `GET /api/audit/traces/recent` - Execution traces with performance metrics
  - `GET /api/audit/stats/decisions` - Decision statistics and trends
  - `GET /api/audit/stats/traces` - Performance analytics
- **Retention Policies**: Configurable data retention (default: 90 days)
  - `POST /api/audit/cleanup/decisions` - Remove old decisions per policy
  - `POST /api/audit/cleanup/traces` - Remove old traces per policy
- **Feature Flags**: Enable/disable database logging via configuration
  - `enable_database_logging` setting (default: True)
  - Async persistence to avoid blocking agent execution
  - Dual-mode: in-memory + database for reliability

### System Design Choices
- **Repository Pattern:** Abstracted data access for flexibility.
- **Dependency Injection:** Used for managing and providing dependencies throughout the backend.
- **Adapter Pattern:** Isolates external services like OpenAI from core domain logic.
- **Value Objects:** Ensures type safety and immutability for critical domain concepts (e.g., Money, DateRange).
- **Database Schema:** PostgreSQL with tables for `services`, `market_signals`, `campaigns`, `campaign_ideas`, `channel_plans`, `agent_decisions`, `execution_traces`, and `reasoning_steps`, designed for data integrity, performance, and compliance auditing.
- **CORS Configuration:** Setup for development with plans for production-grade security.

## External Dependencies

**AI & ML:**
- **OpenAI GPT-4o:** Campaign ideation, content generation, and agent reasoning
- **OpenAI Embeddings (text-embedding-3-small):** RAG vector embeddings for knowledge retrieval
- **scikit-learn:** Cosine similarity calculations for RAG retrieval
- **NumPy:** Vector operations and numerical computations

**Backend:**
- **FastAPI 0.115.0:** High-performance API framework
- **PostgreSQL:** Primary database (Neon-backed via Replit)
- **SQLAlchemy 2.x:** ORM for database interactions
- **Pydantic 2.9.2:** Data validation and settings management
- **Uvicorn:** ASGI server
- **python-jose[cryptography]:** JWT authentication (ready for auth implementation)
- **passlib[bcrypt]:** Password hashing (ready for auth implementation)

**Frontend:**
- **React 19.1.1 + Vite:** Modern frontend development
- **Axios 1.12.2:** HTTP client for API communication
- **Lucide React:** Lightweight icon library

**Future Integrations (Prepared):**
- **HubSpot CRM:** Customer data integration (mock data currently active)
- **Salesforce:** Alternative CRM integration option
- **Customer Data Platforms (CDP):** For unified behavioral signals