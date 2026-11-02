# Month-end Bank Reconciliation Helper

## Summary

This Python command-line demo compares synthetic general-ledger and bank statement rows. It matches by normalized reference, amount within a stated tolerance, and posting date within a configurable window. Unmatched, duplicate, and mismatched records are written to an exception file for review.

All amounts are synthetic INR. The example is an automation demonstration, not an accounting control or production reconciliation service.

## Files

- `src/reconcile.py` — standard-library Python CLI.
- `data/general_ledger.csv` and `data/bank_statement.csv` — synthetic input files.
- `examples/matched.csv` — generated matches.
- `examples/exceptions.csv` — generated unresolved items.
- `examples/summary.json` — generated record counts and totals.

## Run

From this project folder:

```text
python src/reconcile.py
```

To use different files or output folder:

```text
python src/reconcile.py --ledger path/to/general_ledger.csv --bank path/to/bank_statement.csv --output-dir path/to/output --date-window-days 3 --amount-tolerance 0.01
```

The script does not post journal entries, clear transactions, or decide whether an exception is valid. A reviewer should investigate exceptions and approve any accounting action through the organisation's normal controls.
