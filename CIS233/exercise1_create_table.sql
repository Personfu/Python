-- Exercise 1: CREATE TABLE & Constraints
-- CIS 233 — Database Management | Preston Furulie

USE my_guitar_shop;

-- Create a reviews table with proper constraints
CREATE TABLE reviews (
    review_id       INT            PRIMARY KEY  AUTO_INCREMENT,
    product_id      INT            NOT NULL,
    customer_id     INT            NOT NULL,
    rating          INT            NOT NULL     CHECK (rating BETWEEN 1 AND 5),
    review_text     VARCHAR(2000)  DEFAULT      '',
    review_date     DATETIME       DEFAULT      NOW(),

    CONSTRAINT fk_reviews_products
        FOREIGN KEY (product_id)
        REFERENCES products (product_id),

    CONSTRAINT fk_reviews_customers
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
);

-- Verify the table structure
DESCRIBE reviews;
