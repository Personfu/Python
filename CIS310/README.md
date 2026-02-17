# Phase 06 — Systems Analysis & Project Management
**Department:** Project Management Office | **Course:** CIS 310 — Systems Analysis & Design | **Status:** Complete

---

## Purpose

Define FLLC's enterprise system through formal requirements engineering, use case analysis, and architecture design. These artifacts serve as the blueprint for the enterprise platform built in Phase 09 and the infrastructure deployed in Phase 08.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`requirements_document.md`](requirements_document.md) | Software Requirements Specification (SRS) | 40+ requirements (MoSCoW priority), document control, stakeholder analysis, FR/NFR tables (performance, availability, security, scalability, usability), RBAC permissions matrix, acceptance criteria |
| [`use_cases.md`](use_cases.md) | Use Case Documentation (6 use cases) | UC-01 Process Stock Intake (main/alternative/exception flows, business rules), UC-02 Generate Report, UC-03 Manage Product Catalog, UC-04 Create Purchase Order, UC-05 User Authentication, UC-06 Search Inventory — with actor/system columns and trigger conditions |
| [`system_architecture.md`](system_architecture.md) | System Architecture Design Document | Three-tier architecture (ASCII diagram), design principles table, technology stack justification, API route table (12 endpoints), middleware pipeline, caching strategy (5 layers), database backup/recovery (RPO/RTO), security architecture (7 layers), monitoring stack, CI/CD pipeline, environment strategy, scaling plan |

## Enterprise Application

- SRS requirements directly map to API endpoints in **Phase 09**
- Architecture design is implemented via Terraform in **Phase 08**
- Use cases define the test scenarios for integration testing
- RBAC matrix is enforced in the API auth middleware
