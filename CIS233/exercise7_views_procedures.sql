-- ============================================================
-- Exercise 7: Views & Stored Procedures — Complete
-- CIS 233 — Database Management | Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: CREATE VIEW, updatable views, CREATE PROCEDURE,
-- IN/OUT/INOUT parameters, IF/ELSE logic, CURSOR, LOOP,
-- error handling (DECLARE HANDLER), and practical examples.
-- ============================================================

USE my_guitar_shop;

-- ════════════════════════════════════════════════════════════
-- PART A: VIEWS
-- A view is a stored SELECT query that acts like a virtual table.
-- Benefits: simplify complex queries, enforce security (expose
-- only certain columns), and provide a stable interface.
-- ════════════════════════════════════════════════════════════

-- ── View 1: Product Summary with Calculated Columns ────────

CREATE OR REPLACE VIEW v_product_summary AS
SELECT p.product_id,
       c.category_name,
       p.product_name,
       p.list_price,
       p.discount_percent,
       ROUND(p.list_price * (1 - p.discount_percent / 100), 2) AS sale_price,
       ROUND(p.list_price * p.discount_percent / 100, 2)       AS discount_amount
FROM products p
    JOIN categories c ON p.category_id = c.category_id;

-- Use the view like a table
SELECT * FROM v_product_summary
ORDER BY sale_price DESC;

-- Filter the view
SELECT category_name, product_name, sale_price
FROM v_product_summary
WHERE sale_price > 500
ORDER BY sale_price DESC;


-- ── View 2: Customer Order History ─────────────────────────

CREATE OR REPLACE VIEW v_customer_orders AS
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       c.email_address,
       COUNT(DISTINCT o.order_id)   AS total_orders,
       SUM(oi.quantity)              AS total_items,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS total_spent,
       MAX(o.order_date)             AS last_order_date
FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email_address;

SELECT * FROM v_customer_orders
ORDER BY total_spent DESC;


-- ── View 3: Inventory Status ───────────────────────────────

CREATE OR REPLACE VIEW v_order_details AS
SELECT o.order_id,
       o.order_date,
       o.ship_date,
       CASE
           WHEN o.ship_date IS NOT NULL THEN 'Shipped'
           ELSE 'Pending'
       END AS status,
       c.first_name,
       c.last_name,
       p.product_name,
       oi.item_price,
       oi.discount_amount,
       oi.quantity,
       (oi.item_price - oi.discount_amount) * oi.quantity AS line_total
FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id;

SELECT * FROM v_order_details
ORDER BY order_date DESC, order_id;


-- ════════════════════════════════════════════════════════════
-- PART B: STORED PROCEDURES
-- A stored procedure is a set of SQL statements stored in the
-- database that can be called by name. Benefits: reusable logic,
-- reduced network traffic, and security (EXECUTE privilege).
-- ════════════════════════════════════════════════════════════

-- ── Procedure 1: Get Orders by Customer Email ──────────────

DELIMITER //

CREATE PROCEDURE sp_customer_orders(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT o.order_id,
           o.order_date,
           o.ship_date,
           p.product_name,
           oi.item_price,
           oi.discount_amount,
           oi.quantity,
           (oi.item_price - oi.discount_amount) * oi.quantity AS line_total
    FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
    WHERE c.email_address = p_email
    ORDER BY o.order_date DESC;
END //

DELIMITER ;

-- Call the procedure
CALL sp_customer_orders('allan.sherwood@yahoo.com');


-- ── Procedure 2: OUT Parameter (Return a Value) ────────────

DELIMITER //

CREATE PROCEDURE sp_product_count(
    IN  p_category_name VARCHAR(255),
    OUT p_count INT
)
BEGIN
    SELECT COUNT(*)
    INTO p_count
    FROM products p
        JOIN categories c ON p.category_id = c.category_id
    WHERE c.category_name = p_category_name;
END //

DELIMITER ;

-- Call with OUT parameter
CALL sp_product_count('Guitars', @guitar_count);
SELECT @guitar_count AS guitar_product_count;


-- ── Procedure 3: IF/ELSE Logic ─────────────────────────────

DELIMITER //

CREATE PROCEDURE sp_apply_discount(
    IN p_product_id INT,
    IN p_new_discount DECIMAL(5,2)
)
BEGIN
    DECLARE v_current_discount DECIMAL(5,2);
    DECLARE v_product_name VARCHAR(255);

    -- Get current values
    SELECT discount_percent, product_name
    INTO v_current_discount, v_product_name
    FROM products
    WHERE product_id = p_product_id;

    -- Validate
    IF p_new_discount < 0 OR p_new_discount > 100 THEN
        SELECT CONCAT('Error: Discount must be 0-100. Got: ', p_new_discount) AS result;
    ELSEIF v_product_name IS NULL THEN
        SELECT CONCAT('Error: Product ID ', p_product_id, ' not found') AS result;
    ELSE
        UPDATE products
        SET discount_percent = p_new_discount
        WHERE product_id = p_product_id;

        SELECT CONCAT('Updated ', v_product_name,
                       ' discount from ', v_current_discount,
                       '% to ', p_new_discount, '%') AS result;
    END IF;
END //

DELIMITER ;


-- ── Procedure 4: Error Handling ────────────────────────────

DELIMITER //

CREATE PROCEDURE sp_safe_insert_category(
    IN p_category_name VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT CONCAT('Error: Could not insert category "',
                       p_category_name, '"') AS result;
    END;

    INSERT INTO categories (category_name)
    VALUES (p_category_name);

    SELECT CONCAT('Successfully added category "',
                   p_category_name,
                   '" with ID ', LAST_INSERT_ID()) AS result;
END //

DELIMITER ;


-- ── Procedure 5: Product Search ────────────────────────────

DELIMITER //

CREATE PROCEDURE sp_search_products(
    IN p_search_term VARCHAR(255),
    IN p_min_price DECIMAL(10,2),
    IN p_max_price DECIMAL(10,2),
    IN p_sort_by VARCHAR(20)
)
BEGIN
    SET p_min_price = COALESCE(p_min_price, 0);
    SET p_max_price = COALESCE(p_max_price, 99999);
    SET p_sort_by = COALESCE(p_sort_by, 'name');

    SELECT p.product_name,
           c.category_name,
           p.list_price,
           p.discount_percent,
           ROUND(p.list_price * (1 - p.discount_percent/100), 2) AS sale_price
    FROM products p
        JOIN categories c ON p.category_id = c.category_id
    WHERE (p.product_name LIKE CONCAT('%', p_search_term, '%')
           OR p_search_term IS NULL)
      AND p.list_price BETWEEN p_min_price AND p_max_price
    ORDER BY
        CASE p_sort_by
            WHEN 'price_asc'  THEN p.list_price
            WHEN 'price_desc' THEN -p.list_price
            ELSE NULL
        END,
        CASE p_sort_by
            WHEN 'name' THEN p.product_name
            ELSE NULL
        END;
END //

DELIMITER ;

-- Usage examples
CALL sp_search_products('Guitar', NULL, NULL, 'price_asc');
CALL sp_search_products(NULL, 500, 2000, 'price_desc');


-- ── Show All Created Objects ───────────────────────────────

-- List all views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- List all procedures
SHOW PROCEDURE STATUS WHERE Db = 'my_guitar_shop';
