--  ===============================================================================================================
-- ----------------------------------------------------------------------------------------------------------------
-- -------------------------Advanced queries -- WINDOW FUNCTIONS, LAG, RUNNING TOTAL-------------------------------
-- ----------------------------------------------------------------------------------------------------------------
-- ================================================================================================================
-- 
-- ================================================================================================================
-- Query #1 - Return rate % by product category
-- CTE + DENSE_RANK() OVER PARTITION — ranks every product within its category by return rate for full leaderboard 
-- view
-- ================================================================================================================
WITH return_rates AS(
    SELECT
        od.product_id
        , od.total_sales 
        , rd.total_refunds
        , ROUND((rd.total_refunds * 100) /  od.total_sales, 2) AS return_rate
    FROM    
        v_sale_pdt od 
        LEFT OUTER JOIN v_refund_pdt rd 
            ON rd.product_id = od.product_id
)
SELECT 
    rr.product_id
    , rr.total_sales
    , rr.total_refunds
    , rr.return_rate
    , p.category
    , DENSE_RANK() OVER(
        PARTITION BY p.category
        ORDER BY return_rate DESC
    ) AS return_rate_rnk
FROM
    return_rates rr
    INNER JOIN products p
        ON p.product_id = rr.product_id
        
-- ================================================================================================================
-- Query #2 Top 3 idividual Customer lifetime value (CLV) within each loyalty tier
-- DENSE_RANK() OVER PARTITION + WHERE rnk <= 3 — filters to top 3 per tier, DENSE_RANK ensures no positions are
-- skipped on ties
-- ================================================================================================================
WITH ctn AS (
    SELECT 
        c.customer_id
        , c.loyalty_tier
        , SUM(vsr.net_order_value) AS clv_loyalty
        , DENSE_RANK () OVER(
            PARTITION BY c.loyalty_tier
            ORDER BY SUM(vsr.net_order_value) DESC
        ) AS rnk
    FROM 
        v_sales_refund_summary vsr
        INNER JOIN customers c 
            ON c.customer_id = vsr.customer_id
    GROUP BY
        c.customer_id
    ORDER BY 
        SUM(vsr.net_order_value) DESC
)
SELECT 
    * 
FROM 
    ctn 
WHERE 
    rnk <=3
ORDER BY 
    loyalty_tier
    , rnk
-- ================================================================================================================
-- Query #3 - 30-Day Moving Average Revenue
-- SUM() OVER with ROWS BETWEEN frame — smooths daily revenue over rolling 30 days
-- ================================================================================================================
SELECT
    order_date
    , SUM(total) AS daily_sales
    , ROUND(
        AVG(SUM(total)) OVER (
            ORDER BY order_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW 
        ) 
    , 2)AS moving_30_day_averge
FROM 
    orders
GROUP BY
    order_date
ORDER BY 
    order_date

-- ================================================================================================================
-- Query #4 - Supplier Scorecard Ranked by Region 
-- Score = rating × 1/lead_time
-- Weighted score in CTE + RANK() OVER PARTITION — best supplier per region
-- ================================================================================================================
WITH ctn AS (    
    SELECT
        supplier_name
        , region 
        , ROUND(rating * (1/lead_time_days), 2) AS supplier_score
        , RANK() OVER(
            PARTITION BY region
            ORDER BY ROUND(rating * (1/lead_time_days), 2) DESC
        ) AS rnk
    FROM 
        suppliers
    ORDER BY 
        region
        , rnk
)
SELECT 
    region
    , supplier_name
FROM
    ctn
WHERE 
    rnk = 1
ORDER BY 
    region

-- ================================================================================================================
-- Query #5 - Churn Risk by Loyalty Tier - finding customers with no purchase in the last 90-days
-- Note: the data is from 2022 to 2024 so, I am increasing the 90 days to 790 days to go 2-year before
-- MAX() + HAVING + SUBDATE — flags customers with no order in lookback window
-- ================================================================================================================
WITH ctn AS 
    (
    SELECT
        o.customer_id
        , c.loyalty_tier
        , MAX(o.order_date) AS most_recent_order
    FROM
        orders o
        INNER JOIN customers c 
            ON c.customer_id = o.customer_id
    GROUP BY
        o.customer_id
    HAVING
        MAX(o.order_date) < SUBDATE(CURRENT_DATE(),  INTERVAL 790 DAY)
)
SELECT 
    loyalty_tier
    , COUNT(most_recent_order) AS customer_churn
