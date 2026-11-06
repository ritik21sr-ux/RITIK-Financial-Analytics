import csv,json,sqlite3,html
from pathlib import Path
from finance import variance,cash_forecast,reconcile
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/'data'/name).open(newline='') as f: return list(csv.DictReader(f))
def write(name,rows):
    if not rows: return
    with (ROOT/'outputs'/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def main():
    (ROOT/'outputs').mkdir(exist_ok=True)
    v=variance(read('operating_plan.csv'));write('variance.csv',v)
    cash=read('cash_plan.csv'); scenarios={}
    for name,delay in [('base',0),('collections_delay_2w',2)]:
        rows,deferred=cash_forecast(cash,2500000,750000,delay);write('cash_'+name+'.csv',rows)
        scenarios[name]={'minimum_cash':min(r['closing'] for r in rows),'peak_liquidity_gap':max(r['liquidity_gap'] for r in rows),'deferred_receipts_after_week13':deferred}
    bank,ledger=read('bank.csv'),read('ledger.csv')
    matches,exceptions=reconcile(bank,ledger);write('matches.csv',matches);write('exceptions.csv',exceptions)
    db=sqlite3.connect(':memory:')
    db.execute('CREATE TABLE operating(month TEXT,segment TEXT,budget_qty INTEGER,actual_qty INTEGER,budget_price INTEGER,actual_price INTEGER,budget_unit_cost INTEGER,actual_unit_cost INTEGER,budget_opex INTEGER,actual_opex INTEGER)')
    for r in read('operating_plan.csv'): db.execute('INSERT INTO operating VALUES(?,?,?,?,?,?,?,?,?,?)',[r['month'],r['segment']]+[int(v) for v in list(r.values())[2:]])
    cur=db.execute((ROOT/'sql'/'monthly_performance.sql').read_text());sqlrows=[dict(zip([d[0] for d in cur.description],r)) for r in cur.fetchall()];write('sql_monthly.csv',sqlrows)
    summary={'currency':'INR','data':'Synthetic demonstration only','budget_revenue':sum(r['budget_revenue'] for r in v),'actual_revenue':sum(r['actual_revenue'] for r in v),'ebitda_variance':sum(r['ebitda_variance'] for r in v),'cash_scenarios':scenarios,'matched_pairs':len(matches),'exception_rows':len(exceptions),'bank_rows':len(bank),'ledger_rows':len(ledger)}
    (ROOT/'outputs'/'summary.json').write_text(json.dumps(summary,indent=2))
    cards=''.join('<article><small>'+html.escape(k.replace('_',' ').title())+'</small><h2>'+format(summary[k],',')+'</h2></article>' for k in ('budget_revenue','actual_revenue','ebitda_variance','matched_pairs'))
    table=''.join('<tr><td>'+r['month']+'</td><td>'+format(r['actual_revenue'],',')+'</td><td>'+format(r['actual_ebitda'],',')+'</td></tr>' for r in sqlrows)
    cashcards=''.join('<article><h3>'+k.replace('_',' ')+'</h3><p>Minimum cash: ₹'+format(s['minimum_cash'],',')+'</p><p>Peak funding gap: ₹'+format(s['peak_liquidity_gap'],',')+'</p></article>' for k,s in scenarios.items())
    page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ritik | Finance Analytics</title><style>body{font:17px system-ui;background:#101c2d;color:#eef4ff;margin:0;padding:5vw}main{max-width:1100px;margin:auto}h1{font-size:clamp(32px,5vw,56px)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px}article{background:#1b2d44;padding:22px;border-radius:12px}small{color:#74dccc}table{width:100%;border-collapse:collapse}td,th{padding:14px;text-align:left;border-bottom:1px solid #38516e}p{line-height:1.7}a{color:#74dccc}</style><main><small>RITIK SRIVASTAVA / FINANCE PORTFOLIO</small><h1>From transactions to decisions.</h1><p>Synthetic case study • INR • Python + SQL • Reproducible outputs</p><div class="grid">'+cards+'</div><h2>Monthly operating performance</h2><table><tr><th>Month</th><th>Revenue ₹</th><th>EBITDA ₹</th></tr>'+table+'</table><h2>13-week liquidity stress test</h2><div class="grid">'+cashcards+'</div><h2>Control exceptions</h2><p>'+str(len(exceptions))+' source rows require review. Duplicate references are not automatically cleared. See exceptions.csv for the audit queue.</p><p>Illustrative analytics, not employer results. EBITDA excludes depreciation, interest and tax. Open the repository README for assumptions and validation.</p></main></html>'
    (ROOT/'outputs'/'dashboard.html').write_text(page)
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
