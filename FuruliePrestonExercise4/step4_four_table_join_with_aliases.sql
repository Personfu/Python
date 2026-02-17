-- =============================================================================
-- MySQL Exercise 4 - Step 4
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: JOIN across four tables: Customers, Orders, Order_Items,
--              and Products using table aliases.
--              Returns last_name, first_name, order_date, product_name,
--              item_price, discount_amount, and quantity.
--              Sorted by last_name, order_date, and product_name.
-- =============================================================================

USE my_guitar_shop;

SELECT c.last_name, c.first_name, o.order_date, p.product_name,
       oi.item_price, oi.discount_amount, oi.quantity
FROM customers c
    INNER JOIN orders o
        ON c.customer_id = o.customer_id
    INNER JOIN order_items oi
        ON o.order_id = oi.order_id
    INNER JOIN products p
        ON oi.product_id = p.product_id
ORDER BY c.last_name ASC, o.order_date ASC, p.product_name ASC;
