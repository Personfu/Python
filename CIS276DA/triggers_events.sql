-- ============================================================
-- Triggers & Event Scheduling
-- CIS 276DA — Advanced SQL & Data Analytics | FLLC Enterprise
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: BEFORE/AFTER triggers (INSERT, UPDATE, DELETE),
-- OLD/NEW references, audit trail logging, data validation,
-- cascading business logic, and MySQL event scheduler.
-- ============================================================

USE my_guitar_shop;

-- ════════════════════════════════════════════════════════════
-- SECTION 0: SUPPORTING TABLES FOR TRIGGERS
-- ════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS product_audit_log (
    log_id         INT            AUTO_INCREMENT PRIMARY KEY,
    action_type    VARCHAR(10)    NOT NULL,
    product_id     INT            NOT NULL,
    product_name   VARCHAR(255),
    old_price      DECIMAL(10,2),
    new_price      DECIMAL(10,2),
    changed_by     VARCHAR(100),
    changed_at     DATETIME       DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_status_log (
    log_id      INT            AUTO_INCREMENT PRIMARY KEY,
    order_id    INT            NOT NULL,
    old_status  VARCHAR(20),
    new_status  VARCHAR(20),
    changed_at  DATETIME       DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS price_change_alerts (
    alert_id       INT            AUTO_INCREMENT PRIMARY KEY,
    product_id     INT            NOT NULL,
    product_name   VARCHAR(255),
    old_price      DECIMAL(10,2),
    new_price      DECIMAL(10,2),
    change_pct     DECIMAL(6,2),
    alert_level    VARCHAR(10),
    created_at     DATETIME       DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS daily_revenue_snapshot (
    snapshot_id    INT            AUTO_INCREMENT PRIMARY KEY,
    snapshot_date  DATE           NOT NULL,
    total_orders   INT,
    total_revenue  DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    created_at     DATETIME       DEFAULT NOW()
);


-- ════════════════════════════════════════════════════════════
-- SECTION 1: BEFORE INSERT TRIGGER — DATA VALIDATION
-- Fires before a new row is written. Use NEW to inspect and
-- modify the incoming values.
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_products_before_insert
BEFORE INSERT ON products
FOR EACH ROW
BEGIN
    IF NEW.list_price < 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'list_price cannot be negative';
    END IF;

    IF NEW.discount_percent < 0 OR NEW.discount_percent > 100 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'discount_percent must be between 0 and 100';
    END IF;

    IF NEW.product_name IS NULL OR TRIM(NEW.product_name) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'product_name cannot be empty';
    END IF;

    SET NEW.product_name = TRIM(NEW.product_name);
    SET NEW.date_added   = COALESCE(NEW.date_added, NOW());
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 2: AFTER INSERT TRIGGER — AUDIT LOGGING
-- Fires after the row is successfully inserted. OLD is not
-- available (there is no previous state for an INSERT).
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_products_after_insert
AFTER INSERT ON products
FOR EACH ROW
BEGIN
    INSERT INTO product_audit_log
        (action_type, product_id, product_name,
         old_price, new_price, changed_by)
    VALUES
        ('INSERT', NEW.product_id, NEW.product_name,
         NULL, NEW.list_price, CURRENT_USER());
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 3: BEFORE UPDATE TRIGGER — BUSINESS RULE ENFORCEMENT
-- Both OLD (current values) and NEW (incoming values) are
-- available. Modify NEW to override incoming data.
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_products_before_update
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    IF NEW.list_price < 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'list_price cannot be negative';
    END IF;

    IF NEW.discount_percent < 0 OR NEW.discount_percent > 100 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'discount_percent must be between 0 and 100';
    END IF;

    -- Prevent price increases greater than 50% in a single update
    IF OLD.list_price > 0
       AND NEW.list_price > OLD.list_price * 1.50 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Price increase cannot exceed 50% per update';
    END IF;
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 4: AFTER UPDATE TRIGGER — AUDIT TRAIL + ALERTS
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_products_after_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    DECLARE v_change_pct DECIMAL(6,2);
    DECLARE v_alert_level VARCHAR(10);

    -- Always log the change
    INSERT INTO product_audit_log
        (action_type, product_id, product_name,
         old_price, new_price, changed_by)
    VALUES
        ('UPDATE', NEW.product_id, NEW.product_name,
         OLD.list_price, NEW.list_price, CURRENT_USER());

    -- Generate alert when price changes significantly
    IF OLD.list_price != NEW.list_price AND OLD.list_price > 0 THEN
        SET v_change_pct = ROUND(
            (NEW.list_price - OLD.list_price) * 100.0 / OLD.list_price, 2);

        SET v_alert_level = CASE
            WHEN ABS(v_change_pct) >= 25 THEN 'CRITICAL'
            WHEN ABS(v_change_pct) >= 10 THEN 'WARNING'
            ELSE 'INFO'
        END;

        INSERT INTO price_change_alerts
            (product_id, product_name, old_price,
             new_price, change_pct, alert_level)
        VALUES
            (NEW.product_id, NEW.product_name, OLD.list_price,
             NEW.list_price, v_change_pct, v_alert_level);
    END IF;
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 5: BEFORE DELETE TRIGGER — PREVENT DELETION OF
--            PRODUCTS THAT HAVE BEEN ORDERED
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_products_before_delete
BEFORE DELETE ON products
FOR EACH ROW
BEGIN
    DECLARE v_order_count INT;

    SELECT COUNT(*)
    INTO v_order_count
    FROM order_items
    WHERE product_id = OLD.product_id;

    IF v_order_count > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot delete product with existing orders';
    END IF;
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 6: AFTER DELETE TRIGGER — LOG DELETIONS
-- Only OLD is available (the row that was removed).
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_products_after_delete
AFTER DELETE ON products
FOR EACH ROW
BEGIN
    INSERT INTO product_audit_log
        (action_type, product_id, product_name,
         old_price, new_price, changed_by)
    VALUES
        ('DELETE', OLD.product_id, OLD.product_name,
         OLD.list_price, NULL, CURRENT_USER());
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 7: ORDER SHIPPING TRIGGER — CASCADING LOGIC
-- When ship_date is set, log the status transition.
-- ════════════════════════════════════════════════════════════

DELIMITER //

CREATE TRIGGER tr_orders_after_update
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    DECLARE v_old_status VARCHAR(20);
    DECLARE v_new_status VARCHAR(20);

    SET v_old_status = CASE
        WHEN OLD.ship_date IS NOT NULL THEN 'Shipped'
        ELSE 'Processing'
    END;

    SET v_new_status = CASE
        WHEN NEW.ship_date IS NOT NULL THEN 'Shipped'
        ELSE 'Processing'
    END;

    IF v_old_status != v_new_status THEN
        INSERT INTO order_status_log
            (order_id, old_status, new_status)
        VALUES
            (NEW.order_id, v_old_status, v_new_status);
    END IF;
END //

DELIMITER ;


-- ════════════════════════════════════════════════════════════
-- SECTION 8: TRIGGER TESTING
-- ════════════════════════════════════════════════════════════

-- 8a. Test BEFORE INSERT validation (should succeed)
INSERT INTO products (category_id, product_code, product_name,
                      list_price, discount_percent, date_added)
VALUES (1, 'test_trg', 'Trigger Test Guitar', 599.99, 10, NOW());

-- 8b. Test AFTER INSERT audit log
SELECT * FROM product_audit_log ORDER BY log_id DESC LIMIT 1;

-- 8c. Test price update with alert generation
UPDATE products
SET list_price = 749.99
WHERE product_code = 'test_trg';

SELECT * FROM product_audit_log ORDER BY log_id DESC LIMIT 2;
SELECT * FROM price_change_alerts ORDER BY alert_id DESC LIMIT 1;

-- 8d. Test BEFORE INSERT validation (should fail — negative price)
-- INSERT INTO products (category_id, product_code, product_name,
--                       list_price, discount_percent, date_added)
-- VALUES (1, 'bad_price', 'Negative Price', -50.00, 10, NOW());

-- 8e. Clean up test data
DELETE FROM products WHERE product_code = 'test_trg';
SELECT * FROM product_audit_log ORDER BY log_id DESC LIMIT 3;


-- ════════════════════════════════════════════════════════════
-- SECTION 9: EVENT SCHEDULER
-- Events run SQL on a schedule (like cron jobs inside MySQL).
-- ════════════════════════════════════════════════════════════

-- 9a. Enable the event scheduler (requires SUPER or EVENT privilege)
SET GLOBAL event_scheduler = ON;
SHOW VARIABLES LIKE 'event_scheduler';

-- 9b. Daily revenue snapshot — runs every day at midnight
DELIMITER //

CREATE EVENT IF NOT EXISTS ev_daily_revenue_snapshot
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY
ON COMPLETION PRESERVE
COMMENT 'Captures daily revenue metrics at midnight'
DO
BEGIN
    INSERT INTO daily_revenue_snapshot
        (snapshot_date, total_orders, total_revenue, avg_order_value)
    SELECT CURDATE() - INTERVAL 1 DAY,
           COUNT(DISTINCT o.order_id),
           COALESCE(SUM((oi.item_price - oi.discount_amount) * oi.quantity), 0),
           COALESCE(AVG(order_totals.order_total), 0)
    FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN (SELECT o2.order_id,
                     SUM((oi2.item_price - oi2.discount_amount) * oi2.quantity) AS order_total
              FROM orders o2
                  JOIN order_items oi2 ON o2.order_id = oi2.order_id
              WHERE DATE(o2.order_date) = CURDATE() - INTERVAL 1 DAY
              GROUP BY o2.order_id) order_totals
            ON o.order_id = order_totals.order_id
    WHERE DATE(o.order_date) = CURDATE() - INTERVAL 1 DAY;
END //

DELIMITER ;

-- 9c. Cleanup event — purge audit logs older than 90 days
DELIMITER //

CREATE EVENT IF NOT EXISTS ev_purge_old_audit_logs
ON SCHEDULE EVERY 1 WEEK
STARTS CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 2 HOUR
ON COMPLETION PRESERVE
COMMENT 'Removes audit log entries older than 90 days'
DO
BEGIN
    DELETE FROM product_audit_log
    WHERE changed_at < NOW() - INTERVAL 90 DAY;

    DELETE FROM price_change_alerts
    WHERE created_at < NOW() - INTERVAL 90 DAY;
END //

DELIMITER ;

-- 9d. View scheduled events
SELECT event_name, event_type, execute_at, interval_value,
       interval_field, last_executed, status
FROM information_schema.events
WHERE event_schema = 'my_guitar_shop';


-- ════════════════════════════════════════════════════════════
-- SECTION 10: MANAGE TRIGGERS AND EVENTS
-- ════════════════════════════════════════════════════════════

-- List all triggers on the database
SHOW TRIGGERS FROM my_guitar_shop;

-- View trigger definitions
SELECT trigger_name, event_manipulation, event_object_table,
       action_timing, action_statement
FROM information_schema.triggers
WHERE trigger_schema = 'my_guitar_shop'
ORDER BY event_object_table, action_timing, event_manipulation;

-- Drop a trigger (uncomment to execute)
-- DROP TRIGGER IF EXISTS tr_products_before_insert;

-- Drop an event (uncomment to execute)
-- DROP EVENT IF EXISTS ev_daily_revenue_snapshot;
