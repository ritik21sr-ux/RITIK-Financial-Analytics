# 01 · FP&A Performance

**Business question:** Budget variance and exact EBITDA drivers.

Synthetic, AI-assisted personal case study for Ritik Srivastava. No employer/client impact claimed.

## Run and inspect
From repository root: `python run_all.py`, then `python -m unittest discover -s tests -v`.
Open `../../outputs/portfolio.html` for presentation and `../../outputs/variance.csv` for results.
For projects 04–10, input is the matching numbered JSON under `data/`; output is keyed by that number in advanced_results.json. Projects 01–03 use the original CSV fixtures.

## Method and limitations
Price and volume attribution depend on bridge order; no causal inference.
See `src/finance.py` (01–03) or `src/advanced.py` (04–10) for formulas, and tests for independently specified expected values.

## Interview prompt
Explain how contribution-volume differs from revenue-volume.
Explain the input grain, formula, output, business decision and one limitation in that order. Run a changed-input scenario before claiming proficiency.
