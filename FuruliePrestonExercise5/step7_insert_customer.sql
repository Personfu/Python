-- =============================================================================
-- MySQL Exercise 5 - Step 7
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: INSERT a new customer into the Customers table using a
--              column list. The password is an empty string.
-- =============================================================================

USE my_guitar_shop;

-- Insert the new customer with a column list
INSERT INTO customers
    (email_address, password, first_name, last_name)
VALUES
    ('rick@raven.com', '', 'Rick', 'Raven');

-- Verify the insert was successful
SELECT *
FROM customers
WHERE email_address = 'rick@raven.com';
