-- ============================================================
-- Capstone Production Database Schema — Complete DDL
-- CIS 425 — Capstone | Preston Furulie
-- ============================================================
-- Covers: 10 normalized tables (3NF), AUTO_INCREMENT,
-- FOREIGN KEY constraints with referential actions,
-- CHECK constraints, ENUM types, DEFAULT values,
-- composite indexes, full-text indexes, triggers,
-- views for reporting, and seed data.
-- ============================================================

DROP DATABASE IF EXISTS capstone_guitar_shop;
CREATE DATABASE capstone_guitar_shop
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE capstone_guitar_shop;


-- ════════════════════════════════════════════════════════════
-- TABLE 1: categories (hierarchical with self-reference)
-- ════════════════════════════════════════════════════════════

CREATE TABLE categories (
    category_id   INT            PRIMARY KEY  AUTO_INCREMENT,
    category_name VARCHAR(100)   NOT NULL     UNIQUE,
    description   VARCHAR(500)   DEFAULT '',
    parent_id     INT            DEFAULT NULL,
    sort_order    INT            DEFAULT 0,
    is_active     BOOLEAN        DEFAULT TRUE,
    created_at    DATETIME       DEFAULT NOW(),

    CONSTRAINT fk_category_parent
        FOREIGN KEY (parent_id) REFERENCES categories(category_id)
        ON DELETE SET NULL
);


-- ════════════════════════════════════════════════════════════
-- TABLE 2: suppliers
-- ════════════════════════════════════════════════════════════

CREATE TABLE suppliers (
    supplier_id   INT            PRIMARY KEY  AUTO_INCREMENT,
    company_name  VARCHAR(200)   NOT NULL,
    contact_name  VARCHAR(150)   DEFAULT '',
    contact_email VARCHAR(255)   DEFAULT '',
    phone         VARCHAR(20)    DEFAULT '',
    address       VARCHAR(500)   DEFAULT '',
    website       VARCHAR(255)   DEFAULT '',
    payment_terms VARCHAR(100)   DEFAULT 'Net 30',
    is_active     BOOLEAN        DEFAULT TRUE,
    created_at    DATETIME       DEFAULT NOW()
);


-- ════════════════════════════════════════════════════════════
-- TABLE 3: products
-- ════════════════════════════════════════════════════════════

CREATE TABLE products (
    product_id       INT            PRIMARY KEY  AUTO_INCREMENT,
    category_id      INT            NOT NULL,
    supplier_id      INT            DEFAULT NULL,
    product_code     VARCHAR(20)    NOT NULL     UNIQUE,
    product_name     VARCHAR(255)   NOT NULL,
    description      TEXT,
    list_price       DECIMAL(10,2)  NOT NULL     CHECK (list_price >= 0),
    cost_price       DECIMAL(10,2)  DEFAULT 0.00 CHECK (cost_price >= 0),
    discount_percent DECIMAL(5,2)   DEFAULT 0    CHECK (discount_percent BETWEEN 0 AND 100),
    quantity_on_hand INT            DEFAULT 0    CHECK (quantity_on_hand >= 0),
    reorder_point    INT            DEFAULT 10,
    weight_lbs       DECIMAL(6,2)   DEFAULT NULL,
    date_added       DATETIME       DEFAULT NOW(),
    is_active        BOOLEAN        DEFAULT TRUE,

    CONSTRAINT fk_products_categories
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_products_suppliers
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE SET NULL,

    FULLTEXT INDEX idx_products_search (product_name, description)
);


-- ════════════════════════════════════════════════════════════
-- TABLE 4: customers
-- ════════════════════════════════════════════════════════════

CREATE TABLE customers (
    customer_id       INT            PRIMARY KEY  AUTO_INCREMENT,
    email_address     VARCHAR(255)   NOT NULL     UNIQUE,
    password_hash     VARCHAR(255)   NOT NULL,
    first_name        VARCHAR(100)   NOT NULL,
    last_name         VARCHAR(100)   NOT NULL,
    phone             VARCHAR(20)    DEFAULT '',
    shipping_address_id INT          DEFAULT NULL,
    billing_address_id  INT          DEFAULT NULL,
    is_active         BOOLEAN        DEFAULT TRUE,
    created_at        DATETIME       DEFAULT NOW(),
    last_login        DATETIME       DEFAULT NULL
);


-- ════════════════════════════════════════════════════════════
-- TABLE 5: addresses
-- ════════════════════════════════════════════════════════════

