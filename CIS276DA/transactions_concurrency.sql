-- ============================================================
-- Transactions & Concurrency Control
-- CIS 276DA — Advanced SQL & Data Analytics | FLLC Enterprise
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: BEGIN/COMMIT/ROLLBACK, SAVEPOINT, isolation levels,
-- locking concepts (shared, exclusive, deadlocks), and
-- concurrency anomalies (dirty/non-repeatable/phantom reads).
-- ============================================================

USE my_guitar_shop;

-- ════════════════════════════════════════════════════════════
-- SECTION 1: TRANSACTION BASICS — BEGIN, COMMIT, ROLLBACK
-- A transaction is a logical unit of work: all statements
-- succeed together or fail together (atomicity).
-- ════════════════════════════════════════════════════════════

-- 1a. Simple committed transaction — insert a new category
START TRANSACTION;

    INSERT INTO categories (category_name)
    VALUES ('Keyboards');

    SELECT * FROM categories ORDER BY category_id DESC LIMIT 1;

COMMIT;

-- 1b. Rolled-back transaction — undo a mistaken delete
START TRANSACTION;

    DELETE FROM products
    WHERE product_id = 1;

    SELECT COUNT(*) AS remaining_products FROM products;

ROLLBACK;

SELECT COUNT(*) AS products_after_rollback FROM products;

-- 1c. Multi-statement transaction — transfer logic pattern
--     Simulates moving an item between categories atomically
START TRANSACTION;

    UPDATE products
    SET    category_id = 2
    WHERE  product_id = 3;

    UPDATE products
    SET    discount_percent = discount_percent + 5
    WHERE  product_id = 3;

COMMIT;


-- ════════════════════════════════════════════════════════════
-- SECTION 2: SAVEPOINTS
-- SAVEPOINTs create named markers within a transaction so you
-- can roll back to a specific point without aborting the
-- entire transaction.
-- ════════════════════════════════════════════════════════════

START TRANSACTION;

    INSERT INTO categories (category_name)
    VALUES ('Violins');

    SAVEPOINT sp_after_violins;

    INSERT INTO categories (category_name)
    VALUES ('Cellos');

    SAVEPOINT sp_after_cellos;

    INSERT INTO categories (category_name)
    VALUES ('Harps');

    -- Undo only the Harps insert; Violins and Cellos remain
    ROLLBACK TO SAVEPOINT sp_after_cellos;

    SELECT * FROM categories ORDER BY category_id DESC LIMIT 5;

COMMIT;

-- Clean up demonstration data
DELETE FROM categories WHERE category_name IN ('Violins', 'Cellos', 'Keyboards');


-- ════════════════════════════════════════════════════════════
-- SECTION 3: ISOLATION LEVELS
-- Isolation levels control what concurrent transactions can
-- see. Higher isolation = more consistency but lower throughput.
--
-- Level               | Dirty Read | Non-Repeatable Read | Phantom Read
-- --------------------|------------|---------------------|-------------
-- READ UNCOMMITTED    |    Yes     |        Yes          |     Yes
-- READ COMMITTED      |    No      |        Yes          |     Yes
-- REPEATABLE READ     |    No      |        No           |     Yes*
-- SERIALIZABLE        |    No      |        No           |     No
--
-- * MySQL InnoDB prevents phantom reads at REPEATABLE READ
--   via gap locks (an engine-specific optimization).
-- ════════════════════════════════════════════════════════════

-- 3a. READ UNCOMMITTED — allows dirty reads
--     Session A can see uncommitted changes from Session B.
--     Rarely used in production; useful only for rough estimates.
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

START TRANSACTION;
    SELECT @@transaction_isolation AS current_level;
    SELECT product_name, list_price FROM products WHERE product_id = 1;
COMMIT;

-- 3b. READ COMMITTED — the default in many RDBMS (PostgreSQL, Oracle)
--     Each SELECT sees only committed data, but re-reading the
--     same row may return different values if another transaction
--     committed between reads (non-repeatable read).
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

START TRANSACTION;
    SELECT @@transaction_isolation AS current_level;
    SELECT product_name, list_price FROM products WHERE product_id = 1;
    -- Another session could UPDATE and COMMIT product_id = 1 here
    SELECT product_name, list_price FROM products WHERE product_id = 1;
COMMIT;

-- 3c. REPEATABLE READ — MySQL InnoDB default
--     Guarantees the same result for repeated reads within a
--     transaction. Uses snapshot isolation.
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

START TRANSACTION;
    SELECT @@transaction_isolation AS current_level;
    SELECT product_name, list_price FROM products WHERE product_id = 1;
    -- Even if another session updates and commits, this SELECT
    -- returns the same snapshot value
    SELECT product_name, list_price FROM products WHERE product_id = 1;
COMMIT;

-- 3d. SERIALIZABLE — strictest level
--     Transactions behave as if executed one at a time.
--     All SELECTs implicitly become SELECT ... LOCK IN SHARE MODE.
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

START TRANSACTION;
    SELECT @@transaction_isolation AS current_level;
    SELECT COUNT(*) AS product_count FROM products;
    -- No other session can INSERT into products until this commits
COMMIT;

-- Reset to MySQL default
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;


-- ════════════════════════════════════════════════════════════
-- SECTION 4: LOCKING CONCEPTS
-- InnoDB uses row-level locking by default.
-- Shared locks (S) allow concurrent reads.
-- Exclusive locks (X) block all other access to the row.
-- ════════════════════════════════════════════════════════════

