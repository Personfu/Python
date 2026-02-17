# Software Requirements Specification
## CIS 310 — Systems Analysis & Design | Preston Furulie

## Project: Guitar Shop Inventory Tracker
**Version:** 1.0

## 1. Functional Requirements

- **FR-01:** System shall track product quantities in real-time
- **FR-02:** System shall generate low-stock alerts when quantity falls below threshold
- **FR-03:** Users shall be able to add, update, and remove products
- **FR-04:** System shall generate monthly inventory reports (PDF/CSV)
- **FR-05:** System shall support barcode scanning for stock intake

## 2. Non-Functional Requirements

- **NFR-01:** Page load time under 2 seconds (95th percentile)
- **NFR-02:** System availability 99.9% uptime
- **NFR-03:** Support concurrent access for 50+ users
- **NFR-04:** All data encrypted at rest (AES-256) and in transit (TLS 1.3)

## 3. User Roles

- **Admin:** Full CRUD access, user management, report generation
- **Manager:** Read/write access to inventory, view reports
- **Staff:** Read-only access, submit stock intake requests
