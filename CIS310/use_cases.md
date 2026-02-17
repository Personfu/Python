# Use Case Documentation
## CIS 310 — Systems Analysis & Design | Preston Furulie

---

## Use Case Index

| UC ID  | Name                    | Primary Actor     | Priority |
|--------|-------------------------|-------------------|----------|
| UC-01  | Process Stock Intake    | Warehouse Staff   | Must     |
| UC-02  | Generate Report         | Manager           | Must     |
| UC-03  | Manage Product Catalog  | Manager           | Must     |
| UC-04  | Create Purchase Order   | Manager           | Should   |
| UC-05  | User Authentication     | All Users         | Must     |
| UC-06  | Search Inventory        | All Users         | Must     |

---

## UC-01: Process Stock Intake

### Overview

| Field           | Value                                          |
|-----------------|------------------------------------------------|
| **Use Case ID** | UC-01                                          |
| **Name**        | Process Stock Intake                           |
| **Actor**       | Warehouse Staff                                |
| **Description** | Staff receives a shipment, scans items, and updates inventory quantities |
| **Preconditions** | Staff is authenticated; shipment has arrived |
| **Postconditions** | Inventory quantities updated; intake logged  |
| **Trigger**     | New shipment arrives at warehouse               |
| **Priority**    | Must Have                                      |

### Main Success Scenario

| Step | Actor            | System                                          |
|------|------------------|-------------------------------------------------|
| 1    | Scans shipment barcode or enters PO number | —                              |
| 2    | —                | Looks up Purchase Order, displays expected line items with quantities |
| 3    | Verifies physical count against expected quantities | —                 |
| 4    | Confirms quantities match (or enters actual counts) | —                 |
| 5    | —                | Validates: actual qty ≤ PO qty for each line    |
| 6    | —                | Updates `inventory.quantity_on_hand` for each product |
| 7    | —                | Creates `inventory_log` entry with timestamp, staff ID, PO reference |
| 8    | —                | Updates PO status to "Received" (or "Partially Received") |
| 9    | —                | Displays confirmation summary                    |

### Alternative Flows

| ID   | Condition                              | Steps                                    |
|------|----------------------------------------|------------------------------------------|
| 3a   | Quantity mismatch (short shipment)     | Staff enters actual count; system flags variance; notification sent to Manager; PO status → "Partially Received" |
| 3b   | Damaged items                          | Staff marks items as damaged; system records damage count; creates return authorization |
| 2a   | No matching PO found                   | Staff selects "Manual Intake"; enters product SKU, quantity, supplier manually; Manager approval required |
| 1a   | Barcode unreadable                     | Staff manually enters PO number           |

### Exception Flows

| ID   | Condition                 | Steps                                       |
|------|---------------------------|---------------------------------------------|
| E1   | Network connection lost   | System saves intake data locally; syncs when connection restored |
| E2   | Product SKU not in system | Staff cannot proceed; must create product first or contact Manager |
| E3   | Staff session expired     | Redirect to login; unsaved data preserved in local storage |

### Business Rules
- BR-01: All intake operations require at least one item to be scanned
- BR-02: Intake quantity cannot exceed PO expected quantity by more than 10% without Manager override
- BR-03: All intake timestamps use UTC with local timezone display

---

## UC-02: Generate Report

### Overview

| Field           | Value                                          |
|-----------------|------------------------------------------------|
| **Use Case ID** | UC-02                                          |
| **Name**        | Generate Report                                |
| **Actor**       | Manager                                        |
| **Description** | Manager creates inventory/sales reports with configurable parameters |
| **Preconditions** | Manager is authenticated with reporting permissions |
| **Postconditions** | Report generated and available for download  |

### Main Success Scenario

| Step | Actor                                  | System                                 |
|------|----------------------------------------|----------------------------------------|
| 1    | Navigates to Reports section           | Displays available report types         |
| 2    | Selects report type (Stock Levels, Movement, Valuation, Turnover) | Shows parameter form |
| 3    | Configures parameters: date range, categories, locations, format | Validates inputs |
| 4    | Clicks "Generate Report"              | Queues report generation                |
| 5    | —                                      | Processes data, applies calculations    |
| 6    | —                                      | Displays progress indicator             |
| 7    | —                                      | Generates file (PDF or CSV)             |
| 8    | Downloads report or shares via email   | Logs report generation in audit trail   |

### Report Types

