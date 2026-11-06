# Interview walkthrough / Hinglish

## 90-second introduction
“Yeh mera AI-assisted personal finance analytics portfolio hai, synthetic data par. Isme maine operating plan variance, 13-week liquidity scenarios aur conservative bank reconciliation ka workflow review kiya hai. Outputs reproducible hain aur accounting identities tests se validate hoti hain.” Use this only after personally running and reviewing it.

## Questions to practise
1. Revenue badha, phir EBITDA kyun gira? Unit contribution, price discounts, unit cost aur operating expense ko separately examine karo.
2. Price-volume formula mein actual quantity kyun? Cross-term ko price effect mein allocate karte hain; isliye bridge exact reconcile hota hai. Alternative order attribution change karega, total nahi.
3. Profit aur cash same kyun nahi? Collection/payment timing, capex and financing create differences. These two demo datasets are independent; don't claim a linked three-statement model.
4. Two-week delay ka impact? Beginning receipts move later; end receipts horizon ke baahar carry hote hain. Missing collections ko loss mat bolo.
5. Same reference twice aaye? Ambiguous candidates exception mein; amount alone se auto-clear nahi.
6. Production mein kya missing hai? Source validation, access controls, approval trail, period/currency checks, logging, change management and reconciliation sign-offs.
7. AI ka use? Explain drafted code, manually reviewed finance logic, test evidence, limitations. Never invent your own contribution or deployment history.

## Practical exercises before interviews
- Set actual price equal to budget; verify price effect becomes zero.
- Increase week-5 capex by ₹100,000; explain the resulting cash trajectory.
- Add an extra ledger reference duplicate; verify the original match becomes ambiguous.
- Explain why rounding and foreign currencies need an explicit policy.

## CV wording after review and completion
Personal project — Finance Analytics & Controls (Python, SQL): implemented and validated a synthetic-data workflow covering 36 segment-month operating records, a 13-week cash forecast and 201 bank/ledger source rows; built variance bridges, liquidity stress scenarios and an exception-based reconciliation queue.

If you have not yet reviewed or run it, say “Developing an AI-assisted finance analytics portfolio” instead. Add a GitHub URL only after the repository exists. Do not present synthetic impact as salary savings or employer achievements.

## GitHub launch
Suggested repository name: ritik-finance-analytics-controls
Description: Reproducible FP&A, cash-flow stress testing and reconciliation case studies with Python, SQL and synthetic data.
Topics: finance, fp-and-a, python, sql, cash-flow, reconciliation, portfolio.
Upload the contents of this folder at repository root. Pin the repository to your profile. Use README as the landing page. No GitHub URL is currently claimed by this package.
