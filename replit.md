# NexusPlanner - AI-Powered Marketing Campaign Generator

## Recent Changes (October 18, 2025)

**Option 1: Complete the Transformation - COMPLETED:**
- ✅ **OpenAI Integration**: Configured OPENAI_API_KEY via Replit Secrets for secure API key management
- ✅ **Production Database**: PostgreSQL + SQLAlchemy with full ORM models and repositories
- ✅ **Clean Architecture**: Use cases, domain services, and dependency injection fully implemented
- ✅ **Frontend SOLID Refactoring**: 
  - Custom hooks for state management (useApi, useDashboard, useCampaigns, useMarketIntelligence, useServices)
  - Presentational components following Single Responsibility Principle (StatCard, CampaignCard, InsightItem)
  - Complete separation of business logic from UI
  - Proper error handling and loading states throughout
- ✅ **Code Cleanup**: Removed all old code files (app/main_old.py, root main.py)
- ✅ **Architect Review**: All components reviewed and approved as production-ready

**Previous Implementation (October 17, 2025):**
- Built full-stack application with FastAPI backend and React frontend
- Implemented all 4 main pages: Dashboard, Market Intelligence, Campaigns, Services
- Created AI campaign generation modal with form validation
- Set up complete API integration between frontend and backend
- Configured dual workflows for backend (port 8000) and frontend (port 5000)

**Technical Stack:**
- Backend: FastAPI with Pydantic models, running on Uvicorn
- Frontend: React 19 with Vite 7, React Router, Axios, Lucide icons
- Styling: Dark theme with CSS custom properties
- Data: In-memory storage with seed data for 6 services, 5 market signals, 3 campaigns

## Overview

NexusPlanner is an AI-powered marketing campaign planning platform that helps enterprises generate data-driven marketing campaigns based on market intelligence, service offerings, and competitive analysis. The application uses market signals to create targeted campaign ideas with channel-specific strategies and budget allocations.

**Core Purpose:** Automate the process of campaign planning by analyzing market trends, service capabilities, and competitive landscapes to generate comprehensive marketing strategies with actionable channel plans.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- **Framework:** React 19.1.1 with Vite 7.1.7 build tooling
- **Routing:** React Router DOM v7.9.4 for client-side navigation
- **HTTP Client:** Axios 1.12.2 for API communication
- **Icons:** Lucide React for UI iconography
- **Styling:** Pure CSS with CSS custom properties (CSS variables) for theming

**Design Decisions:**
- **SPA Architecture:** Single-page application with client-side routing to provide a seamless user experience
- **Component-Based Structure:** Organized into reusable components (Navbar, CampaignModal) and page-level views (Dashboard, Campaigns, MarketIntelligence, Services)
- **API Layer Abstraction:** Centralized API client (`src/api/client.js`) that exports domain-specific API modules (dashboardAPI, campaignsAPI, marketIntelligenceAPI, servicesAPI)
- **Custom Theming:** CSS variables defined in `index.css` for consistent dark theme across the application
- **Development Server Configuration:** Configured for Replit environment with HMR over WSS and external host binding

**Rationale:** React with Vite provides fast development experience and optimal production builds. The component architecture allows for code reuse and maintainability. Centralized API client prevents code duplication and makes endpoint management easier.

### Backend Architecture

**Technology Stack:**
- **Framework:** FastAPI (async-capable Python web framework)
- **Data Validation:** Pydantic v2 for request/response schemas and type safety
- **Server:** Uvicorn ASGI server

**Design Patterns:**
- **Layered Architecture:** Clear separation between routes (app/main.py), business logic (app/services/), data models (app/models/), and storage (app/storage/)
- **Service Layer Pattern:** Campaign generation logic encapsulated in `CampaignGenerator` class
- **Repository Pattern:** `MemStorage` class provides abstraction over data access
- **Pydantic Models:** Strong typing and validation for all data structures (Campaign, MarketSignal, Service, etc.)

