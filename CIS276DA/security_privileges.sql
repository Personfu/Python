-- ============================================================
-- Security & Privileges
-- CIS 276DA — Advanced SQL & Data Analytics | FLLC Enterprise
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: CREATE USER, GRANT/REVOKE, role-based access,
-- security views (column/row-level), SQL injection prevention,
-- and password management.
-- ============================================================

USE my_guitar_shop;

-- ════════════════════════════════════════════════════════════
-- SECTION 1: USER MANAGEMENT
-- ════════════════════════════════════════════════════════════

-- 1a. Create users with different access patterns
CREATE USER IF NOT EXISTS 'fllc_admin'@'localhost'
    IDENTIFIED BY 'Admin$ecure2026!';

CREATE USER IF NOT EXISTS 'fllc_analyst'@'localhost'
    IDENTIFIED BY 'Analyst$ecure2026!';

CREATE USER IF NOT EXISTS 'fllc_app'@'localhost'
    IDENTIFIED BY 'App$ecure2026!';

CREATE USER IF NOT EXISTS 'fllc_readonly'@'%'
    IDENTIFIED BY 'Read0nly$2026!';

-- 1b. View existing users
SELECT user, host, account_locked, password_expired
FROM mysql.user
WHERE user LIKE 'fllc_%'
ORDER BY user;


-- ════════════════════════════════════════════════════════════
-- SECTION 2: GRANT PRIVILEGES
-- Principle of Least Privilege: grant only what is needed.
-- ════════════════════════════════════════════════════════════

-- 2a. Full admin — all privileges on the shop database
GRANT ALL PRIVILEGES
ON my_guitar_shop.*
TO 'fllc_admin'@'localhost'
WITH GRANT OPTION;

-- 2b. Analyst — read-only on all tables plus EXECUTE for procedures
GRANT SELECT
ON my_guitar_shop.*
TO 'fllc_analyst'@'localhost';

GRANT EXECUTE
ON my_guitar_shop.*
TO 'fllc_analyst'@'localhost';

-- 2c. Application user — CRUD on transactional tables only
GRANT SELECT, INSERT, UPDATE, DELETE
ON my_guitar_shop.orders
TO 'fllc_app'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
ON my_guitar_shop.order_items
TO 'fllc_app'@'localhost';

GRANT SELECT
ON my_guitar_shop.products
TO 'fllc_app'@'localhost';

GRANT SELECT
ON my_guitar_shop.categories
TO 'fllc_app'@'localhost';

GRANT SELECT
ON my_guitar_shop.customers
TO 'fllc_app'@'localhost';

-- 2d. Read-only user — SELECT only, from any host
GRANT SELECT
ON my_guitar_shop.*
TO 'fllc_readonly'@'%';

-- 2e. Column-level grant — restrict to non-sensitive columns
GRANT SELECT (customer_id, first_name, last_name)
ON my_guitar_shop.customers
TO 'fllc_readonly'@'%';

-- Apply privilege changes
FLUSH PRIVILEGES;

-- 2f. View granted privileges
SHOW GRANTS FOR 'fllc_admin'@'localhost';
SHOW GRANTS FOR 'fllc_analyst'@'localhost';
SHOW GRANTS FOR 'fllc_app'@'localhost';
SHOW GRANTS FOR 'fllc_readonly'@'%';


-- ════════════════════════════════════════════════════════════
-- SECTION 3: REVOKE PRIVILEGES
-- ════════════════════════════════════════════════════════════

-- 3a. Revoke DELETE from the application user on orders
REVOKE DELETE
ON my_guitar_shop.orders
FROM 'fllc_app'@'localhost';

-- 3b. Revoke all from read-only user and re-grant narrower access
REVOKE ALL PRIVILEGES, GRANT OPTION
FROM 'fllc_readonly'@'%';

GRANT SELECT
ON my_guitar_shop.products
TO 'fllc_readonly'@'%';

GRANT SELECT
ON my_guitar_shop.categories
TO 'fllc_readonly'@'%';

FLUSH PRIVILEGES;


-- ════════════════════════════════════════════════════════════
-- SECTION 4: ROLE-BASED ACCESS CONTROL (MySQL 8.0+)
-- Roles group privileges so they can be assigned and revoked
-- as a unit rather than per-user.
-- ════════════════════════════════════════════════════════════

-- 4a. Create roles
CREATE ROLE IF NOT EXISTS 'role_read', 'role_write', 'role_admin';

-- 4b. Assign privileges to roles
GRANT SELECT
ON my_guitar_shop.*
TO 'role_read';

GRANT INSERT, UPDATE, DELETE
ON my_guitar_shop.*
TO 'role_write';

GRANT ALL PRIVILEGES
ON my_guitar_shop.*
TO 'role_admin';

-- 4c. Grant roles to users
GRANT 'role_read'
TO 'fllc_analyst'@'localhost';

GRANT 'role_read', 'role_write'
TO 'fllc_app'@'localhost';

