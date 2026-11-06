-- SQLite. Month stored as ISO YYYY-MM; amounts are INR.
SELECT month,
 SUM(budget_qty*budget_price) AS budget_revenue,
 SUM(actual_qty*actual_price) AS actual_revenue,
 SUM(actual_qty*(actual_price-actual_unit_cost)-actual_opex) AS actual_ebitda,
 ROUND(100.0*SUM(actual_qty*(actual_price-actual_unit_cost)-actual_opex)
 / NULLIF(SUM(actual_qty*actual_price),0),2) AS ebitda_margin_pct,
 SUM(actual_qty*actual_price)-SUM(budget_qty*budget_price) AS revenue_variance
FROM operating GROUP BY month ORDER BY month;
