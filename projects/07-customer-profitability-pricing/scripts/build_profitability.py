#!/usr/bin/env python3
"""Build monthly, product, segment, and customer profitability summaries."""

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MONEY = ["gross_sales_inr", "discount_inr", "returns_inr", "net_revenue_inr", "cogs_inr", "shipping_inr", "sales_commission_inr", "contribution_inr"]


def read_rows():
    with (ROOT / "data" / "sales_lines.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for field in MONEY + ["units"]:
            row[field] = float(row[field])
    return rows


def rollup(rows, key_fields):
    groups = defaultdict(list)
    for row in rows:
        key = tuple(row[field] for field in key_fields)
        groups[key].append(row)
    output = []
    for key, members in sorted(groups.items()):
        totals = {field: sum(row[field] for row in members) for field in MONEY + ["units"]}
        result = {field: value for field, value in zip(key_fields, key)}
        result.update({field: round(value, 2) for field, value in totals.items()})
        result["contribution_margin_pct"] = round(totals["contribution_inr"] / totals["net_revenue_inr"], 4) if totals["net_revenue_inr"] else 0
        result["discount_pct_of_gross"] = round(totals["discount_inr"] / totals["gross_sales_inr"], 4) if totals["gross_sales_inr"] else 0
        result["invoice_count"] = len({row["invoice_id"] for row in members})
        output.append(result)
    return output


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_rows()
    monthly = rollup(rows, ["month"])
    products = sorted(rollup(rows, ["product"]), key=lambda row: row["contribution_inr"], reverse=True)
    segments = rollup(rows, ["segment"])
    customers = sorted(rollup(rows, ["customer_id", "customer_name", "segment"]), key=lambda row: row["contribution_inr"], reverse=True)
    write_csv(ROOT / "examples" / "monthly_profitability.csv", monthly)
    write_csv(ROOT / "examples" / "product_profitability.csv", products)
    write_csv(ROOT / "examples" / "segment_profitability.csv", segments)
    write_csv(ROOT / "examples" / "customer_profitability.csv", customers)
    total_revenue = sum(row["net_revenue_inr"] for row in rows)
    total_contribution = sum(row["contribution_inr"] for row in rows)
    summary = {
        "dataset": "synthetic portfolio demonstration",
        "order_line_count": len(rows),
        "invoice_count": len({row["invoice_id"] for row in rows}),
        "customer_count": len({row["customer_id"] for row in rows}),
        "product_count": len({row["product"] for row in rows}),
        "net_revenue_inr": round(total_revenue, 2),
        "contribution_inr": round(total_contribution, 2),
        "contribution_margin_pct": round(total_contribution / total_revenue, 4) if total_revenue else 0,
        "interpretation": "Synthetic results only; no fixed overhead allocation or pricing recommendation.",
    }
    (ROOT / "examples" / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
