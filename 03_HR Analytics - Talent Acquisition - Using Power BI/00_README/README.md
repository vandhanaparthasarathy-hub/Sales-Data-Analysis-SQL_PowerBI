# 👥 HR Analytics — Talent Acquisition Intelligence Dashboard
### Microsoft Power BI Desktop | Personal Portfolio Project

---

## 📌 Project Overview

This project is a fully interactive **Talent Acquisition Analytics Dashboard** built in **Microsoft Power BI Desktop**, using a synthetically generated dataset designed to simulate the hiring operations of a growing SaaS company across six departments over a three-year period (2023–2026).

The dataset was purpose-built using a custom **Python script**, with deliberate data quality issues injected to demonstrate real-world ETL skills. The end result is a six-page dashboard covering the full recruiting lifecycle — from headcount planning and pipeline funnel analysis through to source effectiveness, diversity reporting, and offer intelligence.

---

## 🎯 Objectives

- Generate a realistic, analytics-ready HR dataset programmatically using Python
- Apply structured **data cleaning and transformation** in Power Query across three tiers
- Build a fully normalised **star schema** data model with 12 connected tables
- Write purposeful **DAX measures** for time intelligence, cumulative funnel analysis, cost attribution, and diversity metrics
- Design a professional, dark-themed multi-page dashboard following the **Obsidian Gold** design system
- Surface a compelling analytical story: a three-layer hiring gap between planning, sourcing, and conversion

---

## 🤖 Dataset Generation — GenAI-Assisted Python Script

The dataset does not come from an external source. It was **generated from scratch** using a Python script, developed through an iterative GenAI-assisted workflow and executed locally in a **Jupyter Notebook**.

### Why Python — not Excel

The initial approach considered building the dataset directly in Excel. This was quickly ruled out — Excel files are extremely token-heavy when passed to a GenAI model for refinement, making iteration slow and impractical. Instead, the decision was made to shift to a **Python script approach**: prompting the model to generate code rather than data, then running the code locally to produce output files of any desired size.

This turned out to be a significantly more efficient and scalable workflow:

- The script itself is compact and token-light — easy to refine iteratively
- Running the script locally produces thousands of rows in seconds with no model involvement
- Scaling up (more candidates, more jobs, larger pipelines) required only a few parameter changes rather than regenerating data row by row
- The output is deterministic and reproducible — `random.seed(2025)` ensures the same dataset on every run

### How the script was developed

The script was built through a series of prompts and refinements:

1. **Initial prompt** — described the desired dataset structure: a SaaS company, six departments, hiring funnel with five stages, multiple recruitment sources, and supporting planning data
2. **Schema iteration** — refined the column list, data types, and relationships between entities through back-and-forth dialogue
3. **Business logic refinement** — added realistic patterns: seasonal hiring variation, source-specific conversion rates, department-specific salary bands, posting closure errors, and recruiter tenure tracking
4. **Scale adjustment** — increased candidate pool from 1,800 to 3,200, job postings from 40 to 94, and pipeline size per role from 10–18 to 20–34 applicants to reach the desired dataset volume
5. **Dirty data injection** — added a deliberate corruption layer (~2.5% of rows) to create a meaningful data cleaning exercise

The final script required no external libraries — only Python built-ins (`csv`, `random`, `datetime`, `collections`) — making it portable and dependency-free.

### Output files

| File | Rows | Purpose |
|---|---|---|
| `HiringData_Flat.csv` | 8,645 | Single denormalised source — all dimensions and facts in one file |
| `HeadcountPlan.csv` | 78 | Quarterly hiring targets by department |
| `SourceCosts.csv` | 267 | Monthly recruitment channel spend (6 sources) |

---

## 🔄 ETL — Extract, Transform, Load

### Extract

All three CSV files were loaded into **Power Query Editor** in Power BI Desktop. `HiringData_Flat.csv` was loaded with **Enable Load disabled** — it exists in Power Query as the raw source for all Reference queries but is never loaded into the model directly. This keeps the model clean while preserving full audit access to the original data.

### Transform — Three-Tier Cleaning Structure

Cleaning was applied in three tiers to reflect where each type of error belongs in the data flow:

**Tier 1 — HiringData_Flat (source query)**

