#!/usr/bin/env python3
"""Create a deterministic synthetic AP register for the controls-review demo."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
random.seed(5105)


def main():
    rows = []
    for index in range(1, 51):
        invoice_date = date(2026, 6, 1) + timedelta(days=random.randrange(0, 125))
        amount = random.randrange(20, 301) * 1000
        rows.append({
            "invoice_id": f"AP-{index:04d}",
            "vendor_id": f"V{(index - 1) % 10 + 1:03d}",
            "invoice_number": f"INV-2026-{index:04d}",
            "invoice_date": invoice_date.isoformat(),
            "due_date": (invoice_date + timedelta(days=random.choice((30, 45, 60)))).isoformat(),
            "amount_inr": amount,
            "po_number": f"PO-{index + 3000:04d}" if amount < 180000 or random.random() < 0.78 else "",
            "approval_status": "Approved" if random.random() < 0.86 else "Pending",
            "bank_change_pending": int(random.random() < 0.04),
            "paid_flag": int(random.random() < 0.62),
        })

    # Controlled synthetic examples so the output includes reviewable cases.
    exact_duplicate = dict(rows[4], invoice_id="AP-9001", paid_flag=0)
    rows.append(exact_duplicate)
    near_duplicate = dict(rows[7], invoice_id="AP-9002", invoice_number=rows[7]["invoice_number"].replace("0008", "OO08"), paid_flag=0)
    rows.append(near_duplicate)
    rows.extend([
        {"invoice_id": "AP-9003", "vendor_id": "V002", "invoice_number": "INV-2026-PO-MISS", "invoice_date": "2026-09-04", "due_date": "2026-10-04", "amount_inr": 98000, "po_number": "", "approval_status": "Approved", "bank_change_pending": 0, "paid_flag": 0},
        {"invoice_id": "AP-9004", "vendor_id": "V006", "invoice_number": "INV-2026-BANK-01", "invoice_date": "2026-10-02", "due_date": "2026-11-01", "amount_inr": 142000, "po_number": "PO-9904", "approval_status": "Approved", "bank_change_pending": 1, "paid_flag": 0},
        {"invoice_id": "AP-9005", "vendor_id": "V009", "invoice_number": "INV-2026-APP-01", "invoice_date": "2026-09-01", "due_date": "2026-10-01", "amount_inr": 185000, "po_number": "PO-9905", "approval_status": "Pending", "bank_change_pending": 0, "paid_flag": 0},
        {"invoice_id": "AP-9006", "vendor_id": "V004", "invoice_number": "INV-2026-OVER-01", "invoice_date": "2026-07-01", "due_date": "2026-07-31", "amount_inr": 76000, "po_number": "PO-9906", "approval_status": "Approved", "bank_change_pending": 0, "paid_flag": 0},
    ])

    path = ROOT / "data" / "invoice_register.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic invoice rows to {path.name}")


if __name__ == "__main__":
    main()
