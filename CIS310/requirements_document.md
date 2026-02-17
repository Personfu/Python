# Software Requirements Specification (SRS)
## CIS 310 — Systems Analysis & Design | Preston Furulie

---

## Document Control

| Field       | Value                                  |
|-------------|----------------------------------------|
| Project     | Guitar Shop Inventory Management System |
| Version     | 2.0                                    |
| Author      | Preston Furulie                        |
| Date        | February 2026                          |
| Status      | Approved                               |
| Methodology | Agile / Iterative                      |

---

## 1. Introduction

### 1.1 Purpose
This document defines the complete functional and non-functional requirements for the Guitar Shop Inventory Management System (GSIMS). It serves as the primary reference for design, development, testing, and acceptance of the system.

### 1.2 Scope
GSIMS will replace the existing manual spreadsheet-based inventory tracking with a web-based system that provides real-time inventory visibility, automated alerts, comprehensive reporting, and multi-location support.

### 1.3 Stakeholders

| Role              | Name/Title          | Interest                              |
|-------------------|---------------------|---------------------------------------|
| Project Sponsor   | Store Owner         | ROI, business value                   |
| End Users         | Warehouse Staff     | Daily stock operations                |
| End Users         | Store Managers      | Reporting, oversight                  |
| System Admin      | IT Department       | Maintenance, security                 |
| External          | Suppliers           | Purchase order integration            |

### 1.4 Definitions & Acronyms

| Term   | Definition                                        |
|--------|---------------------------------------------------|
| SKU    | Stock Keeping Unit — unique product identifier    |
| PO     | Purchase Order — order placed with a supplier     |
| RBAC   | Role-Based Access Control                         |
| SLA    | Service Level Agreement                           |
| MTTR   | Mean Time To Recovery                             |
| RTO    | Recovery Time Objective                           |
| RPO    | Recovery Point Objective                          |

---

## 2. Overall System Description

### 2.1 System Context
GSIMS sits at the center of the retail operation, interfacing with:
- **POS System** — receives real-time sale deductions
- **Supplier Portal** — sends purchase orders, receives shipping notifications
- **Accounting System** — exports valuation data for financial reporting
- **Employee Directory** — imports user accounts for SSO authentication

### 2.2 Assumptions
- Users have modern web browsers (Chrome 100+, Firefox 100+, Edge 100+, Safari 16+)
- Warehouse has reliable Wi-Fi coverage for barcode scanner connectivity
- Supplier EDI (Electronic Data Interchange) standards are supported (ANSI X12 850/856)
- Organization uses Google Workspace or Microsoft 365 for SSO integration

### 2.3 Constraints
- Budget: $50,000 total development cost
- Timeline: 6-month delivery (3 sprints of 2 months each)
- Must run on existing AWS infrastructure
- Must comply with PCI-DSS for payment-adjacent data

---

## 3. Functional Requirements

### 3.1 Product Management

| ID     | Priority | Requirement                                                      |
|--------|----------|------------------------------------------------------------------|
| FR-01  | Must     | System shall maintain a product catalog with SKU, name, description, category, list price, cost, and supplier |
| FR-02  | Must     | System shall support CRUD operations on products with audit logging |
| FR-03  | Must     | System shall auto-generate unique SKU codes using format: CAT-NNNNN |
| FR-04  | Should   | System shall support product images (up to 5 per product, max 5 MB each) |
| FR-05  | Should   | System shall support product variants (size, color, finish)       |
| FR-06  | Could    | System shall support bulk import/export via CSV                   |

### 3.2 Inventory Tracking

| ID     | Priority | Requirement                                                      |
|--------|----------|------------------------------------------------------------------|
| FR-10  | Must     | System shall track real-time quantity on hand per product per location |
| FR-11  | Must     | System shall log every quantity change with timestamp, user, and reason |
| FR-12  | Must     | System shall generate low-stock alerts when quantity falls below configurable threshold |
| FR-13  | Must     | System shall support barcode scanning (Code 128, QR) for stock intake |
| FR-14  | Should   | System shall calculate reorder points based on average daily sales velocity |
| FR-15  | Should   | System shall support cycle counting with variance reporting       |
| FR-16  | Could    | System shall predict stock-out dates using linear trend analysis  |

### 3.3 Purchase Orders

| ID     | Priority | Requirement                                                      |
|--------|----------|------------------------------------------------------------------|
| FR-20  | Must     | System shall generate purchase orders to suppliers                |
| FR-21  | Must     | System shall track PO status (draft, submitted, acknowledged, received, closed) |
| FR-22  | Should   | System shall auto-generate POs when inventory hits reorder point  |
| FR-23  | Could    | System shall support partial receiving against a PO               |

