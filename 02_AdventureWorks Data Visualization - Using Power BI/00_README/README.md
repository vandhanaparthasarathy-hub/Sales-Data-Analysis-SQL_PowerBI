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
- Featured product: **Fender Set – Mountain.** ***NOTE:*** *Choose to change the Products from Top 10 Products Table of Page 1 - Exec Dashboard*

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

```
02_AdventureWorks Data Visualization - Using Power BI/
│
├── 00_README/
│   └── README.md                                         # Project documentation
│
├── 01_POWER BI - pbix File/
│   └── Adventure-Works-PowerBI.pbix                      # Main Power BI report
│
├── 02_data/                                              # Raw source data (CSV)
│   ├── 01_Calendar Lookup.csv                            # Dimension
│   ├── 02_Customer Lookup.csv                            # Dimension
│   ├── 03_Product Categories Lookup.csv                  # Dimension
│   ├── 04_Product Subcategories Lookup.csv               # Dimension
│   ├── 05_Product Lookup.csv                             # Dimension
│   ├── 06_Territory Lookup.csv                           # Dimension
│   ├── 07_Sales Data 2020.csv                            # Fact
│   ├── 08_Sales Data 2021.csv                            # Fact
│   ├── 09_Sales Data 2022.csv                            # Fact
│   └── 10_Returns Data.csv                               # Fact
│
├── 03_Screenshots/                                       # Dashboard preview images
│   ├── 01_Exec_Dashboard.png
│   ├── 02_Map.png
│   ├── 03_Product_Detail.png
│   └── 04_Customer_Detail.png
│
└── 04_PDF/                                               # Exported PDF reports
```
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

| Executive Summary | Map View |
|---|---|
| ![Executive Summary](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/blob/main/02_AdventureWorks%20Data%20Visualization%20-%20Using%20Power%20BI/03_Screenshots/01_Exec_Dashboard.png) | ![Map View](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/blob/main/02_AdventureWorks%20Data%20Visualization%20-%20Using%20Power%20BI/03_Screenshots/02_Map.png) |

| Product Detail | Customer Detail |
|---|---|
| ![Product Detail](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/blob/main/02_AdventureWorks%20Data%20Visualization%20-%20Using%20Power%20BI/03_Screenshots/03_Product_Detail.png) | ![Customer Detail](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/blob/main/02_AdventureWorks%20Data%20Visualization%20-%20Using%20Power%20BI/03_Screenshots/04_Customer_Detail.png) |

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

---


[← Back to Portfolio](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/tree/main/00_README#readme)