GRANT 'role_admin'
TO 'fllc_admin'@'localhost';

-- 4d. Activate roles for the current session
-- Users must activate roles or set them as default
SET DEFAULT ROLE 'role_read' TO 'fllc_analyst'@'localhost';
SET DEFAULT ROLE 'role_read', 'role_write' TO 'fllc_app'@'localhost';
SET DEFAULT ROLE 'role_admin' TO 'fllc_admin'@'localhost';

-- 4e. Revoke a role
REVOKE 'role_write' FROM 'fllc_app'@'localhost';


-- ════════════════════════════════════════════════════════════
-- SECTION 5: VIEWS FOR SECURITY (COLUMN & ROW-LEVEL)
-- Views restrict which columns and rows a user can access,
-- without modifying the base tables.
-- ════════════════════════════════════════════════════════════

-- 5a. Column-level security — hide sensitive fields
CREATE OR REPLACE VIEW v_customer_public AS
SELECT customer_id,
       first_name,
       last_name,
       LEFT(email_address, 3) AS email_hint
FROM customers;

GRANT SELECT ON my_guitar_shop.v_customer_public TO 'fllc_readonly'@'%';

-- 5b. Row-level security — only shipped orders
CREATE OR REPLACE VIEW v_shipped_orders AS
SELECT o.order_id,
       o.order_date,
       o.ship_date,
       c.first_name,
       c.last_name
FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
WHERE o.ship_date IS NOT NULL;

GRANT SELECT ON my_guitar_shop.v_shipped_orders TO 'fllc_readonly'@'%';

-- 5c. Aggregated view — prevents access to individual records
CREATE OR REPLACE VIEW v_category_summary AS
SELECT cat.category_name,
       COUNT(p.product_id)   AS product_count,
       ROUND(AVG(p.list_price), 2) AS avg_price,
       MIN(p.list_price)     AS min_price,
       MAX(p.list_price)     AS max_price
FROM categories cat
    LEFT JOIN products p ON cat.category_id = p.category_id
GROUP BY cat.category_name;

GRANT SELECT ON my_guitar_shop.v_category_summary TO 'fllc_readonly'@'%';


-- ════════════════════════════════════════════════════════════
-- SECTION 6: SQL INJECTION PREVENTION
-- Prepared statements send the query structure and data
-- separately, making injection impossible.
-- ════════════════════════════════════════════════════════════

-- 6a. VULNERABLE pattern (never do this in application code):
--     SET @sql = CONCAT('SELECT * FROM customers WHERE last_name = "',
--                       user_input, '"');
--     If user_input = '" OR 1=1 --' → returns all rows.

-- 6b. SAFE pattern — MySQL prepared statement
PREPARE stmt_find_customer FROM
    'SELECT customer_id, first_name, last_name, email_address
     FROM customers
     WHERE last_name = ?';

SET @search_name = 'Sherwood';
EXECUTE stmt_find_customer USING @search_name;

DEALLOCATE PREPARE stmt_find_customer;

-- 6c. Stored procedure with parameterized input (inherently safe)
DELIMITER //

CREATE PROCEDURE sp_safe_customer_lookup(
    IN p_last_name VARCHAR(60)
)
BEGIN
    SELECT customer_id,
           first_name,
           last_name,
           email_address
    FROM customers
    WHERE last_name = p_last_name;
END //

DELIMITER ;

CALL sp_safe_customer_lookup('Sherwood');


-- ════════════════════════════════════════════════════════════
-- SECTION 7: PASSWORD MANAGEMENT
-- ════════════════════════════════════════════════════════════

-- 7a. Change a user's password
ALTER USER 'fllc_readonly'@'%'
    IDENTIFIED BY 'NewRead0nly$2026!';

-- 7b. Force password expiration (user must change on next login)
ALTER USER 'fllc_analyst'@'localhost'
    PASSWORD EXPIRE;

-- 7c. Set password policy (requires global SUPER privilege)
-- ALTER USER 'fllc_app'@'localhost'
--     PASSWORD EXPIRE INTERVAL 90 DAY
--     FAILED_LOGIN_ATTEMPTS 5
--     PASSWORD_LOCK_TIME 1;

-- 7d. Lock / unlock an account
ALTER USER 'fllc_readonly'@'%' ACCOUNT LOCK;
ALTER USER 'fllc_readonly'@'%' ACCOUNT UNLOCK;


-- ════════════════════════════════════════════════════════════
-- CLEANUP — remove demonstration users and roles
-- Uncomment to execute.
-- ════════════════════════════════════════════════════════════

-- DROP USER IF EXISTS 'fllc_admin'@'localhost';
-- DROP USER IF EXISTS 'fllc_analyst'@'localhost';
-- DROP USER IF EXISTS 'fllc_app'@'localhost';
-- DROP USER IF EXISTS 'fllc_readonly'@'%';
-- DROP ROLE IF EXISTS 'role_read', 'role_write', 'role_admin';