### 3.4 Reporting

| ID     | Priority | Requirement                                                      |
|--------|----------|------------------------------------------------------------------|
| FR-30  | Must     | System shall generate inventory valuation report (FIFO, weighted average) |
| FR-31  | Must     | System shall generate stock movement report by date range         |
| FR-32  | Should   | System shall provide dashboard with KPIs: turnover rate, days-of-supply, stock accuracy |
| FR-33  | Should   | System shall export reports in PDF and CSV formats                |
| FR-34  | Could    | System shall schedule automated report delivery via email         |

### 3.5 User Management

| ID     | Priority | Requirement                                                      |
|--------|----------|------------------------------------------------------------------|
| FR-40  | Must     | System shall support role-based access control (Admin, Manager, Staff, Viewer) |
| FR-41  | Must     | System shall log all user actions for audit trail                 |
| FR-42  | Should   | System shall integrate with SSO (OAuth 2.0 / SAML)               |
| FR-43  | Should   | System shall enforce password policy (min 12 chars, complexity)   |

---

## 4. Non-Functional Requirements

### 4.1 Performance

| ID      | Requirement                                                    |
|---------|----------------------------------------------------------------|
| NFR-01  | Page load time: < 2 seconds (95th percentile)                  |
| NFR-02  | API response time: < 500ms for single-record operations        |
| NFR-03  | Barcode scan to confirmation: < 1 second                       |
| NFR-04  | Report generation: < 30 seconds for datasets up to 100K rows   |
| NFR-05  | System shall handle 50 concurrent users without degradation     |

### 4.2 Availability & Reliability

| ID      | Requirement                                                    |
|---------|----------------------------------------------------------------|
| NFR-10  | System uptime: 99.9% (≤ 8.76 hours downtime/year)             |
| NFR-11  | Recovery Time Objective (RTO): 1 hour                          |
| NFR-12  | Recovery Point Objective (RPO): 15 minutes                     |
| NFR-13  | Automated daily backups with 30-day retention                  |
| NFR-14  | Multi-AZ database deployment for failover                      |

### 4.3 Security

| ID      | Requirement                                                    |
|---------|----------------------------------------------------------------|
| NFR-20  | All data encrypted at rest (AES-256)                           |
| NFR-21  | All data encrypted in transit (TLS 1.3)                        |
| NFR-22  | Session timeout after 30 minutes of inactivity                 |
| NFR-23  | Brute-force protection: lock account after 5 failed attempts   |
| NFR-24  | SQL injection prevention via parameterized queries             |
| NFR-25  | OWASP Top 10 mitigations implemented and verified              |
| NFR-26  | Annual penetration testing required                            |

### 4.4 Scalability

| ID      | Requirement                                                    |
|---------|----------------------------------------------------------------|
| NFR-30  | Horizontal scaling to 200 concurrent users within 5 minutes    |
| NFR-31  | Database read replicas for reporting workloads                 |
| NFR-32  | CDN for static assets (< 100ms global latency)                 |

### 4.5 Usability

| ID      | Requirement                                                    |
|---------|----------------------------------------------------------------|
| NFR-40  | WCAG 2.1 AA accessibility compliance                           |
| NFR-41  | Mobile-responsive design (tablets for warehouse floor)          |
| NFR-42  | New user onboarding: productive within 1 hour of training      |
| NFR-43  | Keyboard-navigable for all critical workflows                  |

---

## 5. User Roles & Permissions Matrix

| Permission          | Admin | Manager | Staff | Viewer |
|---------------------|-------|---------|-------|--------|
| View inventory      | Yes   | Yes     | Yes   | Yes    |
| Add/edit products   | Yes   | Yes     | No    | No     |
| Delete products     | Yes   | No      | No    | No     |
| Process stock intake| Yes   | Yes     | Yes   | No     |
| Create purchase orders | Yes | Yes    | No    | No     |
| View reports        | Yes   | Yes     | No    | Yes    |
| Generate reports    | Yes   | Yes     | No    | No     |
| Manage users        | Yes   | No      | No    | No     |
| System configuration| Yes   | No      | No    | No     |

---

## 6. Acceptance Criteria

Each functional requirement must pass the following before sign-off:
1. **Unit tests** cover all business logic with ≥ 80% code coverage
2. **Integration tests** verify database operations and API contracts
3. **UAT (User Acceptance Testing)** signed off by at least one Manager-level stakeholder
4. **Performance tests** confirm NFR thresholds under simulated load
5. **Security scan** passes with zero critical/high findings
