-- ================================================================================================================
-- ----------------------------------------------------------------------------------------------------------------
-- -------------------------------------------Database and DDL Setup-----------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------
-- ================================================================================================================
-- 
-- ================================================================================================================
-- Create and Use the new Database
-- ================================================================================================================
CREATE DATABASE IF NOT EXISTS nexamart;

USE nexamart;
 
-- ================================================================================================================
-- Create New Tables
-- ================================================================================================================
-- ================================================================================================================
-- 1. REGIONS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS regions (
    region_id       INT         NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , region_code   CHAR(2)     NOT NULL    -- 'Two-letter abbreviation, e.g. NE'
    , region_name   VARCHAR(50) NOT NULL
    , hub_city      VARCHAR(50) NOT NULL
);

-- ================================================================================================================
-- 2. STATES
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS states (
    state_id        INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , region_id     INT             NOT NULL
    , state_code    CHAR(2)         NOT NULL    -- 'USPS two-letter code'
    , state_name    VARCHAR(50)     NOT NULL
    , tax_rate      DECIMAL(6,4)    NOT NULL    -- 'Statutory rate e.g. 0.0800 = 8%'
    , CONSTRAINT fk_states_region
        FOREIGN KEY (region_id) REFERENCES regions (region_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ================================================================================================================
-- 3. DATES  (date dimension spine, no gaps 2022-01-01 to 2024-12-31)
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS dates (
    date_id       INT         NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , date_full   DATE        NOT NULL
    , year_full   INT         NOT NULL
    , qtr_num     INT         NOT NULL    -- '1 to 4'
    , month_num   INT         NOT NULL    -- '1 to 12'
    , week_num    INT         NOT NULL    -- 'ISO week number'
    , is_weekend  BOOLEAN     NOT NULL    DEFAULT 0
    , is_holiday  BOOLEAN     NOT NULL    DEFAULT 0
    , KEY idx_dates_year_month   (year_full, month_num)
    , KEY idx_dates_year_quarter (year_full, qtr_num)
);

-- ================================================================================================================
-- 4. CHANNELS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS channels (
    channel_id     INT            NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , channel_name VARCHAR(30)    NOT NULL -- 'Online | Store | Marketplace',
);

-- ================================================================================================================
-- 5. SUPPLIERS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id         INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , supplier_name     VARCHAR(80)     NOT NULL
    , region            VARCHAR(30)     NOT NULL
    , lead_time_days    INT             NOT NULL -- 'Avg days PO to delivery'
    , rating            DECIMAL(2,1)    NOT NULL -- 'Internal score 1.0 to 5.0'
);

ALTER TABLE suppliers 
MODIFY COLUMN rating DECIMAL(2,1);

-- ================================================================================================================
-- 6. PRODUCTS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS products (
    product_id      INT             NOT NULL    AUTO_INCREMENT   PRIMARY KEY
    , product_name  VARCHAR(120)    NOT NULL
    , category      VARCHAR(40)     NOT NULl
    , brand         VARCHAR(60)     NOT NULL
    , supplier_id   INT             NOT NULL
    , KEY idx_products_category (category)
    , KEY idx_products_brand    (brand)
    , CONSTRAINT fk_products_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ================================================================================================================
-- 7. VARIANTS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS variants (
    variant_id      INT             NOT NULL    AUTO_INCREMENT PRIMARY KEY 
    , product_id    INT             NOT NULL
    , variant_type  VARCHAR(20)     NOT NULL    -- 'Color | Size | Pack | Edition | Scent | Age'
    , variant_name  VARCHAR(30)     NOT NULL
    , unit_cost     DECIMAL(10,2)   NOT NULL    -- 'Landed cost from supplier'
    , unit_price    DECIMAL(10,2)   NOT NULL    -- 'Retail selling price'
    , KEY idx_variants_product (product_id)
    , CONSTRAINT fk_variants_product
        FOREIGN KEY (product_id) REFERENCES products (product_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ================================================================================================================
-- 8. CUSTOMERS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id         INT             NOT NULL    AUTO_INCREMENT PRIMARY KEY
    , customer_name     VARCHAR(100)    NOT NULL
    , email             VARCHAR(120)    NOT NULL
    , country           CHAR(3)         NOT NULL    DEFAULT 'USA'
    , region_id         INT             NOT NULL    
    , city              VARCHAR(60)     NOT NULL
    , loyalty_tier      ENUM('Standard'
                            ,'Premium'
                            ,'VIP')     NOT NULL    DEFAULT 'Standard'
    , join_date         DATE            NOT NULL
    , KEY idx_customers_tier   (loyalty_tier)
    , KEY idx_customers_region (region_name)
    , CONSTRAINT fk_customers_regid 
    FOREIGN KEY (region_id) REFERENCES regions (region_id)  ON UPDATE CASCADE ON DELETE RESTRICT; 
);

-- ================================================================================================================
-- 9. PROMOTIONS
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS promotions (
    promo_id            INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , promo_code        VARCHAR(20)     NOT NULL
    , discount_type     ENUM('percentage'
                            ,'fixed')   NOT NULL
    , discount_value    DECIMAL(6,2)    NOT NULL    -- 'Pct (0-100) or fixed $ amount'
    , start_date        DATE            NOT NULL
    , end_date          DATE            NOT NULL
    , KEY idx_promos_dates (start_date, end_date)
);

-- ================================================================================================================
-- 10. ORDERS  (fact table — transaction header)
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS orders (
    order_id            INT     NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , date_id           INT     NOT NULL
    , order_date        DATE            NOT NULL
    , customer_id       INT     NOT NULL
    , channel_id        INT             NOT NULL
    , promo_id          INT             NULL        -- 'NULL when no promo applied'
    , subtotal          DECIMAL(12,2)   NOT NULL    -- 'Sum of line totals after discounts'
    , discount_amount   DECIMAL(10,2)   NOT NULL    DEFAULT 0.00
    , tax_rate          DECIMAL(6,4)    NOT NULL    -- 'State tax rate at time of order'
    , total             DECIMAL(12,2)   NOT NULL    -- 'subtotal + (subtotal * tax_rate)'
    , KEY idx_orders_date      (order_date)
    , KEY idx_orders_date_id   (date_id)
    , KEY idx_orders_customer  (customer_id)
    , KEY idx_orders_channel   (channel_id)
    , KEY idx_orders_promo     (promo_id)
    , CONSTRAINT fk_orders_date
        FOREIGN KEY (date_id)     REFERENCES dates     (date_id)     ON UPDATE CASCADE ON DELETE RESTRICT
    , CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
    , CONSTRAINT fk_orders_channel
        FOREIGN KEY (channel_id)  REFERENCES channels  (channel_id)  ON UPDATE CASCADE ON DELETE RESTRICT
    , CONSTRAINT fk_orders_promo
        FOREIGN KEY (promo_id)    REFERENCES promotions(promo_id)    ON UPDATE CASCADE ON DELETE SET NULL
);

-- ================================================================================================================
-- 11. ORDER_DETAILS  (fact table — line items)
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , order_id      INT             NOT NULL
    , product_id    INT             NOT NULL
    , variant_id    INT             NOT NULL
    , qty           INT             NOT NULL    DEFAULT 1
    , unit_price    DECIMAL(10,2)   NOT NULL    -- 'Price at time of sale'
    , unit_discount DECIMAL(10,2)   NOT NULL    DEFAULT 0.00
    , line_total    DECIMAL(12,2)   NOT NULL    -- '(unit_price - unit_discount) * qty'
    , KEY idx_od_order   (order_id)
    , KEY idx_od_product (product_id)
    , KEY idx_od_variant (variant_id)
    , CONSTRAINT fk_od_order
        FOREIGN KEY (order_id)   REFERENCES orders   (order_id)   ON UPDATE CASCADE ON DELETE RESTRICT
    , CONSTRAINT fk_od_product
        FOREIGN KEY (product_id) REFERENCES products (product_id) ON UPDATE CASCADE ON DELETE RESTRICT
    , CONSTRAINT fk_od_variant
        FOREIGN KEY (variant_id) REFERENCES variants (variant_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ================================================================================================================
-- 12. RETURNS  (return header — one per returned order)
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS returns (
    return_id               INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , order_id              INT             NOT NULL
    , return_date           DATE            NOT NULL
    , total_refund_amount   DECIMAL(12,2)   NOT NULL
    , KEY idx_returns_order       (order_id)
    , KEY idx_returns_return_date (return_date)
    , CONSTRAINT fk_returns_order
        FOREIGN KEY (order_id) REFERENCES orders (order_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ================================================================================================================
-- 13. RETURN_DETAILS  (line-level return detail)
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS return_details (
    return_detail_id        INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , return_id             INT             NOT NULL
    , product_id            INT             NOT NULL
    , qty                   INT             NOT NULL    DEFAULT 1
    , reason                VARCHAR(80)     NOT NULL
    , unit_return_amount    DECIMAL(10,2)   NOT NULL    -- 'Refund per unit (may exclude restocking fee)'
    , KEY idx_rd_return  (return_id)
    , KEY idx_rd_product (product_id)
    , CONSTRAINT fk_rd_return
        FOREIGN KEY (return_id)  REFERENCES returns  (return_id)  ON UPDATE CASCADE ON DELETE RESTRICT
    , CONSTRAINT fk_rd_product
        FOREIGN KEY (product_id) REFERENCES products (product_id) ON UPDATE CASCADE ON DELETE RESTRICT
);
-- ================================================================================================================
-- 13. CITIES (As a part of the cleanup, added this new table to identify the states and update the correct Tax)
-- ================================================================================================================
CREATE TABLE IF NOT EXISTS cities (
    city_id     INT             NOT NULL    AUTO_INCREMENT  PRIMARY KEY
    , city_name VARCHAR(60)     NOT NULL
    , state_id  INT             NOT NULL 
    , CONSTRAINT fk_cities_state
      FOREIGN KEY (state_id) REFERENCES states (state_id) ON UPDATE CASCADE ON DELETE RESTRICT
);
-- ================================================================================================================
-- ================================================================================================================