# Power BI report build guide

This folder provides a synthetic CSV source, starter DAX measures, and a report plan. A Power BI `.pbix` report has not been created yet and remains **Coming soon**.

## Model setup

1. Import `../data/monthly_finance.csv` as `monthly_finance`.
2. Set `period` to Date, department/category/account_type to Text, and budget/actual to Whole Number.
3. Create a calendar table covering the source periods and relate its date field to `monthly_finance[period]`.
4. Add the measures in `measures.dax`. Format INR measures as whole rupees and variance/margin measures as percentages.

## Suggested report page

- KPI cards: Revenue Actual, Expense Actual, Contribution Actual, and Contribution Favorable Variance.
- Line chart: monthly Contribution Actual and Contribution Budget.
- Matrix: department by Revenue, Expense, Contribution, and favorable variance.
- Bar chart: favorable variance by category, with revenue and expense directions interpreted separately.
- Slicers: period, department, and category.

All values are synthetic and should not be presented as company performance.
