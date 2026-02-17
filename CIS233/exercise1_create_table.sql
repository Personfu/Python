-- ============================================================
-- Exercise 1: CREATE TABLE & Constraints — Complete
-- CIS 233 — Database Management | Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: CREATE TABLE, data types (INT, VARCHAR, DECIMAL,
-- TEXT, DATETIME, ENUM, BOOLEAN), PRIMARY KEY, FOREIGN KEY,
-- AUTO_INCREMENT, NOT NULL, UNIQUE, DEFAULT, CHECK constraints,
-- ON DELETE/UPDATE actions, and DESCRIBE/SHOW statements.
-- ============================================================

USE my_guitar_shop;

-- ── Table 1: Product Reviews ───────────────────────────────
-- Demonstrates all major constraint types

CREATE TABLE IF NOT EXISTS reviews (
    -- PRIMARY KEY with AUTO_INCREMENT: auto-generates unique IDs
    review_id       INT             PRIMARY KEY  AUTO_INCREMENT,

    -- FOREIGN KEYS: enforce referential integrity
    product_id      INT             NOT NULL,
    customer_id     INT             NOT NULL,

    -- CHECK: restrict values to valid range
    rating          INT             NOT NULL
                                    CHECK (rating BETWEEN 1 AND 5),

    -- VARCHAR: variable-length string with max length
    review_title    VARCHAR(100)    NOT NULL,

    -- TEXT: for longer content (up to 65,535 chars)
    review_text     TEXT            DEFAULT NULL,

    -- DATETIME: date + time with DEFAULT of current timestamp
    review_date     DATETIME        NOT NULL     DEFAULT NOW(),

    -- BOOLEAN: stored as TINYINT(1) in MySQL
    is_verified     BOOLEAN         DEFAULT FALSE,

    -- ENUM: restricts to predefined set of values
    status          ENUM('pending', 'approved', 'rejected')
                                    DEFAULT 'pending',

    -- FOREIGN KEY constraints with referential actions
    -- ON DELETE CASCADE: if the parent row is deleted, delete this row too
    -- ON UPDATE CASCADE: if the parent PK changes, update the FK here
    CONSTRAINT fk_reviews_products
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_reviews_customers
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- UNIQUE constraint: prevent duplicate reviews per product per customer
    CONSTRAINT uq_one_review_per_product
        UNIQUE (product_id, customer_id)
);


-- ── Table 2: Wishlists ─────────────────────────────────────
-- Demonstrates composite keys and DEFAULT values

CREATE TABLE IF NOT EXISTS wishlists (
    wishlist_id     INT             PRIMARY KEY  AUTO_INCREMENT,
    customer_id     INT             NOT NULL,
    product_id      INT             NOT NULL,
    priority        INT             DEFAULT 1    CHECK (priority BETWEEN 1 AND 5),
    notes           VARCHAR(500)    DEFAULT '',
    date_added      DATETIME        DEFAULT NOW(),

    CONSTRAINT fk_wishlist_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_wishlist_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,

    -- Prevent duplicate entries
    CONSTRAINT uq_wishlist_entry
        UNIQUE (customer_id, product_id)
);


-- ── Table 3: Inventory Log ─────────────────────────────────
-- Demonstrates DECIMAL precision and computed defaults

CREATE TABLE IF NOT EXISTS inventory_log (
    log_id          INT             PRIMARY KEY  AUTO_INCREMENT,
    product_id      INT             NOT NULL,
    change_type     ENUM('restock', 'sale', 'return', 'adjustment')
                                    NOT NULL,
    quantity_change INT             NOT NULL,
    unit_cost       DECIMAL(10, 2)  DEFAULT 0.00
                                    CHECK (unit_cost >= 0),
    logged_by       VARCHAR(100)    NOT NULL     DEFAULT 'system',
    log_date        DATETIME        NOT NULL     DEFAULT NOW(),

    CONSTRAINT fk_invlog_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
);


-- ── Verify Table Structures ────────────────────────────────

DESCRIBE reviews;
DESCRIBE wishlists;
DESCRIBE inventory_log;

-- Show full CREATE TABLE statement (useful for documentation)
SHOW CREATE TABLE reviews;

-- Show all tables in the database
SHOW TABLES;

-- Show indexes on a table
SHOW INDEX FROM reviews;


-- ── Clean Up (for re-running) ──────────────────────────────
-- DROP TABLE IF EXISTS inventory_log;
-- DROP TABLE IF EXISTS wishlists;
-- DROP TABLE IF EXISTS reviews;
