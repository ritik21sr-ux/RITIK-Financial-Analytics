-- SQLite-compatible FP&A demo queries.
-- All amounts are synthetic INR. Import data/monthly_finance.csv into monthly_finance.

-- Example table definition (create once before importing the CSV):
-- CREATE TABLE monthly_finance (
--   period TEXT NOT NULL,
--   department TEXT NOT NULL,
--   category TEXT NOT NULL,
--   account_type TEXT NOT NULL CHECK (account_type IN ('Revenue', 'Expense')),
--   budget_inr INTEGER NOT NULL,
--   actual_inr INTEGER NOT NULL
-- );

-- Monthly department review. Positive contribution variance is favorable.
WITH monthly_department AS (
    SELECT
        substr(period, 1, 7) AS month,
        department,
        SUM(CASE WHEN account_type = 'Revenue' THEN budget_inr ELSE 0 END) AS revenue_budget_inr,
        SUM(CASE WHEN account_type = 'Revenue' THEN actual_inr ELSE 0 END) AS revenue_actual_inr,
        SUM(CASE WHEN account_type = 'Expense' THEN budget_inr ELSE 0 END) AS expense_budget_inr,
        SUM(CASE WHEN account_type = 'Expense' THEN actual_inr ELSE 0 END) AS expense_actual_inr
    FROM monthly_finance
    GROUP BY substr(period, 1, 7), department
)
SELECT
    month,
    department,
    revenue_budget_inr,
    revenue_actual_inr,
    revenue_actual_inr - revenue_budget_inr AS revenue_variance_inr,
    expense_budget_inr,
    expense_actual_inr,
    expense_budget_inr - expense_actual_inr AS expense_favorable_variance_inr,
    revenue_budget_inr - expense_budget_inr AS contribution_budget_inr,
    revenue_actual_inr - expense_actual_inr AS contribution_actual_inr,
    (revenue_actual_inr - expense_actual_inr)
      - (revenue_budget_inr - expense_budget_inr) AS contribution_favorable_variance_inr,
    CASE
      WHEN revenue_budget_inr - expense_budget_inr = 0 THEN NULL
      ELSE 1.0 * (
        (revenue_actual_inr - expense_actual_inr)
        - (revenue_budget_inr - expense_budget_inr)
      ) / (revenue_budget_inr - expense_budget_inr)
    END AS contribution_variance_pct
FROM monthly_department
ORDER BY month, department;

-- Category view to locate favorable/unfavorable variance by department and month.
SELECT
    substr(period, 1, 7) AS month,
    department,
    category,
    account_type,
    budget_inr,
    actual_inr,
    actual_inr - budget_inr AS actual_minus_budget_inr,
    CASE
      WHEN account_type = 'Revenue' THEN actual_inr - budget_inr
      ELSE budget_inr - actual_inr
    END AS favorable_variance_inr,
    CASE
      WHEN budget_inr = 0 THEN NULL
      ELSE 1.0 * (actual_inr - budget_inr) / budget_inr
    END AS actual_vs_budget_pct
FROM monthly_finance
ORDER BY month, department, category;
