# System Architecture Design Document
## CIS 310 — Systems Analysis & Design | Preston Furulie

---

## 1. Architecture Overview

### 1.1 Architecture Style: Three-Tier with Microservice Readiness

The Guitar Shop Inventory Management System uses a **three-tier architecture** that cleanly separates concerns across Presentation, Application, and Data layers. This design provides independent scaling, easier maintenance, and clear security boundaries.

```
┌────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                             │
│   React SPA ──── CDN (CloudFront) ──── Browser / Tablet / Mobile      │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │ HTTPS (TLS 1.3)
                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                              │
│   ALB ──── ECS Fargate (Node.js API) ──── ElastiCache (Redis)         │
│                    │              │                                     │
│            Auth Service    Business Logic                               │
│            (JWT/OAuth)     (Inventory, Orders, Reports)                 │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │ Private subnet (no public access)
                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                  │
│   RDS MySQL 8.0 (Multi-AZ) ──── S3 (Backups, Images, Reports)        │
│   Primary + Read Replica        Lifecycle policies for archival        │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Design Principles

| Principle                | Implementation                                    |
|--------------------------|--------------------------------------------------|
| Separation of Concerns   | UI, API, and database are independently deployable |
| Stateless API            | No server-side session state; JWT tokens carry auth context |
| Defense in Depth         | WAF → ALB → Security Groups → NACL → Encryption |
| Fail Fast                | Input validation at API boundary; detailed error codes |
| Observability            | Structured logging, metrics, distributed tracing  |
| Infrastructure as Code   | All resources defined in Terraform (versioned)    |

---

## 2. Presentation Layer

### 2.1 Technology Stack

| Component       | Technology          | Purpose                           |
|-----------------|---------------------|-----------------------------------|
| Framework       | React 18 (TypeScript) | Component-based SPA              |
| State Mgmt      | React Query (TanStack) | Server state caching & sync    |
| Routing         | React Router v6     | Client-side navigation            |
| UI Library      | Tailwind CSS        | Utility-first styling             |
| Build Tool      | Vite                | Fast bundling & HMR               |
| Testing         | Vitest + Playwright | Unit + E2E tests                  |
| Hosting         | AWS CloudFront + S3 | Global CDN with edge caching      |

### 2.2 Key Features
- **Mobile-first responsive design** — tablet-optimized for warehouse floor use
- **Offline capability** — Service Worker caches critical pages for intermittent connectivity
- **Real-time updates** — WebSocket connection for live inventory changes
- **Barcode scanning** — uses device camera via Web API (no hardware required)
- **Accessibility** — WCAG 2.1 AA compliant, keyboard navigable

---

## 3. Application Layer

### 3.1 Technology Stack

| Component       | Technology          | Purpose                           |
|-----------------|---------------------|-----------------------------------|
| Runtime         | Node.js 20 LTS     | JavaScript server environment     |
| Framework       | Express.js          | HTTP routing and middleware        |
| Validation      | Joi / Zod           | Request schema validation         |
| Auth            | Passport.js + JWT   | Authentication & authorization    |
| ORM             | Prisma              | Type-safe database access         |
| Queue           | Bull (Redis-backed) | Background job processing         |
| Testing         | Jest + Supertest    | Unit + integration tests          |
| Container       | Docker              | Consistent deployment packaging   |
| Orchestration   | AWS ECS Fargate     | Serverless container hosting      |

### 3.2 API Design (RESTful)

| Method | Endpoint                  | Description                   | Auth Required |
|--------|---------------------------|-------------------------------|---------------|
| GET    | /api/v1/products          | List products (paginated)     | Viewer+       |
| GET    | /api/v1/products/:id      | Get single product            | Viewer+       |
| POST   | /api/v1/products          | Create product                | Manager+      |
| PUT    | /api/v1/products/:id      | Update product                | Manager+      |
| DELETE | /api/v1/products/:id      | Deactivate product            | Admin         |
| GET    | /api/v1/inventory         | Current stock levels          | Staff+        |
| POST   | /api/v1/inventory/intake  | Process stock intake          | Staff+        |
| GET    | /api/v1/orders            | List purchase orders          | Manager+      |
| POST   | /api/v1/orders            | Create purchase order         | Manager+      |
| GET    | /api/v1/reports/:type     | Generate report               | Manager+      |
| POST   | /api/v1/auth/login        | Authenticate user             | Public        |
| POST   | /api/v1/auth/refresh      | Refresh JWT token             | Authenticated |

### 3.3 Middleware Pipeline

```
Request → Rate Limiter → CORS → Auth → Validation → Handler → Response
            ↓              ↓       ↓        ↓            ↓
         429 Reject    Headers   401/403   400 Bad    200/201/204
                                          Request
