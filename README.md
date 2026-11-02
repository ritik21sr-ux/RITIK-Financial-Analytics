# RITIK Financial Analytics & FP&A Portfolio

An evolving portfolio of self-directed examples in financial analytics, FP&A, reporting, financial modelling, and accounting and finance automation.

> All project data is synthetic. These demonstrations are not client or employment deliverables and do not claim professional experience or verified proficiency. Each project page explains what is included, the assumptions used, and what remains planned.

## Featured projects

### 1. Department FP&A review and forecast

A formula-driven Excel workbook compares synthetic FY2025 departmental budgets and actuals, then builds an illustrative FY2026 forecast from editable category growth assumptions. SQL variance queries, Power BI starter measures, a report build guide, forecast methodology, and VBA module source accompany it.

- [Download the Excel workbook](projects/01-fpna-department-review/workbooks/fy2025_review_fy2026_plan.xlsx)
- [Project notes](projects/01-fpna-department-review/README.md)
- Power BI `.pbix`: **Coming soon**. VBA source is not embedded in the workbook or tested in Excel.

### 2. Month-end bank reconciliation helper

A Python command-line demo matches synthetic ledger and bank entries, then exports matched rows, exceptions, and a summary for review.

- [Project notes and sample outputs](projects/02-month-end-reconciliation/README.md)
- The script does not post entries or approve accounting actions.

### 3. 13-week cash flow forecast

An Excel cash bridge combines collection assumptions, supplier payment schedules, payroll, operating costs, and capex. Change the scenario to compare Base, Downside, and Upside assumptions; a Python version exports the weekly forecast and cash-floor watchlist.

![Cash forecast dashboard preview](projects/03-thirteen-week-cash-forecast/images/cash_forecast_dashboard.png)

- [Download the Excel workbook](projects/03-thirteen-week-cash-forecast/workbooks/13_week_cash_forecast.xlsx)
- [Project notes, methodology, and scenarios](projects/03-thirteen-week-cash-forecast/README.md)
- Synthetic example: Base closes at ₹1,456,600 with no weeks below the ₹500,000 floor; Downside closes at ₹31,320 and falls below the floor for two weeks.

### 4. SaaS revenue and retention analytics

A deterministic Python data generator creates 1,446 synthetic customer-month movement rows across 24 months for MRR, expansion, contraction, churn, NRR, and cohort retention analysis. The project includes SQL queries, Power BI DAX measures, and generated monthly and cohort summaries.

- [Project notes and outputs](projects/04-saas-revenue-retention/README.md)
- Power BI `.pbix`: **Coming soon**; DAX and the report guide are starter materials.

### 5. Accounts payable controls review

A Python review identifies duplicate and near-duplicate candidates, missing purchase orders above a sample threshold, pending approvals, pending bank-detail changes, and overdue unpaid invoices. SQL queries and Power BI starter measures are included.

- [Project notes and exception outputs](projects/05-ap-controls-review/README.md)
- Power BI `.pbix`: **Coming soon**. Flags are prompts for human review, not fraud or policy findings.

## Portfolio coverage

| Area | Demonstration included | Status and limits |
|---|---|---|
| Excel and finance reporting | Department budget vs actual workbook and 13-week cash forecast workbook | Synthetic, formula-driven examples |
| Excel automation | Optional VBA refresh/export module source | Starter source only; not embedded or executed in Excel |
| Power BI | DAX and build guides for FP&A, SaaS, and AP views | Native `.pbix` reports are **Coming soon** |
| SQL | Budget variance, recurring-revenue, cohort, and AP exception queries | SQLite-compatible examples |
| Python | Reconciliation, cash forecasting, SaaS movement analysis, and AP review | Reproducible synthetic-data demos |
| Financial modelling | Category-growth forecast and weekly liquidity scenarios | Illustrative models, not management guidance |
| Accounting and finance automation | Reconciliation and AP exception review | No posting, payment blocking, or ERP integration |

## Reproducibility and data

Each project contains its own source data, scripts, and run notes. All data is synthetic, generated for portfolio demonstration, and must not be interpreted as company results. The cash forecast is not a treasury system; SaaS ARR is a simple run-rate calculation; AP flags require a human reviewer.
