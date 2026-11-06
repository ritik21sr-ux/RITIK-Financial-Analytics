# Finance Analytics & Controls | Ritik Srivastava

Ten reproducible portfolio case studies for Financial Analyst, FP&A and finance automation interviews. **All data is synthetic. This is AI-assisted personal project work, not client or employer performance.**

## Quick start
Python 3.11+; standard library only. No credentials, API keys or paid tools.
```bash
python run_all.py
python -m unittest discover -s tests -v
```
Open `outputs/portfolio.html` in a browser. CSV and JSON outputs are generated locally. Run commands from this repository's root. Windows users may use `py` instead of `python`.

## Expanded casebook

Open `outputs/portfolio.html` for the ten-case visual presentation. The seven new cases are receivables ageing, inventory valuation, SaaS retention, capex appraisal, rolling forecast backtesting, journal controls and a linked one-year three-statement model. Each has a guide under `projects/04` through `projects/10`, JSON inputs and calculated results. The original three cases are described below.

18 local tests pass. Calculations are educational prototypes; JSON financial models use floating-point arithmetic and balance tolerances, not production decimal accounting.

## Projects
| Case | Decision supported | Implementation | Evidence |
|---|---|---|---|
| 01 FP&A operating performance | Which volume, pricing and cost drivers explain plan misses? | Exact price-volume bridge, EBITDA bridge, SQLite monthly rollup | `outputs/variance.csv`, `outputs/sql_monthly.csv` |
| 02 Treasury liquidity stress | When would collections delays create a funding gap? | 13-week direct cash forecast; two-week receipt delay; minimum cash floor | `outputs/cash_*.csv`, `outputs/summary.json` |
| 03 Bank reconciliation controls | Which transactions can be cleared safely and which need review? | Unique reference + signed amount match; duplicate quarantine; exception queue | `outputs/matches.csv`, `outputs/exceptions.csv` |

## Assumptions and definitions
- Currency: whole INR. Annual operating dataset is calendar 2026, 12 months × 3 segments. Cash forecast is a separate illustrative 13-week case, not a cash conversion of that operating plan.
- Revenue = units × realized price. Variable cost = units × unit cost. EBITDA = revenue − variable cost − operating expense. Depreciation, interest and tax excluded.
- Revenue bridge: volume = (actual units − budget units) × budget price; price = actual units × (actual price − budget price). This is an exact bridge; no separate mix attribution is claimed.
- EBITDA bridge uses budget contribution per unit for volume; price effect as above; cost effect = −actual units × change in unit cost; opex effect = budget opex − actual opex. Positive EBITDA effect is favourable.
- Cash opens at ₹2,500,000; minimum operating cash is ₹750,000. Funding gap = max(0, floor − closing cash). Reported gaps are requirements, not assumed loans. Peak gap is not the sum of weekly gaps.
- Delayed receipts beyond week 13 are reported separately. No collections are silently lost. Base case already includes payments as scheduled; no interest, tax or borrowing engine is implied.
- Reconciliation amounts use cash inflow positive, cash outflow negative on both sources. Both files are assumed to cover the same statement period. No fuzzy or date-tolerance matching. Real bank and ledger adapters would need sign mapping, period validation and decimal/currency handling.

## Data and architecture
`data/` → Python pure functions / SQLite → `outputs/` → static dashboard.
Source fixtures are committed for reproducibility; no production records. `docs/DATA_DICTIONARY.md` specifies their grain. `tests/` checks financial identities, source conservation, duplicate handling and SQL/Python parity. GitHub Actions configuration runs the same commands after upload; remote CI has not been run yet.

## Review in five minutes
1. Open the dashboard and explain the EBITDA gap.
2. Inspect one row of `variance.csv` and reconstruct both bridges.
3. Compare cash scenarios and identify the peak funding requirement.
4. Inspect `exceptions.csv`; explain why DUP and FEE need manual review.
5. Run tests and change an input in a copy of the data to demonstrate sensitivity.

## Scope and honest presentation
An interview portfolio, not a production treasury platform, audited financial report, bank integration or delivered Power BI report. AI helped draft implementation and documentation. Ritik should review, run and explain the code before claiming independent proficiency. No measured business savings, forecast accuracy or employer outcomes are claimed.

## Next extensions
Add forecast backtesting on historical actuals; approved matching tolerances and exception ownership; real-data adapters; Power BI model using the output CSVs. These are future improvements, not completed features.