**Key Components:**

1. **Models Layer** (`app/models/`):
   - Domain entities: Campaign, MarketSignal, Service
   - Enums for status and impact levels (CampaignStatus, ImpactLevel)
   - Request/response DTOs (CampaignGenerationRequest)
   - **Why:** Ensures type safety, automatic validation, and clear API contracts

2. **Services Layer** (`app/services/`):
   - `CampaignGenerator`: Core business logic for generating campaign plans based on services and market signals
   - Implements idea generation, channel planning, and budget allocation algorithms
   - **Why:** Separates business logic from HTTP layer, making it testable and reusable

3. **Storage Layer** (`app/storage/`):
   - `MemStorage`: In-memory data storage for MVP
   - Seed data generation for services, market signals, and sample campaigns
   - **Why:** Simple implementation for prototype; designed to be replaceable with database integration

4. **API Layer** (`app/main.py`):
   - RESTful endpoints for dashboard metrics, campaigns, market intelligence, and services
   - CORS middleware configured to allow frontend access
   - **Why:** FastAPI provides automatic OpenAPI documentation and high performance

**API Endpoints:**
- `GET /api/dashboard/metrics` - Dashboard statistics
- `GET /api/campaigns` - List all campaigns
- `GET /api/campaigns/recent` - Recent campaigns
- `GET /api/campaigns/{id}` - Single campaign details
- `POST /api/campaigns/generate` - Generate new campaign from request

**Rationale:** FastAPI chosen for its automatic validation, async support, and excellent developer experience. The layered architecture makes the codebase maintainable and allows for future scalability. In-memory storage is appropriate for MVP but designed to be easily replaced with persistent storage.

### Cross-Cutting Concerns

**CORS Configuration:**
- Configured to allow all origins (`allow_origins=["*"]`) for development
- **Production Consideration:** Should be restricted to specific frontend domain

**Data Flow:**
1. User submits campaign generation request through frontend
2. Request validated by Pydantic models
3. CampaignGenerator analyzes services and market signals
4. Campaign plan generated with ideas and channel strategies
5. Campaign stored in MemStorage and returned to client

## External Dependencies

### Frontend Dependencies

**Production:**
- `axios` (^1.12.2) - Promise-based HTTP client for API requests
- `lucide-react` (^0.546.0) - Icon library for UI elements
- `react` (^19.1.1) - UI library
- `react-dom` (^19.1.1) - React DOM rendering
- `react-router-dom` (^7.9.4) - Client-side routing

**Development:**
- `@vitejs/plugin-react` (^5.0.4) - Vite plugin for React with Fast Refresh
- `eslint` (^9.36.0) - Code linting
- `vite` (^7.1.7) - Build tool and dev server

### Backend Dependencies

**Production:**
- `fastapi` (0.115.0) - Modern Python web framework
- `uvicorn[standard]` (0.30.6) - ASGI server with WebSocket and watchdog support
- `pydantic` (2.9.2) - Data validation using Python type annotations

**Development:**
- `python-dotenv` (1.0.1) - Environment variable management

### Third-Party Services

**Current State:**
- No external APIs or cloud services currently integrated
- Application runs entirely on local/container infrastructure

**Future Integration Points:**
- AI/LLM APIs for enhanced campaign idea generation (suggested by codebase structure)
- Analytics platforms for campaign performance tracking
- CRM integrations for audience data
- Market intelligence data providers
- Cloud storage for persistent data (when moving beyond MemStorage)

### Database

**Current Implementation:**
- In-memory storage using Python dictionaries
- Seed data includes sample services, market signals, and campaigns
- No persistent storage layer

**Migration Path:**
- Storage abstraction (`MemStorage`) designed to be replaced with database-backed implementation
- Pydantic models can be adapted to work with ORMs like SQLAlchemy or database clients like PostgreSQL via psycopg2/asyncpg