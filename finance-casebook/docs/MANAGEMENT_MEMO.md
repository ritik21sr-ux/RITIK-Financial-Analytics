# Management memo — synthetic case study

## Operating performance
Actual revenue is ₹72,914,154 against budget ₹74,304,000: an adverse gap of ₹1,389,846 (1.87%). EBITDA is ₹3,351,132 below plan. Review segment-level price, contribution-volume, cost and opex effects in variance.csv before assigning responsibility. This bridge establishes arithmetic attribution, not causality.

## Liquidity
Base minimum cash is ₹2,220,000. A two-week receipt delay reduces minimum cash to ₹160,000, leaving a peak ₹590,000 shortfall against the ₹750,000 operating floor. ₹1,820,000 receipts move beyond week 13 and are not assumed uncollectible. Consider collections follow-up and capex timing; financing decisions require actual dates, credit terms and interest costs.

## Reconciliation
95 unique pairs match out of 103 bank and 98 ledger rows. The 11 exception rows consist of eight bank rows and three ledger rows. Investigate duplicates, missing postings and fee amount differences. These counts are source rows, not necessarily 11 separate business incidents. No exception has been automatically posted or written off.

## Limitations
Independent operating and treasury examples; no three-statement linkage. Synthetic inputs do not demonstrate actual forecast accuracy, time saved or commercial outcomes. Before production, add schema validation, source controls, currency precision, period controls, approvals and audit logging.
