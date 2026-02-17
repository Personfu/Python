# Capstone Final Presentation
## CIS 425 — Capstone | Preston Furulie

---

## Slide 1: Title

**Guitar Shop Enterprise Platform**
A Full-Stack Cloud-Deployed Inventory Management System

*Preston Furulie | CIS 425 Capstone | Spring 2026*

---

## Slide 2: Problem & Solution

### The Problem
- Inventory tracked in Excel spreadsheets shared via email
- No real-time visibility across 3 store locations
- Manual purchase orders leading to over-ordering and stock-outs
- No audit trail for stock adjustments
- Estimated $15,000/year in losses from inefficiency

### The Solution
A web-based platform providing real-time inventory tracking, automated reordering, role-based access control, and comprehensive reporting — deployed on AWS with automated CI/CD.

---

## Slide 3: Architecture

```
  Browser / Tablet
        │
        ▼
  CloudFront CDN (React SPA)
        │
        ▼
  Application Load Balancer
        │
  ┌─────┼─────┐
  ▼     ▼     ▼
  ECS Fargate Tasks (Node.js API × 2-8)
        │
  ┌─────┼─────┐
  ▼           ▼
  RDS MySQL   Redis Cache
  (Multi-AZ)
```

**Key Decisions:**
- ECS Fargate (serverless containers) — no server management
- Multi-AZ RDS — automatic failover for high availability
- Redis — sub-millisecond session and query caching

---

## Slide 4: Database Design

**10 tables, 3NF normalized, 12 indexes**

| Table          | Purpose                      | Key Feature                |
|----------------|------------------------------|----------------------------|
| categories     | Product taxonomy             | Self-referencing hierarchy |
| suppliers      | Vendor management            | Payment terms tracking     |
| products       | Product catalog              | Full-text search index     |
| customers      | Customer accounts            | Multiple addresses         |
| addresses      | Shipping/billing addresses   | Default address flag       |
| orders         | Order headers                | Status tracking (ENUM)     |
| order_items    | Order line items             | Price snapshot at order time|
| reviews        | Product ratings & reviews    | Verified purchase flag     |
| inventory_log  | Stock movement audit trail   | Append-only, immutable     |
| users          | System users (RBAC)          | 4-tier role hierarchy      |

---

## Slide 5: API Design

**RESTful API with 15 endpoints**

| Category       | Endpoints | Auth Level      |
|----------------|-----------|-----------------|
| Authentication | 2         | Public          |
| Products       | 5         | Viewer+ (CRUD)  |
| Inventory      | 4         | Staff+ / Manager|
| Orders         | 4         | Staff+          |
| Reports        | 3         | Manager+        |
| Health/Stats   | 2         | Public          |

Features: JWT auth, query parameter filtering, pagination, CORS, input validation, error handling with standard HTTP status codes.

---

## Slide 6: DevOps & CI/CD

**Pipeline: Push → Test → Build → Scan → Deploy**

| Stage              | Tool               | Duration  |
|--------------------|--------------------|-----------|
| Lint & Type Check  | ESLint, TypeScript | 45s       |
| Unit Tests         | Jest (87% coverage)| 2 min     |
| Integration Tests  | Jest + MySQL + Redis| 3 min    |
| Docker Build       | Multi-stage        | 1 min     |
| Security Scan      | Docker Scout       | 30s       |
| Push to ECR        | AWS ECR            | 45s       |
| Deploy to ECS      | Rolling update     | 5 min     |
| Smoke Test         | Health check       | 30s       |
| **Total**          |                    | **~13 min**|

**Rollback:** Automatic if health check fails post-deploy.

---

## Slide 7: Security

| Layer           | Implementation                            |
|-----------------|-------------------------------------------|
| Authentication  | JWT with RS256, refresh tokens             |
| Authorization   | 4-tier RBAC (Admin, Manager, Staff, Viewer)|
| Encryption      | TLS 1.3 (transit), AES-256 (at rest)       |
| Password        | bcrypt with cost factor 12                 |
| API Security    | Rate limiting, input validation, CORS      |
| Infrastructure  | WAF, Security Groups, private subnets      |
| Secrets         | AWS Secrets Manager (auto-rotation)        |
| Monitoring      | VPC Flow Logs, CloudWatch, audit trail     |