Structural errors that affect all downstream Reference queries were fixed at source:

- Set data types — 7 date columns to Date, numeric columns to Decimal or Whole Number, all others to Text
- Replaced blank strings with null in all date columns before type conversion
- Fixed Department casing using **Capitalize Each Word** — done before DeptID mapping to ensure consistent matching
- Fixed HireStage casing and replaced invalid values: `Shortlisted → Screened`, `In Review → Screened`, `rejected → null`, `HIRED → Hired`
- Generated `DeptID` as a conditional column mapped from DepartmentName — generated at source so it flows into every Reference query automatically
- Rebuilt `StageID` from cleaned HireStage values
- Removed duplicate ApplicationIDs
- Filtered future-dated ApplicationDates (post April 2026)
- Flagged posting closure errors (4 rows — JOB001 and JOB002, January–March 2023)

**Tier 2 — Applications table (Reference query)**

Business logic errors affecting metrics only:

- Nulled SalaryOffered for stages STG01, STG02, STG03 — salary only applies at Offered and Hired
- Nulled BudgetVariance for the same stages
- Nulled AvgDaysToHire for non-Hired rows
- Nulled ReferralBonus unless the row is Hired via Referral source
- Added `ValidApplication` flag — marks rows meeting all expected data quality conditions
- Added `OfferDeclined` calculated column in Data view — Yes for Offered stage rows, No for all others

**Tier 3 — Dimension queries**

Attribute-specific cleanup in each dimension:

- `Candidates` — extracted FirstName and LastName via Split Column, calculated Age from DateOfBirth, derived AgeGroup brackets, removed duplicates on CandidateID
- `Jobs` — removed Department text columns after DeptID generation, removed duplicates on JobID, added `JobLevelOrder` calculated column for correct level sorting
- `Recruiters` — replaced blank RecruiterEndDate with null, set to Date type, removed duplicates on RecruiterID
- `Departments` — loaded from a separate Excel reference file; DeptID generated using Index column and Text.PadStart for zero-padded IDs

**Referral cost appended to SourceCosts**

A separate Power Query named `ReferralSpend` calculated monthly referral bonus spend directly from the Applications table — filtered to Hired Referral rows and grouped by StartDate month. This was **appended** into SourceCosts so that Referral appears naturally in all cost visuals alongside the other six channels, eliminating the need for workaround measures.

### Load

| Stage | Row count |
|---|---|
| Raw flat file | 8,645 |
| After cleaning | 8,436 |
| Removed | 209 (duplicates, future dates, closure error stragglers) |

All 12 normalised tables were loaded into the model. `HiringData_Flat` was kept in Power Query with load disabled as an audit reference.

---

## 🏗️ Data Model — Star Schema

> *(Insert schema screenshot here — `03_Screenshots/00_schema.png`)*

The model follows a **star schema** with the `Applications` table as the central fact table, surrounded by 7 dimension tables. Two supporting tables (HeadcountPlan and SourceCosts) connect to dimension tables rather than the fact table directly.

### Tables

| Table | Type | Rows | Columns | Primary Key |
|---|---|---|---|---|
| Applications | Fact | 8,418 | 21 | ApplicationID |
| Candidates | Dimension | 2,996 | 9 | CandidateID |
| Jobs | Dimension | 94 | 12 | JobID |
| Departments | Dimension | 6 | 5 | DepartmentID |
| Stages | Dimension | 5 | 6 | StageID |
| Sources | Dimension | 7 | 3 | SourceID |
| Recruiters | Dimension | 12 | 8 | RecruiterID |
| Hiring Managers | Dimension | 12 | 5 | HiringManagerID |
| Position Slots | Dimension | 293 | 3 | PositionSlotID |
| Dates | Date table | 1,186 | 8 | Date |
| HeadcountPlan | Supporting | 78 | 7 | HeadCountPlanID |
| SourceCosts | Supporting | 300 | 9 | SourceCostID |

### Key relationship decisions

