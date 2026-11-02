# Power BI report build guide

1. Load `data/invoice_register.csv` and generated `examples/exceptions.csv`.
2. Set amount fields to whole-number INR, dates to Date, and exception rule to a categorical field.
3. Relate invoice register to exceptions on `invoice_id` (one-to-many). Use measures in `measures.dax` to avoid counting an invoice's amount more than once when it has multiple flags.
4. Suggested visuals: exception exposure by rule, affected invoices by vendor, overdue and pending-approval cards, and a detail table with invoice ID, rule, amount, and due date.

The `.pbix` is **Coming soon**. This is a suggested model/report layout, not a published Power BI dashboard.
