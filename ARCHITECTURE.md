# FLLC Enterprise Architecture
**Author:** Preston Furulie | **Version:** 2.0 | **Last Updated:** February 2026

---

## 1. Architecture Principles

| # | Principle | Implementation |
|---|-----------|---------------|
| 1 | **Defense in Depth** | Every layer has its own security controls (WAF → ALB → SG → NACL → Encryption) |
| 2 | **Separation of Concerns** | Three-tier architecture: Presentation, Application, Data — independently deployable |
| 3 | **Infrastructure as Code** | All cloud resources defined in Terraform — version controlled, peer reviewed |
| 4 | **Stateless Services** | API servers carry no session state; JWT tokens and Redis handle auth context |
| 5 | **Observability** | Structured logging, CloudWatch metrics, VPC Flow Logs, distributed tracing |
| 6 | **Least Privilege** | RBAC with 4 tiers; security groups restrict traffic to minimum required ports |
| 7 | **Immutable Infrastructure** | Docker images are versioned artifacts; deployed via rolling update, never patched in-place |
| 8 | **Fail Gracefully** | Health checks, circuit breakers, automated rollback on deployment failure |

---

## 2. System Context

```
                    ┌─────────────────────────────────────┐
                    │          EXTERNAL SYSTEMS            │
                    │                                     │
                    │  POS System ←──┐                    │
                    │  Supplier EDI ←┼── Integration Layer│
                    │  Payment GW  ←─┘                    │
                    └────────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │     FLLC ENTERPRISE PLATFORM        │
                    │                                     │
                    │  ┌─────────┐  ┌──────────────────┐ │
                    │  │ Web SPA │  │ REST API (v1)     │ │
                    │  │ React   │──│ Node.js/Express   │ │
                    │  └─────────┘  └────────┬─────────┘ │
                    │                        │            │
                    │  ┌─────────────┬───────┘            │
                    │  │             │                     │
                    │  ▼             ▼                     │
                    │  MySQL 8.0    Redis 7                │
                    │  (Primary)    (Cache)                │
                    └─────────────────────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │       INTERNAL CONSUMERS            │
                    │                                     │
                    │  Warehouse Staff (tablet/barcode)   │
                    │  Store Managers (dashboard/reports)  │
                    │  Admin (user mgmt, config)          │
                    └─────────────────────────────────────┘
```

---

## 3. Network Architecture

### 3.1 AWS VPC Design (Phase 08)

```
Region: us-west-2
VPC: 10.0.0.0/16

┌──────────────────────────────────────────────────────────────┐
│                          VPC                                  │
│                                                              │
│  ┌── AZ-a ──────────┐ ┌── AZ-b ──────────┐ ┌── AZ-c ─────┐│
│  │                   │ │                   │ │              ││
│  │ Public 10.0.0.0/24│ │ Public 10.0.1.0/24│ │ Pub .2.0/24 ││
│  │ [ALB] [NAT]       │ │ [ALB]             │ │ [ALB]       ││
│  │                   │ │                   │ │              ││
│  │ App  10.0.10.0/24 │ │ App  10.0.11.0/24 │ │ App .12/24  ││
│  │ [ECS Tasks]       │ │ [ECS Tasks]        │ │ [ECS]       ││
│  │                   │ │                   │ │              ││
│  │ Data 10.0.20.0/24 │ │ Data 10.0.21.0/24 │ │ Data .22/24 ││
│  │ [RDS Primary]     │ │ [RDS Standby]      │ │ [Redis]     ││
│  └───────────────────┘ └───────────────────┘ └──────────────┘│
│                                                              │
│  Route: Public → IGW       Security Groups:                  │
│  Route: App    → NAT GW   ALB: 80,443 ← 0.0.0.0/0          │
│  Route: Data   → (none)   ECS: 3000 ← ALB SG only           │
│                            RDS: 3306 ← ECS SG only           │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 On-Premises Network (Phase 07)

```
Internet ── ISP (1G Fiber + 500M Cable backup)
               │
         Palo Alto PA-850 (Zone-Based Firewall)
               │
    ┌──────────┼──────────────────────────────────┐
    │          │                                   │
  DMZ          Core Switch (Cisco Cat 9300 Stack)
  VLAN 100     │
  172.16.0/24  ├── VLAN 10: Management  10.0.10/24
               ├── VLAN 20: Corporate   10.0.20/24
               ├── VLAN 30: Servers     10.0.30/24
               ├── VLAN 40: VoIP        10.0.40/24
               ├── VLAN 50: Guest       10.0.50/24 (isolated)
               └── VLAN 60: IoT/Cameras 10.0.60/24 (no internet)
```

---

## 4. Application Architecture

### 4.1 API Layer Design

```
Request Flow:

  Client Request
       │
       ▼
  ┌─ Rate Limiter ─┐  429 Too Many Requests
       │
       ▼
  ┌─ CORS ─────────┐  Access-Control headers
       │
       ▼
  ┌─ Auth Middleware ┐  401 Unauthorized / 403 Forbidden
  │  JWT validation  │
  │  Role checking   │
       │
       ▼
  ┌─ Input Validation┐  400 Bad Request
  │  Schema (Zod/Joi)│
       │
       ▼
  ┌─ Route Handler ──┐  Business logic
  │  Service layer   │
  │  DB queries      │
       │
       ▼
  ┌─ Response ───────┐  200/201/204 + JSON body
  │  Structured JSON │
  │  Pagination meta │
  └──────────────────┘