- `Dates[Date]` → `Applications[ApplicationDate]` is the **active** relationship. Four additional inactive relationships exist for ScreenDate, InterviewDate, OfferDate, and StartDate — activated in DAX measures using `USERELATIONSHIP()` when needed.
- `Jobs[HiringManagerID]` → `Hiring Managers[HiringManagerID]` — Hiring Manager context flows to Applications through the Jobs chain, avoiding ambiguous dual-path relationships. HiringManagerID was deliberately removed from the Applications table to eliminate filter path ambiguity.
- `SourceCosts` connects to `Sources` via SourceID and to `Dates` via an inactive relationship on MonthDate — activated in the Total Sourcing Cost measure using `USERELATIONSHIP()`.
- `HeadcountPlan` connects to `Departments` via DepartmentID and to `Dates` via QuarterStartDate.
- `Dates` is marked as a Date Table (Table Tools → Mark as Date Table) — required for all time intelligence DAX functions to work correctly.

---

## 📐 DAX — Highlighted Measures

All measures are stored in a dedicated `MeasureTable`. The model contains 76 measures in total covering funnel analysis, time intelligence, cost attribution, diversity metrics, scenario modelling, and conditional colour formatting.

---

### 1 — Dynamic page title (Dynamic Title)

Each page has a dynamic title card that updates automatically when slicers change. The base measure appends the selected department name to create a contextual heading.

```dax
Dynamic Title =
"Talent Acquisition · " &
COALESCE(
    SELECTEDVALUE(Departments[DepartmentName]),
    "All Departments"
)
```

A variant without the page prefix is used across Pages 2–6, keeping the measure reusable across the entire report without duplication.

---

### 2 — Cumulative funnel stages (All Screened)

The funnel chart requires cumulative counts — not point-in-time counts. A candidate who was hired passed through every prior stage. Without cumulative measures, the funnel bars would not narrow correctly and conversion rates would be understated.

```dax
All Screened =
CALCULATE(
    COUNTROWS(Applications),
    Applications[StageID] IN {"STG02","STG03","STG04","STG05"}
)
```

This pattern repeats for All Interviewed, All Offered, and All Hired. Conversion rates are then the ratio between consecutive measures — for example `Screen Rate % = DIVIDE([All Screened], [All Applied])`.

---

### 3 — Total Sourcing Cost using USERELATIONSHIP

SourceCosts connects to the Dates table via an inactive relationship on `MonthDate`. Using the active relationship (ApplicationDate) would cause incorrect filtering. `USERELATIONSHIP()` temporarily activates the correct relationship inside the measure context only — without affecting any other visual on the page.

```dax
Total Sourcing Cost =
CALCULATE(
    SUM(SourceCosts[MonthlyCost]),
    USERELATIONSHIP(Dates[Date], SourceCosts[MonthDate])
)
```

---

### 4 — Year-over-year hiring change (Hires YoY %)

Uses `SAMEPERIODLASTYEAR()` — a time intelligence function that shifts the filter context back exactly one year. The result updates dynamically as the Year slicer changes, comparing like-for-like periods automatically.

```dax
Hires YoY % =
VAR CurrentHires = [Total Hires]
VAR PriorHires =
    CALCULATE(
        [Total Hires],
        SAMEPERIODLASTYEAR(Dates[Date])
    )
RETURN
    DIVIDE(CurrentHires - PriorHires, PriorHires)
```

`VAR` stores each result once — improving readability and preventing `[Total Hires]` from being evaluated twice. `DIVIDE()` handles division by zero gracefully throughout all ratio measures.

---

### 5 — Conditional colour for KPI formatting (Offer Acceptance Colour)

Returns a hex colour string based on a three-tier threshold. Applied via the `fx` conditional formatting option on card values and table columns — making colour logic explicit, reusable, and independent of visual settings.

```dax
Offer Acceptance Colour =
VAR Rate = [Offer Acceptance Rate]
RETURN
    IF(Rate >= 0.75, "#36D399",
    IF(Rate >= 0.60, "#F5C842",
    "#F87171"))
```

Ten colour measures follow this pattern across the model — covering departments, sources, stages, gender, ethnicity, recruiter status, plan status, budget variance, and gauge fill.

---

### 6 — COALESCE for null-safe KPI cards

Any count measure risks showing blank when no matching rows exist in the current filter context. `COALESCE()` replaces blank with zero, ensuring cards always display a value rather than appearing broken.

