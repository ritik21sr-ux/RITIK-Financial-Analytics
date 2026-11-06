# 03 · Reconciliation Controls

**Business question:** Unique matching with an exception trail.

Synthetic, AI-assisted personal case study for Ritik Srivastava. No employer/client impact claimed.

## Run and inspect
From repository root: `python run_all.py`, then `python -m unittest discover -s tests -v`.
Open `../../outputs/portfolio.html` for presentation and `../../outputs/exceptions.csv` for results.
For projects 04–10, input is the matching numbered JSON under `data/`; output is keyed by that number in advanced_results.json. Projects 01–03 use the original CSV fixtures.

## Method and limitations
No fuzzy matches, period controls or live bank integration.
See `src/finance.py` (01–03) or `src/advanced.py` (04–10) for formulas, and tests for independently specified expected values.

## Interview prompt
Why should duplicate references require review?
Explain the input grain, formula, output, business decision and one limitation in that order. Run a changed-input scenario before claiming proficiency.
