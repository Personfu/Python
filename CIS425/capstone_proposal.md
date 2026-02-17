# Capstone Project Proposal
## CIS 425 — Capstone | Preston Furulie

---

## 1. Project Overview

| Field            | Detail                                               |
|------------------|------------------------------------------------------|
| **Project Title**| Guitar Shop Enterprise Platform                      |
| **Student**      | Preston Furulie                                      |
| **Course**       | CIS 425 — Capstone Project                           |
| **Semester**     | Spring 2026                                          |
| **Advisor**      | CIS Department Faculty                               |
| **Duration**     | 16 weeks (February — May 2026)                       |

---

## 2. Problem Statement

The Guitar Shop currently manages inventory using Excel spreadsheets shared via email between three locations. This approach suffers from:

- **Data inconsistency** — multiple copies of the spreadsheet lead to version conflicts
- **No real-time visibility** — managers cannot see current stock levels across locations
- **Manual order processing** — purchase orders are created by hand, increasing errors
- **No audit trail** — stock adjustments cannot be traced to specific users or events
- **Reporting limitations** — generating financial reports requires manual data aggregation
- **Security gaps** — spreadsheets contain no access control or password protection

**Business Impact:** An estimated $15,000/year in losses from over-ordering, stock-outs, and labor spent on manual data reconciliation.

---

## 3. Proposed Solution

Build a **web-based inventory management platform** that provides:

### Core Features
1. **Real-time inventory tracking** across all locations with barcode scanning
2. **Automated purchase order generation** when stock falls below reorder points
3. **Role-based access control** (Admin, Manager, Staff, Viewer)
4. **Comprehensive reporting** dashboard with stock levels, movement, and valuation
5. **RESTful API** for integration with POS systems and supplier portals
6. **Audit logging** of all data modifications for compliance

### Differentiators
- Mobile-responsive design for tablet use on the warehouse floor
- Sub-second barcode scan response time
- Real-time WebSocket updates across all connected clients
- Exportable reports in PDF and CSV formats

---

## 4. Technology Stack

| Layer          | Technology            | Justification                                |
|----------------|-----------------------|----------------------------------------------|
| Frontend       | React 18 + TypeScript | Component-based, strong typing, large ecosystem|
| Styling        | Tailwind CSS          | Utility-first, rapid UI development           |
| API Server     | Node.js + Express     | JavaScript full-stack, async I/O              |
| Database       | MySQL 8.0             | Relational integrity, course alignment        |
| Cache          | Redis 7               | Session storage, query caching                |
| Containerization| Docker + Compose     | Consistent dev/prod environments              |
| CI/CD          | GitHub Actions         | Automated testing and deployment              |
| Cloud Hosting  | AWS (ECS, RDS, S3)    | Industry standard, scalable                   |
| IaC            | Terraform             | Reproducible infrastructure                   |

---

## 5. System Architecture

```
                ┌─────────────────────┐
                │   React SPA (CDN)   │
                └──────────┬──────────┘
                           │ HTTPS
                           ▼
                ┌─────────────────────┐
                │   AWS ALB           │
                └──────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │ ECS Task 1│   │ ECS Task 2│   │ ECS Task N│
    │ (Node.js) │   │ (Node.js) │   │ (Node.js) │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │                │                │
          └────────┬───────┘────────────────┘
                   │
          ┌────────┼────────┐
          ▼                 ▼
    ┌───────────┐    ┌───────────┐
    │ RDS MySQL │    │   Redis   │
    │ Multi-AZ  │    │  Cache    │
    └───────────┘    └───────────┘
```

---

## 6. Database Design (Simplified)

**10 tables in 3NF:**

| Table            | Records (est.) | Key Relationships                    |
|------------------|----------------|--------------------------------------|
| categories       | 20             | Parent of products                   |
| products         | 5,000          | Belongs to category and supplier     |
| suppliers        | 50             | Parent of products                   |
| customers        | 2,000          | Parent of orders and addresses       |
| addresses        | 3,000          | Belongs to customer                  |
| orders           | 10,000         | Belongs to customer, has order_items  |
| order_items      | 30,000         | Belongs to order and product         |
| inventory_log    | 100,000/year   | References product                   |
| reviews          | 5,000          | Belongs to product and customer      |
| users            | 100            | System users (RBAC)                  |

---

## 7. Project Timeline

| Week  | Phase              | Deliverables                                    |
|-------|--------------------|-------------------------------------------------|
| 1-2   | Planning           | Requirements doc, ER diagram, wireframes         |
| 3-4   | Database           | Schema DDL, seed data, stored procedures         |
| 5-7   | Backend API        | REST endpoints, auth, validation, testing        |
| 8-10  | Frontend           | React components, routing, state management      |
| 11-12 | Integration        | API integration, barcode scanning, reporting     |
| 13    | DevOps             | Docker, CI/CD pipeline, Terraform, deployment    |
| 14    | Testing            | UAT, performance testing, security review        |
| 15    | Documentation      | API docs, user manual, deployment guide          |
| 16    | Presentation       | Final demo, code review, project submission      |

---

## 8. Risk Assessment

| Risk                           | Probability | Impact | Mitigation                              |
|--------------------------------|-------------|--------|-----------------------------------------|
| Database performance issues    | Medium      | High   | Indexing strategy, read replicas, caching|
| Scope creep                    | High        | Medium | Fixed feature set per sprint, backlog   |
| Security vulnerabilities       | Medium      | High   | OWASP checklist, automated scanning     |
| AWS cost overruns              | Low         | Medium | Budget alerts, right-sized instances    |
| Schedule delays                | Medium      | High   | 2-week buffer, weekly progress reviews  |

---

## 9. Success Criteria

| Metric                         | Target                                |
|--------------------------------|---------------------------------------|
| Core features completed        | 100% of Must-Have requirements        |
| Unit test coverage             | ≥ 80%                                 |
| API response time              | < 500ms (95th percentile)             |
| Page load time                 | < 2 seconds                           |
| Security scan                  | Zero critical/high findings           |
| Database normalization         | 3NF with documented exceptions        |
| Documentation                  | API docs, deployment guide, user manual|
| Code quality                   | Zero linting errors, consistent style |

---

## 10. Skills Demonstrated

This capstone integrates skills from the entire CIS curriculum:

| Course   | Skills Applied                                        |
|----------|------------------------------------------------------|
| CIS 120  | Computing fundamentals, binary/data representation    |
| CIS 133  | Python programming, algorithms, OOP                   |
| CIS 195  | HTML/CSS/JS, responsive design, REST API integration  |
| CIS 233  | Database design, SQL (DDL, DML, JOINs, procedures)    |
| CIS 275  | Data structures, algorithm efficiency (Big-O)         |
| CIS 310  | Requirements analysis, use cases, system architecture |
| CIS 350  | Network security, encryption, vulnerability assessment|
| CIS 410  | Docker, CI/CD, Terraform, AWS cloud deployment        |
