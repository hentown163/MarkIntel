# NexusPlanner - Database Design

## 📋 Table of Contents
1. [Overview](#overview)
2. [Entity Relationship Diagram](#entity-relationship-diagram)
3. [Table Schemas](#table-schemas)
4. [Indexes and Performance](#indexes-and-performance)
5. [Data Dictionary](#data-dictionary)
6. [Migration Strategy](#migration-strategy)
7. [Backup and Recovery](#backup-and-recovery)

---

## 1. Overview

### 1.1 Database Technology
- **RDBMS**: PostgreSQL 15+
- **Hosting**: Neon (managed PostgreSQL)
- **ORM**: SQLAlchemy 2.0
- **Migration Tool**: Alembic

### 1.2 Design Principles
- **Normalization**: 3NF (Third Normal Form) for core tables
- **Denormalization**: JSON columns for flexible metadata and nested structures
- **Audit Trail**: Full agent decision logging for compliance
- **Scalability**: Designed for horizontal scaling with read replicas

### 1.3 Key Features
- Multi-table relationships with cascading deletes
- JSON columns for complex nested data
- Comprehensive indexing for query performance
- Enum types for status fields
- Timestamps for audit trails

---

## 2. Entity Relationship Diagram

### 2.1 Core Business Entities

\`\`\`plantuml
@startuml
!define table(x) class x << (T,#FFAAAA) >>
!define view(x) class x << (V,#FFAAAA) >>
!define pk(x) <b><color:red>x</color></b>
!define fk(x) <color:blue>x</color>

title NexusPlanner Database Schema - Core Entities

table(campaigns) {
  pk(id): VARCHAR
  --
  name: VARCHAR NOT NULL
  status: ENUM NOT NULL
  theme: VARCHAR NOT NULL
  start_date: DATE NOT NULL
  end_date: DATE NOT NULL
  total_budget: FLOAT NOT NULL
  expected_roi: FLOAT NOT NULL
  metrics_json: JSON
  fk(service_id): VARCHAR
  feedback_history: JSON
}

table(campaign_ideas) {
  pk(id): VARCHAR
  --
  fk(campaign_id): VARCHAR NOT NULL
  theme: VARCHAR NOT NULL
  core_message: TEXT NOT NULL
  target_segments: JSON NOT NULL
  competitive_angle: TEXT NOT NULL
}

table(channel_plans) {
  pk(id): VARCHAR
  --
  fk(campaign_id): VARCHAR NOT NULL
  channel: VARCHAR NOT NULL
  budget_allocation: FLOAT NOT NULL
  strategy: TEXT NOT NULL
  expected_reach: INTEGER
  expected_engagement: FLOAT
  kpis: JSON
}

table(services) {
  pk(id): VARCHAR
  --
  name: VARCHAR NOT NULL
  category: VARCHAR NOT NULL
  description: TEXT NOT NULL
  target_audience: JSON NOT NULL
  key_benefits: JSON NOT NULL
  market_mentions: INTEGER
  active_campaigns: INTEGER
  competitors: JSON
}

table(market_signals) {
  pk(id): VARCHAR
  --
  source: VARCHAR NOT NULL
  content: TEXT NOT NULL
  timestamp: TIMESTAMP NOT NULL
  relevance_score: FLOAT NOT NULL
  category: VARCHAR NOT NULL
  impact: ENUM NOT NULL
}

campaigns "1" *-- "many" campaign_ideas
campaigns "1" *-- "many" channel_plans
campaigns "many" -- "0..1" services

@enduml
\`\`\`

### 2.2 User and Authentication Entities

\`\`\`plantuml
@startuml
!define table(x) class x << (T,#AAAAFF) >>
!define pk(x) <b><color:red>x</color></b>

title User Management Schema

table(users) {
  pk(id): VARCHAR
  --
  email: VARCHAR UNIQUE NOT NULL
  username: VARCHAR UNIQUE NOT NULL
  hashed_password: VARCHAR NOT NULL
  full_name: VARCHAR
  role: VARCHAR NOT NULL
  is_active: BOOLEAN NOT NULL
  created_at: TIMESTAMP NOT NULL
  updated_at: TIMESTAMP NOT NULL
  last_login: TIMESTAMP
  preferences: JSON
}

note right of users
  **Security:**
  - Password hashed with bcrypt
  - Email and username unique
  - Role-based access (admin, user, viewer)
end note

@enduml
\`\`\`

### 2.3 Agent Observability Entities

\`\`\`plantuml
@startuml
!define table(x) class x << (T,#AAFFAA) >>
!define pk(x) <b><color:red>x</color></b>
!define fk(x) <color:blue>x</color>

title Agent Observability Schema

table(agent_decisions) {
  pk(id): VARCHAR
  --
  decision_id: VARCHAR UNIQUE NOT NULL
  session_id: VARCHAR
  timestamp: TIMESTAMP NOT NULL
  decision_type: VARCHAR NOT NULL
  reasoning_chain: JSON NOT NULL
  data_sources: JSON NOT NULL
  confidence_score: FLOAT NOT NULL
  decision_metadata: JSON
  model_used: VARCHAR
  latency_ms: FLOAT
  error_message: TEXT
  created_at: TIMESTAMP NOT NULL
}

table(execution_traces) {
  pk(id): VARCHAR
  --
  trace_id: VARCHAR UNIQUE NOT NULL
  session_id: VARCHAR
  start_time: TIMESTAMP NOT NULL
  end_time: TIMESTAMP
  total_duration_ms: FLOAT
  steps: JSON NOT NULL
  success: BOOLEAN NOT NULL
  error_message: TEXT
  trace_metadata: JSON
  created_at: TIMESTAMP NOT NULL
}

table(reasoning_steps) {
  pk(id): VARCHAR
  --
  step_id: VARCHAR UNIQUE NOT NULL
  fk(trace_id): VARCHAR NOT NULL
  step_number: INTEGER NOT NULL
  step_type: VARCHAR NOT NULL
  input_data: JSON
  output_data: JSON
  reasoning: TEXT
  confidence_score: FLOAT
  duration_ms: FLOAT
  timestamp: TIMESTAMP NOT NULL
}

table(agent_memory) {
  pk(id): VARCHAR
  --
  memory_id: VARCHAR UNIQUE NOT NULL
  agent_id: VARCHAR NOT NULL
  session_id: VARCHAR
  memory_type: VARCHAR NOT NULL
  content: TEXT NOT NULL
  context: JSON
  importance_score: FLOAT NOT NULL
  relevance_decay: FLOAT NOT NULL
  created_at: TIMESTAMP NOT NULL
  last_accessed: TIMESTAMP NOT NULL
  access_count: INTEGER NOT NULL
  tags: JSON
  meta: JSON
}

table(agent_learnings) {
  pk(id): VARCHAR
  --
  learning_id: VARCHAR UNIQUE NOT NULL
  agent_id: VARCHAR NOT NULL
  source_type: VARCHAR NOT NULL
  source_id: VARCHAR
  learning_category: VARCHAR NOT NULL
  finding: TEXT NOT NULL
  evidence: JSON NOT NULL
  confidence: FLOAT NOT NULL
  impact_score: FLOAT
  created_at: TIMESTAMP NOT NULL
  applied_count: INTEGER NOT NULL
  success_rate: FLOAT
  tags: JSON
}

execution_traces "1" *-- "many" reasoning_steps

@enduml
\`\`\`

### 2.4 Complete ERD

\`\`\`plantuml
@startuml
!define table(x) class x << (T,#FFAAAA) >>
!define pk(x) <b>PK: x</b>
!define fk(x) <i>FK: x</i>

skinparam linetype ortho

entity campaigns {
  pk(id)
  --
  name
  status
  theme
  start_date
  end_date
  total_budget
  expected_roi
  metrics_json
  fk(service_id)
  feedback_history
}

entity campaign_ideas {
  pk(id)
  --
  fk(campaign_id)
  theme
  core_message
  target_segments
  competitive_angle
}

entity channel_plans {
  pk(id)
  --
  fk(campaign_id)
  channel
  budget_allocation
  strategy
  expected_reach
  expected_engagement
  kpis
}

entity services {
  pk(id)
  --
  name
  category
  description
  target_audience
  key_benefits
  market_mentions
  active_campaigns
  competitors
}

entity market_signals {
  pk(id)
  --
  source
  content
  timestamp
  relevance_score
  category
  impact
}

entity users {
  pk(id)
  --
  email
  username
  hashed_password
  full_name
  role
  is_active
  created_at
  updated_at
  last_login
  preferences
}

entity campaign_templates {
  pk(id)
  --
  name
  description
  theme
  ideas
  channel_mix
  created_at
  updated_at
  created_by
  tags
}

entity agent_decisions {
  pk(id)
  --
  decision_id
  session_id
  timestamp
  decision_type
  reasoning_chain
  data_sources
  confidence_score
  model_used
}

campaigns ||--o{ campaign_ideas : "has many"
campaigns ||--o{ channel_plans : "has many"
campaigns }o--|| services : "belongs to"

@enduml
\`\`\`

---

## 3. Table Schemas

### 3.1 campaigns

Primary table storing campaign data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique campaign identifier |
| name | VARCHAR(255) | NOT NULL | Campaign name |
| status | ENUM | NOT NULL, DEFAULT 'draft' | Campaign status (draft, active, paused, completed, cancelled) |
| theme | VARCHAR(255) | NOT NULL | Campaign theme |
| start_date | DATE | NOT NULL | Campaign start date |
| end_date | DATE | NOT NULL | Campaign end date |
| total_budget | FLOAT | NOT NULL | Total campaign budget |
| expected_roi | FLOAT | NOT NULL | Expected ROI percentage |
| metrics_json | JSON | NULL | Campaign performance metrics |
| service_id | VARCHAR(255) | NULL, FK → services.id | Associated service |
| feedback_history | JSON | NULL, DEFAULT [] | User feedback history |

**Indexes:**
- Primary key on `id`
- Index on `status`
- Index on `service_id`
- Index on `start_date`, `end_date`

---

### 3.2 campaign_ideas

Stores campaign creative ideas.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique idea identifier |
| campaign_id | VARCHAR(255) | NOT NULL, FK → campaigns.id | Parent campaign |
| theme | VARCHAR(255) | NOT NULL | Idea theme |
| core_message | TEXT | NOT NULL | Core marketing message |
| target_segments | JSON | NOT NULL | Target audience segments |
| competitive_angle | TEXT | NOT NULL | Competitive differentiation |

**Relationships:**
- `campaign_id` → `campaigns.id` (CASCADE DELETE)

---

### 3.3 channel_plans

Stores multi-channel marketing strategies.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique plan identifier |
| campaign_id | VARCHAR(255) | NOT NULL, FK → campaigns.id | Parent campaign |
| channel | VARCHAR(100) | NOT NULL | Channel name (email, social, paid_ads, etc.) |
| budget_allocation | FLOAT | NOT NULL | Budget % allocated to this channel |
| strategy | TEXT | NOT NULL | Channel-specific strategy |
| expected_reach | INTEGER | NULL | Expected audience reach |
| expected_engagement | FLOAT | NULL | Expected engagement rate |
| kpis | JSON | NULL | Channel-specific KPIs |

**Relationships:**
- `campaign_id` → `campaigns.id` (CASCADE DELETE)

---

### 3.4 services

Product/service catalog.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique service identifier |
| name | VARCHAR(255) | NOT NULL, INDEX | Service name |
| category | VARCHAR(100) | NOT NULL, INDEX | Service category |
| description | TEXT | NOT NULL | Service description |
| target_audience | JSON | NOT NULL | Target personas |
| key_benefits | JSON | NOT NULL | Key value propositions |
| market_mentions | INTEGER | DEFAULT 0 | Number of market mentions |
| active_campaigns | INTEGER | DEFAULT 0 | Number of active campaigns |
| competitors | JSON | NULL | Competitor list |

**Indexes:**
- Primary key on `id`
- Index on `name`
- Index on `category`

---

### 3.5 market_signals

Real-time market intelligence data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique signal identifier |
| source | VARCHAR(255) | NOT NULL, INDEX | Signal source (Twitter, News, Industry Report) |
| content | TEXT | NOT NULL | Signal content/description |
| timestamp | TIMESTAMP | NOT NULL, INDEX | Signal timestamp |
| relevance_score | FLOAT | NOT NULL | Relevance score (0.0-1.0) |
| category | VARCHAR(100) | NOT NULL, INDEX | Signal category |
| impact | ENUM | NOT NULL | Impact level (low, medium, high) |

**Indexes:**
- Primary key on `id`
- Index on `source`
- Index on `timestamp`
- Index on `category`
- Composite index on `impact` + `timestamp`

---

### 3.6 users

User authentication and profile data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User email address |
| username | VARCHAR(100) | UNIQUE, NOT NULL, INDEX | Username |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| full_name | VARCHAR(255) | NULL | User's full name |
| role | VARCHAR(50) | NOT NULL, DEFAULT 'user' | User role (admin, user, viewer) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |
| last_login | TIMESTAMP | NULL | Last login timestamp |
| preferences | JSON | NULL | User preferences |

**Indexes:**
- Primary key on `id`
- Unique index on `email`
- Unique index on `username`
- Index on `role`

**Security:**
- Passwords hashed using bcrypt with salt
- Email verification (planned)
- Password reset tokens (planned)

---

### 3.7 campaign_templates

Reusable campaign templates.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Template identifier |
| name | VARCHAR(255) | NOT NULL, INDEX | Template name |
| description | TEXT | NULL | Template description |
| theme | VARCHAR(255) | NOT NULL | Campaign theme |
| ideas | JSON | NOT NULL | Template ideas |
| channel_mix | JSON | NOT NULL | Template channel strategies |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Update timestamp |
| created_by | VARCHAR(255) | NULL | Creator user ID |
| tags | JSON | NULL | Template tags |

**Indexes:**
- Primary key on `id`
- Index on `name`
- Index on `created_at`

---

### 3.8 agent_decisions

AI agent decision audit trail (GDPR/SOC 2 compliance).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Record identifier |
| decision_id | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Decision identifier |
| session_id | VARCHAR(255) | INDEX | Session identifier |
| timestamp | TIMESTAMP | NOT NULL, INDEX | Decision timestamp |
| decision_type | VARCHAR(100) | NOT NULL, INDEX | Type (market_analysis, idea_generation, etc.) |
| reasoning_chain | JSON | NOT NULL | Step-by-step reasoning |
| data_sources | JSON | NOT NULL | Data sources used |
| confidence_score | FLOAT | NOT NULL | Confidence (0.0-1.0) |
| decision_metadata | JSON | NULL | Additional metadata |
| model_used | VARCHAR(100) | NULL | LLM model used |
| latency_ms | FLOAT | NULL | Processing time |
| error_message | TEXT | NULL | Error details if failed |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `decision_id`
- Index on `session_id`
- Index on `timestamp`
- Index on `decision_type`
- Composite index on `decision_type` + `timestamp`
- Composite index on `session_id` + `timestamp`

**Compliance:**
- Retention policy: 90 days default
- Audit-ready: Full decision trail
- GDPR: User data deletion compliance

---

### 3.9 agent_memory

Persistent agent memory for context retention.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Record identifier |
| memory_id | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Memory identifier |
| agent_id | VARCHAR(255) | NOT NULL, INDEX | Agent identifier |
| session_id | VARCHAR(255) | INDEX | Session identifier |
| memory_type | VARCHAR(100) | NOT NULL, INDEX | Type (conversation, learning, insight) |
| content | TEXT | NOT NULL | Memory content |
| context | JSON | NULL | Contextual information |
| importance_score | FLOAT | NOT NULL, DEFAULT 0.5 | Importance (0.0-1.0) |
| relevance_decay | FLOAT | NOT NULL, DEFAULT 1.0 | Decay factor |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| last_accessed | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last access |
| access_count | INTEGER | NOT NULL, DEFAULT 0 | Access frequency |
| tags | JSON | NULL | Memory tags |
| meta | JSON | NULL | Additional metadata |

**Indexes:**
- Composite index on `agent_id` + `memory_type` + `importance_score`
- Composite index on `session_id` + `created_at`

---

## 4. Indexes and Performance

### 4.1 Primary Indexes

| Table | Index | Columns | Type | Purpose |
|-------|-------|---------|------|---------|
| campaigns | pk_campaigns | id | PRIMARY KEY | Unique identification |
| campaigns | idx_campaigns_status | status | BTREE | Filter by status |
| campaigns | idx_campaigns_dates | start_date, end_date | BTREE | Date range queries |
| market_signals | idx_signals_timestamp | timestamp | BTREE | Time-based queries |
| market_signals | idx_signals_impact_time | impact, timestamp | COMPOSITE | High-impact recent signals |
| agent_decisions | idx_decisions_type_time | decision_type, timestamp | COMPOSITE | Decision analytics |
| users | unique_email | email | UNIQUE | User lookup |

### 4.2 Query Optimization Strategies

1. **Connection Pooling**
   - Pool size: 10
   - Max overflow: 20
   - Recycle connections after 3600 seconds

2. **Eager Loading**
   - Use `joinedload()` for campaigns + ideas + channel_plans
   - Reduces N+1 query problem

3. **Pagination**
   - Default limit: 20 items
   - Max limit: 100 items
   - Offset-based pagination

4. **Caching**
   - Cache service catalog (rarely changes)
   - Cache campaign templates
   - TTL: 1 hour

---

## 5. Data Dictionary

### 5.1 Enums

#### CampaignStatus
- `draft`: Campaign being created
- `active`: Campaign is live
- `paused`: Temporarily paused
- `completed`: Campaign finished successfully
- `cancelled`: Campaign cancelled

#### ImpactLevel
- `low`: Minor impact on market
- `medium`: Moderate impact
- `high`: Significant market impact

#### UserRole
- `admin`: Full system access
- `user`: Standard user access
- `viewer`: Read-only access

### 5.2 JSON Column Structures

#### campaigns.metrics_json
\`\`\`json
{
  "impressions": 150000,
  "clicks": 7500,
  "conversions": 450,
  "ctr": 5.0,
  "conversion_rate": 6.0,
  "roi": 250.5
}
\`\`\`

#### campaign_ideas.target_segments
\`\`\`json
["Enterprise CISOs", "Security Teams", "IT Directors"]
\`\`\`

#### channel_plans.kpis
\`\`\`json
["CTR > 3%", "Conversion Rate > 5%", "Cost per Lead < $50"]
\`\`\`

#### agent_decisions.reasoning_chain
\`\`\`json
[
  {
    "step": 1,
    "action": "analyze_market_signals",
    "reasoning": "Identified 3 high-impact signals...",
    "confidence": 0.85
  },
  {
    "step": 2,
    "action": "generate_ideas",
    "reasoning": "Based on market trends...",
    "confidence": 0.78
  }
]
\`\`\`

---

## 6. Migration Strategy

### 6.1 Alembic Configuration

\`\`\`python
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://user:pass@host/db

# alembic/env.py
from app.infrastructure.persistence.models import Base
target_metadata = Base.metadata
\`\`\`

### 6.2 Migration Workflow

1. **Create Migration**
   \`\`\`bash
   alembic revision --autogenerate -m "Add new table"
   \`\`\`

2. **Review Generated SQL**
   \`\`\`bash
   alembic upgrade head --sql > migration.sql
   \`\`\`

3. **Apply Migration**
   \`\`\`bash
   alembic upgrade head
   \`\`\`

4. **Rollback (if needed)**
   \`\`\`bash
   alembic downgrade -1
   \`\`\`

### 6.3 Migration Best Practices

- ✅ Always backup database before migration
- ✅ Test migrations on staging first
- ✅ Use transactions for atomicity
- ✅ Create migration scripts for data transformations
- ✅ Document breaking changes
- ❌ Never modify existing migrations after deployment
- ❌ Avoid large data migrations during peak hours

---

## 7. Backup and Recovery

### 7.1 Backup Strategy

#### Automated Backups
- **Frequency**: Daily at 2:00 AM UTC
- **Retention**: 7 days (rolling)
- **Storage**: AWS S3 / Neon managed backups
- **Method**: pg_dump with compression

#### Manual Backups
\`\`\`bash
# Full database backup
pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE -F c -f nexusplanner_$(date +%Y%m%d).dump

# Schema only
pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE -s -f schema.sql

# Data only
pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE -a -f data.sql
\`\`\`

### 7.2 Disaster Recovery

#### Recovery Time Objective (RTO)
- Target: < 1 hour
- Process:
  1. Provision new database instance
  2. Restore from latest backup
  3. Apply transaction logs (if available)
  4. Update application config
  5. Run health checks

#### Recovery Point Objective (RPO)
- Target: < 1 hour
- Implementation: Point-in-time recovery with transaction logs

### 7.3 Data Retention Policies

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| Campaigns | Indefinite | Soft delete (status = deleted) |
| Market Signals | 90 days | Hard delete (automated cleanup) |
| Agent Decisions | 90 days (configurable) | Hard delete with audit log |
| User Data | Until account deletion | GDPR-compliant deletion |
| Backups | 7 days | Automated rotation |

---

## 8. Database Scaling

### 8.1 Vertical Scaling
- Start: 2 vCPU, 4GB RAM
- Scale up to: 8 vCPU, 32GB RAM
- Storage: Auto-scaling (10GB to 1TB)

### 8.2 Horizontal Scaling
- **Read Replicas**: 2 replicas for read-heavy workloads
- **Connection Pooling**: PgBouncer for connection management
- **Caching Layer**: Redis for frequently accessed data

### 8.3 Partitioning Strategy (Future)
- Partition `agent_decisions` by timestamp (monthly)
- Partition `market_signals` by date (weekly)

---

## Appendix: Sample Queries

### A1. Get Active Campaigns with Ideas and Strategies
\`\`\`sql
SELECT 
  c.id,
  c.name,
  c.theme,
  c.status,
  json_agg(DISTINCT ci.*) AS ideas,
  json_agg(DISTINCT cp.*) AS channel_strategies
FROM campaigns c
LEFT JOIN campaign_ideas ci ON c.id = ci.campaign_id
LEFT JOIN channel_plans cp ON c.id = cp.campaign_id
WHERE c.status = 'active'
GROUP BY c.id;
\`\`\`

### A2. Find High-Impact Recent Market Signals
\`\`\`sql
SELECT *
FROM market_signals
WHERE impact = 'high'
  AND timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC
LIMIT 10;
\`\`\`

### A3. Agent Decision Analytics
\`\`\`sql
SELECT 
  decision_type,
  COUNT(*) as total_decisions,
  AVG(confidence_score) as avg_confidence,
  AVG(latency_ms) as avg_latency_ms
FROM agent_decisions
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY decision_type
ORDER BY total_decisions DESC;
\`\`\`

---

**Document Version**: 1.0  
**Last Updated**: 2024-10-19  
**Database Version**: PostgreSQL 15+
