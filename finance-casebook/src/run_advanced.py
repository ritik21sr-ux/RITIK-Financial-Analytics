import json
from pathlib import Path
from advanced import aging,inventory,saas,capex,backtest,journal_controls,statements
ROOT=Path(__file__).resolve().parents[1]
def main():
    results={}
    for name,fn in [('04_receivables',lambda a:aging(a['invoices'],a['as_of'])),('05_inventory',lambda a:inventory(a['items'])),('06_saas',lambda a:saas(a['rows'])),('07_capex',lambda a:capex(a['flows'],a['rate'])),('08_forecasting',lambda a:backtest(a['actuals'],a['window'])),('09_journal_controls',lambda a:journal_controls(a['lines'])),('10_three_statements',statements)]:
        results[name]=fn(json.loads((ROOT/'data'/f'{name}.json').read_text()))
    (ROOT/'outputs'/'advanced_results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