-- 4a. Shared lock — SELECT ... FOR SHARE
--     Other sessions can read but cannot modify locked rows.
START TRANSACTION;

    SELECT product_name, list_price
    FROM products
    WHERE product_id = 1
    FOR SHARE;

    -- Another session can SELECT but cannot UPDATE product_id = 1
    -- until this transaction commits or rolls back.

COMMIT;

-- 4b. Exclusive lock — SELECT ... FOR UPDATE
--     Locks the row for modification; blocks all other access.
START TRANSACTION;

    SELECT product_name, list_price
    FROM products
    WHERE product_id = 1
    FOR UPDATE;

    UPDATE products
    SET list_price = list_price * 1.10
    WHERE product_id = 1;

COMMIT;

-- 4c. Lock wait timeout
--     If a lock cannot be acquired within innodb_lock_wait_timeout
--     seconds, the statement fails with ER_LOCK_WAIT_TIMEOUT.
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';


-- ════════════════════════════════════════════════════════════
-- SECTION 5: CONCURRENCY ANOMALIES — DEMONSTRATIONS
-- These examples describe multi-session scenarios. Run each
-- numbered step in the indicated session.
-- ════════════════════════════════════════════════════════════

-- ── 5a. Dirty Read (requires READ UNCOMMITTED) ──────────
-- Session A:
--   SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
--   START TRANSACTION;
--   SELECT list_price FROM products WHERE product_id = 1;
--   -- Sees the uncommitted value from Session B
--
-- Session B:
--   START TRANSACTION;
--   UPDATE products SET list_price = 9999.99 WHERE product_id = 1;
--   -- Does NOT commit yet
--
-- Session A reads 9999.99 (dirty data).
-- Session B then ROLLBACK → the value never really was 9999.99.

-- ── 5b. Non-Repeatable Read (READ COMMITTED) ────────────
-- Session A:
--   SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
--   START TRANSACTION;
--   SELECT list_price FROM products WHERE product_id = 1;  -- sees 799.00
--
-- Session B:
--   UPDATE products SET list_price = 849.00 WHERE product_id = 1;
--   COMMIT;
--
-- Session A:
--   SELECT list_price FROM products WHERE product_id = 1;  -- sees 849.00
--   COMMIT;
-- Same row, same transaction, different values.

-- ── 5c. Phantom Read (READ COMMITTED) ───────────────────
-- Session A:
--   SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
--   START TRANSACTION;
--   SELECT COUNT(*) FROM products WHERE list_price > 2000;  -- e.g. 3
--
-- Session B:
--   INSERT INTO products (category_id, product_code, product_name,
--                         list_price, discount_percent, date_added)
--   VALUES (1, 'phantom', 'Phantom Guitar', 2500, 0, NOW());
--   COMMIT;
--
-- Session A:
--   SELECT COUNT(*) FROM products WHERE list_price > 2000;  -- now 4
--   COMMIT;
-- A new "phantom" row appeared within the same transaction.


-- ════════════════════════════════════════════════════════════
-- SECTION 6: DEADLOCK SCENARIO
-- A deadlock occurs when two transactions each hold a lock
-- that the other needs. InnoDB detects deadlocks and aborts
-- one transaction (the victim) so the other can proceed.
-- ════════════════════════════════════════════════════════════

-- Session A:
--   START TRANSACTION;
--   UPDATE products SET list_price = 100 WHERE product_id = 1;  -- locks row 1
--
-- Session B:
--   START TRANSACTION;
--   UPDATE products SET list_price = 200 WHERE product_id = 2;  -- locks row 2
--
-- Session A:
--   UPDATE products SET list_price = 300 WHERE product_id = 2;  -- waits for B
--
-- Session B:
--   UPDATE products SET list_price = 400 WHERE product_id = 1;  -- DEADLOCK
--   -- InnoDB rolls back one session and returns:
--   -- ERROR 1213: Deadlock found when trying to get lock

-- Check recent deadlock information
SHOW ENGINE INNODB STATUS;


-- ════════════════════════════════════════════════════════════
-- SECTION 7: BEST PRACTICES FOR TRANSACTION MANAGEMENT
-- ════════════════════════════════════════════════════════════

-- 7a. Keep transactions short to minimize lock duration
-- BAD:  START TRANSACTION → complex report → UPDATE → COMMIT
-- GOOD: START TRANSACTION → UPDATE → COMMIT (report separately)

-- 7b. Stored procedure with proper error handling and rollback
DELIMITER //

CREATE PROCEDURE sp_place_order(
    IN p_customer_id  INT,
    IN p_product_id   INT,
    IN p_quantity      INT,
    OUT p_order_id     INT
)
BEGIN
    DECLARE v_price      DECIMAL(10,2);
    DECLARE v_discount   DECIMAL(10,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_order_id = -1;
    END;

    START TRANSACTION;

        SELECT list_price,
               ROUND(list_price * discount_percent / 100, 2)
        INTO v_price, v_discount
        FROM products
        WHERE product_id = p_product_id
        FOR UPDATE;

        INSERT INTO orders (customer_id, order_date)
        VALUES (p_customer_id, NOW());

        SET p_order_id = LAST_INSERT_ID();

        INSERT INTO order_items (order_id, product_id, item_price,
                                 discount_amount, quantity)
        VALUES (p_order_id, p_product_id, v_price, v_discount, p_quantity);

    COMMIT;
END //

DELIMITER ;

-- 7c. Always access tables in the same order to prevent deadlocks
-- Convention: categories → products → orders → order_items

-- 7d. Use appropriate isolation level for the workload
-- OLTP (fast writes):  REPEATABLE READ or READ COMMITTED
-- Reporting (reads):   READ COMMITTED (avoids long-held locks)
-- Financial / audit:   SERIALIZABLE (full consistency)
