# RITIK Financial Analytics & FP&A Portfolio

An evolving portfolio of self-directed examples in financial analytics, FP&A, reporting, financial modelling, and accounting and finance automation.

> Project datasets are synthetic. These demonstrations are not client or employment deliverables and do not claim professional experience or verified proficiency. Each project page describes what is included and what is still planned.

## Projects

### 1. Department FP&A review and forecast

A formula-driven Excel workbook compares synthetic FY2025 departmental budgets and actuals, then builds an illustrative FY2026 forecast from editable category growth assumptions. The project also includes a deterministic data generator, SQLite-compatible variance queries, starter Power BI measures and a report build guide, forecast methodology, and VBA module source.

- [Download the Excel workbook](projects/01-fpna-department-review/workbooks/fy2025_review_fy2026_plan.xlsx)
- [Read the project notes](projects/01-fpna-department-review/README.md)
- Power BI `.pbix` report: **Coming soon**
- VBA source is provided as a starter module; it is not embedded in the workbook or tested in Excel.

### 2. Month-end bank reconciliation helper

A runnable Python command-line demo matches synthetic general-ledger and bank statement entries and writes matched rows, review exceptions, and a summary. It does not post entries or approve accounting actions.

- [Read the project notes](projects/02-month-end-reconciliation/README.md)
- Python source, sample inputs, and generated example outputs are included.

## Portfolio areas

| Area | Current evidence in this portfolio | Status |
|---|---|---|
| Excel automation and finance reporting | FP&A workbook with formulas, assumptions, source data, and a monthly trend chart; optional VBA refresh/export module source | Workbook demo and VBA starter included; macro not embedded or tested in Excel |
| Power BI | Starter DAX measures and report build guide | `.pbix` coming soon |
| SQL | SQLite-compatible monthly and category variance queries | Demo included |
| Python | Bank reconciliation command-line example | Demo included |
| Financial modelling | Illustrative FY2026 category-growth forecast based on synthetic FY2025 actuals | Demo included; simplified model |
| Accounting and finance automation | Reconciliation helper and optional VBA source module | Demos included; VBA not executed in Excel |

## Data and limitations

- All included finance and transaction data is synthetic and generated for these examples.
- The forecast is a simple same-month run-rate model, not a complete three-statement or valuation model.
- Power BI report publishing and additional portfolio examples remain planned work and are marked **Coming soon** until files are added.