CREATE TABLE addresses (
    address_id   INT            PRIMARY KEY  AUTO_INCREMENT,
    customer_id  INT            NOT NULL,
    address_type ENUM('shipping', 'billing', 'both') DEFAULT 'shipping',
    line1        VARCHAR(255)   NOT NULL,
    line2        VARCHAR(255)   DEFAULT '',
    city         VARCHAR(100)   NOT NULL,
    state        CHAR(2)        NOT NULL,
    zip_code     VARCHAR(10)    NOT NULL,
    phone        VARCHAR(20)    DEFAULT '',
    is_default   BOOLEAN        DEFAULT FALSE,

    CONSTRAINT fk_addresses_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

-- Add FK from customers to addresses (deferred due to circular ref)
ALTER TABLE customers
    ADD CONSTRAINT fk_customers_shipping_addr
        FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id)
        ON DELETE SET NULL;

ALTER TABLE customers
    ADD CONSTRAINT fk_customers_billing_addr
        FOREIGN KEY (billing_address_id) REFERENCES addresses(address_id)
        ON DELETE SET NULL;


-- ════════════════════════════════════════════════════════════
-- TABLE 6: orders
-- ════════════════════════════════════════════════════════════

CREATE TABLE orders (
    order_id     INT            PRIMARY KEY  AUTO_INCREMENT,
    customer_id  INT            NOT NULL,
    order_date   DATETIME       NOT NULL     DEFAULT NOW(),
    ship_date    DATETIME       DEFAULT NULL,
    ship_amount  DECIMAL(10,2)  DEFAULT 0.00,
    tax_amount   DECIMAL(10,2)  DEFAULT 0.00,
    order_status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled')
                                DEFAULT 'pending',
    payment_type ENUM('credit', 'debit', 'paypal', 'bank_transfer')
                                DEFAULT 'credit',
    card_last_four CHAR(4)      DEFAULT NULL,
    notes        TEXT           DEFAULT NULL,

    CONSTRAINT fk_orders_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE RESTRICT
);


-- ════════════════════════════════════════════════════════════
-- TABLE 7: order_items
-- ════════════════════════════════════════════════════════════

CREATE TABLE order_items (
    item_id         INT            PRIMARY KEY  AUTO_INCREMENT,
    order_id        INT            NOT NULL,
    product_id      INT            NOT NULL,
    quantity        INT            NOT NULL     CHECK (quantity > 0),
    item_price      DECIMAL(10,2)  NOT NULL     CHECK (item_price >= 0),
    discount_amount DECIMAL(10,2)  DEFAULT 0.00,

    CONSTRAINT fk_items_orders
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_items_products
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT
);


-- ════════════════════════════════════════════════════════════
-- TABLE 8: reviews
-- ════════════════════════════════════════════════════════════

CREATE TABLE reviews (
    review_id    INT            PRIMARY KEY  AUTO_INCREMENT,
    product_id   INT            NOT NULL,
    customer_id  INT            NOT NULL,
    rating       INT            NOT NULL     CHECK (rating BETWEEN 1 AND 5),
    review_title VARCHAR(150)   NOT NULL,
    review_text  TEXT           DEFAULT NULL,
    review_date  DATETIME       DEFAULT NOW(),
    is_verified  BOOLEAN        DEFAULT FALSE,

    CONSTRAINT fk_reviews_products
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_one_review_per_product
        UNIQUE (product_id, customer_id)
);


-- ════════════════════════════════════════════════════════════
-- TABLE 9: inventory_log (append-only audit trail)
-- ════════════════════════════════════════════════════════════

CREATE TABLE inventory_log (
    log_id          INT            PRIMARY KEY  AUTO_INCREMENT,
    product_id      INT            NOT NULL,
    change_type     ENUM('restock', 'sale', 'return', 'adjustment', 'initial')
                                   NOT NULL,
    quantity_change INT            NOT NULL,
    quantity_after  INT            NOT NULL,
    unit_cost       DECIMAL(10,2)  DEFAULT 0.00,
    reference_id    VARCHAR(50)    DEFAULT NULL,
    logged_by       VARCHAR(100)   NOT NULL     DEFAULT 'system',
    log_date        DATETIME       NOT NULL     DEFAULT NOW(),
    notes           VARCHAR(500)   DEFAULT '',

    CONSTRAINT fk_invlog_products
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);


-- ════════════════════════════════════════════════════════════
-- TABLE 10: users (system access / RBAC)
-- ════════════════════════════════════════════════════════════

CREATE TABLE users (
    user_id       INT            PRIMARY KEY  AUTO_INCREMENT,
    username      VARCHAR(50)    NOT NULL     UNIQUE,
    email         VARCHAR(255)   NOT NULL     UNIQUE,
    password_hash VARCHAR(255)   NOT NULL,
    first_name    VARCHAR(100)   NOT NULL,
    last_name     VARCHAR(100)   NOT NULL,
    role          ENUM('admin', 'manager', 'staff', 'viewer')
                                 DEFAULT 'viewer',
    is_active     BOOLEAN        DEFAULT TRUE,
    last_login    DATETIME       DEFAULT NULL,
    created_at    DATETIME       DEFAULT NOW()
);


