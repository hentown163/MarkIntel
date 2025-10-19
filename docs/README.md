# NexusPlanner Documentation

Welcome to the NexusPlanner documentation! This directory contains comprehensive documentation covering architecture, setup, database design, and future roadmap.

## 📚 Documentation Index

### 1. [High-Level Design (HLD)](./HIGH_LEVEL_DESIGN.md)
**What**: System architecture and design overview  
**For**: Architects, Technical Leads, Stakeholders  
**Contents**:
- System context and component diagrams (PlantUML)
- Clean Architecture layer breakdown
- Technology stack
- Deployment architecture (Kubernetes/EKS)
- Container architecture
- Security and observability design

**Start here if**: You want to understand the overall system architecture and how components interact.

---

### 2. [Low-Level Design (LLD)](./LOW_LEVEL_DESIGN.md)
**What**: Detailed implementation specifications  
**For**: Developers, Software Engineers  
**Contents**:
- Module architecture and directory structure
- Domain layer details (entities, value objects, repositories)
- Application layer (use cases, DTOs, mappers)
- Infrastructure layer (ORM, adapters, RAG system)
- Sequence diagrams for key workflows
- Class diagrams
- API specifications
- Error handling patterns

**Start here if**: You're implementing features or need detailed class/module specifications.

---

### 3. [Database Design](./DATABASE_DESIGN.md)
**What**: Complete database schema and design  
**For**: Database Administrators, Backend Developers  
**Contents**:
- Entity Relationship Diagrams (ERD)
- Complete table schemas with all columns
- Indexes and performance optimization
- Data dictionary and enum definitions
- Migration strategy
- Backup and recovery procedures
- Sample SQL queries

**Start here if**: You're working with the database or need to understand data models.

---

### 4. [Setup and Build Tutorial](./SETUP_AND_BUILD_TUTORIAL.md)
**What**: Step-by-step guide to get NexusPlanner running  
**For**: New Developers, DevOps Engineers  
**Contents**:
- Prerequisites and required software
- Quick start guide (5 minutes)
- Detailed setup steps (backend, frontend, database)
- Configuration guide (environment variables)
- Running tests
- Troubleshooting common issues
- Production deployment (Docker, Kubernetes, Helm)
- Development workflow best practices

**Start here if**: You're setting up the project for the first time or deploying to production.

---

### 5. [Future Enhancements and Limitations](./FUTURE_ENHANCEMENTS_AND_LIMITATIONS.md)
**What**: Roadmap, limitations, and planned improvements  
**For**: Product Managers, Stakeholders, Contributors  
**Contents**:
- Current limitations (AI, data integration, auth, UI, observability)
- Planned enhancements (prioritized by quarter)
- Feature roadmap (Q1-Q4 2025)
- Technical debt tracking
- Known issues and workarounds
- Performance and security considerations
- Scalability roadmap

**Start here if**: You want to understand project limitations, contribute features, or plan capacity.

---

## 🚀 Quick Navigation

### I want to...

**Understand the system architecture**  
→ Read [High-Level Design](./HIGH_LEVEL_DESIGN.md)

**Set up the project locally**  
→ Follow [Setup and Build Tutorial](./SETUP_AND_BUILD_TUTORIAL.md)

**Implement a new feature**  
→ Check [Low-Level Design](./LOW_LEVEL_DESIGN.md) + [Database Design](./DATABASE_DESIGN.md)

**Deploy to production**  
→ See [Setup Tutorial - Production Deployment](./SETUP_AND_BUILD_TUTORIAL.md#7-production-deployment)

**Understand database schema**  
→ Review [Database Design](./DATABASE_DESIGN.md)

**Contribute or plan features**  
→ Explore [Future Enhancements](./FUTURE_ENHANCEMENTS_AND_LIMITATIONS.md)

**Troubleshoot issues**  
→ Check [Setup Tutorial - Troubleshooting](./SETUP_AND_BUILD_TUTORIAL.md#6-troubleshooting)

---

## 📐 PlantUML Diagrams

Many documents contain PlantUML diagrams. To view/render them:

### Online Rendering
1. Copy PlantUML code from markdown
2. Paste into http://www.plantuml.com/plantuml/uml/
3. View rendered diagram

### VS Code Extension
1. Install "PlantUML" extension
2. Open markdown file
3. Right-click on code block → "Preview Current Diagram"

### IntelliJ IDEA Plugin
1. Install PlantUML Integration plugin
2. Open markdown file
3. Click preview icon

---

## 🏗️ Architecture Overview

NexusPlanner follows **Clean Architecture** principles with clear separation of concerns:

\`\`\`
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│     (FastAPI Routes, React SPA)         │
├─────────────────────────────────────────┤
│         Application Layer               │
│    (Use Cases, DTOs, Mappers)           │
├─────────────────────────────────────────┤
│           Domain Layer                  │
│  (Entities, Value Objects, Interfaces)  │  ← Core Business Logic
├─────────────────────────────────────────┤
│        Infrastructure Layer             │
│  (ORM, AI Adapters, External Services)  │
└─────────────────────────────────────────┘
\`\`\`

**Key Principle**: Dependencies point inward. Domain layer has no external dependencies.

---

## 📊 Technology Stack Summary

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI 0.115+
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15+
- **AI**: OpenAI GPT-4 / AWS Bedrock Claude 3.5
- **Migration**: Alembic

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 7
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios
- **Language**: JavaScript (ES6+)

### Infrastructure
- **Container**: Docker
- **Orchestration**: Kubernetes (AWS EKS)
- **Package Manager**: Helm
- **Database Host**: Neon (PostgreSQL)

---

## 🤝 Contributing

See [Future Enhancements](./FUTURE_ENHANCEMENTS_AND_LIMITATIONS.md#11-contributing) for contribution guidelines.

---

## 📞 Support

- **Documentation Issues**: Open GitHub issue
- **Setup Help**: Check [Troubleshooting](./SETUP_AND_BUILD_TUTORIAL.md#6-troubleshooting)
- **Feature Requests**: See [Future Enhancements](./FUTURE_ENHANCEMENTS_AND_LIMITATIONS.md#2-planned-enhancements)

---

## 📝 Document Metadata

| Document | Version | Last Updated | Status |
|----------|---------|--------------|--------|
| High-Level Design | 1.0 | 2024-10-19 | ✅ Current |
| Low-Level Design | 1.0 | 2024-10-19 | ✅ Current |
| Database Design | 1.0 | 2024-10-19 | ✅ Current |
| Setup Tutorial | 1.0 | 2024-10-19 | ✅ Current |
| Future Enhancements | 1.0 | 2024-10-19 | ✅ Current |

---

**Maintained by**: NexusPlanner Development Team  
**Last Updated**: 2024-10-19  
**Next Review**: 2025-01-01
