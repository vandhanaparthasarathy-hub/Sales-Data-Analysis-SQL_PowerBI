-- ================================================================================================================
-- -------------------------------------------------Stored Views---------------------------------------------------
-- ================================================================================================================
-- 
-- ================================================================================================================
-- View #1 - Summary of orders and items returned in the order to identify 
-- Net Sales through an order
-- ================================================================================================================
CREATE OR REPLACE VIEW v_sales_refund_summary AS
    SELECT 
        o.order_id
        , o.customer_id
        , o.channel_id
        , o.promo_id
        , o.order_date
        , o.total 
        , r.return_id
        , r.return_date
        , r.total_refund_amount
        , o.total - COALESCE(r.total_refund_amount,0) AS net_order_value
    FROM
        orders o
        LEFT OUTER JOIN returns r 
            ON o.order_id = r.order_id

-- ================================================================================================================
-- View #2 - Sum of each product items that was sold
-- ================================================================================================================
CREATE OR REPLACE VIEW v_sale_pdt AS
    SELECT 
            product_id
            , SUM(line_total) AS total_sales
            , SUM(qty) AS total_units_sold
        FROM
            order_details
        GROUP BY 
            product_id

-- ================================================================================================================
-- View #3 - Sum of each product items that was returned and a refund issued
-- ================================================================================================================
CREATE OR REPLACE VIEW v_refund_pdt AS
    SELECT 
            product_id
            , SUM(qty * unit_return_amount) AS total_refunds
            , SUM(qty) AS total_units_returned
        FROM
            return_details
        GROUP BY
        product_id

-- ================================================================================================================
-- View #4 - Order Summary and information
-- ================================================================================================================
CREATE OR REPLACE VIEW v_order_summary AS
    SELECT
        o.order_id
        , o.order_date
        , SUM(od.unit_price * od.qty) AS total_pre_discount 
        , CASE 
            WHEN p.discount_type ='percentage' 
                THEN CONCAT(p.discount_value , '%') 
            WHEN  p.discount_type = 'fixed'
                THEN CONCAT(SUM(od.qty) * p.discount_value , ' dollar') 
            ELSE 
                'NA'
        END AS discount
        , o.discount_applied
        , o.subtotal
        , CONCAT(
            ROUND(
                o.subtotal * o.tax_rate
                , 2)
            , ' ('
            ,CAST(
                (ROUND(
                    o.tax_rate * 100
                    , 1)
                ) AS CHAR)
            , '%)'
        ) AS tax
        , o.total
    FROM
        orders o
        INNER JOIN order_details od
            ON od.order_id = o.order_id
        LEFT OUTER JOIN promotions p
            ON p.promo_id = o.promo_id
    GROUP BY 
        o.order_id
        , o.order_date
        , p.discount_value
        , p.discount_type
        , o.subtotal
        , o.discount_applied
        , o.tax_rate
        , o.total