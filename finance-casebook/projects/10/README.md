# 10 · Three-Statement Model

**Business question:** Linked earnings, working capital and cash.

Synthetic, AI-assisted personal case study for Ritik Srivastava. No employer/client impact claimed.

## Run and inspect
From repository root: `python run_all.py`, then `python -m unittest discover -s tests -v`.
Open `../../outputs/portfolio.html` for presentation and `../../outputs/advanced_results.json` for results.
For projects 04–10, input is the matching numbered JSON under `data/`; output is keyed by that number in advanced_results.json. Projects 01–03 use the original CSV fixtures.

## Method and limitations
Single forecast year. Interest on opening debt; tax paid equals tax expense; no deferred tax or negative-tax benefit.
See `src/finance.py` (01–03) or `src/advanced.py` (04–10) for formulas, and tests for independently specified expected values.

## Interview prompt
Explain how a 10-day DSO increase affects cash and the balance sheet.
Explain the input grain, formula, output, business decision and one limitation in that order. Run a changed-input scenario before claiming proficiency.