```

### 4.2 Data Flow

| Flow | Path | Latency |
|------|------|---------|
| Product search | Client → CDN → ALB → ECS → Redis (cache hit) | ~15ms |
| Product search (miss) | Client → ALB → ECS → MySQL → Redis (cache set) → Response | ~50ms |
| Stock intake | Client → ALB → ECS → MySQL (write) → WebSocket broadcast | ~80ms |
| Report generation | Client → ALB → ECS → RDS Read Replica → S3 (PDF) | ~5s |
| Authentication | Client → ALB → ECS → MySQL (verify) → JWT issued | ~100ms |

---

## 5. Data Architecture (Phase 04)

### 5.1 Schema Overview

```
categories ──1:M──▶ products ◀──M:1── suppliers
                       │
              ┌────────┼────────┐
              │        │        │
           1:M│     1:M│     1:M│
              ▼        ▼        ▼
         order_items reviews  inventory_log
              │
           M:1│
              ▼
           orders ──M:1──▶ customers ──1:M──▶ addresses
```

### 5.2 Storage Estimates (Year 1)

| Table | Row Size | Rows/Year | Annual Size | Index Size |
|-------|----------|-----------|-------------|------------|
| products | ~500 B | 5,000 | 2.5 MB | 1 MB |
| orders | ~200 B | 10,000 | 2 MB | 1.5 MB |
| order_items | ~100 B | 30,000 | 3 MB | 2 MB |
| inventory_log | ~150 B | 500,000 | 75 MB | 30 MB |
| audit_log | ~300 B | 1,000,000 | 300 MB | 100 MB |
| **Total** | | | **~380 MB** | **~135 MB** |

---

## 6. Security Architecture (Phase 07)

### 6.1 Security Layers

```
Layer 1: Edge          AWS WAF — SQL injection, XSS, rate limiting
Layer 2: Transport     TLS 1.3 — all connections encrypted
Layer 3: Network       Security Groups — port-level firewall
Layer 4: Application   JWT + RBAC — authentication & authorization
Layer 5: Data          AES-256 at rest — RDS, S3, EBS encryption
Layer 6: Secrets       AWS Secrets Manager — auto-rotating credentials
Layer 7: Audit         CloudWatch + VPC Flow Logs — full observability
```

### 6.2 RBAC Matrix

| Permission | Admin | Manager | Staff | Viewer |
|-----------|-------|---------|-------|--------|
| View products | Yes | Yes | Yes | Yes |
| Modify products | Yes | Yes | No | No |
| Delete products | Yes | No | No | No |
| Process stock intake | Yes | Yes | Yes | No |
| Create purchase orders | Yes | Yes | No | No |
| Generate reports | Yes | Yes | No | No |
| Manage users | Yes | No | No | No |
| System configuration | Yes | No | No | No |

---

## 7. DevOps Architecture (Phase 08)

### 7.1 CI/CD Pipeline

```
┌─────────┐   ┌──────┐   ┌──────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│  Push   │──▶│ Lint │──▶│Unit Tests│──▶│Int Test│──▶│ Build  │──▶│Deploy  │
│  to     │   │ ESLint│  │ Jest 87% │   │MySQL   │   │Docker  │   │ECS     │
│  main   │   │ tsc   │  │ coverage │   │Redis   │   │Scout   │   │Rolling │
└─────────┘   └──────┘   └──────────┘   └────────┘   └────────┘   └────────┘
                                                                       │
                                                          ┌────────────┘
                                                          ▼
                                                    ┌──────────┐
                                                    │Health    │──▶ Pass: Done
                                                    │Check     │──▶ Fail: Auto-rollback
                                                    └──────────┘
```

### 7.2 Environment Strategy

| Environment | Purpose | Infrastructure | Data |
|------------|---------|---------------|------|
| Local | Development | Docker Compose (5 services) | Seed data |
| Staging | QA / Pre-prod | Terraform (scaled-down) | Sanitized production copy |
| Production | Live system | Terraform (full spec) | Real data |

---

## 8. Observability

| Signal | Tool | Retention | Alert Threshold |
|--------|------|-----------|----------------|
| Metrics | CloudWatch | 15 months | CPU > 80%, Memory > 85% |
| Logs | CloudWatch Logs | 30 days | Error rate > 1% in 5 min |
| Traces | AWS X-Ray | 30 days | P99 latency > 2s |
| Uptime | External monitor | Indefinite | Any downtime |
| Network | VPC Flow Logs | 30 days | Anomalous traffic patterns |
| Security | Nessus | Per-scan | Any critical/high finding |

---

## 9. Disaster Recovery

| Metric | Objective | Implementation |
|--------|-----------|---------------|
| **RPO** | 15 minutes | RDS continuous backup, S3 versioning |
| **RTO** | 1 hour | Multi-AZ failover, ECS auto-recovery |
| **Backup** | Daily automated | RDS snapshots (30-day retention) |
| **Cross-Region** | Weekly | Snapshot replication to us-east-1 |
| **Runbook** | Documented | Step-by-step recovery procedures |
