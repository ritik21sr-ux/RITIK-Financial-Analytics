-- SQLite-compatible examples for sales_lines.csv.

-- Monthly net revenue, contribution, margin, and discount rate.
SELECT month,
       SUM(gross_sales_inr) AS gross_sales_inr,
       SUM(discount_inr) AS discount_inr,
       SUM(returns_inr) AS returns_inr,
       SUM(net_revenue_inr) AS net_revenue_inr,
       SUM(contribution_inr) AS contribution_inr,
       1.0 * SUM(contribution_inr) / NULLIF(SUM(net_revenue_inr), 0) AS contribution_margin,
       1.0 * SUM(discount_inr) / NULLIF(SUM(gross_sales_inr), 0) AS discount_rate
FROM sales_lines
GROUP BY month
ORDER BY month;

-- Product economics and mix.
SELECT product,
       SUM(units) AS units,
       SUM(net_revenue_inr) AS net_revenue_inr,
       SUM(cogs_inr) AS cogs_inr,
       SUM(shipping_inr) AS shipping_inr,
       SUM(sales_commission_inr) AS sales_commission_inr,
       SUM(contribution_inr) AS contribution_inr,
       1.0 * SUM(contribution_inr) / NULLIF(SUM(net_revenue_inr), 0) AS contribution_margin
FROM sales_lines
GROUP BY product
ORDER BY contribution_inr DESC;

-- Customer concentration, ranked by contribution.
WITH customer_totals AS (
    SELECT customer_id, customer_name, segment,
           SUM(net_revenue_inr) AS net_revenue_inr,
           SUM(contribution_inr) AS contribution_inr
    FROM sales_lines
    GROUP BY customer_id, customer_name, segment
)
SELECT *,
       RANK() OVER (ORDER BY contribution_inr DESC) AS contribution_rank,
       1.0 * contribution_inr / NULLIF(SUM(contribution_inr) OVER (), 0) AS share_of_total_contribution
FROM customer_totals
ORDER BY contribution_rank;

-- Segment view: discounting and margin.
SELECT segment,
       SUM(gross_sales_inr) AS gross_sales_inr,
       SUM(discount_inr) AS discount_inr,
       SUM(net_revenue_inr) AS net_revenue_inr,
       SUM(contribution_inr) AS contribution_inr,
       1.0 * SUM(discount_inr) / NULLIF(SUM(gross_sales_inr), 0) AS discount_rate,
       1.0 * SUM(contribution_inr) / NULLIF(SUM(net_revenue_inr), 0) AS contribution_margin
FROM sales_lines
GROUP BY segment
ORDER BY contribution_inr DESC;
