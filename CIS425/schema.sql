-- Capstone Database Schema
-- CIS 425 — Capstone | Preston Furulie

DROP DATABASE IF EXISTS capstone_guitar_shop;
CREATE DATABASE capstone_guitar_shop;
USE capstone_guitar_shop;

CREATE TABLE categories (
    category_id   INT            PRIMARY KEY  AUTO_INCREMENT,
    category_name VARCHAR(100)   NOT NULL     UNIQUE,
    created_at    DATETIME       DEFAULT      NOW()
);

CREATE TABLE products (
    product_id       INT            PRIMARY KEY  AUTO_INCREMENT,
    category_id      INT            NOT NULL,
    product_code     VARCHAR(20)    NOT NULL     UNIQUE,
    product_name     VARCHAR(255)   NOT NULL,
    description      TEXT,
    list_price       DECIMAL(10,2)  NOT NULL     CHECK (list_price >= 0),
    discount_percent DECIMAL(5,2)   DEFAULT 0    CHECK (discount_percent BETWEEN 0 AND 100),
    stock_quantity   INT            DEFAULT 0    CHECK (stock_quantity >= 0),
    date_added       DATETIME       DEFAULT      NOW(),

    CONSTRAINT fk_products_categories
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE customers (
    customer_id   INT            PRIMARY KEY  AUTO_INCREMENT,
    email_address VARCHAR(255)   NOT NULL     UNIQUE,
    password_hash VARCHAR(255)   NOT NULL,
    first_name    VARCHAR(100)   NOT NULL,
    last_name     VARCHAR(100)   NOT NULL,
    created_at    DATETIME       DEFAULT      NOW()
);

CREATE TABLE addresses (
    address_id  INT            PRIMARY KEY  AUTO_INCREMENT,
    customer_id INT            NOT NULL,
    line1       VARCHAR(255)   NOT NULL,
    line2       VARCHAR(255),
    city        VARCHAR(100)   NOT NULL,
    state       CHAR(2)        NOT NULL,
    zip_code    VARCHAR(10)    NOT NULL,
    is_default  BOOLEAN        DEFAULT FALSE,

    CONSTRAINT fk_addresses_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

CREATE TABLE orders (
    order_id    INT            PRIMARY KEY  AUTO_INCREMENT,
    customer_id INT            NOT NULL,
    order_date  DATETIME       DEFAULT      NOW(),
    ship_date   DATETIME,
    status      ENUM('pending','processing','shipped','delivered','cancelled')
                               DEFAULT 'pending',
    total       DECIMAL(10,2)  NOT NULL,

    CONSTRAINT fk_orders_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id     INT            PRIMARY KEY  AUTO_INCREMENT,
    order_id    INT            NOT NULL,
    product_id  INT            NOT NULL,
    quantity    INT            NOT NULL     CHECK (quantity > 0),
    unit_price  DECIMAL(10,2)  NOT NULL,
    discount    DECIMAL(10,2)  DEFAULT 0,

    CONSTRAINT fk_items_orders
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_items_products
        FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Indexes for performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_items_order ON order_items(order_id);