| Report             | Key Metrics                                     | Frequency |
|--------------------|------------------------------------------------|-----------|
| Stock Levels       | Qty on hand, reorder point, days of supply      | Daily     |
| Stock Movement     | Receipts, sales, adjustments, transfers          | Weekly    |
| Inventory Valuation| Cost basis (FIFO/Weighted Avg), total value     | Monthly   |
| Turnover Analysis  | Sales velocity, slow movers, dead stock          | Monthly   |
| Low Stock Alert    | Items below reorder point                        | Real-time |

### Alternative Flows
- **4a.** Date range > 1 year: System warns about large dataset; offers to run asynchronously and email when complete
- **7a.** Report exceeds 50,000 rows: CSV only (PDF too large); system notifies user

---

## UC-03: Manage Product Catalog

### Overview

| Field           | Value                                          |
|-----------------|------------------------------------------------|
| **Use Case ID** | UC-03                                          |
| **Name**        | Manage Product Catalog                         |
| **Actor**       | Manager                                        |
| **Description** | Add, edit, or deactivate products in the catalog |
| **Preconditions** | Manager authenticated with product management permissions |

### Main Flow — Add New Product

| Step | Actor                              | System                                  |
|------|------------------------------------|-----------------------------------------|
| 1    | Clicks "Add Product"              | Displays product form                   |
| 2    | Enters: name, description, category, supplier, cost, list price, reorder point | — |
| 3    | Uploads product images (optional)  | Validates file type and size             |
| 4    | Clicks "Save"                     | Validates all required fields            |
| 5    | —                                  | Auto-generates SKU (CAT-NNNNN format)    |
| 6    | —                                  | Saves to database; creates audit log entry |
| 7    | —                                  | Displays confirmation with new SKU       |

### Main Flow — Edit Product

| Step | Actor                              | System                                  |
|------|------------------------------------|-----------------------------------------|
| 1    | Searches for product by SKU or name | Displays matching products              |
| 2    | Selects product                    | Displays current product details in form |
| 3    | Modifies fields                    | Highlights changed fields                |
| 4    | Clicks "Save"                     | Validates; saves diff to audit log       |

### Business Rules
- BR-10: List price must be ≥ cost price (no selling at a loss without Admin override)
- BR-11: Product deactivation (soft delete) preserves historical data; hard delete requires Admin
- BR-12: Category must exist before assigning to a product

---

## UC-04: Create Purchase Order

### Overview

| Field           | Value                                          |
|-----------------|------------------------------------------------|
| **Use Case ID** | UC-04                                          |
| **Name**        | Create Purchase Order                          |
| **Actor**       | Manager                                        |
| **Trigger**     | Inventory falls below reorder point (auto) or manual creation |

### Main Flow

| Step | Actor                              | System                                  |
|------|------------------------------------|-----------------------------------------|
| 1    | Selects supplier                   | Displays supplier's product catalog      |
| 2    | Adds line items (product, qty)     | Calculates line totals and PO total      |
| 3    | Reviews PO summary                 | Displays total cost, estimated delivery  |
| 4    | Submits PO                        | Assigns PO number (PO-YYYYMMDD-NNN)      |
| 5    | —                                  | Sends PO to supplier (email or EDI)      |
| 6    | —                                  | Sets PO status to "Submitted"            |

---

## UC-05: User Authentication

### Main Flow

| Step | Actor                     | System                                        |
|------|---------------------------|-----------------------------------------------|
| 1    | Navigates to login page   | Displays login form                            |
| 2    | Enters email and password | Validates credentials against hashed password  |
| 3    | —                         | Checks account status (active, locked)         |
| 4    | —                         | Creates session with JWT (30-min expiry)        |
| 5    | —                         | Redirects to role-appropriate dashboard         |

### Alternative Flows
- **2a.** Invalid credentials: Increment failed attempt counter; display generic error "Invalid email or password"
- **3a.** Account locked (5+ failures): Display "Account locked. Contact administrator."
- **2b.** SSO login: Redirect to identity provider; receive SAML assertion; create session

---

## UC-06: Search Inventory

### Main Flow

| Step | Actor                              | System                                  |
|------|------------------------------------|-----------------------------------------|
| 1    | Types search query in search bar   | Shows real-time results (debounced 300ms)|
| 2    | Applies filters (category, price range, stock status) | Refines result set |
| 3    | Sorts results (name, price, stock qty) | Re-renders sorted list              |
| 4    | Clicks product row                 | Displays full product detail with stock history |

### Search Capabilities
- Full-text search on product name and description
- Filter by: category, price range, stock status (in-stock, low, out), supplier
- Sort by: name (A-Z/Z-A), price (asc/desc), quantity (asc/desc), last updated
- Pagination: 25 results per page with page navigation
