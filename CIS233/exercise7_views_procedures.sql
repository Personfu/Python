-- Exercise 7: Views & Stored Procedures
-- CIS 233 — Database Management | Preston Furulie

USE my_guitar_shop;

-- View: Product summary with category
CREATE OR REPLACE VIEW v_product_summary AS
SELECT p.product_id, c.category_name, p.product_name,
       p.list_price, p.discount_percent,
       p.list_price * (1 - p.discount_percent / 100) AS sale_price
FROM products p
    JOIN categories c ON p.category_id = c.category_id;

SELECT * FROM v_product_summary
ORDER BY sale_price DESC;

-- Stored Procedure: Get orders by customer email
DELIMITER //

CREATE PROCEDURE sp_customer_orders(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT o.order_id, o.order_date, o.ship_date,
           p.product_name, oi.item_price, oi.quantity
    FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
    WHERE c.email_address = p_email
    ORDER BY o.order_date DESC;
END //

DELIMITER ;

CALL sp_customer_orders('allan.sherwood@yahoo.com');