```dax
Data Quality Issues =
COALESCE(
    CALCULATE(
        COUNTROWS(Applications),
        Applications[PostingClosureError] = "Yes"
    ),
    0
)
```

---

## 📊 Dashboard Pages

---

### Page 1 — Overview

The executive summary. Answers: *how is hiring performing overall?*

**Visuals:**
- Dynamic title card — updates with Year and Department slicer selections
- 5 KPI cards — Total Applications, Offer Acceptance Rate, Avg Days to Hire, Hiring vs Plan %
- Gauge 1 — **Hired vs Posted Positions** (Total Hires needle vs Total Positions marker)
- Gauge 2 — **Positions Posted vs Target Hire** (Total Positions needle vs Target Hires marker)
- Line + Clustered Column chart — Monthly Hires (gold bars) vs Applications (violet line)
- Waterfall chart — Hiring vs Plan by Department, green = over plan, red = behind
- What-if slider — Conversion Boost % → Projected Hires card
- What-if slider — Target Headcount → Headcount Gap card
- Pipeline Errors — Jobs that were not closed after filling, Applications that were not re-assigned after a recruiter left the company

**Key numbers:** 236 hires made · 291 positions posted · 316 target hires planned

**Story:** The dashboard surfaces a three-layer hiring gap — 316 hires were planned, 291 positions were posted, and only 236 hires were made. Each layer represents a distinct process failure: planning execution, sourcing reach, and funnel conversion.

---

### Page 2 — Funnel Analysis

Tracks candidate progression through all five hiring stages.

**Visuals:**
- 4 KPI cards — Total Applications, Total Screened, Total Intervied and Total Hired
- Funnel chart — visualises the narrowing pipeline using cumulative stage measures
- Stacked Column Chart — stage distribution by source
- Matrix with heatmap — Stage × Department conversion rates, colour scaled red → gold → green
- Stage summary table — stage name, cumulative count, stage transition, conversion rate
- Callout cards — Biggest Drop-off stage (e.g. "Interview → Offered") and Least Drop-off stage

**Story:** Interview to Offer is consistently the weakest conversion point. Engineering shows the lowest funnel efficiency across all departments.

---

### Page 3 — Time to Hire

Measures recruiting speed at department and job level.

**Visuals:**
- 4 KPI cards — Avg Days to Hire, Avg Days to Offer, Time to Fill, Fastest Department to fill a role
- Horizontal bar chart — Avg Days to Hire by Department, colour-coded: green <45d, amber 45-55d, red >55d
- Grouped bar chart — Time to Hire vs Time to Fill side by side per department
- Rolling 90 Day Hires trend line
- Grouped column chart — Time to Hire vs Time to Fill side by side across job levels

**Story:** Engineering takes the longest to hire. The gap between Time to Hire and Time to Fill reveals how long roles were posted before the first application arrived — a sourcing lag, not a recruiter speed problem.

---

### Page 4 — Source Impact

Evaluates the effectiveness and cost of each recruitment channel.

**Visuals:**
- 4 KPI cards — Total Sourcing Cost, Cost Per Hire, Top Source, Best Quality Source
- Monthly Sourcing Cost line chart — spend per channel over time including Referral bonus costs
- Scatter quadrant — Source Quality Index (Y) vs Cost Per Hire (X), sized by Total Applications, coloured by Source Type. Median reference lines create four labelled quadrants: Sweet Spot has a High Quality with Low Cost, Premium has a High Quality with High Cost, Low Value has a Low Quality with Low Cost and  Costly & Weak a Low Quality with High Cost
- Horizontal bar chart — Total Hires by Source, sorted and coloured by source
- Source detail table — all 7 sources with Applications, Hires, Cost Per Hire, Quality Index and their Ranks, based on the total hires

**Story:** Referral sits in the Sweet Spot — highest quality, yet, lowest effective cost. Agency sits in Costly & Weak which has a high spend, mediocre output.

---

### Page 5 — Diversity Pipeline

Tracks representation across gender, ethnicity, and age through every hiring stage.

