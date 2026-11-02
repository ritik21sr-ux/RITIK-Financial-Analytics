#!/usr/bin/env python3
"""Summarize synthetic customer-month MRR movements and cohort retention."""

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NUMERIC = ["opening_mrr_inr", "new_mrr_inr", "expansion_mrr_inr", "contraction_mrr_inr", "churned_mrr_inr", "ending_mrr_inr"]


def read_movements():
    with (ROOT / "data" / "customer_month_movements.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for field in NUMERIC:
            row[field] = float(row[field])
        row["active_customer"] = int(row["active_customer"])
    return rows


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    movements = read_movements()
    monthly = defaultdict(list)
    customer_rows = defaultdict(dict)
    cohort_customers = defaultdict(set)
    for row in movements:
        monthly[row["month"]].append(row)
        customer_rows[row["customer_id"]][row["month"]] = row
        cohort_customers[row["cohort_month"]].add(row["customer_id"])

    kpis = []
    for month in sorted(monthly):
        rows = monthly[month]
        totals = {field: sum(row[field] for row in rows) for field in NUMERIC}
        opening = totals["opening_mrr_inr"]
        active = sum(row["active_customer"] for row in rows)
        kpis.append({
            "month": month,
            **{key: round(value, 2) for key, value in totals.items()},
            "net_revenue_retention_pct": round((opening + totals["expansion_mrr_inr"] - totals["contraction_mrr_inr"] - totals["churned_mrr_inr"]) / opening, 4) if opening else "",
            "gross_revenue_retention_pct": round((opening - totals["contraction_mrr_inr"] - totals["churned_mrr_inr"]) / opening, 4) if opening else "",
            "new_customers": sum(row["new_mrr_inr"] > 0 for row in rows),
            "churned_customers": sum(row["churned_mrr_inr"] > 0 for row in rows),
            "active_customers": active,
            "arpa_inr": round(totals["ending_mrr_inr"] / active, 2) if active else 0,
        })

    cohort_rows = []
    month_index = {month: index for index, month in enumerate(sorted(monthly))}
    months = sorted(monthly)
    for cohort, customer_set in sorted(cohort_customers.items()):
        customers = sorted(customer_set)
        start = month_index[cohort]
        cohort_start_mrr = sum(customer_rows[c].get(cohort, {}).get("new_mrr_inr", 0) for c in customers)
        for index in range(start, len(months)):
            month = months[index]
            active_customers = sum(customer_rows[c].get(month, {}).get("active_customer", 0) for c in customers)
            retained_mrr = sum(customer_rows[c].get(month, {}).get("ending_mrr_inr", 0) for c in customers)
            cohort_rows.append({
                "cohort_month": cohort,
                "month": month,
                "months_since_start": index - start,
                "cohort_customers": len(customers),
                "active_customers": active_customers,
                "logo_retention_pct": round(active_customers / len(customers), 4) if customers else 0,
                "cohort_start_mrr_inr": round(cohort_start_mrr, 2),
                "retained_mrr_inr": round(retained_mrr, 2),
                "revenue_retention_pct": round(retained_mrr / cohort_start_mrr, 4) if cohort_start_mrr else 0,
            })

    write_csv(ROOT / "examples" / "monthly_kpis.csv", kpis)
    write_csv(ROOT / "examples" / "cohort_retention.csv", cohort_rows)
    summary = {
        "dataset": "synthetic portfolio demonstration",
        "customer_month_rows": len(movements),
        "month_count": len(monthly),
        "customer_count": len(customer_rows),
        "latest_month": kpis[-1]["month"],
        "latest_ending_mrr_inr": kpis[-1]["ending_mrr_inr"],
        "latest_nrr_pct": kpis[-1]["net_revenue_retention_pct"],
        "definitions": "MRR movements are simulated; NRR excludes new MRR.",
    }
    (ROOT / "examples" / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
