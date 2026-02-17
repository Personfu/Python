-- MySQL Exercise 4 - Preston Furulie
-- Database: my_guitar_shop

USE my_guitar_shop;

-- Step 1: Join Categories to Products
SELECT c.category_name, p.product_name, p.list_price
FROM categories c
    JOIN products p ON c.category_id = p.category_id
ORDER BY c.category_name, p.product_name;

-- Step 2: Join Customers to Addresses for allan.sherwood@yahoo.com
SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
FROM customers c
    JOIN addresses a ON c.customer_id = a.customer_id
WHERE c.email_address = 'allan.sherwood@yahoo.com';

-- Step 3: Join Customers to Addresses (shipping address only)
SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
FROM customers c
    JOIN addresses a ON c.shipping_address_id = a.address_id;

-- Step 4: Join Customers, Orders, Order_Items, and Products with aliases
SELECT c.last_name, c.first_name, o.order_date, p.product_name,
       oi.item_price, oi.discount_amount, oi.quantity
FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
ORDER BY c.last_name, o.order_date, p.product_name;

-- Step 5: Self-join to find products with the same list price
SELECT DISTINCT p1.product_name, p1.list_price
FROM products p1
    JOIN products p2
        ON p1.product_id != p2.product_id
        AND p1.list_price = p2.list_price
ORDER BY p1.product_name;

-- Step 6: Outer join to find categories that have never been used
SELECT c.category_name, p.product_id
FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id
WHERE p.product_id IS NULL;

-- Step 7: Union to show shipped vs not shipped orders
SELECT 'SHIPPED' AS ship_status, order_id, order_date
FROM orders
WHERE ship_date IS NOT NULL
UNION
SELECT 'NOT SHIPPED' AS ship_status, order_id, order_date
FROM orders
WHERE ship_date IS NULL
ORDER BY order_date;
