# NexusPlanner - Setup and Build Tutorial

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (Local Development)](#quick-start-local-development)
3. [Detailed Setup Steps](#detailed-setup-steps)
4. [Configuration Guide](#configuration-guide)
5. [Running Tests](#running-tests)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 20+ | Frontend build tool |
| PostgreSQL | 15+ | Database |
| Git | Latest | Version control |
| Docker | Latest (optional) | Containerization |
| UV | Latest | Python package manager |

### 1.2 Optional Software

| Software | Purpose |
|----------|---------|
| kubectl | Kubernetes deployment |
| helm | K8s package management |
| aws-cli | AWS Bedrock integration |

### 1.3 Required Accounts

- **PostgreSQL Database**: Neon, AWS RDS, or local PostgreSQL
- **AI Provider** (choose one):
  - OpenAI API account (for GPT-4)
  - AWS account (for Bedrock Claude 3.5)
  - Or use rule-based fallback (no AI account needed)

---

## 2. Quick Start (Local Development)

Follow these steps to get NexusPlanner running locally in under 5 minutes:

### Step 1: Clone the Repository

\`\`\`bash
git clone https://github.com/yourorg/nexusplanner.git
cd nexusplanner
\`\`\`

### Step 2: Set Up Backend

\`\`\`bash
# Install UV (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Create Replit secrets or .env file (see Configuration section)
# Add: JWT_SECRET_KEY, DATABASE_URL, etc.
\`\`\`

### Step 3: Set Up Frontend

\`\`\`bash
cd frontend
npm install
cd ..
\`\`\`

### Step 4: Run Database Migrations

\`\`\`bash
# The application runs migrations automatically on startup
# Or run manually:
uv run alembic upgrade head
\`\`\`

### Step 5: Start the Application

\`\`\`bash
# Terminal 1: Start Backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Frontend
cd frontend && npm run dev
\`\`\`

### Step 6: Access the Application

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Default Login Credentials

\`\`\`
Username: demo
Password: demo123
\`\`\`

---

## 3. Detailed Setup Steps

### 3.1 Backend Setup (Detailed)

#### 3.1.1 Install Python and UV

**macOS:**
\`\`\`bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
\`\`\`

**Ubuntu/Debian:**
\`\`\`bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
\`\`\`

**Windows:**
\`\`\`powershell
# Install Python 3.11 from python.org
# Then install UV
irm https://astral.sh/uv/install.ps1 | iex
\`\`\`

#### 3.1.2 Install Dependencies

\`\`\`bash
# Navigate to project root
cd nexusplanner

# Sync dependencies (creates virtual environment automatically)
uv sync

# Activate virtual environment (optional, UV handles this)
source .venv/bin/activate  # macOS/Linux
# OR
.venv\\Scripts\\activate  # Windows
\`\`\`

#### 3.1.3 Verify Installation

\`\`\`bash
# Check Python version
uv run python --version
# Should output: Python 3.11.x

# Check installed packages
uv pip list
# Should show fastapi, sqlalchemy, alembic, etc.
\`\`\`

---

### 3.2 Frontend Setup (Detailed)

#### 3.2.1 Install Node.js

**macOS:**
\`\`\`bash
# Using Homebrew
brew install node@20
\`\`\`

**Ubuntu/Debian:**
\`\`\`bash
# Using NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
\`\`\`

**Windows:**
- Download installer from https://nodejs.org/
- Run installer and follow prompts

#### 3.2.2 Install Frontend Dependencies

\`\`\`bash
cd frontend

# Install dependencies
npm install

# Verify installation
npm list --depth=0
# Should show react, vite, axios, etc.
\`\`\`

#### 3.2.3 Build Frontend (Production)

\`\`\`bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
\`\`\`

---

### 3.3 Database Setup

#### 3.3.1 Option A: Use Neon (Recommended for Development)

1. Go to https://neon.tech
2. Sign up for free account
3. Create a new project
4. Copy the connection string
5. Add to your secrets/environment:

\`\`\`bash
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
\`\`\`

#### 3.3.2 Option B: Local PostgreSQL

\`\`\`bash
# Install PostgreSQL
# macOS:
brew install postgresql@15
brew services start postgresql@15

# Ubuntu:
sudo apt install postgresql-15

# Create database
createdb nexusplanner

# Set connection string
DATABASE_URL=postgresql://localhost/nexusplanner
\`\`\`

#### 3.3.3 Run Migrations

\`\`\`bash
# Automatic (on app startup)
uv run uvicorn app.main:app

# Manual
uv run alembic upgrade head

# Check migration status
uv run alembic current

# View migration history
uv run alembic history
\`\`\`

---

## 4. Configuration Guide

### 4.1 Environment Variables

Create environment secrets or `.env` file (never commit .env to git!):

\`\`\`bash
# Required
JWT_SECRET_KEY=<generate with: openssl rand -hex 32>
DATABASE_URL=postgresql://user:pass@host/db

# Optional - AI Provider (choose one)
# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# AWS Bedrock
LLM_PROVIDER=bedrock
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
BEDROCK_MODEL_NAME=claude-3-5-sonnet

# Or use rule-based (no AI required)
USE_AI_GENERATION=false

# Optional - Settings
DEBUG=true
RUN_MIGRATIONS_ON_STARTUP=true
ENABLE_DATABASE_LOGGING=true
AGENT_LOG_RETENTION_DAYS=90

# Optional - Authentication
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480
AWS_AD_SERVER=ldap://ad.example.com
AWS_AD_DOMAIN=EXAMPLE
\`\`\`

### 4.2 Generate JWT Secret Key

\`\`\`bash
# Generate secure random key
openssl rand -hex 32

# Example output:
# c2c44e78b71e42914b9d834eb1eeea68d5e71e657be63b8fdec09725bccc2c6c
\`\`\`

### 4.3 AI Provider Configuration

#### OpenAI Setup

1. Go to https://platform.openai.com/
2. Create API key
3. Add to environment:

\`\`\`bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4
\`\`\`

#### AWS Bedrock Setup

1. Enable Bedrock in AWS Console
2. Request model access (Claude 3.5 Sonnet)
3. Create IAM user with Bedrock permissions
4. Add credentials:

\`\`\`bash
LLM_PROVIDER=bedrock
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
BEDROCK_MODEL_NAME=claude-3-5-sonnet
\`\`\`

#### Rule-Based (No AI)

\`\`\`bash
USE_AI_GENERATION=false
\`\`\`

---

## 5. Running Tests

### 5.1 Backend Tests

\`\`\`bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/unit/domain/test_campaign.py

# Run specific test
uv run pytest tests/unit/domain/test_campaign.py::test_campaign_creation

# Run tests in parallel
uv run pytest -n auto
\`\`\`

### 5.2 Frontend Tests (Planned)

\`\`\`bash
cd frontend

# Run unit tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
\`\`\`

### 5.3 Integration Tests

\`\`\`bash
# Run integration tests (requires database)
uv run pytest tests/integration/

# Run with test database
TEST_DATABASE_URL=postgresql://localhost/nexusplanner_test \\
  uv run pytest tests/integration/
\`\`\`

---

## 6. Troubleshooting

### 6.1 Backend Issues

#### Error: "Module not found"

\`\`\`bash
# Solution: Reinstall dependencies
uv sync --reinstall
\`\`\`

#### Error: "Database connection failed"

\`\`\`bash
# Check DATABASE_URL is set
echo $DATABASE_URL

# Test connection
uv run python -c "from app.infrastructure.config.database import engine; print(engine.url)"

# Check PostgreSQL is running
pg_isready
\`\`\`

#### Error: "JWT_SECRET_KEY not set"

\`\`\`bash
# Generate and add secret key
openssl rand -hex 32
# Add to environment/secrets
\`\`\`

#### Error: "Migration failed"

\`\`\`bash
# Rollback migration
uv run alembic downgrade -1

# Stamp database to current state
uv run alembic stamp head

# Try again
uv run alembic upgrade head
\`\`\`

### 6.2 Frontend Issues

#### Error: "vite: command not found"

\`\`\`bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
\`\`\`

#### Error: "CORS error"

Check `app/core/settings.py`:
\`\`\`python
cors_origins: list[str] = ["*"]  # For development
# Production: ["https://yourdomain.com"]
\`\`\`

#### Error: "WebSocket connection failed"

Check `frontend/vite.config.js` has correct HMR config:
\`\`\`javascript
hmr: {
  clientPort: 443,
  protocol: "wss",
}
\`\`\`

### 6.3 Database Issues

#### Clean Database and Restart

\`\`\`bash
# WARNING: This deletes all data!

# Drop all tables
uv run alembic downgrade base

# Recreate schema
uv run alembic upgrade head

# Seed data
uv run python -c "from app.infrastructure.persistence.seed_data import seed_database; from app.infrastructure.config.database import get_db; seed_database(next(get_db()))"
\`\`\`

---

## 7. Production Deployment

### 7.1 Docker Deployment

#### Build Images

\`\`\`bash
# Build backend image
docker build -f Dockerfile.backend -t nexusplanner-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t nexusplanner-frontend:latest .
\`\`\`

#### Run with Docker Compose

\`\`\`bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
\`\`\`

#### docker-compose.yml Example

\`\`\`yaml
version: '3.8'

services:
  backend:
    image: nexusplanner-backend:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - JWT_SECRET_KEY=\${JWT_SECRET_KEY}
      - OPENAI_API_KEY=\${OPENAI_API_KEY}
    depends_on:
      - db

  frontend:
    image: nexusplanner-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=nexusplanner
      - POSTGRES_USER=nexus
      - POSTGRES_PASSWORD=\${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
\`\`\`

---

### 7.2 Kubernetes/EKS Deployment

#### Prerequisites

\`\`\`bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Configure AWS CLI
aws configure
\`\`\`

#### Deploy with Kubectl

\`\`\`bash
# Create namespace
kubectl create namespace nexusplanner-prod

# Apply secrets
kubectl create secret generic nexusplanner-secrets \\
  --from-literal=jwt-secret-key=\${JWT_SECRET_KEY} \\
  --from-literal=database-url=\${DATABASE_URL} \\
  --from-literal=openai-api-key=\${OPENAI_API_KEY} \\
  -n nexusplanner-prod

# Apply manifests
kubectl apply -f kubernetes/base/ -n nexusplanner-prod

# Check status
kubectl get pods -n nexusplanner-prod
kubectl get svc -n nexusplanner-prod
\`\`\`

#### Deploy with Helm

\`\`\`bash
# Install Helm chart
helm install nexusplanner ./helm/nexusplanner \\
  --namespace nexusplanner-prod \\
  --create-namespace \\
  --set secrets.jwtSecretKey=\${JWT_SECRET_KEY} \\
  --set secrets.databaseUrl=\${DATABASE_URL} \\
  --set secrets.openaiApiKey=\${OPENAI_API_KEY}

# Upgrade release
helm upgrade nexusplanner ./helm/nexusplanner \\
  --namespace nexusplanner-prod

# Rollback
helm rollback nexusplanner -n nexusplanner-prod
\`\`\`

#### Scale Deployment

\`\`\`bash
# Manual scaling
kubectl scale deployment nexusplanner-backend --replicas=5 -n nexusplanner-prod

# Auto-scaling is configured via HPA in kubernetes/base/hpa.yaml
kubectl get hpa -n nexusplanner-prod
\`\`\`

---

### 7.3 Production Checklist

Before deploying to production, verify:

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] JWT secret key is secure (32+ characters)
- [ ] CORS origins restricted to production domain
- [ ] Database backups configured
- [ ] SSL/TLS certificates installed
- [ ] Health checks configured
- [ ] Monitoring and logging set up
- [ ] Resource limits configured (CPU, memory)
- [ ] Secrets stored securely (AWS Secrets Manager, K8s Secrets)
- [ ] Rate limiting enabled
- [ ] Error tracking configured (Sentry, etc.)

---

## 8. Development Workflow

### 8.1 Daily Development

\`\`\`bash
# 1. Pull latest changes
git pull origin main

# 2. Update dependencies
uv sync
cd frontend && npm install && cd ..

# 3. Run migrations
uv run alembic upgrade head

# 4. Start development servers
# Terminal 1:
uv run uvicorn app.main:app --reload

# Terminal 2:
cd frontend && npm run dev
\`\`\`

### 8.2 Adding New Features

1. Create feature branch
   \`\`\`bash
   git checkout -b feature/new-feature
   \`\`\`

2. Make changes

3. Run tests
   \`\`\`bash
   uv run pytest
   \`\`\`

4. Create migration (if database changes)
   \`\`\`bash
   uv run alembic revision --autogenerate -m "Add new table"
   \`\`\`

5. Commit and push
   \`\`\`bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   \`\`\`

### 8.3 Code Quality

\`\`\`bash
# Format code
uv run black app/
uv run isort app/

# Lint
uv run pylint app/
uv run mypy app/

# Frontend lint
cd frontend && npm run lint
\`\`\`

---

## 9. Useful Commands Reference

### Backend

| Command | Description |
|---------|-------------|
| `uv sync` | Install/update dependencies |
| `uv run uvicorn app.main:app --reload` | Start dev server |
| `uv run pytest` | Run tests |
| `uv run alembic upgrade head` | Run migrations |
| `uv run alembic revision --autogenerate` | Create migration |
| `uv pip list` | List installed packages |

### Frontend

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Lint code |

### Docker

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start all services |
| `docker-compose logs -f` | View logs |
| `docker-compose down` | Stop services |
| `docker-compose build` | Rebuild images |

### Kubernetes

| Command | Description |
|---------|-------------|
| `kubectl get pods` | List pods |
| `kubectl logs <pod-name>` | View pod logs |
| `kubectl describe pod <pod-name>` | Pod details |
| `kubectl exec -it <pod-name> -- /bin/bash` | Shell into pod |

---

## 10. Next Steps

After setup, explore:

1. **API Documentation**: http://localhost:8000/docs
2. **Agent Observability**: http://localhost:5000/observability
3. **Database Schema**: docs/DATABASE_DESIGN.md
4. **Architecture**: docs/HIGH_LEVEL_DESIGN.md
5. **Contributing**: CONTRIBUTING.md (if exists)

---

## Support

### Getting Help

- **Documentation**: Check docs/ folder
- **Issues**: GitHub Issues
- **Community**: Discord/Slack (if available)
- **Email**: support@nexusplanner.example.com

### Common Resources

- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:5000
- Database UI: Use pgAdmin or TablePlus
- Logs: Check terminal output or log files

---

**Document Version**: 1.0  
**Last Updated**: 2024-10-19  
**Tested On**: macOS, Ubuntu 22.04, Windows 11
