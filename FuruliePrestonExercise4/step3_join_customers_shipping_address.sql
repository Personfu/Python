-- =============================================================================
-- MySQL Exercise 4 - Step 3
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: JOIN the Customers table to the Addresses table.
--              Returns first_name, last_name, line1, city, state, zip_code.
--              Only returns addresses that are the shipping address for a
--              customer (where the customer's shipping_address_id matches
--              the address_id).
-- =============================================================================

USE my_guitar_shop;

SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
FROM customers c
    INNER JOIN addresses a
        ON c.shipping_address_id = a.address_id;
