# FP&A Budget vs Actual Analysis — Advanced Excel Case Study

## Project overview
A self-directed FP&A practice case study comparing monthly departmental spending with budget, identifying expense variances, and preparing management commentary.

**Dataset:** fictional / synthetic  
**Period:** January–June 2026  
**Coverage:** 5 departments, 6 expense categories, 180 transaction-level records  
**Currency:** INR  
**Purpose:** demonstrate an Excel-based FP&A workflow for learning and interview discussion.

> This is an independent learning demonstration using synthetic data. It is not client work, employer work, or evidence of production deployment.

## Business questions
1. Which departments are over or under budget?
2. Which months show the largest expense variances?
3. Which expense categories and vendors should be investigated?
4. Are variances one-off / timing-related or potentially recurring?
5. What actions should management consider?

## Workbook structure
The companion workbook is organized into:
- `Start_Here` — scenario, instructions and learning tasks
- `Transactions` — 180 fictional transaction-level records
- `Budget` — monthly department budget summary
- `Analysis` — formula practice for budget, actual, variance, variance %, status and commentary
- `Formula_Guide` — examples using SUMIFS, IFERROR and IF
- `Interview_Prep` — practice questions and answer frameworks

## Excel skills to demonstrate
- SUMIFS for multi-criteria aggregation
- XLOOKUP for mapping / lookup tasks
- IF and IFERROR for business logic and error handling
- PivotTables to summarize actuals by department, month and category
- Conditional formatting to flag overspending
- Charts and slicers for an interactive management view
- Reconciliation of dashboard totals back to source data

## Suggested analysis workflow
1. Check blanks, duplicates, date formats, department names and unusual values.
2. Calculate actual spend and budget by month and department.
3. Calculate expense variance as **Actual − Budget**.
4. Calculate variance percentage as **Variance ÷ Budget**, with a clear zero-budget rule.
5. For expense lines, investigate positive variances as potential overspends; confirm context before calling them unfavourable.
6. Drill into category and vendor detail before writing management commentary.
7. Reconcile all summary totals to the source transactions.

## Interview explanation framework
Use a 60–90 second structure:
- **Objective:** understand departmental spending against budget.
- **Data:** six months of synthetic transaction and budget records.
- **Method:** clean data, aggregate with SUMIFS / PivotTables, calculate variance and investigate drivers.
- **Output:** a department-month analysis and management dashboard.
- **Limitations:** synthetic data; simplified budget assumptions; no ERP or live finance-system integration.

## Next improvements
- Complete the yellow input cells in the Analysis sheet with formulas.
- Add a PivotTable and department / category slicers.
- Create a one-page dashboard with Actual, Budget, Variance and Variance % KPIs.
- Add a written commentary explaining the three largest overspends after independently validating them.
- Add screenshots and a synthetic workbook copy to this repository once reviewed.

## How to describe it on a CV
After you have completed and checked the workbook, you may describe it as:

“Developed an Excel-based FP&A case study using synthetic six-month departmental data; applied SUMIFS, PivotTables and variance analysis to compare actual spend with budget and prepare management review commentary.”

Only claim the formulas, PivotTables and dashboard that you have personally completed and validated.