# Accounts Payable Controls Review

## Purpose

A small, reproducible exception-review demo for a fictional accounts-payable register. Python identifies duplicate and near-duplicate invoice patterns, missing purchase orders above a review threshold, pending approvals, pending bank-detail changes, and overdue unpaid invoices. SQLite queries show equivalent review patterns; Power BI starter measures summarize the generated exception file.

## Included

- `data/invoice_register.csv` — synthetic invoice register, including labeled-in-document control examples.
- `scripts/generate_sample_data.py` — deterministic input generator.
- `scripts/analyze_ap_invoices.py` — standard-library review and exception export.
- `examples/exceptions.csv`, `examples/vendor_summary.csv`, and `examples/summary.json` — generated outputs using the documented synthetic as-of date.
- `sql/ap_controls.sql` — SQLite-compatible exception queries.
- `powerbi/measures.dax` and `powerbi/report_build_guide.md` — starter measures and a report layout.

The Power BI `.pbix` file is **Coming soon**. The included materials are a code-and-data demo, not a completed dashboard or an internal control implementation.

## Run

From this project folder:

```text
python scripts/generate_sample_data.py
python scripts/analyze_ap_invoices.py --as-of 2026-11-01
```

## Review and limitations

- All vendor, invoice, and payment data is synthetic and denominated in INR.
- The sample intentionally includes seeded review cases; its exception frequency is not a benchmark for real AP operations.
- A flagged pattern is a prompt for a person to review; it is not a finding of fraud, duplicate payment, or policy breach.
- The examples do not connect to an ERP, bank, supplier master, approval workflow, or payment system and do not post or block transactions.
- Thresholds and date rules are configurable examples and would require documented policy approval before any real use.
