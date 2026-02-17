-- =============================================================================
-- MySQL Exercise 4 - Step 7
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: Uses the UNION operator to generate a result set with a
--              calculated ship_status column. If ship_date has a value,
--              the status is 'SHIPPED'; otherwise it is 'NOT SHIPPED'.
--              Returns ship_status, order_id, and order_date.
--              Sorted by order_date.
-- =============================================================================

USE my_guitar_shop;

    SELECT 'SHIPPED' AS ship_status, order_id, order_date
    FROM orders
    WHERE ship_date IS NOT NULL

UNION

    SELECT 'NOT SHIPPED' AS ship_status, order_id, order_date
    FROM orders
    WHERE ship_date IS NULL

ORDER BY order_date ASC;
