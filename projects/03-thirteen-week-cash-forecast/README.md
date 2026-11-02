# 13-Week Cash Flow Forecast

## Purpose

An illustrative short-term liquidity forecast for a fictional operating business. The model combines expected customer collections, scheduled supplier payments, payroll, operating costs, and planned capital spending into a rolling 13-week cash view.

## Included

- `workbooks/13_week_cash_forecast.xlsx` — executive summary, scenario assumptions, AR and AP schedules, weekly operating inputs, and the linked 13-week forecast.
- `data/` — synthetic schedule inputs used in the workbook and Python example.
- `scripts/run_cash_forecast.py` — standard-library Python command-line forecast that exports weekly cash, a summary, and any cash-floor watch items.
- `examples/` — generated Base and Downside outputs for review.
- `model/methodology.md` — formulas, scenario treatment, and limitations.

## Run the Python example

From this project folder:

```text
python scripts/run_cash_forecast.py --scenario Base
python scripts/run_cash_forecast.py --scenario Downside --output-dir examples/downside
```

The script does not move or reserve cash. A cash-floor watch item is a planning signal for review, not a payment instruction.

The synthetic register intentionally produces a tighter Downside case so that the cash-floor review flow is visible. The number and timing of watch items are illustrative, not a real-company benchmark.

| Synthetic scenario | Closing cash after 13 weeks | Weeks below ₹500,000 floor |
|---|---:|---:|
| Base | ₹1,456,600 | 0 |
| Downside | ₹31,320 | 2 |

## Model notes

- All data is synthetic and stated in INR.
- Collection timing and probability, payment timing, cost assumptions, and scenarios are illustrative.
- The Excel file is a portfolio demonstration, not a treasury system or approved forecast.
- Actual liquidity decisions require validated bank balances, dated customer and supplier commitments, and review by the responsible finance team.