FROM 
    ctn 
GROUP BY
    loyalty_tier
ORDER BY 
    customer_churn DESC
    
-- ================================================================================================================
-- Query #6 - Revenue split by channel each quarter
-- CASE WHEN inside SUM() — three channel columns in one pass, no UNION
-- ================================================================================================================
SELECT
    d.year_full
    , d.qtr_num
    , SUM(
        CASE 
            WHEN c.channel_id = 1 THEN o.total ELSE 0 
        END
    ) AS online_revenue
    , SUM(
        CASE 
            WHEN c.channel_id = 2 THEN o.total ELSE 0 
        END
    ) AS store_revenue
    , SUM(
        CASE 
            WHEN c.channel_id = 3 THEN o.total ELSE 0 
        END
    ) AS marketplace_revenue
    , SUM(total) AS total_revenue
FROM 
    orders o
    INNER JOIN channels c 
        ON c.channel_id = o.channel_id
    INNER JOIN dates d 
        ON d.date_id = o.date_id 
GROUP BY 
    d.year_full
    , d.qtr_num
ORDER BY
     d.year_full
    , d.qtr_num
    
-- ================================================================================================================
-- Query #7 - Top 3 products by revenue inside each category
-- Chained CTEs + DENSE_RANK() OVER PARTITION — top revenue SKUs per category
-- ================================================================================================================
WITH product_rev AS (
    SELECT
        p.category
        , p.product_name
        , SUM(od.line_total) AS revenue
    FROM 
        order_details od
        INNER JOIN products p 
            ON od.product_id = p.product_id
    GROUP BY 
        p.category
        , p.product_name
), rnk AS (
    SELECT
        category
        , product_name
        , revenue
        , DENSE_RANK() OVER(
        PARTITION BY category 
            ORDER BY revenue DESC
        ) AS dense_rnk
    FROM 
        product_rev
)
SELECT 
    category
    , product_name
    , revenue
    , dense_rnk
FROM
    rnk
WHERE 
    dense_rnk <=3

-- ================================================================================================================
-- Query #8 - Cumulative revenue by month — see when you hit yearly targets
-- A running total accumulates as it goes — each row holds the sum of all previous rows plus itself. 
-- This is the simplest window function and a great entry point for understanding OVER().
-- ================================================================================================================
SELECT
    d.year_full 
    , d.month_num
    , SUM(o.total) AS monthly_revenue
    , SUM(SUM(o.total)) OVER(
        PARTITION BY d.year_full
        ORDER BY d.month_num
    ) AS cumulative_ytd
FROM
    orders o
    INNER JOIN dates d 
        ON d.date_id = o.date_id
GROUP BY
    d.year_full 
    , d.month_num
ORDER BY
    d.year_full 
    , d.month_num

-- ================================================================================================================
-- Query #9 - Channel revenue share shift year-over-year
-- Year-over-year comparison using LAG window function 
-- ================================================================================================================
WITH ctn AS(
    SELECT
        v.channel_id 
        , c.channel_name
        , YEAR(v.order_date) AS order_year
        , SUM(v.net_order_value) AS channel_sales
        , LAG(SUM(v.net_order_value)) OVER(
            PARTITION BY channel_id
            ORDER BY YEAR(v.order_date) 
        ) AS prev_year_sales
    FROM 
        v_sales_refund_summary v 
        INNER JOIN channels c 
         ON c.channel_id = v.channel_id
    GROUP BY
        v.channel_id 
        , YEAR(v.order_date)
)
SELECT 
    channel_name
    , order_year
    , COALESCE(channel_sales - prev_year_sales, "NA") AS rev_shift_yearly
FROM
    ctn
ORDER BY 
    channel_id
    , order_year