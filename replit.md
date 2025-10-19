# NexusPlanner - Enterprise GenAI Agent Platform

## Overview
NexusPlanner is an enterprise-grade GenAI Agent platform designed to autonomously plan, generate, and optimize marketing campaigns. It leverages advanced AI capabilities such as autonomous reasoning, RAG (Retrieval-Augmented Generation), observability, and closed-loop learning to deliver revenue-aware, data-driven campaign strategies. The platform has evolved into a full Agentic AI system capable of multi-step planning, RAG-powered intelligence using customer data, transparent reasoning trails, and continuous learning from campaign outcomes. It is built for enterprise integration with CRM systems like HubSpot and Salesforce.

## User Preferences
**Communication Style:** Simple, everyday language - avoid technical jargon when talking to users.

**Development Approach:** Fast iteration with working features first, then refinement.

## System Architecture

### UI/UX Decisions
The frontend is built with React, focusing on an interactive and responsive user interface. Key features include a 5-step visual guide for AI campaign generation, interactive modals for campaign details, status filtering ('All', 'Active', 'Draft', 'Completed'), and an Observability Dashboard. The dashboard provides complete visibility into agent reasoning, decision-making, execution traces, and performance metrics, with real-time filtering and interactive detail views. The design uses a default dark theme and Pure CSS with CSS Custom Properties for maintainability, and custom React hooks for state management.

### Technical Implementations
The system follows Clean Architecture principles, Domain-Driven Design (DDD), and SOLID patterns, comprising a React frontend and a FastAPI backend communicating via RESTful APIs.

**Frontend (React):**
- **Framework:** React 19.1.1 with Vite.
- **Routing:** React Router DOM v7.9.4.
- **HTTP Client:** Axios 1.12.2.
- **Component Design:** Presentational components.
- **API Client:** Centralized for backend interactions.

**Backend (FastAPI):**
- **Framework:** FastAPI 0.115.0.
- **ORM:** SQLAlchemy 2.x for PostgreSQL.
- **Validation:** Pydantic 2.9.2.
- **Layered Architecture:** Domain (business logic), Application (use cases), Infrastructure (external concerns like database and AI integration), and API (FastAPI routes).

### Feature Specifications

**Core GenAI Features:**
- **AI-Powered Campaign Generation:** Utilizes OpenAI GPT-4o for campaign ideas and strategies.
- **Campaign Management:** Allows viewing, filtering, searching, and deleting campaigns.
- **Regeneration and Feedback:** Features for regenerating campaign ideas or channel strategies, and user feedback (like/dislike) with history tracking.

**Agentic AI Features:**
- **Autonomous Planning:** Agent creates multi-step execution plans.
- **Campaign Evaluation:** Closed-loop learning from campaign outcomes.
- **Observability APIs:** Provides access to agent decisions, reasoning chains, execution traces, and performance metrics.
- **RAG Statistics & CRM Statistics:** Insights into vector store metrics and customer data segmentation.
- **Market Intelligence:** Tracks and displays market signals.
- **Service Catalog:** Manages and displays available services.
- **Enterprise Audit & Compliance:** Database-persisted audit logs for all agent decisions and execution traces in PostgreSQL, with configurable retention policies and Audit Trail APIs for querying.

### System Design Choices
- **Repository Pattern:** Abstracted data access.
- **Dependency Injection:** For managing backend dependencies.
- **Adapter Pattern:** Isolates external services like OpenAI.
- **Value Objects:** Ensures type safety and immutability.
- **Database Schema:** PostgreSQL with tables for services, market signals, campaigns, agent decisions, execution traces, and reasoning steps, designed for integrity, performance, and auditing.
- **CORS Configuration:** Setup for development.
- **Authentication:** JWT Token-Based Authentication with AWS Active Directory Integration, securing all business endpoints.

## External Dependencies

**AI & ML:**
- **OpenAI GPT-4o:** Campaign ideation, content generation, agent reasoning.
- **OpenAI Embeddings (text-embedding-3-small):** RAG vector embeddings.
- **scikit-learn:** Cosine similarity calculations for RAG.
- **NumPy:** Vector operations.

**Backend:**
- **FastAPI 0.115.0:** API framework.
- **PostgreSQL:** Primary database.
- **SQLAlchemy 2.x:** ORM.
- **Pydantic 2.9.2:** Data validation.
- **Uvicorn:** ASGI server.
- **python-jose[cryptography]:** JWT authentication.
- **passlib[bcrypt]:** Password hashing.

**Frontend:**
- **React 19.1.1 + Vite:** Frontend development.
- **Axios 1.12.2:** HTTP client.
- **Lucide React:** Icon library.