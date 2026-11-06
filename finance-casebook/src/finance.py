"""Finance portfolio engines. Amounts are integer INR; no external dependencies."""
from collections import Counter

def variance(rows):
    """Exact revenue bridge; positive EBITDA variance is favourable."""
    result=[]
    for r in rows:
        bq,aq,bp,ap,bc,ac,bo,ao=(int(r[k]) for k in ('budget_qty','actual_qty','budget_price','actual_price','budget_unit_cost','actual_unit_cost','budget_opex','actual_opex'))
        if min(bq,aq,bp,ap,bc,ac,bo,ao)<0: raise ValueError('Negative operating inputs')
        budget=bq*bp; actual=aq*ap
        be=bq*(bp-bc)-bo; ae=aq*(ap-ac)-ao
        result.append(dict(month=r['month'],segment=r['segment'],budget_revenue=budget,actual_revenue=actual,revenue_variance=actual-budget,volume_effect=(aq-bq)*bp,price_effect=aq*(ap-bp),budget_ebitda=be,actual_ebitda=ae,ebitda_variance=ae-be,cost_effect=-aq*(ac-bc),opex_effect=bo-ao,contribution_volume_effect=(aq-bq)*(bp-bc)))
    return result

def cash_forecast(rows, opening, floor, delay_weeks=0):
    """Shift receipts, never delete delayed receipts. No automatic borrowing."""
    if delay_weeks<0 or int(delay_weeks)!=delay_weeks: raise ValueError('Invalid delay')
    balance=opening; out=[]; deferred=0
    for i,r in enumerate(rows):
        receipts=int(rows[i-delay_weeks]['receipts']) if i>=delay_weeks else 0
        payments=sum(int(r[k]) for k in ('suppliers','payroll','overheads','capex','debt_service'))
        closing=balance+receipts-payments
        out.append(dict(week=r['week'],opening=balance,receipts=receipts,payments=payments,closing=closing,liquidity_gap=max(0,floor-closing)))
        balance=closing
    if delay_weeks: deferred=sum(int(r['receipts']) for r in rows[max(0,len(rows)-delay_weeks):])
    return out,deferred

def reconcile(bank,ledger):
    """Conservative one-to-one match: normalized reference + signed amount.
    Ambiguous duplicates are exceptions, never auto-cleared.
    """
    def key(r): return (r['reference'].strip().upper(),int(r['amount']))
    for rows in (bank,ledger):
        ids=[r['id'] for r in rows]
        if len(ids)!=len(set(ids)): raise ValueError('Duplicate source IDs')
    bc=Counter(map(key,bank));lc=Counter(map(key,ledger))
    lookup={key(r):r for r in ledger};matches=[];exceptions=[];used=set()
    for r in bank:
        k=key(r)
        if k[0] and bc[k]==lc[k]==1:
            l=lookup[k];used.add(l['id']);matches.append(dict(bank_id=r['id'],ledger_id=l['id'],reference=k[0],amount=k[1]))
        else:
            reason='ambiguous_duplicate' if bc[k]>1 or lc[k]>1 else 'unmatched_or_amount_difference'
            exceptions.append(dict(source='bank',**r,reason=reason))
    for r in ledger:
        if r['id'] not in used: exceptions.append(dict(source='ledger',**r,reason='review_required'))
    return matches,exceptions
