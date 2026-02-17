# FLLC Enterprise Platform — REST API Documentation
## CIS 425 — Capstone | Preston Furulie

---

## Overview

| Field | Value |
|-------|-------|
| **Base URL** | `https://api.fllc.internal/v1` |
| **Protocol** | HTTPS (TLS 1.3) |
| **Format** | JSON (`Content-Type: application/json`) |
| **Auth** | JWT Bearer tokens (RS256) |
| **Rate Limit** | 100 requests/minute per API key |
| **Versioning** | URL path (`/v1/`) |

---

## 1. Authentication

### POST /auth/login

Authenticate a user and receive access + refresh tokens.

**Request:**
```json
{
    "email": "admin@fllc.net",
    "password": "SecureP@ss2026!"
}
```

**Response (200 OK):**
```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
        "id": 1,
        "email": "admin@fllc.net",
        "role": "admin",
        "first_name": "Preston",
        "last_name": "Furulie"
    }
}
```

**Errors:**
| Code | Body | Cause |
|------|------|-------|
| 401 | `{"error": "INVALID_CREDENTIALS"}` | Wrong email or password |
| 429 | `{"error": "RATE_LIMITED"}` | Too many login attempts (5 in 15 min) |

### POST /auth/refresh

Exchange a refresh token for a new access token.

