#!/usr/bin/env python3
"""Reconcile synthetic ledger and bank rows into matches and review exceptions."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


FIELDS = {"transaction_id", "transaction_date", "reference", "description", "amount_inr"}
MATCH_FIELDS = [
    "reference", "ledger_id", "bank_id", "ledger_date", "bank_date",
    "ledger_amount_inr", "bank_amount_inr", "date_difference_days", "amount_difference_inr",
]
EXCEPTION_FIELDS = [
    "exception_type", "source", "reference", "ledger_id", "bank_id",
    "ledger_date", "bank_date", "ledger_amount_inr", "bank_amount_inr", "note",
]


def load_rows(path: Path, source: str) -> list[dict[str, Any]]:
    with path.open("r", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        missing = FIELDS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{source} file is missing required columns: {', '.join(sorted(missing))}")
        rows = []
        seen_ids: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            transaction_id = (row.get("transaction_id") or "").strip()
            reference = (row.get("reference") or "").strip().upper()
            if not transaction_id or not reference:
                raise ValueError(f"{source} row {line_number} needs transaction_id and reference")
            if transaction_id in seen_ids:
                raise ValueError(f"{source} row {line_number} repeats transaction_id {transaction_id}")
            seen_ids.add(transaction_id)
            try:
                transaction_date = date.fromisoformat((row.get("transaction_date") or "").strip())
                amount = Decimal((row.get("amount_inr") or "").strip())
            except (ValueError, InvalidOperation) as exc:
                raise ValueError(f"{source} row {line_number} has an invalid date or amount") from exc
            if not amount.is_finite() or amount < 0:
                raise ValueError(f"{source} row {line_number} has an invalid non-negative INR amount")
            rows.append({
                "transaction_id": transaction_id,
                "transaction_date": transaction_date,
                "reference": reference,
                "description": (row.get("description") or "").strip(),
                "amount": amount,
            })
    return rows


def amount_text(value: Decimal | None) -> str:
    return "" if value is None else format(value, "f")


def make_exception(
    exception_type: str,
    source: str,
    reference: str,
    ledger: dict[str, Any] | None,
    bank: dict[str, Any] | None,
    note: str,
) -> dict[str, str]:
    return {
        "exception_type": exception_type,
        "source": source,
        "reference": reference,
        "ledger_id": ledger["transaction_id"] if ledger else "",
        "bank_id": bank["transaction_id"] if bank else "",
        "ledger_date": ledger["transaction_date"].isoformat() if ledger else "",
        "bank_date": bank["transaction_date"].isoformat() if bank else "",
        "ledger_amount_inr": amount_text(ledger["amount"] if ledger else None),
        "bank_amount_inr": amount_text(bank["amount"] if bank else None),
        "note": note,
    }


def reconcile(
    ledger_rows: list[dict[str, Any]],
    bank_rows: list[dict[str, Any]],
    date_window_days: int,
    amount_tolerance: Decimal,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    ledger_by_ref: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bank_by_ref: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in ledger_rows:
        ledger_by_ref[row["reference"]].append(row)
    for row in bank_rows:
        bank_by_ref[row["reference"]].append(row)

    matches: list[dict[str, str]] = []
    exceptions: list[dict[str, str]] = []
    for reference in sorted(set(ledger_by_ref) | set(bank_by_ref)):
        ledgers = ledger_by_ref.get(reference, [])
        banks = bank_by_ref.get(reference, [])

        if len(ledgers) > 1 or len(banks) > 1:
            note = "Reference is not unique on at least one input side; review before matching."
            for ledger in ledgers:
                exceptions.append(make_exception("duplicate_reference", "ledger", reference, ledger, None, note))
            for bank in banks:
                exceptions.append(make_exception("duplicate_reference", "bank", reference, None, bank, note))
            continue

        if not ledgers:
            for bank in banks:
                exceptions.append(make_exception("unmatched_bank", "bank", reference, None, bank, "No ledger row has this reference."))
            continue
        if not banks:
            for ledger in ledgers:
                exceptions.append(make_exception("unmatched_ledger", "ledger", reference, ledger, None, "No bank row has this reference."))
            continue

        ledger, bank = ledgers[0], banks[0]
        amount_difference = bank["amount"] - ledger["amount"]
        date_difference = (bank["transaction_date"] - ledger["transaction_date"]).days
        if abs(amount_difference) > amount_tolerance:
            exceptions.append(make_exception(
                "amount_mismatch", "both", reference, ledger, bank,
                f"Absolute amount difference exceeds tolerance {amount_tolerance} INR.",
            ))
        elif abs(date_difference) > date_window_days:
            exceptions.append(make_exception(
                "date_outside_window", "both", reference, ledger, bank,
                f"Absolute date difference exceeds the {date_window_days}-day window.",
            ))
        else:
            matches.append({
                "reference": reference,
                "ledger_id": ledger["transaction_id"],
                "bank_id": bank["transaction_id"],
                "ledger_date": ledger["transaction_date"].isoformat(),
                "bank_date": bank["transaction_date"].isoformat(),
                "ledger_amount_inr": amount_text(ledger["amount"]),
                "bank_amount_inr": amount_text(bank["amount"]),
                "date_difference_days": str(date_difference),
                "amount_difference_inr": amount_text(amount_difference),
            })
    return matches, exceptions


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    project_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=project_dir / "data" / "general_ledger.csv")
    parser.add_argument("--bank", type=Path, default=project_dir / "data" / "bank_statement.csv")
    parser.add_argument("--output-dir", type=Path, default=project_dir / "examples")
    parser.add_argument("--date-window-days", type=int, default=3)
    parser.add_argument("--amount-tolerance", type=Decimal, default=Decimal("0.01"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.date_window_days < 0 or args.amount_tolerance < 0:
        raise SystemExit("Date window and amount tolerance must be non-negative.")

    ledger_rows = load_rows(args.ledger, "Ledger")
    bank_rows = load_rows(args.bank, "Bank")
    matches, exceptions = reconcile(ledger_rows, bank_rows, args.date_window_days, args.amount_tolerance)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "matched.csv", MATCH_FIELDS, matches)
    write_csv(args.output_dir / "exceptions.csv", EXCEPTION_FIELDS, exceptions)

    exception_counts = Counter(row["exception_type"] for row in exceptions)
    matched_ledger_total = sum((Decimal(row["ledger_amount_inr"]) for row in matches), Decimal("0"))
    matched_bank_total = sum((Decimal(row["bank_amount_inr"]) for row in matches), Decimal("0"))
    summary = {
        "currency": "INR",
        "synthetic_demo_data": True,
        "ledger_rows": len(ledger_rows),
        "bank_rows": len(bank_rows),
        "matched_rows": len(matches),
        "exception_rows": len(exceptions),
        "exception_counts": dict(sorted(exception_counts.items())),
        "matched_ledger_total_inr": int(matched_ledger_total),
        "matched_bank_total_inr": int(matched_bank_total),
        "unresolved_items_require_review": True,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
