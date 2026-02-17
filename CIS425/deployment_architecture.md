# FLLC Enterprise Platform — Deployment Architecture
## CIS 425 — Capstone | Preston Furulie

---

## 1. Production Environment Overview

| Field | Value |
|-------|-------|
| **Cloud Provider** | AWS (us-west-2, Oregon) |
| **Infrastructure** | Terraform-managed (version-controlled IaC) |
| **CI/CD** | GitHub Actions (6-stage pipeline) |
| **Container Registry** | Amazon ECR (private) |
| **DNS** | AWS Route 53 (health-checked records) |
| **TLS Certificates** | AWS Certificate Manager (auto-renewal) |

---

## 2. AWS Service Inventory

| Service | Component | Specification | Monthly Cost (est.) |
|---------|-----------|---------------|-------------------|
| **CloudFront** | CDN / Static assets | React SPA, edge caching | $2 |
| **ALB** | Load Balancer | TLS termination, health checks, path routing | $18 |
| **ECS Fargate** | API Containers | 2 tasks (0.5 vCPU, 1 GB), auto-scale 2-8 | $30 |
| **ECR** | Image Registry | Docker images with lifecycle policy | $1 |
| **RDS MySQL** | Primary Database | db.t3.medium, Multi-AZ, 50 GB encrypted | $65 |
| **RDS Replica** | Read Replica | db.t3.small (reporting queries) | $25 |
| **ElastiCache** | Redis Cache | cache.t3.micro, session + query cache | $13 |
| **S3** | Object Storage | File uploads, report PDFs, backups | $3 |
| **Route 53** | DNS | Health-checked A/AAAA records | $1 |
| **CloudWatch** | Monitoring | Metrics, logs, alarms, dashboards | $10 |
| **Secrets Manager** | Credentials | DB passwords, API keys (auto-rotate) | $2 |
| **WAF** | Web Firewall | SQL injection, XSS, rate limiting rules | $6 |
| | | **Estimated Total** | **~$176/mo** |

---

## 3. Network Architecture

### VPC Layout (10.0.0.0/16)

```
┌─────────────────────────────────────────────────────────────────┐
│                     VPC: 10.0.0.0/16                            │
│                                                                 │
│  ┌── us-west-2a ──────┐ ┌── us-west-2b ──────┐ ┌── 2c ──────┐│
│  │                     │ │                     │ │             ││
│  │ Public 10.0.0.0/24  │ │ Public 10.0.1.0/24  │ │ Pub .2.0/24││
│  │ ┌─────────────────┐ │ │ ┌─────────────────┐ │ │ ┌────────┐││
│  │ │ ALB Endpoint    │ │ │ │ ALB Endpoint    │ │ │ │ ALB    │││
│  │ │ NAT Gateway     │ │ │ │                 │ │ │ │        │││
│  │ └─────────────────┘ │ │ └─────────────────┘ │ │ └────────┘││
│  │                     │ │                     │ │             ││
│  │ App  10.0.10.0/24   │ │ App  10.0.11.0/24   │ │ App .12/24 ││
│  │ ┌─────────────────┐ │ │ ┌─────────────────┐ │ │ ┌────────┐││
│  │ │ ECS Task (API)  │ │ │ │ ECS Task (API)  │ │ │ │ ECS    │││
│  │ │ Port 3000       │ │ │ │ Port 3000       │ │ │ │        │││
│  │ └─────────────────┘ │ │ └─────────────────┘ │ │ └────────┘││
│  │                     │ │                     │ │             ││
│  │ Data 10.0.20.0/24   │ │ Data 10.0.21.0/24   │ │ Data .22/24││
│  │ ┌─────────────────┐ │ │ ┌─────────────────┐ │ │ ┌────────┐││
│  │ │ RDS Primary     │ │ │ │ RDS Standby     │ │ │ │ Redis  │││
│  │ │ MySQL 8.0       │ │ │ │ (Auto-failover) │ │ │ │        │││
│  │ └─────────────────┘ │ │ └─────────────────┘ │ │ └────────┘││
│  └─────────────────────┘ └─────────────────────┘ └────────────┘│
│                                                                 │
│  Security Groups:                                               │
│    ALB-SG:  80,443 ← 0.0.0.0/0                                 │
│    ECS-SG:  3000 ← ALB-SG only                                 │
│    RDS-SG:  3306 ← ECS-SG only                                 │
│    Redis-SG: 6379 ← ECS-SG only                                │
└─────────────────────────────────────────────────────────────────┘
```

