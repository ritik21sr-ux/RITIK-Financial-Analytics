"""Seven small, auditable finance case engines; synthetic examples only."""
from datetime import date
from collections import defaultdict

def aging(invoices,as_of):
    out=[]
    for r in invoices:
        outstanding=r['amount']-r['paid']
        if outstanding<0: raise ValueError('Overpayment requires separate credit handling')
        days=(date.fromisoformat(as_of)-date.fromisoformat(r['due'])).days
        bucket='Current' if days<=0 else '1-30' if days<=30 else '31-60' if days<=60 else '61-90' if days<=90 else '90+'
        out.append(dict(id=r['id'],outstanding=outstanding,days_overdue=max(0,days),bucket=bucket))
    return out

def inventory(items):
    if any(r['units']<0 or min(r['cost'],r['nrv'])<0 for r in items): raise ValueError('Invalid inventory input')
    ranked=sorted(items,key=lambda r:r['annual_units']*r['cost'],reverse=True)
    total=sum(r['annual_units']*r['cost'] for r in ranked);running=0;out=[]
    for r in ranked:
        share=running/total if total else 0
        cls='A' if share<.8 else 'B' if share<.95 else 'C'
        running+=r['annual_units']*r['cost']
        out.append(dict(sku=r['sku'],abc=cls,carrying_value=r['units']*min(r['cost'],r['nrv']),write_down=r['units']*max(0,r['cost']-r['nrv']),annual_usage_value=r['annual_units']*r['cost']))
    return out

def saas(rows):
    out=[]
    for r in rows:
        end=r['opening']+r['new']+r['expansion']-r['contraction']-r['churn']
        if min(r.values())<0 or end<0: raise ValueError('Invalid MRR bridge')
        out.append(dict(ending_mrr=end,arr_run_rate=end*12,nrr=(r['opening']+r['expansion']-r['contraction']-r['churn'])/r['opening'] if r['opening'] else None,grr=(r['opening']-r['contraction']-r['churn'])/r['opening'] if r['opening'] else None))
    return out

def npv(rate,flows):
    if rate<=-1: raise ValueError('Rate must exceed -100%')
    return sum(c/(1+rate)**t for t,c in enumerate(flows))

def capex(flows,rate):
    cumulative=flows[0];payback=0 if cumulative>=0 else None
    for t,c in enumerate(flows[1:],1):
        previous=cumulative;cumulative+=c
        if payback is None and previous<0<=cumulative and c>0:payback=t-1+(-previous/c)
    return dict(npv=npv(rate,flows),undiscounted_payback_years=payback,discount_rate=rate)

def backtest(actuals,window=3):
    if window<1 or window>=len(actuals):raise ValueError('Insufficient history')
    rows=[]
    for t in range(window,len(actuals)):
        prediction=sum(actuals[t-window:t])/window
        rows.append(dict(period=t+1,actual=actuals[t],forecast=prediction,error=actuals[t]-prediction))
    denom=sum(abs(r['actual']) for r in rows)
    return dict(rows=rows,mae=sum(abs(r['error']) for r in rows)/len(rows),wape=sum(abs(r['error']) for r in rows)/denom if denom else None,bias=sum(r['error'] for r in rows)/len(rows))

def journal_controls(lines):
    groups=defaultdict(list)
    for r in lines:groups[r['journal']].append(r)
    exceptions=[]
    for jid,rs in groups.items():
        reasons=[]
        if sum(r['debit']-r['credit'] for r in rs)!=0:reasons.append('unbalanced')
        if any(min(r['debit'],r['credit'])<0 or (r['debit']>0 and r['credit']>0) for r in rs):reasons.append('invalid_line')
        if any(r['preparer']==r['approver'] or not r['approver'] for r in rs):reasons.append('approval_conflict')
        if any(date.fromisoformat(r['date']).weekday()>=5 for r in rs):reasons.append('weekend_review')
        if reasons:exceptions.append(dict(journal=jid,reasons=reasons))
    return exceptions

def statements(a):
    """Single-year simplified accrual model, fixed working-capital assumptions."""
    revenue=a['revenue'];cogs=revenue*a['cogs_pct'];depreciation=a['depreciation']
    ebit=revenue-cogs-a['opex']-depreciation
    interest=a['opening_debt']*a['interest_rate'];tax=max(0,ebit-interest)*a['tax_rate'];net=ebit-interest-tax
    ar=revenue*a['dso']/365;inv=cogs*a['dio']/365;ap=cogs*a['dpo']/365
    cfo=net+depreciation-(ar-a['opening_ar'])-(inv-a['opening_inventory'])+(ap-a['opening_ap'])
    cash=a['opening_cash']+cfo-a['capex']+a['new_debt']-a['repayment']-a['dividends']
    ppe=a['opening_ppe']+a['capex']-depreciation;debt=a['opening_debt']+a['new_debt']-a['repayment']
    opening_equity=a['opening_cash']+a['opening_ar']+a['opening_inventory']+a['opening_ppe']-a['opening_ap']-a['opening_debt']
    equity=opening_equity+net-a['dividends']
    return dict(revenue=revenue,cogs=cogs,ebit=ebit,interest=interest,tax=tax,net_income=net,cfo=cfo,closing_cash=cash,closing_ar=ar,closing_inventory=inv,closing_ap=ap,closing_ppe=ppe,closing_debt=debt,closing_equity=equity,balance_check=cash+ar+inv+ppe-ap-debt-equity)