**Visuals:**
- 5 KPI cards — Ethnic Diversity, Top Minority Group, Female Hire Rate, Male Hire Rate, Average age when Hired
- Horizontal bar chart — Hires by Ethnicity with ethnicity-matched colour formatting
- 100% Stacked Bar (ethnicity) — ethnicity split at each funnel stage
- 100% Stacked Bar (gender) — gender split at each funnel stage
- Pie Chart — Hires by AgeGroup showing age distribution of hired candidates
- Gauge — Female Hire Rate vs 40% benchmark

> *Diversity data is self-reported and shown in aggregate only. No individual candidate is identifiable. Data covers 2023–2026.*

---

### Page 6 — Offer Intelligence *(Drillthrough)*

Accessed by right-clicking any department bar on the Overview waterfall → Drillthrough → Offer Intelligence. Filtered to the selected department automatically.

**Visuals:**
- 5 KPI cards — Selected Department, Total Offers, Offer Acceptance Rate, Over Budget Offers, Avg Salary Offered
- Decomposition Tree — Total Offers broken down interactively by Source Name → Job Level → Recruited  
- Budget scatter plot — Avg Salary Offered (Y) vs Avg Budget Per Position (X), coloured by Job Level. Ratio line marks the on-budget diagonal — points above are over budget
- Recruiter performance table — Top 5 recruiters by hire volume showing: Name, Applications, Hires, Avg Days to Hire, Acceptance %, Recruiter Status (colour-coded)
- Back button — returns to Funnel Analysis page

**Story:** Junior roles are offered salaries significantly below their approved budget, while the trend is reversed as seniority increases.

---

## 💬 Custom Tooltips

Two custom tooltip pages built for Source and Department.

### Tooltip — Source (Page 4)

Appears on hover over source bars and scatter bubbles. Canvas: 320 × 240px.

**Shows:** Source name · Source type badge · Total Applicants · Total Hires · Source Quality Index · Cost Per Hire · Funnel breakdown bar chart by stage · Avg Monthly Spend

### Tooltip — Department (Pages 1 and 3)

Appears on hover over department bars on the Overview waterfall and Time to Hire chart. Canvas: 260 × 330px.

**Shows:** Department name · Total Hires · Hiring vs Plan % · Avg Days to Hire · Offer Acceptance Rate · Hires by Job Level mini bar chart

---

## 🏗️ Schema Design

<img width="1027" height="751" alt="image" src="https://github.com/user-attachments/assets/85f59575-aabe-4917-9555-6a44e766390b" />

> Hybrid relational data structure - Snowflake schema with `Applications` as the central fact tables surrounded by 11 dimension tables after Normalization.

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Microsoft Power BI Desktop | Report building and visualisation |
| Power Query Editor | Data ingestion, cleaning, and normalisation |
| DAX | 77 measures — funnel, time intelligence, cost, diversity, colour |
| Python 3 (Jupyter Notebook) | Synthetic dataset generation |
| GenAI (text-based) | Dataset design, script iteration, documentation support |
| GitHub | Version control and portfolio hosting |

---

## 🔄 BI Workflow

```
Prompt-driven Python script development (GenAI-assisted, Jupyter Notebook)
↓
01_HiringData_Flat.csv · 02_HeadcountPlan.csv · 03_SourceCosts.csv
↓
Power Query Editor
  Tier 1 — Source cleaning    (01_HiringData_Flat — load disabled)
  Tier 2 — Business logic     (Applications Reference query)
  Tier 3 — Dimension cleaning (each Dim Reference query)
  ReferralSpend appended to SourceCosts
↓
Star schema data model (12 tables)
  Active + inactive date relationships · USERELATIONSHIP in DAX
↓
77 DAX measures (MeasureTable)
  Cumulative funnel · Time intelligence · Cost · Diversity · Colour
↓
6-page dashboard + 2 custom tooltip pages
  Overview · Funnel Analysis · Time to Hire · Source Impact
  Diversity Pipeline · Offer Intelligence (drillthrough)
↓
Performance Analyser — all visuals verified under 2,000ms
↓
GitHub portfolio
```

---

## 📁 Project Structure

