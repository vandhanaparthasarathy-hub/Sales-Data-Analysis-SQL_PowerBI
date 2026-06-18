# 🛒 NexaMart Retail Analytics

> *"Everything, Everywhere, Every Day"*

A full-stack analytics project on a synthetic US omnichannel mega-retailer — built to answer real business questions using advanced SQL, with a Power BI dashboard in progress.

---

## 🏢 Business Context

NexaMart is an imaginary US-based omnichannel retailer operating across 6 US regions — Online, In-Store, and Marketplace — with a catalog of 100 products across 5 categories, served by 12 specialized suppliers. The company has 2,000 customers (75% B2C, 25% B2B), runs 6 strategic promo events per year, and spans 3 years of transaction history from January 2022 to December 2024.

The goal was not just to write SQL queries — it was to **behave like an analyst embedded in this business**: identify real problems, clean the data, design the model, and answer the questions leadership would actually ask.

Please note that this synthetic data was created with the help of **Claude AI**.

---

## 🗂️ Dataset at a Glance

| | |
|---|---|
| **Transaction rows** | 5,738 orders · 15,613 line items |
| **Date range** | Jan 2022 — Dec 2024 (3 years) |
| **Customers** | 2,000 (75% B2C · 25% B2B) |
| **Products** | 100 SKUs · 287 variants |
| **Suppliers** | 12 across 5 categories |
| **US Coverage** | 6 regions · 24 states · 72 cities |
| **Tables** | 14 (including cities dimension) |
| **Gross Revenue** | $3.18M · $228K in refunds |

---

## 🏗️ Schema Design
<img width="975" height="758" alt="image" src="https://github.com/user-attachments/assets/ba1ad049-2f1f-4ec4-9195-fb3ba2b6866c" />

> Star schema with `orders` and `order_details` as the central fact tables surrounded by 10 dimension tables. A `cities` table was added mid-project after discovering a data lineage gap — see the Data Cleaning section below.

---

## 📂 File Structure

```text
    01_NexaMart Retail Analysis - Using SQL/
├── 00_README/
│   └── README.md
├── 01_data/                           ← 14 CSV files
└── 02_SQL/
    ├── 01_db_table_setup.sql          ← database + all table DDL
    ├── 02_data_cleaning.sql           ← schema fixes + tax lineage correction
    ├── 03_functional_queries.sql      ← reusable analytical views
    ├── 03_views.sql                   ← stored views
    ├── 04_core_analytics.sql          ← joins, aggregations, CTEs, subqueries
    └── 05_advanced_SQL.sql            ← window functions, LAG, running totals
```

---

## 🧹 Data Cleaning — What I Found and Fixed

This was one of the most valuable parts of the project — two real data quality issues discovered and resolved mid-build.

### Fix 1 · Misleading Column Name and Position

The `discount_amount` appeared after `subtotal` in the orders table, making it look like a discount still to be applied — when it was already reflected in the subtotal. Fixed by renaming it `discount_applied` and moving it before `subtotal` to accurately represent the order of operations.

```sql
ALTER TABLE orders
MODIFY COLUMN discount_amount DECIMAL(10,2) AFTER promo_id;

ALTER TABLE orders
RENAME COLUMN discount_amount TO discount_applied;
```

### Fix 2 · Broken Tax Rate Lineage

`orders.tax_rate` had no traceable path back to the `states` reference table. There was no way to verify whether the correct statutory rate had been applied — the lineage was completely broken.

**What I did:**
1. Created a `cities` table — 72 cities mapped to `state_id` FK
2. Added `city_id` to `customers` and populated it via `UPDATE ... JOIN`
3. Established the full join chain: `orders → customers → cities → states`
4. Ran a targeted `UPDATE` to overwrite only the mismatched rows
5. Verified with a `WHERE tax_rate <> states.tax_rate` check — returned 0

```sql
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
```

> This is the kind of problem that goes unnoticed in production systems for months. Finding it, documenting it, and fixing it properly is the work.

📂 `sql/02_data_cleaning.sql`

---

## 👁️ Analytical Views

Four reusable views built to simplify analysis queries and avoid repeating complex joins.

| View | Purpose |
|---|---|
| `v_sales_refund_summary` | Every order with its refund — calculates `net_order_value` |
| `v_sale_pdt` | Total sales and units sold per product |
| `v_refund_pdt` | Total refunds and units returned per product |
| `v_order_summary` | Full order breakdown — pre-discount total, discount label, tax display, final total |

> These views became the foundation for most analytical queries — especially CLV, return rates, and channel analysis.

📂 `sql/03_views.sql`

---

## 🔍 Core Analytics Queries