-- ════════════════════════════════════════════════════════════
-- INDEXES (Performance Optimization)
-- ════════════════════════════════════════════════════════════

CREATE INDEX idx_products_category   ON products(category_id);
CREATE INDEX idx_products_supplier   ON products(supplier_id);
CREATE INDEX idx_products_active     ON products(is_active, category_id);
CREATE INDEX idx_orders_customer     ON orders(customer_id);
CREATE INDEX idx_orders_date         ON orders(order_date);
CREATE INDEX idx_orders_status       ON orders(order_status);
CREATE INDEX idx_items_order         ON order_items(order_id);
CREATE INDEX idx_items_product       ON order_items(product_id);
CREATE INDEX idx_addresses_customer  ON addresses(customer_id);
CREATE INDEX idx_reviews_product     ON reviews(product_id);
CREATE INDEX idx_invlog_product_date ON inventory_log(product_id, log_date);


-- ════════════════════════════════════════════════════════════
-- VIEWS (Reporting)
-- ════════════════════════════════════════════════════════════

CREATE OR REPLACE VIEW v_product_catalog AS
SELECT p.product_id, c.category_name, p.product_code, p.product_name,
       p.list_price, p.discount_percent,
       ROUND(p.list_price * (1 - p.discount_percent/100), 2) AS sale_price,
       p.quantity_on_hand,
       CASE WHEN p.quantity_on_hand <= p.reorder_point THEN 'LOW' ELSE 'OK' END AS stock_status,
       s.company_name AS supplier
FROM products p
    JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE p.is_active = TRUE;

CREATE OR REPLACE VIEW v_order_summary AS
SELECT o.order_id, o.order_date, o.order_status,
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       c.email_address,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS subtotal,
       o.ship_amount, o.tax_amount,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) + o.ship_amount + o.tax_amount AS total
FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;


-- ════════════════════════════════════════════════════════════
-- SEED DATA
-- ════════════════════════════════════════════════════════════

INSERT INTO categories (category_name, description) VALUES
    ('Guitars',      'Acoustic, electric, and bass guitars'),
    ('Basses',       'Electric and acoustic bass guitars'),
    ('Drums',        'Acoustic and electronic drum kits'),
    ('Keyboards',    'Digital pianos, synthesizers, MIDI controllers'),
    ('Amplifiers',   'Guitar, bass, and keyboard amplifiers'),
    ('Accessories',  'Strings, picks, cables, cases, stands');

INSERT INTO suppliers (company_name, contact_email, payment_terms) VALUES
    ('Fender Musical Instruments', 'orders@fender.com', 'Net 30'),
    ('Gibson Brands',              'wholesale@gibson.com', 'Net 45'),
    ('Yamaha Corporation',         'sales@yamaha.com', 'Net 30'),
    ('Roland Corporation',         'orders@roland.com', 'Net 30');

INSERT INTO products (category_id, supplier_id, product_code, product_name, list_price, cost_price, discount_percent, quantity_on_hand) VALUES
    (1, 1, 'strat_am_pro', 'Fender American Professional II Stratocaster', 1699.99, 850.00, 0,  12),
    (1, 2, 'lp_standard',  'Gibson Les Paul Standard 50s',                 2499.99, 1250.00, 10, 5),
    (1, 1, 'tele_player',  'Fender Player Telecaster',                      849.99, 425.00, 15,  8),
    (4, 3, 'dgx_670',      'Yamaha DGX-670 88-Key Digital Piano',           799.99, 400.00, 0,   8),
    (3, 4, 'td_17kvx',     'Roland TD-17KVX V-Drums',                      1599.99, 800.00, 5,   3),
    (6, NULL, 'sm58',       'Shure SM58 Dynamic Microphone',                 99.99, 50.00,  0,   45),
    (1, NULL, 'taylor_214', 'Taylor 214ce Acoustic-Electric',               1299.99, 650.00, 0,   7),
    (5, NULL, 'katana_100', 'Boss Katana 100 MKII Combo Amp',               369.99, 185.00, 10,  15);

INSERT INTO users (username, email, password_hash, first_name, last_name, role) VALUES
    ('admin',   'admin@guitarshop.com',   SHA2('admin123', 256),   'System', 'Admin',   'admin'),
    ('manager', 'manager@guitarshop.com', SHA2('manager123', 256), 'Store',  'Manager', 'manager'),
    ('staff',   'staff@guitarshop.com',   SHA2('staff123', 256),   'Floor',  'Staff',   'staff');

-- Verify
SELECT 'Tables created:' AS status, COUNT(*) AS count
FROM information_schema.tables
WHERE table_schema = 'capstone_guitar_shop';

SHOW TABLES;
