# 🚴 AdventureWorks Business Intelligence Dashboard
### Microsoft Power BI Desktop | Udemy Course Project

---

## 📌 Project Overview

This project is a fully interactive **Business Intelligence Dashboard** built in **Microsoft Power BI Desktop**, using the AdventureWorks dataset — a fictional cycling company that sells bikes, accessories, clothing, and components globally.

The dashboard was developed as part of the **"Microsoft Power BI Desktop for Business Intelligence"** course on Udemy, covering the end-to-end BI workflow: from raw data ingestion to polished, interactive reporting.

---

## 🎯 Objectives

- Connect to and transform raw business data using **Power Query Editor**
- Build a clean, relational **data model** with multiple linked tables
- Write **DAX (Data Analysis Expressions)** measures and calculated columns for advanced analytics
- Design professional, interactive **reports and dashboards** for executive-level insights
- Analyze key business metrics: revenue, profit, orders, returns, and customer behaviour

---

## 📊 Dashboard Pages

### Page 1 — Exec Dashboard
A high-level overview of company performance:

| KPI | Value |
|-----|-------|
| Revenue | $24.9M |
| Profit | $10.5M |
| Orders | 25.2K |
| Return Rate | 2.2% |

**Visuals include:**
- Revenue trend line chart (Jan 2020 – Jan 2022)
- Total Orders by Category (Accessories, Bikes, Clothing)
- Top 10 Products based on Total number of Orders
- Monthly Revenue, Orders, and, Returns with MoM comparison
- Most Ordered & Most Returned Product Type highlights

---

### Page 2 — Geographic Map View
- Interactive world map filtered by region: **Europe**, **North America**, **Pacific**
- "Select All" toggle for global view

---

### Page 3 — Product Detail
Drill through view for individual product performance ***(Referneced from Products in Top 10 Products Table of Page 1 - Exec Dashboard)***:

- Monthly Orders, Revenue & Profit vs. Target (gauge charts)
- Profit vs. Adjusted Profit trend (with dynamic **Price Adjustment %** slider)
- Return % trend over time
- Metric selector: switch between Orders, Revenue, Profit, Returns, Return %
- Featured product: **Fender Set – Mountain** ***NOTE:*** *Choose to change the Products from Top 10 Products Table of Page 1 - Exec Dashboard*

---

### Page 4 — Customer Detail
Customer segmentation and behaviour analysis:

- **17.4K Unique Customers** | **$1,431 Revenue per Customer**
- Total/Revenue trend over time (2020–2022)
- Top 100 Customers ranked by Orders & Revenue
- Total Orders by **Occupation** (Skilled Manual, Professional, Management)
- Total Orders by **Income Level** (Low, Average, High)
- Year range slicer with highlighted top customer insights
- **Top customer:** Mr. Maurice Shan — 6 orders, $12.4K revenue

---
## 🏗️ Schema Design

<img width="1412" height="782" alt="image" src="https://github.com/user-attachments/assets/451d4c83-701b-471a-9b24-7e5ff92e2753" />

> Hybrid relational data structure - Star schema with `Sales Data` and `Returns Data` as the central fact tables surrounded by 4 main dimension tables, and a Snowflake schema with `Product Lookup` extended to `Product Subcategories Lookup` and `Product Categories Lookup` for Normalization. Measure Tables are also shown but are not connected to the main tables. 

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Microsoft Power BI Desktop | Report building & visualisation |
| Power Query Editor | Data ingestion, cleaning & transformation |
| DAX | Calculated columns, measures, KPIs |
| AdventureWorks Dataset | Source data (10 CSV files) |

---

## 🔄 BI Workflow
Raw Data Sources
↓
Power Query Editor (Connect → Clean → Transform)

↓

Data Model (Relationships between tables)

↓

DAX Measures & Calculated Columns

↓

Interactive Reports & Dashboards

**Key steps covered:**

1. **Data Connection** — Loaded 10 CSV files into Power BI (6 dimension tables, 4 fact tables)
2. **Data Cleaning** — Removed duplicates, errors, irrelevant columns; corrected data types
3. **Data Transformation** — Reshaped tables, renamed fields, filtered rows in Power Query
4. **Data Modelling** — Defined relationships across fact and dimension tables (star schema)
5. **DAX Development** — Created measures for revenue, profit, return rate, MoM comparisons, rolling totals, and target tracking
6. **Report Design** — Built multi-page dashboards with slicers, drill-throughs, KPI cards, and custom visuals

