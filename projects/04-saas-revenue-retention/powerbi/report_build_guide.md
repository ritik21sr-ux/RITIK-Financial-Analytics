# Power BI report build guide

## Model setup

1. Load `data/customer_month_movements.csv` as `customer_month_movements`.
2. Parse `month` and `cohort_month` as dates; set MRR fields to whole-number INR and retention measures to percentages.
3. Create a contiguous Month dimension and relate its month key one-to-many to `customer_month_movements[month]`.
4. Add measures from `measures.dax`; keep the customer-month fact table at its current grain.

## Suggested report pages

- **Executive:** ending MRR, ARR run-rate, active customers, NRR, and monthly MRR bridge.
- **Retention:** cohort logo retention matrix and NRR by month.
- **Movement:** new, expansion, contraction, and churn MRR by month, plan, and segment.

The `.pbix` file is **Coming soon**. This guide describes a suggested build and does not claim that a Power BI report has been published or validated.