### Traffic Flow

```
User → CloudFront (CDN) → Static assets (S3)
                        → ALB (dynamic /api/* requests)
                            → ECS Task (Node.js)
                                → Redis (cache hit? return)
                                → RDS MySQL (cache miss? query → cache → return)
```

| Flow | Path | Latency |
|------|------|---------|
| Static asset | User → CloudFront edge | ~5ms |
| API (cache hit) | User → ALB → ECS → Redis | ~15ms |
| API (cache miss) | User → ALB → ECS → MySQL → Redis set | ~50ms |
| Report generation | User → ALB → ECS → RDS read replica → S3 | ~5s |

---

## 4. CI/CD Pipeline

### Pipeline Stages

```
Push to main ──▶ Lint ──▶ Unit Tests ──▶ Integration Tests ──▶ Build ──▶ Deploy ──▶ Verify
                 2 min     3 min          4 min                 2 min     1 min       1 min
                                                                                Total: ~13 min
```

| Stage | Tool | Actions | Gate |
|-------|------|---------|------|
| **1. Lint** | ESLint + TypeScript | Style check, type errors | Zero errors |
| **2. Unit Tests** | Jest | 450+ test cases | ≥ 80% coverage |
| **3. Integration** | Jest + MySQL + Redis | API endpoint testing with real DB | All pass |
| **4. Build** | Docker | Multi-stage image build → ECR push | Image < 200 MB |
| **5. Security Scan** | Docker Scout | CVE scan of container image | Zero critical |
| **6. Deploy** | AWS ECS | Rolling update (min 50% healthy) | Health check pass |
| **7. Verify** | curl + jq | Smoke test: GET /health returns 200 | 3 consecutive passes |

### Rollback Strategy

```
Deploy fails? ──▶ Wait 10 minutes for stability
                    │
                    ├── Health check passes → Done (success)
                    │
                    └── Health check fails → Auto-rollback to previous task definition
                                            → Slack notification
                                            → Pipeline marked FAILED
```

---

## 5. Container Architecture

### Docker Image (Production)

```dockerfile
Stage 1: deps        → Install production npm packages (npm ci --omit=dev)
Stage 2: builder     → Build TypeScript, generate Prisma client
Stage 3: production  → Alpine base, non-root user, healthcheck
```

| Metric | Value |
|--------|-------|
| Base image | `node:20-alpine` |
| Final image size | 178 MB |
| User | `appuser` (non-root, UID 1001) |
| Health check | `wget -q --spider http://localhost:3000/health` (30s interval) |
| Exposed port | 3000 |

### ECS Task Definition

```json
{
    "cpu": 512,
    "memory": 1024,
    "containerDefinitions": [{
        "essential": true,
        "portMappings": [{"containerPort": 3000}],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/ecs/fllc-api",
                "awslogs-region": "us-west-2"
            }
        }
    }]
}
```

---

## 6. Monitoring & Alerting

### CloudWatch Dashboards

| Widget | Metrics | Threshold |
|--------|---------|-----------|
| API Latency | P50, P95, P99 response time | P95 > 500ms → Alarm |
| Error Rate | 4xx and 5xx response codes | 5xx > 1% in 5 min → Alarm |
| CPU Utilization | ECS task CPU % | > 80% for 5 min → Scale out |
| Memory | ECS task memory % | > 85% for 5 min → Alarm |
| Database | RDS connections, IOPS, replication lag | Connections > 80% → Alarm |
| Cache | Redis hit ratio, memory, evictions | Hit ratio < 80% → Investigate |

### Alarm Actions