---

## 📁 Project Structure

AdventureWorks-PowerBI/

│

├── AdventureWorks_Report.pbix                            # Main Power BI file

├── /data                                                 # Raw source data (CSV)

│   │

│   ├──── Dimension Tables (Lookups) ──

│   ├── 01_AdventureWorks_Calendar_Lookup.csv

│   ├── 02_AdventureWorks_Customer_Lookup.csv

│   ├── 03_AdventureWorks_Product_Categories_Lookup.csv

│   ├── 04_AdventureWorks_Product_Subcategories_Lookup.csv

│   ├── 05_AdventureWorks_Product_Lookup.csv

│   ├── 06_AdventureWorks_Territory_Lookup.csv

│   │

│   ├──── Fact Tables ──

│   ├── 07_AdventureWorks_Sales_Data_2020.csv

│   ├── 08_AdventureWorks_Sales_Data_2021.csv

│   ├── 09_AdventureWorks_Sales_Data_2022.csv

│   └── 10_AdventureWorks_Returns_Data.csv

│

├── /screenshots                                          # Dashboard preview images

│   ├── executive_summary.png

│   ├── product_detail.png

│   ├── customer_detail.png

│   └── map_view.png

└── README.md
### 🗂️ Data Sources

| # | File | Type | Description |
|---|------|------|-------------|
| 01 | `AdventureWorks_Calendar_Lookup.csv` | Dimension | Date table used for time intelligence |
| 02 | `AdventureWorks_Customer_Lookup.csv` | Dimension | Customer demographics & details |
| 03 | `AdventureWorks_Product_Categories_Lookup.csv` | Dimension | Top-level product categories |
| 04 | `AdventureWorks_Product_Subcategories_Lookup.csv` | Dimension | Product subcategory groupings |
| 05 | `AdventureWorks_Product_Lookup.csv` | Dimension | Full product list with pricing & cost |
| 06 | `AdventureWorks_Territory_Lookup.csv` | Dimension | Sales regions (Europe, N. America, Pacific) |
| 07 | `AdventureWorks_Sales_Data_2020.csv` | Fact | Transactional sales records for 2020 |
| 08 | `AdventureWorks_Sales_Data_2021.csv` | Fact | Transactional sales records for 2021 |
| 09 | `AdventureWorks_Sales_Data_2022.csv` | Fact | Transactional sales records for 2022 |
| 10 | `AdventureWorks_Returns_Data.csv` | Fact | Product return records across all years |

---

## 📸 Dashboard Preview

| Executive Summary | Product Detail |
|---|---|
| ![Executive Summary](screenshots/executive_summary.png) | ![Product Detail](screenshots/product_detail.png) |

| Customer Detail | Map View |
|---|---|
| ![Customer Detail](screenshots/customer_detail.png) | ![Map View](screenshots/map_view.png) |

---

## 💡 Key DAX Concepts Used

- `CALCULATE()` — context modification for filtered measures
- `DATEADD()` / `SAMEPERIODLASTYEAR()` — time intelligence functions
- `DIVIDE()` — safe division to avoid blank/error returns
- `IF()` / `SWITCH()` — conditional logic in measures
- `RELATED()` — cross-table lookups in calculated columns
- Rolling totals & MoM % change measures

---

## 🎓 Course Information

**Course:** Microsoft Power BI Desktop for Business Intelligence  
**Platform:** Udemy  
**Instructor:** Maven Analytics (Chris Dutton, Aaron Parry)  
**Topics Covered:** Power Query, Data Modelling, DAX, Report Design, Dashboard UX

---

## 🚀 How to Open

1. Download and install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. Clone or download this repository
3. Open `AdventureWorks_Report.pbix` in Power BI Desktop
4. Explore the four report pages using the navigation panel

---

## 👤 Author

**Vandhana Parthasarathy**  
Data Analyst | Power BI Developer  
🔗 [LinkedIn](https://www.linkedin.com/in/vandhana-parthasarathy-be-mba-895852100/)   📧 [Email](vandhanaparthasarathy@gmail.com)

---

*This project was completed as part of a structured Udemy course and is included in my data analytics portfolio to demonstrate proficiency in Power BI, DAX, and business intelligence reporting.*
