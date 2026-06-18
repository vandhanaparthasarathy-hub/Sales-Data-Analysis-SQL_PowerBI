-- ================================================================================================================
-- ----------------------------------------------------------------------------------------------------------------
-- -----------------------------------Column Fixes and Tax Lineage Correction--------------------------------------
-- ----------------------------------------------------------------------------------------------------------------
-- ================================================================================================================
-- 
-- ================================================================================================================
-- #1 - The discount_amount in orders looks misleading - it is the discount already applied on the order that gives 
-- the subtotal, because it is displayed after the subtotal, we might think that this discount will be applied on 
-- the subtotal. So I am moving it to appear after promo_id but before subtotal, and renaming it to discount_applied.
-- This way, we now know that the discount, if any, is applied on the order and that gives the subtotal
-- ================================================================================================================
-- ================================================================================================================
-- Step 1 - Move discount_amount right after promo_id
-- ================================================================================================================
ALTER TABLE orders
MODIFY COLUMN discount_amount DECIMAL(10,2) AFTER promo_id;

-- ================================================================================================================
-- Step 2 - Change name from discount_amount to discount_applied
-- ================================================================================================================
ALTER TABLE orders
RENAME COLUMN discount_amount TO discount_applied;

-- ================================================================================================================
-- #2 - City was not linked to States table and the synthetic data missed the logical connection between these tables.
-- Added cities Table; Made updates to customers table and connected them all to update the tax rate and total in 
-- the orders table
-- ================================================================================================================
-- ================================================================================================================
-- Step 1 - Create a new table - cities (refenece 01_db_tablesetup -- 13. CITIES)
-- ================================================================================================================
-- ================================================================================================================
-- Step 2 - Add a new column to customers table
-- ================================================================================================================
ALTER TABLE customers 
ADD COLUMN city_id INT NULL;

-- ================================================================================================================
-- Step 3 - set city_id in customers table by referencing the city name from the cities table
-- ================================================================================================================
UPDATE customers c
JOIN cities ci ON ci.city_name = c.city
SET c.city_id = ci.city_id;

-- ================================================================================================================
-- Step 4 - For future use, make the city_id coloumn in customers table NOT NULL and create a foreign ket constraint
-- Also move the city_id column after city column
-- ================================================================================================================
ALTER TABLE customers
MODIFY COLUMN city_id INT NOT NULL
, MODIFY COLUMN city_id INT AFTER city
, ADD CONSTRAINT fk_customers_city
FOREIGN KEY (city_id) REFERENCES cities(city_id);

-- ================================================================================================================
-- Step 5 - To maintain data lineage and also save storage, we can drop city column from customers table 
-- Encourage to clean the incoming data to follow this pattern 
-- ================================================================================================================
ALTER TABLE customers
DROP COLUMN city
-- ================================================================================================================
-- #3 - Fix the orders table to reflect the correct tax based on the city id present in orders table 
-- Multi-join Update Query
-- ================================================================================================================
-- ================================================================================================================
-- Step 1 - Identifying all the columns that needed an update and saving a backup
-- ================================================================================================================
/*SELECT
    o.order_id
    , o.tax_rate AS current_tax_rate
    , s.tax_rate AS correct_tax_rate
    , o.subtotal
    , o.total AS current_total
    , ROUND(o.subtotal + (o.subtotal * s.tax_rate), 2) AS correct_total
FROM 
    orders o
    INNER JOIN customers  c 
        ON o.customer_id = c.customer_id
    INNER JOIN cities     ci 
        ON c.city_id    = ci.city_id
    INNER JOIN states     s 
        ON ci.state_id   = s.state_id
WHERE 
    o.tax_rate <> s.tax_rate
*/

-- ================================================================================================================
-- Step 2 - Update the columns that do not match the tax rate in the states table
-- ================================================================================================================
UPDATE orders o
    JOIN customers c 
        ON o.customer_id = c.customer_id
    JOIN cities ci 
        ON c.city_id    = ci.city_id
    JOIN states s 
        ON ci.state_id   = s.state_id
SET
    o.tax_rate = s.tax_rate,
    o.total    = ROUND(o.subtotal + (o.subtotal * s.tax_rate), 2)
WHERE
    o.tax_rate <> s.tax_rate,
    o.total    <> ROUND(o.subtotal + (o.subtotal * s.tax_rate), 2);