```

### 3.4 Caching Strategy

| Data Type         | Cache Layer     | TTL        | Invalidation            |
|-------------------|-----------------|------------|-------------------------|
| Product catalog   | Redis           | 5 minutes  | On product write         |
| User session      | Redis           | 30 minutes | On logout/expiry         |
| Report data       | Redis           | 1 hour     | On new data write        |
| Static assets     | CloudFront CDN  | 24 hours   | Cache-busted on deploy   |
| API responses     | React Query     | 30 seconds | Stale-while-revalidate   |

---

## 4. Data Layer

### 4.1 Database Design

**Engine:** MySQL 8.0 on AWS RDS (Multi-AZ)
**Schema:** 3NF normalized with strategic denormalization for reporting views

**Core Tables:**

| Table            | Description                              | Estimated Rows |
|------------------|------------------------------------------|----------------|
| products         | Product catalog                          | 5,000          |
| categories       | Product categories                       | 20             |
| inventory        | Current stock levels per location         | 5,000          |
| inventory_log    | All stock movements (append-only)         | 500,000/year   |
| purchase_orders  | POs to suppliers                          | 2,000/year     |
| po_line_items    | Individual items on a PO                  | 10,000/year    |
| suppliers        | Supplier contact and payment info         | 50             |
| users            | System users with hashed passwords        | 100            |
| audit_log        | All system actions for compliance         | 1,000,000/year |

### 4.2 Backup & Recovery

| Strategy          | Implementation                           |
|-------------------|------------------------------------------|
| Automated backups | RDS daily snapshots, 30-day retention     |
| Point-in-time     | RDS continuous backup (5-min granularity) |
| Cross-region      | Snapshot replication to us-east-1         |
| RPO               | 15 minutes (continuous backup)            |
| RTO               | 1 hour (failover to standby)              |
| Data export       | Weekly full export to S3 (encrypted)       |

### 4.3 Read Replicas
- One read replica for reporting queries (prevents report generation from impacting transactional performance)
- Application routes read-heavy queries (reports, search) to replica

---

## 5. Security Architecture

### 5.1 Network Security

```
Internet
    │
    ▼
┌─── WAF (AWS WAF) ───── Rate limiting, SQL injection, XSS filtering
    │
    ▼
┌─── ALB (Public Subnet) ───── SSL termination, health checks
    │
    ▼
┌─── ECS Tasks (Private Subnet) ───── No public IP, SG: port 3000 from ALB only
    │
    ▼
┌─── RDS (Private Subnet) ───── SG: port 3306 from ECS SG only
```

### 5.2 Authentication & Authorization

| Mechanism          | Details                                       |
|--------------------|-----------------------------------------------|
| Password hashing   | bcrypt with cost factor 12                     |
| Token type         | JWT (RS256 asymmetric signing)                 |
| Access token TTL   | 15 minutes                                     |
| Refresh token TTL  | 7 days (stored in httpOnly cookie)             |
| MFA                | Optional TOTP (Google Authenticator)           |
| RBAC               | 4 roles (Admin, Manager, Staff, Viewer)        |
| API key            | For machine-to-machine integrations            |

### 5.3 Data Protection

| Data State    | Method                                        |
|---------------|-----------------------------------------------|
| At rest       | AES-256 encryption (RDS, S3, EBS)              |
| In transit    | TLS 1.3 (all connections)                      |
| In use        | Parameterized queries (SQL injection prevention)|
| Secrets       | AWS Secrets Manager (rotated every 90 days)    |
| PII           | Column-level encryption for sensitive fields    |

---

## 6. Monitoring & Observability

| Tool               | Purpose                    | Alert Threshold              |
|--------------------|----------------------------|------------------------------|
| CloudWatch Metrics | CPU, memory, request count | CPU > 80% for 5 min          |
| CloudWatch Logs    | Application logs           | Error rate > 1% in 5 min     |
| X-Ray              | Distributed tracing        | Latency P99 > 2s             |
| Health checks      | ALB target health          | 2 consecutive failures       |
| Uptime monitoring  | External availability      | Any downtime                 |
| PagerDuty          | Incident management        | Critical alerts → on-call    |

---

## 7. Deployment Architecture

### 7.1 CI/CD Pipeline

```
Developer Push → GitHub Actions → Lint → Unit Test → Build Docker Image
    → Integration Test → Security Scan → Push to ECR
    → Deploy to Staging → Smoke Test → Manual Approval → Deploy to Production
    → Health Check → Rollback if unhealthy
```

### 7.2 Environments

| Environment | Purpose              | Data           | URL                      |
|-------------|----------------------|----------------|--------------------------|
| Development | Local development    | Seed data      | localhost:3000            |
| Staging     | Pre-production QA    | Sanitized copy | staging.example.com       |
| Production  | Live system          | Real data      | app.example.com           |

### 7.3 Scaling Strategy

| Component    | Scaling Type       | Trigger                    | Min/Max      |
|--------------|--------------------|----------------------------|--------------|
| ECS Tasks    | Horizontal (auto)  | CPU > 70% or requests > 500/min | 2 / 10  |
| RDS          | Vertical           | Manual upgrade             | db.r6g.large |
| Redis        | Vertical           | Memory > 80%               | cache.r6g.medium |
| CloudFront   | Global (built-in)  | Automatic                  | N/A          |