```
03_HRAnalytics Data Visualization - Using Power BI/
│
├── 00_README/
│   └── README.md                              # This file
│
├── 01_PowerBI/
│   └── HR_Analytics.pbix                      # Main Power BI report
│
├── 02_Data/
│   ├── 01_HiringData_Flat.csv                    # Raw flat file (8,645 rows)
│   ├── 02_HeadcountPlan.csv                      # Quarterly hiring targets (78 rows)
│   ├── 03_SourceCosts.csv                        # Monthly channel spend (267 rows)
│   └── hiring_data_generator.py                  # Python script
│
├── 03_Screenshots/
│   ├── 01_overview.png                        # Page 1 — Overview
│   ├── 02_funnel_analysis.png                 # Page 2 — Funnel Analysis
│   ├── 03_time_to_hire.png                    # Page 3 — Time to Hire
│   ├── 04_source_impact.png                   # Page 4 — Source Impact
│   ├── 05_diversity_pipeline.png              # Page 5 — Diversity Pipeline
│   └── 06_offer_intelligence.png              # Page 6 — Offer Intelligence
│
└── 04_PDF/
    └── HR_Analytics_Dashboard.pdf             # Exported PDF of all pages
```

---

## 🗂️ Data Sources

| # | File | Type | Rows | Description |
|---|---|---|---|---|
| 01 | `HiringData_Flat.csv` | Generated | 8,645 | Single denormalised source — all dimensions and facts |
| 02 | `HeadcountPlan.csv` | Generated | 78 | Quarterly hiring targets set at 112% of actual positions |
| 03 | `SourceCosts.csv` | Generated | 267 | Monthly spend for 6 channels with YoY growth and seasonal spikes |
| 04 | `Departments.xlsx` | Reference | 6 | Department metadata — head, email, short name |

---

## 📸 Dashboard Preview

| Overview | Funnel Analysis |
|---|---|
| ![Overview](03_Screenshots/01_overview.png) | ![Funnel](03_Screenshots/02_funnel_analysis.png) |

| Time to Hire | Source Impact |
|---|---|
| ![Time to Hire](03_Screenshots/03_time_to_hire.png) | ![Source Impact](03_Screenshots/04_source_impact.png) |

| Diversity Pipeline | Offer Intelligence |
|---|---|
| ![Diversity](03_Screenshots/05_diversity_pipeline.png) | ![Offer Intel](03_Screenshots/06_offer_intelligence.png) |

---

## 💡 Key DAX Concepts Used

- `CALCULATE()` — filter context modification
- `SAMEPERIODLASTYEAR()` — year-over-year time intelligence
- `DATESINPERIOD()` — rolling 90-day hire window
- `USERELATIONSHIP()` — activating inactive date relationships
- `DIVIDE()` — safe division across all ratio measures
- `SWITCH()` — conditional colour and dynamic stage logic
- `TOPN()` + `CONCATENATEX()` — dynamic top source and top ethnicity text measures
- `COALESCE()` — null-safe count measures for KPI cards
- `REMOVEFILTERS()` — ethnicity hire rate ignoring ethnicity context
- `MEDIANX()` — scatter plot reference line values
- `SELECTEDVALUE()` — tooltip header cards driven by hover context
- `VAR / RETURN` — readable, performant multi-step measures
- Field parameters — MetricSelector for dynamic measure switching

---

## 🚀 How to Open

1. Download and install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. Clone or download this repository
3. Open `HR_Analytics.pbix` in Power BI Desktop
4. If prompted about data source paths — update file paths to your local `02_Data/` folder
5. Click Refresh to reload data through Power Query
6. Explore all six pages using the left sidebar navigation

---

## 👤 Author

**Vandhana Parthasarathy**
Data Analyst | Power BI Developer
🔗 [LinkedIn](https://www.linkedin.com/in/vandhana-parthasarathy-be-mba-895852100/) · 📧 [Email](vandhanaparthasarathy@gmail.com) · 📝 [Resume](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/blob/main/00_README/VandhanaParthasarathy-Resume.pdf)

---

*This project was independently developed as a portfolio piece to demonstrate end-to-end business intelligence skills — dataset generation, ETL, data modelling, DAX development, and dashboard design in Power BI.*

---

[← Back to Portfolio](https://github.com/vandhanaparthasarathy-hub/Sales-Data-Analysis-SQL_PowerBI/tree/main/00_README#readme)
