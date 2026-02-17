# REST API Documentation
## CIS 425 — Capstone | Preston Furulie

## Base URL

`https://api.example.com/v1`

## Authentication

| Endpoint           | Method | Description                           |
|--------------------|--------|---------------------------------------|
| `/auth/login`      | POST   | Returns JWT access + refresh tokens   |
| `/auth/refresh`    | POST   | Exchange refresh token for new access  |

All other routes require `Authorization: Bearer <token>`.

## Products

| Endpoint           | Method | Auth         | Description                              |
|--------------------|--------|--------------|------------------------------------------|
| `/products`        | GET    | Any          | List products (paginated, filterable)    |
| `/products/:id`    | GET    | Any          | Get product details with stock levels    |
| `/products`        | POST   | Admin/Mgr    | Create product                           |
| `/products/:id`    | PUT    | Admin/Mgr    | Update product details                   |
| `/products/:id`    | DELETE | Admin        | Soft-delete product                      |

### GET /products — Query Parameters

- `page` (int, default 1) — Page number
- `limit` (int, default 20, max 100) — Items per page
- `category` (string) — Filter by category name
- `search` (string) — Full-text search on product name
- `sort` (string) — Sort field: `name`, `price`, `date_added`
- `order` (string) — `asc` or `desc`

### POST /products — Request Body

```json
{
    "category_id": 1,
    "product_code": "str_2024",
    "product_name": "Fender Stratocaster 2024",
    "description": "American Professional II",
    "list_price": 1699.99,
    "discount_percent": 10,
    "stock_quantity": 15
}
```

## Inventory

| Endpoint                   | Method | Auth      | Description                    |
|----------------------------|--------|-----------|--------------------------------|
| `/inventory`               | GET    | Staff+    | View all warehouse stock       |
| `/inventory/:product_id`   | GET    | Staff+    | View stock for one product     |
| `/inventory/intake`        | POST   | Staff+    | Log stock intake (receiving)   |
| `/inventory/adjust`        | POST   | Manager+  | Manual stock adjustment        |

## Orders

| Endpoint              | Method | Auth      | Description               |
|-----------------------|--------|-----------|---------------------------|
| `/orders`             | GET    | Staff+    | List orders (filterable)  |
| `/orders/:id`         | GET    | Staff+    | Get order details         |
| `/orders`             | POST   | Any       | Place new order           |
| `/orders/:id/ship`    | PUT    | Staff+    | Mark order as shipped     |

## Reports

| Endpoint                    | Method | Auth      | Description                        |
|-----------------------------|--------|-----------|------------------------------------|
| `/reports/inventory`        | GET    | Manager+  | Current stock levels (CSV/PDF)     |
| `/reports/sales`            | GET    | Manager+  | Sales report by date range         |
| `/reports/low-stock`        | GET    | Manager+  | Products below reorder threshold   |

## Error Responses

```json
{
    "error": "NOT_FOUND",
    "message": "Product with id 999 not found",
    "status": 404
}
```

Standard HTTP status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Error.
