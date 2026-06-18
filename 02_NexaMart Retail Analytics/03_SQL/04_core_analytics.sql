-- ================================================================================================================
-- ----------------------------------------------------------------------------------------------------------------
-- -------------------------Core Analytics using JOINS, CTE, SUBQUERIES and AGGREGATION----------------------------
-- ----------------------------------------------------------------------------------------------------------------
-- ================================================================================================================
-- 
-- ================================================================================================================
-- Query#1 -- Revenue by region and channel, per quarter
-- Multi-table JOIN and aggregation — total revenue ranked by region
-- ================================================================================================================
SELECT 
    r.region_name
    , SUM(o.total) AS net_total
FROM    
    orders o 
    INNER JOIN customers c 
        ON c.customer_id = o.customer_id
    INNER JOIN regions r 
        ON c.region_id = r.region_id
GROUP BY 
    r.region_name
ORDER BY 
    SUM(o.total) DESC
    
-- ================================================================================================================
-- Query#2 - Top 10 products by gross revenue net of returns
-- CTE + LEFT JOIN + COALESCE — gross sales minus refunds per product.
-- ================================================================================================================
WITH cte_orders AS (
    SELECT 
        product_id
        , SUM(line_total) AS Total_Sales 
    FROM
        order_details
    GROUP BY 
        product_id
), cte_returns AS (
    SELECT 
        product_id
        , SUM(qty * unit_return_amount) AS Total_Refunds
    FROM
        return_details
    GROUP BY
    product_id
)
SELECT 
    od.product_id
    , p.product_name
    , p.brand
    , Total_Sales - COALESCE(Total_Refunds,0) AS Net_Sales
FROM    
    cte_orders od 
    LEFT OUTER JOIN cte_returns rd 
        ON od.product_id = rd.product_id
    INNER JOIN products p 
        ON p.product_id = od.product_id
ORDER BY 
    Total_Sales - Total_Refunds DESC
LIMIT 10

-- ================================================================================================================
-- Query #3 - Customer lifetime value (CLV) by loyalty tier
-- Aggregation on view — net spend grouped by Standard, Premium, VIP.
-- ================================================================================================================
SELECT 
    c.loyalty_tier
    , SUM(vsr.net_order_value) AS clv_loyalty
FROM 
    v_sales_refund_summary vsr
    INNER JOIN customers c 
        ON c.customer_id = vsr.customer_id
GROUP BY
    c.loyalty_tier
ORDER BY 
    SUM(vsr.net_order_value) DESC
    
-- ================================================================================================================
-- Query #4 - Promo code usage frequency and avg discount value
-- CTE + date arithmetic + CASE — orders per active day per promo
-- ================================================================================================================
WITH ctn AS (
    SELECT
        o.promo_id
        , p.promo_code
        , p.start_date
        , p.end_date
        , COUNT(o.promo_id) AS promo_used
    FROM
        orders o
        INNER JOIN promotions p
            ON o.promo_id = p.promo_id
    WHERE
        o.promo_id IS NOT NULL
    GROUP BY
        o.promo_id
        , p.promo_code
        , p.start_date
        , p.end_date
)
SELECT
    promo_id
    , promo_code
    , promo_used
    , end_date - start_date AS active_days
    , CASE 
        WHEN 
            end_date - start_date > 0 
        THEN 
            ROUND(promo_used / (end_date - start_date),2)
        ELSE 0
    END AS promo_freq
FROM
    ctn
ORDER BY 
    promo_freq DESC
    
-- ================================================================================================================
-- Query #5 - Find customers who placed more than 3 orders but spent under $500 average
-- High Frequency Low Spend Customers
-- WHERE vs HAVING — Standard tier customers, 3+ orders under $500
-- ================================================================================================================
SELECT
    o.customer_id
    , c.customer_name
    , COUNT(o.order_id) AS num_of_orders
    , ROUND(AVG(o.total), 2) AS average_sales
    ,  ROUND(SUM(o.total), 2) AS total_sales
FROM 
    orders o
    INNER JOIN customers c 
        ON o.customer_id = c.customer_id
WHERE
    c.loyalty_tier = 'Standard'
GROUP BY 
    o.customer_id
    , c.customer_name
HAVING
    COUNT(o.order_id) > 3
    AND SUM(o.total) <=500
ORDER BY
    total_sales DESC

-- ================================================================================================================
-- Query #6 - Products Never Returned - NOT EXISTS correlated subquery — NULL-safe alternative to NOT IN
-- It short-circuits — stops scanning as soon as it finds one matching row — making it efficient on large tables.

-- SELECT 1 -- You don't need a real column — EXISTS only checks whether any row is found, not what's in it
-- Correlated The subquery references p.product_id from the outer query — it re-runs once per outer row
-- NOT IN risk If the subquery returns any NULL, NOT IN returns no rows at all — NOT EXISTS avoids this trap
-- ================================================================================================================
SELECT
  p.product_id
  , p.product_name
  , p.category
  , p.brand
FROM products p
WHERE NOT EXISTS (
  SELECT 1
  FROM return_details rd
  WHERE rd.product_id = p.product_id 
)
ORDER BY p.category, p.product_name;
-- ================================================================================================================
-- Query #7 - Customer B2C vs B2B Classification - based on email domain and extract region from city
-- String functions let you derive new fields from existing text columns 
-- useful when data isn't perfectly structured. Good for showing you can wrangle real-world messy data.
-- ================================================================================================================
SELECT
    c.customer_id
    , c.customer_name
    , c.email
    , SUBSTRING_INDEX(c.email, '@', -1) AS email_domain
    , CASE
        WHEN SUBSTRING_INDEX(c.email,'@',-1)
            IN ('gmail.com','yahoo.com','outlook.com',
                'hotmail.com','icloud.com','protonmail.com')
        THEN 'B2C'
        ELSE 'B2B'
        END 
    AS customer_type
    , CONCAT(ci.city_name, ', ', s.state_code) AS location_label
FROM 
    customers c
    INNER JOIN cities ci
        ON ci.city_id = c.city_id
    INNER JOIN states s 
        ON s.state_id = ci.state_id
ORDER BY 
    customer_type
    , email_domain

-- ================================================================================================================
-- Query #8 - Average Order Value by Region and Channel
-- SMulti-dimension GROUP BY across channel and region
-- ================================================================================================================
SELECT
    ch.channel_name
    , r.region_name
    , AVG(o.total) AS average_value
FROM
    orders o 
        INNER JOIN channels ch ON ch.channel_id = o.channel_id
        INNER JOIN customers c ON c.customer_id = o.customer_id
        INNER JOIN regions r ON r.region_id = c.region_id
GROUP BY
    ch.channel_name
    , r.region_name