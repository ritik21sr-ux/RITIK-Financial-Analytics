#!/usr/bin/env python3
"""Flag AP invoice patterns for human review; never blocks or posts payments."""

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THRESHOLD_INR = 50000


def normalized_invoice(value):
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["amount_inr"] = int(row["amount_inr"])
        row["invoice_date_value"] = date.fromisoformat(row["invoice_date"])
        row["due_date_value"] = date.fromisoformat(row["due_date"])
        row["paid_flag_value"] = row["paid_flag"] == "1"
        row["bank_change_pending_value"] = row["bank_change_pending"] == "1"
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "invoice_register.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "examples")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date(2026, 11, 1))
    args = parser.parse_args()
    rows = read_rows(args.input)
    flags = defaultdict(set)
    duplicate_groups = defaultdict(list)

    for row in rows:
        duplicate_groups[(row["vendor_id"], normalized_invoice(row["invoice_number"]))].append(row)
        if row["amount_inr"] > THRESHOLD_INR and not row["po_number"].strip():
            flags[row["invoice_id"]].add("missing_po_over_threshold")
        if not row["paid_flag_value"] and row["approval_status"].lower() != "approved":
            flags[row["invoice_id"]].add("approval_pending_unpaid")
        if not row["paid_flag_value"] and row["bank_change_pending_value"]:
            flags[row["invoice_id"]].add("bank_change_pending_unpaid")
        if not row["paid_flag_value"] and row["due_date_value"] < args.as_of:
            flags[row["invoice_id"]].add("overdue_unpaid")

    for group in duplicate_groups.values():
        if len(group) > 1:
            for row in group:
                flags[row["invoice_id"]].add("duplicate_vendor_invoice_number")

    for index, left in enumerate(rows):
        for right in rows[index + 1:]:
            if left["vendor_id"] != right["vendor_id"]:
                continue
            if normalized_invoice(left["invoice_number"]) == normalized_invoice(right["invoice_number"]):
                continue
            days_apart = abs((left["invoice_date_value"] - right["invoice_date_value"]).days)
            if left["amount_inr"] == right["amount_inr"] and days_apart <= 2:
                flags[left["invoice_id"]].add("possible_near_duplicate_same_vendor_amount_date")
                flags[right["invoice_id"]].add("possible_near_duplicate_same_vendor_amount_date")

    by_id = {row["invoice_id"]: row for row in rows}
    high_priority_rules = {
        "duplicate_vendor_invoice_number",
        "approval_pending_unpaid",
        "bank_change_pending_unpaid",
    }
    exception_rows = []
    counts = Counter()
    for invoice_id, rules in sorted(flags.items()):
        row = by_id[invoice_id]
        for rule in sorted(rules):
            counts[rule] += 1
            exception_rows.append({
                "invoice_id": invoice_id,
                "vendor_id": row["vendor_id"],
                "invoice_number": row["invoice_number"],
                "invoice_date": row["invoice_date"],
                "due_date": row["due_date"],
                "amount_inr": row["amount_inr"],
                "rule": rule,
                "review_priority": "High" if rule in high_priority_rules else "Review",
            })

    args.output_dir.mkdir(parents=True, exist_ok=True)
    exception_path = args.output_dir / "exceptions.csv"
    fields = ["invoice_id", "vendor_id", "invoice_number", "invoice_date", "due_date", "amount_inr", "rule", "review_priority"]
    with exception_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(exception_rows)

    vendor_ids = defaultdict(set)
    for invoice_id in flags:
        vendor_ids[by_id[invoice_id]["vendor_id"]].add(invoice_id)
    vendor_summary = []
    for vendor_id, invoice_ids in sorted(vendor_ids.items()):
        vendor_summary.append({
            "vendor_id": vendor_id,
            "flagged_invoice_count": len(invoice_ids),
            "gross_invoice_exposure_inr": sum(by_id[i]["amount_inr"] for i in invoice_ids),
        })
    summary_path = args.output_dir / "vendor_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["vendor_id", "flagged_invoice_count", "gross_invoice_exposure_inr"])
        writer.writeheader()
        writer.writerows(vendor_summary)

    flagged_ids = set(flags)
    summary = {
        "dataset": "synthetic portfolio demonstration",
        "as_of_date": args.as_of.isoformat(),
        "invoice_rows_reviewed": len(rows),
        "flagged_invoice_count": len(flagged_ids),
        "exception_rows": len(exception_rows),
        "gross_invoice_exposure_inr": sum(by_id[i]["amount_inr"] for i in flagged_ids),
        "rule_counts": dict(sorted(counts.items())),
        "thresholds": {"missing_po_over_inr": THRESHOLD_INR, "near_duplicate_date_window_days": 2},
        "disclaimer": "Flags are review prompts and are not fraud or policy findings.",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