**Request:**
```json
{
    "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

**Response (200 OK):**
```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "expires_in": 900
}
```

### Using Tokens

All authenticated endpoints require the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

| Token | TTL | Storage |
|-------|-----|---------|
| Access token | 15 minutes | Memory (JavaScript variable) |
| Refresh token | 7 days | httpOnly cookie |

---

## 2. Products

### GET /products

List products with filtering, sorting, and pagination.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number (1-indexed) |
| `limit` | int | 20 | Items per page (max 100) |
| `category` | string | — | Filter by category name |
| `search` | string | — | Full-text search on product_name |
| `min_price` | float | — | Minimum list_price |
| `max_price` | float | — | Maximum list_price |
| `sort` | string | `name` | Sort field: `name`, `price`, `date_added`, `category` |
| `order` | string | `asc` | Sort direction: `asc` or `desc` |
| `in_stock` | bool | — | If `true`, only products with stock > 0 |

**Response (200 OK):**
```json
{
    "data": [
        {
            "product_id": 1,
            "product_code": "strat_2024",
            "product_name": "Fender Stratocaster",
            "category": "Guitars",
            "list_price": 1199.99,
            "discount_percent": 15,
            "sale_price": 1019.99,
            "stock_quantity": 23,
            "date_added": "2026-01-15T08:30:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total_items": 47,
        "total_pages": 3,
        "has_next": true,
        "has_prev": false
    }
}
```

**Example Requests:**
```
GET /products?category=Guitars&sort=price&order=desc
GET /products?search=fender&min_price=500&max_price=2000
GET /products?page=2&limit=10&in_stock=true
```

### GET /products/:id

Get a single product with full details including stock and reviews.

**Response (200 OK):**
```json
{
    "product_id": 1,
    "product_code": "strat_2024",
    "product_name": "Fender Stratocaster",
    "description": "American Professional II Stratocaster with rosewood fingerboard.",
    "category": {
        "category_id": 1,
        "category_name": "Guitars"
    },
    "supplier": {
        "supplier_id": 3,
        "company_name": "Fender Musical Instruments"
    },
    "list_price": 1199.99,
    "discount_percent": 15,
    "sale_price": 1019.99,
    "stock_quantity": 23,
    "reorder_level": 5,
    "date_added": "2026-01-15T08:30:00Z",
    "average_rating": 4.6,
    "review_count": 12
}
```

### POST /products

Create a new product. **Requires Admin or Manager role.**

**Request:**
```json
{
    "category_id": 1,
    "supplier_id": 3,
    "product_code": "tele_2026",
    "product_name": "Fender Telecaster 2026",
    "description": "Player II Telecaster with maple fingerboard.",
    "list_price": 899.99,
    "discount_percent": 0,
    "stock_quantity": 30,
    "reorder_level": 5
}
```

**Response (201 Created):**
```json
{
    "product_id": 48,
    "message": "Product created successfully"
}
```

**Validation Rules:**
| Field | Rule |
|-------|------|
| `product_code` | Required, unique, 3-50 chars, alphanumeric + underscore |
| `product_name` | Required, 1-255 chars |
| `list_price` | Required, > 0 |
| `discount_percent` | 0-100 |
| `category_id` | Must reference existing category |

### PUT /products/:id

Update an existing product. **Requires Admin or Manager role.**

**Request (partial update supported):**
```json
{
    "list_price": 949.99,
    "discount_percent": 10
}
```

**Response (200 OK):**
```json
{
    "product_id": 48,
    "message": "Product updated successfully",
    "changes": ["list_price", "discount_percent"]
}
```

### DELETE /products/:id

Soft-delete a product (sets `is_active = false`). **Requires Admin role.**

**Response (204 No Content):** Empty body on success.

---

## 3. Inventory

### GET /inventory

View all warehouse stock levels. **Requires Staff+ role.**

**Response (200 OK):**
```json
{
    "data": [
        {
            "product_id": 1,
            "product_name": "Fender Stratocaster",
            "category": "Guitars",
            "stock_quantity": 23,
            "reorder_level": 5,
            "status": "IN_STOCK",
            "last_movement": "2026-02-10T14:22:00Z"
        }
    ],
    "summary": {
        "total_products": 47,
        "in_stock": 42,
        "low_stock": 3,
        "out_of_stock": 2
    }
}
```

### GET /inventory/:product_id

Get stock history for a specific product. **Requires Staff+ role.**

### POST /inventory/intake

Log incoming stock (receiving shipment). **Requires Staff+ role.**

**Request:**
```json
{
    "product_id": 1,
    "quantity": 50,
    "reference": "PO-2026-0042",
    "notes": "Shipment from Fender warehouse"
}
```

### POST /inventory/adjust

Manual stock adjustment with reason. **Requires Manager+ role.**

**Request:**
```json
{
    "product_id": 1,
    "quantity_change": -2,
    "reason": "DAMAGED",
    "notes": "Water damage during storage"
}
```

---

## 4. Orders

### GET /orders

List orders with filtering. **Requires Staff+ role.**

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `status` | string | Filter: `pending`, `shipped`, `delivered`, `cancelled` |
| `customer_id` | int | Filter by customer |
| `date_from` | date | Orders placed on or after |
| `date_to` | date | Orders placed on or before |

### GET /orders/:id

Get order details including all line items. **Requires Staff+ role.**

**Response (200 OK):**
```json
{
    "order_id": 1,
    "customer": {
        "customer_id": 1,
        "name": "Allan Sherwood",
        "email": "allan.sherwood@yahoo.com"
    },
    "order_date": "2026-02-01T10:00:00Z",
    "ship_date": "2026-02-03T14:00:00Z",
    "status": "shipped",
    "items": [
        {
            "product_name": "Fender Stratocaster",
            "item_price": 1199.99,
            "discount_amount": 180.00,
            "quantity": 1,
            "line_total": 1019.99
        }
    ],
    "order_total": 1019.99,
    "shipping_address": {
        "line1": "100 East Ridgewood Ave.",
        "city": "Paramus",
        "state": "NJ",
        "zip_code": "07652"
    }
}
```

### POST /orders

Place a new order. **Any authenticated user.**

### PUT /orders/:id/ship

Mark order as shipped. **Requires Staff+ role.**

**Request:**
```json
{
    "tracking_number": "1Z999AA10123456784",
    "carrier": "UPS"
}
```

---

## 5. Reports

### GET /reports/inventory

Current stock levels across all products. **Requires Manager+ role.**

| Param | Type | Description |
|-------|------|-------------|
| `format` | string | `json` (default), `csv`, `pdf` |

### GET /reports/sales

Sales report by date range. **Requires Manager+ role.**

| Param | Type | Description |
|-------|------|-------------|
| `date_from` | date | Start date (required) |
| `date_to` | date | End date (required) |
| `group_by` | string | `day`, `week`, `month` |

### GET /reports/low-stock

Products below reorder threshold. **Requires Manager+ role.**

**Response (200 OK):**
```json
{
    "data": [
        {
            "product_id": 12,
            "product_name": "Boss Katana Amp",
            "stock_quantity": 2,
            "reorder_level": 10,
            "shortage": 8,
            "suggested_order_qty": 20
        }
    ],
    "total_low_stock": 3
}
```

---

## 6. Health & System

### GET /health

System health check (no auth required).

**Response (200 OK):**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "uptime_seconds": 86400,
    "database": "connected",
    "cache": "connected"
}
```

### GET /stats

System statistics. **Requires Admin role.**

**Response (200 OK):**
```json
{
    "total_products": 47,
    "total_customers": 8,
    "total_orders": 12,
    "revenue_30d": 15249.87,
    "api_requests_24h": 2847
}
```

---

## 7. Error Response Format

All errors follow a consistent JSON format:

```json
{
    "error": "ERROR_CODE",
    "message": "Human-readable description of what went wrong",
    "status": 404,
    "details": {}
}
```

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET or PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error, malformed JSON |
| 401 | Unauthorized | Missing or expired token |
| 403 | Forbidden | Valid token but insufficient role |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate product_code, email, etc. |
| 422 | Unprocessable | Business rule violation |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Unexpected server error |

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_CREDENTIALS` | Wrong email or password |
| `TOKEN_EXPIRED` | Access token has expired |
| `INSUFFICIENT_PERMISSIONS` | User role cannot perform action |
| `VALIDATION_ERROR` | Request body failed validation |
| `RESOURCE_NOT_FOUND` | Requested ID doesn't exist |
| `DUPLICATE_ENTRY` | Unique constraint violated |
| `FOREIGN_KEY_VIOLATION` | Referenced resource doesn't exist |
| `RATE_LIMITED` | Too many requests |

---

## 8. RBAC Permission Matrix

| Endpoint | Viewer | Staff | Manager | Admin |
|----------|--------|-------|---------|-------|
| GET /products | Yes | Yes | Yes | Yes |
| POST /products | — | — | Yes | Yes |
| PUT /products/:id | — | — | Yes | Yes |
| DELETE /products/:id | — | — | — | Yes |
| GET /inventory | — | Yes | Yes | Yes |
| POST /inventory/intake | — | Yes | Yes | Yes |
| POST /inventory/adjust | — | — | Yes | Yes |
| GET /orders | — | Yes | Yes | Yes |
| POST /orders | Yes | Yes | Yes | Yes |
| PUT /orders/:id/ship | — | Yes | Yes | Yes |
| GET /reports/* | — | — | Yes | Yes |
| GET /stats | — | — | — | Yes |
