# FLLC Enterprise IT Infrastructure

**Architect & Lead Engineer:** Preston Furulie
**Organization:** FLLC (Find You Person)
**Status:** Active Development | 9 Phases Complete
**Repository:** [`github.com/Personfu/Python`](https://github.com/Personfu/Python)

---

## Mission

Build and document FLLC's complete enterprise IT infrastructure from the ground up — spanning computing foundations, software engineering, web platforms, data architecture, algorithm libraries, systems design, cybersecurity, cloud/DevOps, and a production-ready enterprise platform. Every artifact in this repository is a working, production-quality deliverable.

---

## Enterprise Phase Map

| Phase | Department | Directory | Deliverables | Status |
|-------|-----------|-----------|-------------|--------|
| **01** | IT Foundations | [`CIS120/`](CIS120/) | Hardware architecture, number systems, algorithm theory | Complete |
| **02** | Software Engineering | [`CIS133/`](CIS133/) | 8 production modules: I/O, control flow, OOP, file systems | Complete |
| **03** | Web Platform Engineering | [`CIS195/`](CIS195/) | Portfolio SPA, DOM framework, responsive system, API client | Complete |
| **04** | Data Architecture | [`CIS233/`](CIS233/) | 7 SQL exercises, ER design, views, stored procedures | Complete |
| **05** | Core Algorithm Library | [`CIS275/`](CIS275/) | Linked lists, BST, 7 sorting algorithms, graph engine | Complete |
| **06** | Systems Analysis & PM | [`CIS310/`](CIS310/) | SRS, use cases, three-tier architecture proposal | Complete |
| **07** | Information Security | [`CIS350/`](CIS350/) | Encryption toolkit, network topology, vuln assessment, firewall | Complete |
| **08** | Cloud & DevOps | [`CIS410/`](CIS410/) | Terraform IaC, Docker, CI/CD pipeline, AWS infrastructure | Complete |
| **09** | Enterprise Platform | [`CIS425/`](CIS425/) | REST API, production schema, deployment architecture, capstone | Complete |

---

## Architecture at a Glance

```
┌──────────────────────────────────────────────────────────────────────┐
│                     FLLC ENTERPRISE STACK                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─ Phase 03 ─────────┐     ┌─ Phase 09 ─────────────────────────┐  │
│  │  Web Platform       │────▶│  Enterprise Platform (REST API)    │  │
│  │  React SPA / CDN    │     │  Node.js + Express on ECS Fargate  │  │
│  └─────────────────────┘     └──────────┬────────────────────────┘  │
│                                         │                            │
│  ┌─ Phase 07 ─────────┐     ┌──────────▼────────────────────────┐  │
│  │  Security Layer     │────▶│  Phase 04: Data Architecture      │  │
│  │  WAF / TLS / RBAC   │     │  MySQL 8.0 Multi-AZ (RDS)         │  │
│  └─────────────────────┘     │  Redis Cache (ElastiCache)        │  │
│                               └──────────────────────────────────┘  │
│  ┌─ Phase 08 ─────────┐     ┌───────────────────────────────────┐  │
│  │  Cloud / DevOps     │────▶│  Phase 01: Foundations            │  │
│  │  Terraform / CI/CD  │     │  Hardware + Binary + Algorithms   │  │
│  │  Docker / AWS       │     └───────────────────────────────────┘  │
│  └─────────────────────┘                                             │
│                               ┌───────────────────────────────────┐  │
│  ┌─ Phase 06 ─────────┐     │  Phase 05: Core Engineering       │  │
│  │  Systems Analysis   │────▶│  Data Structures + Algorithms     │  │
│  │  SRS / Use Cases    │     │  O(n log n) sorting, Dijkstra's   │  │
│  └─────────────────────┘     └───────────────────────────────────┘  │
│                                                                      │
│  ┌─ Phase 02 ────────────────────────────────────────────────────┐  │
│  │  Software Engineering: Python modules, OOP, File I/O, Tests   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Technology Matrix

| Domain | Technologies | Phase |
|--------|-------------|-------|
| **Languages** | Python 3.12, JavaScript (ES2024), TypeScript, SQL, HCL, YAML | 02-09 |
| **Frontend** | React 18, Tailwind CSS, HTML5, CSS3 (Grid/Flexbox) | 03 |
| **Backend** | Node.js 20, Express.js, Python `http.server` | 02, 09 |
| **Database** | MySQL 8.0, Redis 7, Prisma ORM | 04, 09 |
| **Infrastructure** | AWS (VPC, ECS Fargate, RDS, S3, CloudFront, ALB, Route 53) | 08, 09 |
| **IaC** | Terraform 1.5+ (S3 backend, DynamoDB locking) | 08 |
| **Containers** | Docker (multi-stage), Docker Compose, ECR | 08 |
| **CI/CD** | GitHub Actions (6-stage pipeline with rollback) | 08 |
| **Security** | SHA-256/HMAC/PBKDF2, JWT (RS256), RBAC, TLS 1.3, WAF | 07 |
| **Networking** | Palo Alto PA-850, VLANs, DMZ, SNMP v3, 802.1X | 07 |
| **Monitoring** | CloudWatch, VPC Flow Logs, Nessus, PRTG | 07, 08 |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Personfu/Python.git
cd Python

# Run any Python module directly
python CIS133/5_loops_and_iteration.py
python CIS275/sorting_algorithms.py
python CIS350/encryption_hashing.py

# Start the REST API server
python CIS425/api_server.py
# → http://localhost:8080/api/products

# View the coursework portal
# Open index.html in a browser

# SQL exercises require MySQL 8.0 with my_guitar_shop database
mysql -u root -p < CIS425/schema.sql
```

---

## Project Documentation

| Document | Path | Description |
|----------|------|-------------|
| Enterprise Architecture | [`ARCHITECTURE.md`](ARCHITECTURE.md) | Full infrastructure design, data flow, security model |
| Project Charter | [`docs/project-charter.md`](docs/project-charter.md) | Scope, objectives, stakeholders, success criteria |
| Enterprise Roadmap | [`docs/enterprise-roadmap.md`](docs/enterprise-roadmap.md) | 9-phase timeline with milestones and deliverables |
| Engineering Standards | [`docs/coding-standards.md`](docs/coding-standards.md) | Code style, review process, testing requirements |
| Security Policy | [`docs/security-policy.md`](docs/security-policy.md) | InfoSec policies, encryption standards, access control |

---

## Coursework Compliance

This repository serves dual purpose: FLLC enterprise infrastructure **and** PCC coursework deliverables. Each phase maps to a CIS course:

| Phase | Course | Assignment Coverage |
|-------|--------|-------------------|
| 01 | CIS 120 — Intro to Computing | Hardware fundamentals, binary systems, algorithm theory |
| 02 | CIS 133 — Intro to Programming | 8 Python assignments (I/O, variables, strings, branching, loops, functions, file I/O, OOP) |
| 03 | CIS 195 — Web Development | HTML5 portfolio, JavaScript DOM, CSS responsive design, REST API integration |
| 04 | CIS 233 — Database Management | 7 MySQL exercises (DDL, SELECT/WHERE, aggregates, JOINs, DML, subqueries, views/procedures) + ER design |
| 05 | CIS 275 — Data Structures | Linked lists, BST, sorting algorithms, graph traversal |
| 06 | CIS 310 — Systems Analysis | SRS document, use case diagrams, system architecture |
| 07 | CIS 350 — Network & Cybersecurity | Encryption/hashing, network topology, vulnerability assessment, firewall rules |
| 08 | CIS 410 — Cloud & DevOps | Terraform VPC, Dockerfile, Docker Compose, GitHub Actions CI/CD, AWS infrastructure |
| 09 | CIS 425 — Capstone | Project proposal, production schema, REST API, API docs, deployment architecture, final presentation |

---

## Repository Stats

- **63 files** across 9 enterprise phases
- **~12,000 lines** of production code and documentation
- **6 languages:** Python, JavaScript, SQL, HCL (Terraform), YAML, CSS
- **10 normalized database tables** in 3NF
- **7 sorting algorithms** benchmarked
- **15 REST API endpoints** with auth and pagination
- **Full CI/CD pipeline** with automated rollback

---

## License

Internal FLLC project. Academic use at Portland Community College.

**Author:** Preston Furulie | **Organization:** FLLC | **Year:** 2026