| # | Query | What it does |
|---|---|---|
| 1 | Revenue by Region and Channel | Multi-table JOIN and aggregation — total revenue ranked by region |
| 2 | Top 10 Products by Net Revenue | CTE + LEFT JOIN + COALESCE — gross sales minus refunds per product |
| 3 | Customer Lifetime Value by Loyalty Tier | Aggregation on view — net spend grouped by Standard, Premium, VIP |
| 4 | Promo Code Usage Frequency | CTE + date arithmetic + CASE — orders per active day per promo |
| 5 | High Frequency Low Spend Customers | WHERE vs HAVING — Standard tier customers, 3+ orders under $500 |
| 6 | Products Never Returned | NOT EXISTS correlated subquery — NULL-safe alternative to NOT IN |
| 7 | Customer B2C vs B2B Classification | SUBSTRING_INDEX + CASE + CONCAT — derives customer type from email domain |
| 8 | Average Order Value by Region and Channel | Multi-dimension GROUP BY across channel and region |

📂 `sql/04_core_analytics.sql`

---

## ⚡ Advanced SQL Queries

| # | Query | What it does |
|---|---|---|
| 1 | Return Rate by Product Category | CTE + DENSE_RANK() OVER PARTITION — ranks every product within its category by return rate for full leaderboard view |
| 2 | Top 3 CLV Customers per Loyalty Tier | DENSE_RANK() OVER PARTITION + WHERE rnk <= 3 — filters to top 3 per tier, DENSE_RANK ensures no positions are skipped on ties |
| 3 | 30-Day Moving Average Revenue | SUM() OVER with ROWS BETWEEN frame — smooths daily revenue over rolling 30 days |
| 4 | Supplier Scorecard Ranked by Region | Weighted score in CTE + RANK() OVER PARTITION — best supplier per region |
| 5 | Churn Risk by Loyalty Tier | MAX() + HAVING + SUBDATE — flags customers with no order in lookback window |
| 6 | Channel Revenue Pivot by Quarter | CASE WHEN inside SUM() — three channel columns in one pass, no UNION |
| 7 | Top 3 Products per Category | Chained CTEs + DENSE_RANK() OVER PARTITION — top revenue SKUs per category |
| 8 | Cumulative YTD Revenue by Month | SUM(SUM()) OVER PARTITION BY year — running total that resets each January |
| 9 | Channel Revenue Year-over-Year Shift | LAG() OVER PARTITION BY channel — compares each year to the prior year |

📂 `sql/05_advanced_sql.sql`

---

## 📐 SQL Concepts Demonstrated

| Concept | Where Used |
|---|---|
| Multi-table INNER JOIN | Core Q1, Q8 |
| CTE — single | Core Q4, Adv Q4, Q5 |
| CTE — chained | Core Q2, Adv Q1, Q2, Q7 |
| LEFT JOIN + COALESCE | Core Q2, Adv Q1 |
| WHERE vs HAVING | Core Q5 |
| NOT EXISTS correlated subquery | Core Q6 |
| String functions — SUBSTRING_INDEX, CONCAT | Core Q7 |
| Multi-dimension GROUP BY | Core Q8 |
| DENSE_RANK() OVER PARTITION BY | Adv Q1, Q2, Q7 |
| RANK() OVER PARTITION BY | Adv Q4 |
| LAG() window function | Adv Q9 |
| ROWS BETWEEN — moving average frame | Adv Q3 |
| Running total — SUM(SUM()) OVER | Adv Q8 |
| CASE WHEN pivot inside SUM() | Adv Q6 |
| Weighted score calculation in CTE | Adv Q4 |
| HAVING on aggregate | Core Q5, Adv Q5 |
| SUBDATE() date arithmetic | Adv Q5 |
| Reusable analytical views | Core Q3, Adv Q9 |

---

## ⚙️ How to Run

**Requirements:** MySQL 8.x · DBGate

1. Run 03_SQL/01_db_table_setup.sql    — creates the database and all 14 tables
2. Import CSVs from 01_data/ in this order:
   regions → states → cities → dates → channels → suppliers
   → products → variants → customers → promotions
   → orders → order_details → returns → return_details
3. Run 03_SQL/02_data_cleaning.sql     — fixes schema and corrects tax lineage
4. Run 03_SQL/03_views.sql             — creates the 4 analytical views
5. Explore 03_SQL/04_core_analytics.sql and 03_SQL/05_advanced_SQL.sql

> When importing `orders.csv` — ensure empty cells are treated as NULL. The `promo_id` column is intentionally NULL for non-promotional orders.

---

## 🔄 What's Next

- [ ] Power BI dashboard — Executive · Customer · Product · Promotions pages
- [ ] DAX measures library (YTD, MoM growth, CLV, Return Rate)
- [ ] RFM customer segmentation
- [ ] Row-level security by region

---

[← Back to Portfolio](../00_README/README.md)
