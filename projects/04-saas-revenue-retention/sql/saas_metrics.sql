-- SQLite-compatible examples for customer_month_movements.csv.
-- Set up with: .mode csv, then .import --skip 1 data/customer_month_movements.csv customer_month_movements

-- Monthly MRR bridge and retention rates.
SELECT
    month,
    SUM(opening_mrr_inr) AS opening_mrr_inr,
    SUM(new_mrr_inr) AS new_mrr_inr,
    SUM(expansion_mrr_inr) AS expansion_mrr_inr,
    SUM(contraction_mrr_inr) AS contraction_mrr_inr,
    SUM(churned_mrr_inr) AS churned_mrr_inr,
    SUM(ending_mrr_inr) AS ending_mrr_inr,
    CASE WHEN SUM(opening_mrr_inr) = 0 THEN NULL ELSE
        1.0 * (SUM(opening_mrr_inr) + SUM(expansion_mrr_inr) - SUM(contraction_mrr_inr) - SUM(churned_mrr_inr)) / SUM(opening_mrr_inr)
    END AS net_revenue_retention,
    SUM(active_customer) AS active_customers
FROM customer_month_movements
GROUP BY month
ORDER BY month;

-- Cohort logo retention by month age.
WITH cohort_sizes AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM customer_month_movements
    GROUP BY cohort_month
), cohort_months AS (
    SELECT cohort_month, month, SUM(active_customer) AS active_customers
    FROM customer_month_movements
    GROUP BY cohort_month, month
)
SELECT
    cm.cohort_month,
    cm.month,
    CAST((CAST(strftime('%Y', cm.month) AS INTEGER) - CAST(strftime('%Y', cm.cohort_month) AS INTEGER)) * 12
      + CAST(strftime('%m', cm.month) AS INTEGER) - CAST(strftime('%m', cm.cohort_month) AS INTEGER) AS INTEGER) AS months_since_start,
    cs.cohort_customers,
    cm.active_customers,
    1.0 * cm.active_customers / cs.cohort_customers AS logo_retention
FROM cohort_months cm
JOIN cohort_sizes cs ON cs.cohort_month = cm.cohort_month
ORDER BY cm.cohort_month, cm.month;

-- Segment movement overview.
SELECT month, segment,
       SUM(ending_mrr_inr) AS ending_mrr_inr,
       SUM(new_mrr_inr) AS new_mrr_inr,
       SUM(expansion_mrr_inr) AS expansion_mrr_inr,
       SUM(contraction_mrr_inr) AS contraction_mrr_inr,
       SUM(churned_mrr_inr) AS churned_mrr_inr
FROM customer_month_movements
GROUP BY month, segment
ORDER BY month, segment;
