# Data dictionary
| File | Grain / key | Fields and units |
|---|---|---|
| operating_plan.csv | month + segment; 36 rows | month ISO YYYY-MM; segment text; qty units; price and unit_cost INR/unit; opex INR/month/segment |
| cash_plan.csv | week; 13 rows | receipts, suppliers, payroll, overheads, capex, debt_service all non-negative INR cash flows |
| bank.csv | unique id; 103 rows | reference text; amount signed INR |
| ledger.csv | unique id; 98 rows | reference text; amount signed INR |

The fixtures were created for this project with seed 26 for operating inputs. They do not describe a real company. Matching reference is case/whitespace-normalized; empty references never match. Duplicate source IDs fail the run. Reference duplicates are retained in the exception queue.
