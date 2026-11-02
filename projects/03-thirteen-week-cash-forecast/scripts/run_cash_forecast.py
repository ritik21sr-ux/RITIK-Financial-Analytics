#!/usr/bin/env python3
"""Build a synthetic 13-week cash forecast and cash-floor watchlist."""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACTORS = {
    "Base": (1.00, 1.00),
    "Downside": (0.75, 1.08),
    "Upside": (1.05, 0.97),
}


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_forecast(scenario, opening_cash, minimum_cash):
    collection_factor, discretionary_factor = FACTORS[scenario]
    ar_by_week = defaultdict(float)
    ap_by_week = defaultdict(float)
    ops_by_week = {}

    for row in read_rows(ROOT / "data" / "ar_open_items.csv"):
        expected = float(row["amount_inr"]) * float(row["collection_probability"])
        ar_by_week[row["week"]] += expected * min(1.0, collection_factor)
    for row in read_rows(ROOT / "data" / "ap_payment_schedule.csv"):
        ap_by_week[row["week"]] += float(row["amount_inr"])
    for row in read_rows(ROOT / "data" / "weekly_operating_inputs.csv"):
        ops_by_week[row["week"]] = row

    rows = []
    opening = opening_cash
    for index in range(1, 14):
        week = f"Week {index:02d}"
        ops = ops_by_week[week]
        receipts = ar_by_week[week]
        other_inflows = float(ops["other_inflows_inr"])
        vendor = ap_by_week[week]
        payroll = float(ops["payroll_inr"])
        fixed_opex = float(ops["fixed_opex_inr"])
        discretionary = float(ops["discretionary_opex_inr"]) * discretionary_factor
        capex = float(ops["capex_inr"])
        closing = opening + receipts + other_inflows - vendor - payroll - fixed_opex - discretionary - capex
        rows.append({
            "week": week,
            "week_start": ops["week_start"],
            "opening_cash_inr": round(opening, 2),
            "expected_customer_receipts_inr": round(receipts, 2),
            "other_inflows_inr": round(other_inflows, 2),
            "supplier_payments_inr": round(vendor, 2),
            "payroll_inr": round(payroll, 2),
            "fixed_opex_inr": round(fixed_opex, 2),
            "discretionary_opex_inr": round(discretionary, 2),
            "capex_inr": round(capex, 2),
            "closing_cash_inr": round(closing, 2),
            "minimum_cash_inr": round(minimum_cash, 2),
            "headroom_inr": round(closing - minimum_cash, 2),
            "below_cash_floor": closing < minimum_cash,
        })
        opening = closing
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=FACTORS, default="Base")
    parser.add_argument("--opening-cash", type=float, default=3_500_000)
    parser.add_argument("--minimum-cash", type=float, default=500_000)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "examples")
    args = parser.parse_args()

    rows = build_forecast(args.scenario, args.opening_cash, args.minimum_cash)
    fields = list(rows[0])
    write_rows(args.output_dir / "weekly_forecast.csv", rows, fields)
    watch = [row for row in rows if row["below_cash_floor"]]
    write_rows(args.output_dir / "cash_floor_watchlist.csv", watch, fields)
    summary = {
        "dataset": "synthetic portfolio demonstration",
        "scenario": args.scenario,
        "opening_cash_inr": round(args.opening_cash, 2),
        "minimum_cash_inr": round(args.minimum_cash, 2),
        "ending_cash_inr": rows[-1]["closing_cash_inr"],
        "lowest_weekly_close_inr": min(row["closing_cash_inr"] for row in rows),
        "weeks_below_cash_floor": len(watch),
        "maximum_cash_floor_shortfall_inr": round(max((max(0, -row["headroom_inr"]) for row in rows), default=0), 2),
        "total_expected_receipts_inr": round(sum(row["expected_customer_receipts_inr"] for row in rows), 2),
        "total_scheduled_outflows_inr": round(sum(
            row["supplier_payments_inr"] + row["payroll_inr"] + row["fixed_opex_inr"]
            + row["discretionary_opex_inr"] + row["capex_inr"] for row in rows
        ), 2),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
