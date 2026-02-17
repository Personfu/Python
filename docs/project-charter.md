# FLLC Enterprise IT — Project Charter
**Document Owner:** Preston Furulie | **Approved:** February 2026

---

## 1. Project Identity

| Field | Value |
|-------|-------|
| **Project Name** | FLLC Enterprise IT Infrastructure |
| **Project Code** | FLLC-IT-2026 |
| **Sponsor** | FLLC Executive Leadership |
| **Project Lead** | Preston Furulie |
| **Start Date** | January 2025 |
| **Target Completion** | May 2026 |
| **Methodology** | Agile (2-month sprints, 9 phases) |

---

## 2. Business Objective

Establish FLLC's complete enterprise IT capability from zero — delivering production-grade infrastructure, application platforms, security frameworks, and operational tooling that enables the organization to operate at scale with industry-standard practices.

### Success Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| Infrastructure uptime | 99.9% | CloudWatch monitoring |
| API response time (P95) | < 500ms | Performance benchmarks |
| Security posture | Zero critical findings | Quarterly Nessus scans |
| Code quality | 80%+ test coverage | CI/CD pipeline metrics |
| Deployment frequency | On-demand (< 15 min) | Pipeline execution time |
| Mean time to recovery | < 1 hour | Incident post-mortems |

---

## 3. Scope

### In Scope (9 Phases)

| Phase | Scope | Key Deliverables |
|-------|-------|-----------------|
| 01 — IT Foundations | Computing theory, number systems, algorithm fundamentals | Reference documentation, conversion tools |
| 02 — Software Engineering | Core Python engineering: I/O, control flow, data structures, OOP | 8 production modules with full documentation |
| 03 — Web Platform | Frontend architecture: HTML5, CSS3, JavaScript, REST client | Portfolio SPA, DOM framework, responsive system, API client |
| 04 — Data Architecture | Relational database design, SQL mastery, stored procedures | 7 SQL exercises, ER schema, views, procedures |
| 05 — Core Engineering | Algorithm library: data structures, sorting, graph traversal | 4 fully-tested algorithm implementations |
| 06 — Systems Analysis | Project management artifacts, requirements engineering | SRS, use cases, architecture design document |
| 07 — Information Security | Cybersecurity framework: encryption, network security, compliance | Encryption toolkit, network topology, vuln assessment, firewall config |
| 08 — Cloud & DevOps | Infrastructure as Code, containerization, CI/CD automation | Terraform configs, Dockerfile, Docker Compose, GitHub Actions pipeline |
| 09 — Enterprise Platform | Production application: REST API, database, deployment, documentation | Full-stack platform with auth, CRUD, reporting |

### Out of Scope
- Physical hardware procurement and installation
- Third-party vendor contract negotiation
- End-user training program delivery
- Mobile native application development (future phase)

---

## 4. Stakeholders

| Role | Responsibility | Authority Level |
|------|---------------|----------------|
| **Project Lead** (Preston Furulie) | Architecture, development, documentation, delivery | Full technical authority |
| **Executive Sponsor** (FLLC Leadership) | Budget approval, strategic direction | Go/no-go decisions |
| **Academic Advisor** (PCC CIS Faculty) | Coursework compliance review | Grade approval |
| **Operations Team** | Production environment management | Change approval |
| **Security Officer** | Security policy review and enforcement | Veto on security gaps |

---

## 5. Constraints

| Type | Constraint |
|------|-----------|
| **Budget** | AWS Free Tier + minimal paid services |
| **Timeline** | 16-month delivery window (Jan 2025 — May 2026) |
| **Academic** | All deliverables must satisfy PCC CIS course rubrics |
| **Technology** | Python, JavaScript, MySQL as primary stack (course alignment) |
| **Compliance** | OWASP Top 10, NIST CSF framework alignment |

---

## 6. Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Scope creep across 9 phases | High | Medium | Fixed deliverable list per phase; backlog for future work |
| AWS cost overruns | Low | Medium | Budget alerts at $25, $50, $100; right-sized instances |
| Security vulnerabilities in production | Medium | High | Automated scanning in CI/CD; quarterly manual review |
| Single point of failure (one developer) | High | High | Comprehensive documentation; infrastructure as code |
| Academic deadline conflicts | Medium | Medium | 2-week buffer per phase; prioritize coursework compliance |

---

## 7. Communication Plan

| Communication | Frequency | Audience | Medium |
|--------------|-----------|----------|--------|
| Code commits | Daily | All stakeholders | GitHub |
| Phase completion report | Per phase | Academic advisor | Course submission |
| Architecture reviews | Per phase | FLLC leadership | Documentation |
| Security assessments | Quarterly | Security officer | Nessus report |
| Project status | Weekly | Self-assessment | TODO tracking |

---

## 8. Acceptance Criteria

A phase is considered complete when:

1. All deliverables listed in the phase scope are committed to the repository
2. Code passes linting with zero errors
3. Python modules execute without runtime errors
4. SQL scripts execute successfully against the target database
5. Documentation is complete and internally consistent
6. Academic rubric requirements are satisfied
7. No known critical or high security issues remain