| Severity | Action |
|----------|--------|
| Warning | CloudWatch → SNS → Email notification |
| Critical | CloudWatch → SNS → PagerDuty + Slack #incidents |
| Auto-resolve | Clear notification when metric returns to normal |

### Log Aggregation

```
ECS Tasks → CloudWatch Logs (/ecs/fllc-api)
           → Metric Filters (error patterns → custom metrics)
           → Log Insights (ad-hoc queries)
           → S3 export (90-day archive)
```

---

## 7. Scaling Strategy

### Horizontal Auto-Scaling

| Trigger | Action | Cooldown |
|---------|--------|----------|
| CPU > 70% for 3 min | Add 1 ECS task | 300s |
| CPU < 30% for 10 min | Remove 1 ECS task | 300s |
| Request count > 1000/min | Add 2 ECS tasks | 300s |

| Parameter | Value |
|-----------|-------|
| Minimum tasks | 2 |
| Maximum tasks | 8 |
| Desired tasks | 2 |

### Database Scaling

| Strategy | Implementation |
|----------|---------------|
| Vertical | RDS instance upgrade (db.t3.medium → db.r6g.large) |
| Read scaling | Read replica for reporting queries |
| Connection pooling | RDS Proxy (reuse connections, reduce overhead) |
| Query caching | Redis (TTL: 5 min for catalog, 60s for inventory) |

---

## 8. Disaster Recovery

| Metric | Target | Implementation |
|--------|--------|----------------|
| **RPO** | 15 minutes | RDS continuous backup + transaction logs |
| **RTO** | 1 hour | Multi-AZ failover + ECS auto-recovery |

### Backup Schedule

| Component | Method | Frequency | Retention |
|-----------|--------|-----------|-----------|
| RDS MySQL | Automated snapshots | Daily at 3:00 AM UTC | 30 days |
| RDS MySQL | Transaction logs | Continuous (5-min intervals) | 7 days |
| S3 objects | Cross-region replication | Real-time | Indefinite |
| Terraform state | S3 versioning | On every `terraform apply` | 90 days |
| Docker images | ECR lifecycle policy | On every push | Last 10 images |

### Recovery Procedures

| Scenario | Procedure | RTO |
|----------|-----------|-----|
| Single AZ failure | Automatic Multi-AZ failover (RDS + ECS) | ~5 min |
| Full region failure | Restore from cross-region snapshot + Terraform apply in us-east-1 | ~60 min |
| Data corruption | Point-in-time restore from RDS backup | ~30 min |
| Container failure | ECS auto-replaces unhealthy tasks | ~2 min |
| Pipeline failure | Auto-rollback to previous ECS task definition | ~5 min |

---

## 9. Security Controls

| Layer | Control | Implementation |
|-------|---------|----------------|
| Edge | AWS WAF | SQL injection, XSS, rate limiting, geo-blocking |
| Transport | TLS 1.3 | ACM certificate, HTTPS only, HSTS |
| Network | Security Groups | Port-level firewall (least privilege) |
| Application | JWT + RBAC | RS256 tokens, 4-tier role system |
| Data (transit) | TLS | All service-to-service encrypted |
| Data (at rest) | AES-256 | RDS, S3, EBS default encryption |
| Secrets | Secrets Manager | Auto-rotating DB credentials (90 days) |
| Audit | CloudTrail + CloudWatch | API call logging, VPC Flow Logs |

---

## 10. Environment Comparison

| Aspect | Local (Docker Compose) | Staging | Production |
|--------|----------------------|---------|------------|
| API instances | 1 container | 1 ECS task | 2-8 ECS tasks |
| Database | MySQL 8.0 (container) | RDS db.t3.micro | RDS db.t3.medium Multi-AZ |
| Cache | Redis 7 (container) | ElastiCache micro | ElastiCache micro |
| TLS | Self-signed / none | ACM certificate | ACM certificate |
| Domain | localhost:3000 | staging.fllc.internal | api.fllc.internal |
| Data | Seed data | Sanitized prod copy | Production |
| CI/CD | Manual | Auto-deploy on PR merge | Auto-deploy on main push |
| Monitoring | Docker logs | CloudWatch (basic) | CloudWatch + alerts |
