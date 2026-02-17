# Use Case Diagrams
## CIS 310 — Systems Analysis & Design | Preston Furulie

## Use Case: Process Stock Intake

**Actor:** Warehouse Staff
**Precondition:** Staff is authenticated and on the intake screen
**Trigger:** New shipment arrives at warehouse

### Main Flow

1. Staff scans shipment barcode
2. System displays expected items from purchase order
3. Staff verifies and counts each item
4. Staff confirms quantities match
5. System updates inventory quantities
6. System logs the intake with timestamp and staff ID

### Alternative Flows

- **3a.** Quantity mismatch: Staff flags discrepancy, system notifies manager
- **2a.** No matching PO: Staff creates manual intake entry

## Use Case: Generate Report

**Actor:** Manager
**Flow:** Select date range, choose report type (stock levels, turnover, valuation), select format (PDF/CSV), system generates and downloads report.
