# Department FP&A Review and FY2026 Forecast

## Summary

This portfolio demo reviews a synthetic FY2025 departmental budget against actuals and builds an illustrative FY2026 forecast. The workbook keeps source data, assumptions, calculations, and outputs in separate, traceable sections.

All amounts are in Indian rupees (INR). Every row is generated for this demo; no company or client data is used.

## Included files

- `workbooks/fy2025_review_fy2026_plan.xlsx` — formula-driven Overview, monthly review, growth assumptions, forecast build, and source data.
- `data/monthly_finance.csv` — 180 synthetic department, category, and month records for FY2025.
- `scripts/generate_synthetic_data.py` — deterministic source-data generator.
- `sql/variance_analysis.sql` — SQLite-compatible monthly and category variance queries.
- `powerbi/measures.dax` — starter measures for a Power BI model.
- `powerbi/report_build_guide.md` — model setup and a suggested report layout. The `.pbix` report is not included yet.
- `automation/RefreshAndExportOverview.bas` — optional VBA module source. It is not embedded in the `.xlsx` file and has not been run in Excel.
- `model/forecast_methodology.md` — forecast basis, formula flow, and limitations.

## Workbook flow

1. **Overview** shows FY2025 department performance and the monthly contribution trend.
2. **Assumptions** holds editable annual category growth rates for the FY2026 plan.
3. **Monthly review** calculates revenue, expenses, contribution, and favorable variance by department and month.
4. **FY26 forecast** applies each category's growth assumption to the same month and department in FY2025 actuals.
5. **Source data** contains the original synthetic budget and actual rows.

Positive contribution variance is favorable. Revenue variance is actual minus budget. Expense variance is budget minus actual. Contribution is revenue less expenses.

## Rebuild the sample data

From this project folder, run:

```text
python scripts/generate_synthetic_data.py
```

The script writes `data/monthly_finance.csv` with a stable, deterministic sample.

## SQL

The queries use SQLite syntax. Create a table with the columns shown in the SQL file, then import `data/monthly_finance.csv` as CSV with a header row into `monthly_finance`. Run the monthly rollup and category detail queries in `sql/variance_analysis.sql`.

## VBA helper

The `.bas` file contains source code only. To try it in desktop Excel, open the workbook, use **Alt+F11 → File → Import File**, select the module, then run `RefreshAndExportOverview`. The macro refreshes workbook connections, recalculates, and asks where to save a PDF of the Overview sheet. No macro-enabled workbook is included.

## Scope and limitations

- FY2025 figures are synthetic and should not be interpreted as company performance.
- FY2026 forecast is a simple same-month run-rate model: FY2025 actual multiplied by one editable category growth rate.
- The forecast is not a complete three-statement model and does not include hiring, working capital, taxes, debt, cash flow, or seasonality changes.
- The Power BI deliverable is limited to DAX measures and a build guide. A `.pbix` file is still coming soon.
- The VBA module is supplied as a starting point and has not been executed in Excel.
