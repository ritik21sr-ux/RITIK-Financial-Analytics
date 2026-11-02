#!/usr/bin/env python3
"""Generate the deterministic synthetic source data for the FP&A portfolio demo."""

from __future__ import annotations

import csv
from calendar import monthrange
from datetime import date
from pathlib import Path


DEPARTMENTS = {
    "Product": {
        "Revenue": ("Revenue", 1_200_000),
        "Payroll": ("Expense", 560_000),
        "Software": ("Expense", 35_000),
        "Marketing": ("Expense", 90_000),
        "Travel": ("Expense", 25_000),
    },
    "Sales": {
        "Revenue": ("Revenue", 1_000_000),
        "Payroll": ("Expense", 480_000),
        "Software": ("Expense", 28_000),
        "Marketing": ("Expense", 140_000),
        "Travel": ("Expense", 45_000),
    },
    "Operations": {
        "Revenue": ("Revenue", 700_000),
        "Payroll": ("Expense", 350_000),
        "Software": ("Expense", 42_000),
        "Marketing": ("Expense", 45_000),
        "Travel": ("Expense", 38_000),
    },
}

REVENUE_SEASONALITY = (0.90, 0.92, 0.95, 0.98, 1.00, 1.02, 1.04, 1.02, 1.07, 1.10, 1.14, 1.18)
EXPENSE_SEASONALITY = (0.98, 0.98, 0.99, 1.00, 1.00, 1.01, 1.00, 1.00, 1.02, 1.03, 1.04, 1.05)
REVENUE_ACTUAL_FACTORS = (0.99, 1.01, 1.02, 0.98, 1.03, 1.01, 0.98, 1.04, 0.96, 1.02, 0.94, 1.05)
EXPENSE_ACTUAL_FACTORS = {
    "Payroll": (1.01, 1.02, 1.02, 1.01, 1.03, 1.02, 1.01, 1.03, 1.02, 1.03, 1.02, 1.04),
    "Software": (0.98, 0.97, 0.98, 0.96, 0.97, 0.98, 0.95, 0.97, 0.96, 0.98, 0.97, 0.96),
    "Marketing": (1.00, 1.02, 1.01, 1.03, 1.04, 1.02, 1.04, 1.03, 1.05, 1.06, 1.08, 1.07),
    "Travel": (1.02, 1.05, 1.04, 1.03, 1.06, 1.04, 1.07, 1.05, 1.08, 1.10, 1.12, 1.08),
}


def round_to_hundred(value: float) -> int:
    return int(round(value / 100) * 100)


def generate_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for month in range(1, 13):
        last_day = monthrange(2025, month)[1]
        period = date(2025, month, last_day).isoformat()
        for dept_index, (department, accounts) in enumerate(DEPARTMENTS.items()):
            for category, (account_type, base_amount) in accounts.items():
                seasonality = REVENUE_SEASONALITY[month - 1] if account_type == "Revenue" else EXPENSE_SEASONALITY[month - 1]
                budget = round_to_hundred(base_amount * seasonality)
                if account_type == "Revenue":
                    factor = REVENUE_ACTUAL_FACTORS[month - 1] + (dept_index - 1) * 0.005
                else:
                    factor = EXPENSE_ACTUAL_FACTORS[category][month - 1]
                # One clearly visible synthetic overspend to make the variance review useful.
                if department == "Sales" and category == "Marketing" and month == 9:
                    factor += 0.14
                actual = round_to_hundred(budget * factor)
                rows.append({
                    "period": period,
                    "department": department,
                    "category": category,
                    "account_type": account_type,
                    "budget_inr": budget,
                    "actual_inr": actual,
                })
    return rows


def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "data" / "monthly_finance.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["period", "department", "category", "account_type", "budget_inr", "actual_inr"]
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(generate_rows())
    print(f"Wrote {len(generate_rows())} synthetic rows to {output_path}")


if __name__ == "__main__":
    main()
