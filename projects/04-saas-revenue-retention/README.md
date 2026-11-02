# SaaS Revenue and Retention Analytics

## Purpose

A synthetic customer-month dataset for analysing recurring-revenue movement, customer retention, and revenue retention. The example follows customer MRR from signup through expansion, contraction, and churn.

## Included

- `data/customer_month_movements.csv` — deterministic synthetic customer-month movements for Jan 2024–Dec 2025.
- `examples/monthly_kpis.csv` and `examples/cohort_retention.csv` — generated monthly and cohort summaries.
- `scripts/generate_synthetic_data.py` — reproducible dataset generator.
- `scripts/build_metrics.py` — standard-library Python summary and cohort calculations.
- `sql/saas_metrics.sql` — SQLite-compatible monthly movement and cohort queries.
- `powerbi/measures.dax` and `powerbi/report_build_guide.md` — starter measures and model/report notes.

The native Power BI `.pbix` report is **Coming soon**. The DAX and report guide are starter materials, not a completed Power BI dashboard.

## Run

From this project folder:

```text
python scripts/generate_synthetic_data.py
python scripts/build_metrics.py
```

## Definitions and limits

- All customers, contracts, plans, and revenue amounts are synthetic and denominated in INR.
- MRR is recorded at customer-month grain. ARR is shown as MRR × 12 for a simple annualized run-rate view; it is not recognized revenue or contracted ARR.
- Net revenue retention excludes new MRR and compares opening MRR plus expansion less contraction and churn against opening MRR.
- Churn timing, customer counts, and movements are illustrative and should not be used as a benchmark for a real company.
