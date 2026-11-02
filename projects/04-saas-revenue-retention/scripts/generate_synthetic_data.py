#!/usr/bin/env python3
"""Create deterministic synthetic customer-month SaaS MRR movements."""

import csv
import random
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
random.seed(241103)
MONTHS = [date(year, month, 1) for year in (2024, 2025) for month in range(1, 13)]
PLANS = {
    "Starter": (8000, 18000),
    "Growth": (22000, 52000),
    "Enterprise": (65000, 135000),
}
SEGMENTS = ["SMB", "Mid-market", "Enterprise"]


def main():
    ROOT.joinpath("data").mkdir(parents=True, exist_ok=True)
    rows = []
    customer_meta = {}
    for number in range(1, 131):
        start_index = number - 1 if number <= len(MONTHS) else random.randrange(0, len(MONTHS))
        segment = random.choices(SEGMENTS, weights=(55, 32, 13))[0]
        plan = random.choices(list(PLANS), weights=(48, 37, 15))[0]
        low, high = PLANS[plan]
        base_mrr = random.randrange(low // 500, high // 500 + 1) * 500
        customer_id = f"C{number:04d}"
        customer_meta[customer_id] = {
            "start_index": start_index,
            "cohort_month": MONTHS[start_index].isoformat(),
            "segment": segment,
            "plan": plan,
            "base_mrr": base_mrr,
        }
        mrr = 0
        for index in range(start_index, len(MONTHS)):
            month = MONTHS[index]
            opening = mrr
            new = base_mrr if index == start_index else 0
            expansion = 0
            contraction = 0
            churned = 0
            if index > start_index and index - start_index >= 3 and random.random() < 0.022:
                churned = opening
                mrr = 0
            else:
                if opening and random.random() < 0.11:
                    if random.random() < 0.72:
                        expansion = round(opening * random.uniform(0.05, 0.18) / 500) * 500
                    else:
                        contraction = min(opening, round(opening * random.uniform(0.04, 0.14) / 500) * 500)
                mrr = opening + new + expansion - contraction
            rows.append({
                "month": month.isoformat(),
                "customer_id": customer_id,
                "cohort_month": customer_meta[customer_id]["cohort_month"],
                "segment": segment,
                "plan": plan,
                "opening_mrr_inr": opening,
                "new_mrr_inr": new,
                "expansion_mrr_inr": expansion,
                "contraction_mrr_inr": contraction,
                "churned_mrr_inr": churned,
                "ending_mrr_inr": mrr,
                "active_customer": int(mrr > 0),
            })
            if churned:
                break

    path = ROOT / "data" / "customer_month_movements.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic customer-month rows to {path.name}")


if __name__ == "__main__":
    main()
