# NexusPlanner - AI-Powered Marketing Campaign Generator

## Overview
NexusPlanner is an AI-powered platform designed to revolutionize marketing campaign generation. It provides a comprehensive solution for businesses to rapidly create, manage, and optimize marketing campaigns using advanced AI capabilities. The project aims to streamline the campaign ideation process, integrate market intelligence, and offer a service catalog to enhance strategic marketing efforts. NexusPlanner focuses on delivering high-quality, data-driven campaign strategies to drive business growth and improve market responsiveness.

## User Preferences
**Communication Style:** Simple, everyday language - avoid technical jargon when talking to users.

**Development Approach:** Fast iteration with working features first, then refinement.

## System Architecture

### UI/UX Decisions
The frontend is built with React, focusing on an interactive and responsive user interface. Key UI/UX features include:
- **Real-Time Progress Indicator:** A 5-step visual guide for AI campaign generation.
- **Interactive Campaign Details:** Modals for detailed campaign views, including regeneration and feedback options.
- **Status Filtering:** Campaigns can be filtered by 'All', 'Active', 'Draft', and 'Completed'.
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
- **AI-Powered Campaign Generation:** Generates campaign ideas and strategies using OpenAI GPT-5.
- **Campaign Management:** View, filter, and interact with generated campaigns. Future features include editing, duplication, and performance tracking.
- **Market Intelligence:** Tracks and displays market signals to inform campaign strategies.
- **Service Catalog:** Manages and displays available services with associated metrics.
- **Regeneration and Feedback:** Interactive UI elements to regenerate campaign ideas/channels and provide feedback.
- **Feedback History:** Campaign API responses now include full feedback history with timestamps, allowing the frontend to display all user feedback on campaigns.
- **Search and Filtering:** Planned functionality for searching campaigns and filtering market intelligence/services.

### System Design Choices
- **Repository Pattern:** Abstracted data access for flexibility.
- **Dependency Injection:** Used for managing and providing dependencies throughout the backend.
- **Adapter Pattern:** Isolates external services like OpenAI from core domain logic.
- **Value Objects:** Ensures type safety and immutability for critical domain concepts (e.g., Money, DateRange).
- **Database Schema:** PostgreSQL with specific tables for `services`, `market_signals`, `campaigns`, `campaign_ideas`, and `channel_plans`, designed for data integrity and performance.
- **CORS Configuration:** Setup for development with plans for production-grade security.

## External Dependencies

- **OpenAI GPT-5:** Integrated via `gpt-4o` model for AI-powered campaign ideation and content generation.
- **PostgreSQL:** Primary database, managed by Replit (Neon-backed), accessed via SQLAlchemy ORM.
- **Axios:** Frontend HTTP client for API communication.
- **Lucide React:** Lightweight icon library for the frontend.
- **Vite:** Frontend build tool.
- **Uvicorn:** ASGI server for FastAPI.
- **Psycopg2-binary:** PostgreSQL adapter for Python.