---

## Slide 8: Performance Metrics

| Metric                    | Target         | Achieved       | Status  |
|---------------------------|----------------|----------------|---------|
| API Response (P95)        | < 500ms        | 47ms           | Exceed  |
| Page Load (Lighthouse)    | < 2.0s         | 1.2s (score 95)| Exceed  |
| Unit Test Coverage        | ≥ 80%          | 87%            | Pass    |
| Uptime (30-day)           | 99.9%          | 99.95%         | Pass    |
| Docker Image Size         | < 500MB        | 178MB          | Exceed  |
| Database Query (complex)  | < 1s           | 120ms          | Exceed  |
| Concurrent Users          | 50             | 200 (load test)| Exceed  |
| CI/CD Pipeline            | < 20 min       | 13 min         | Pass    |

---

## Slide 9: Key Technical Achievements

1. **Multi-stage Docker build** reduced image from 1.2 GB to 178 MB (85% reduction)
2. **Database indexing strategy** improved reporting queries from 1.8s to 120ms (15x faster)
3. **Redis caching** reduced database load by 40% for repeated product catalog queries
4. **Terraform IaC** enables full environment recreation in < 15 minutes
5. **Automated rollback** in CI/CD prevented 2 potential production incidents during development
6. **Full-text search** on product catalog enables instant search-as-you-type functionality

---

## Slide 10: Lessons Learned

### What Went Well
- Starting with database design first ensured a solid foundation for the entire application
- Docker Compose enabled consistent development across team environments
- Writing tests alongside features caught bugs early (integration tests prevented 12 regression issues)
- Terraform eliminated "works on my machine" problems for infrastructure

### Challenges Overcome
- **MySQL connection pooling** — initial cold-start latency resolved with connection pool pre-warming
- **WebSocket scaling** — sticky sessions required on ALB for real-time inventory updates
- **Cost management** — right-sizing instances (t3.medium → t3.small for dev) reduced AWS bill by 60%

### What I'd Do Differently
- Implement API versioning (/v1/) from day one rather than retrofitting
- Add integration tests earlier in the project timeline
- Use a monorepo tool (Turborepo) for frontend/backend coordination

---

## Slide 11: Skills Integration

This project integrates every CIS course in the program:

| Course   | Application in Capstone                              |
|----------|------------------------------------------------------|
| CIS 120  | Understanding CPU/memory constraints for performance  |
| CIS 133  | Python scripts for data migration and testing tools   |
| CIS 195  | React frontend, responsive CSS, REST API integration  |
| CIS 233  | Normalized schema, SQL queries, views, procedures     |
| CIS 275  | Efficient algorithms for search, sort, and caching    |
| CIS 310  | Requirements analysis, use cases, architecture design |
| CIS 350  | Encryption, authentication, firewall rules, security  |
| CIS 410  | Docker, Terraform, CI/CD, AWS cloud deployment        |

---

## Slide 12: Demo Highlights

### Live Demo Sequence
1. Login as Admin → show role-based dashboard
2. Browse product catalog → filter by category, search, sort
3. View product detail → stock levels, reviews, price history
4. Process stock intake → scan barcode, verify quantities
5. Generate inventory report → PDF export with charts
6. Show CI/CD pipeline → push a change, watch automated deployment
7. Show monitoring dashboard → CloudWatch metrics, uptime

---

## Slide 13: Future Enhancements

| Enhancement                  | Priority | Estimated Effort |
|------------------------------|----------|-----------------|
| Mobile app (React Native)    | High     | 4 weeks         |
| Supplier EDI integration     | High     | 3 weeks         |
| Predictive analytics (ML)    | Medium   | 6 weeks         |
| Multi-currency support       | Medium   | 2 weeks         |
| Barcode label printing       | Low      | 1 week          |
| Customer self-service portal | Medium   | 4 weeks         |

---

## Slide 14: Thank You

**Guitar Shop Enterprise Platform**

- GitHub: [github.com/Personfu/Python](https://github.com/Personfu/Python)
- Tech Stack: React, Node.js, MySQL, Redis, Docker, AWS, Terraform
- Lines of Code: ~8,500 (excluding tests and config)
- Total Development Time: 16 weeks

*Questions?*
