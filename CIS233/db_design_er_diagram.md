# Database Design: E-Commerce Schema
## CIS 233 — Database Management | Preston Furulie

## Entity-Relationship Design (Normalized to 3NF)

### Entities

- **customers** (customer_id PK, email, password, first_name, last_name, shipping_address_id FK, billing_address_id FK)
- **addresses** (address_id PK, customer_id FK, line1, line2, city, state, zip_code)
- **categories** (category_id PK, category_name)
- **products** (product_id PK, category_id FK, product_code, product_name, description, list_price, discount_percent, date_added)
- **orders** (order_id PK, customer_id FK, order_date, ship_amount, tax_amount, ship_date)
- **order_items** (item_id PK, order_id FK, product_id FK, item_price, discount_amount, quantity)

### Relationships

- customers 1:M addresses (one customer, many addresses)
- categories 1:M products (one category, many products)
- customers 1:M orders (one customer, many orders)
- orders 1:M order_items (one order, many line items)
- products 1:M order_items (one product, many order references)

### Indexing Strategy

- Primary keys: clustered index on all PK columns
- Foreign keys: non-clustered indexes for join performance
- email_address: unique index for login lookups
- order_date: index for date-range reporting queries
