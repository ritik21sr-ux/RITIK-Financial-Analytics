import sys,unittest,sqlite3,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from finance import variance,cash_forecast,reconcile
class FinanceTests(unittest.TestCase):
 def test_variance_bridge(self):
  r=dict(month='2026-01',segment='A',budget_qty=10,actual_qty=12,budget_price=100,actual_price=90,budget_unit_cost=60,actual_unit_cost=65,budget_opex=100,actual_opex=110)
  v=variance([r])[0]
  self.assertEqual(v['revenue_variance'],80)
  self.assertEqual(v['price_effect']+v['volume_effect'],80)
  self.assertEqual(v['ebitda_variance'],-110)
  self.assertEqual(sum(v[k] for k in ('contribution_volume_effect','price_effect','cost_effect','opex_effect')),-110)
 def test_cash_rollforward_and_deferred(self):
  rows=[dict(week=i,receipts=100,suppliers=70,payroll=0,overheads=0,capex=0,debt_service=0) for i in range(3)]
  result,deferred=cash_forecast(rows,50,40,1)
  self.assertEqual([r['closing'] for r in result],[-20,10,40]);self.assertEqual(deferred,100)
  self.assertEqual(result[0]['liquidity_gap'],60)
  self.assertEqual(sum(r['receipts'] for r in result)+deferred,300)
 def test_duplicate_not_matched(self):
  b=[dict(id='1',reference='x',amount=20),dict(id='2',reference='x',amount=20)]
  l=[dict(id='3',reference='X',amount=20)]
  m,e=reconcile(b,l);self.assertEqual(len(m),0);self.assertEqual(len(e),3)
 def test_normalization_and_sign(self):
  m,e=reconcile([dict(id='b',reference=' a ',amount=10)],[dict(id='l',reference='A',amount=10)])
  self.assertEqual(len(m),1);self.assertFalse(e)
  m,e=reconcile([dict(id='b',reference='A',amount=-10)],[dict(id='l',reference='A',amount=10)])
  self.assertFalse(m);self.assertEqual(len(e),2)
 def test_duplicate_id_rejected(self):
  with self.assertRaises(ValueError):reconcile([dict(id='a',reference='x',amount=1)]*2,[])
 def test_source_conservation(self):
  def read(n):
   with (ROOT/'data'/n).open() as f:return list(csv.DictReader(f))
  b,l=read('bank.csv'),read('ledger.csv');m,e=reconcile(b,l)
  self.assertEqual(len(m),95)
  for source,rows in [('bank',b),('ledger',l)]:
   ex=[r for r in e if r['source']==source]
   self.assertEqual(len(rows),len(m)+len(ex))
   self.assertEqual(sum(int(r['amount']) for r in rows),sum(r['amount'] for r in m)+sum(int(r['amount']) for r in ex))
 def test_sql_python_parity(self):
  with (ROOT/'data'/'operating_plan.csv').open() as f: rows=list(csv.DictReader(f))
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE operating('+','.join(k+(' TEXT' if k in ('month','segment') else ' INTEGER') for k in rows[0])+')')
  db.executemany('INSERT INTO operating VALUES('+','.join('?' for k in rows[0])+')',[list(r.values()) for r in rows])
  result=db.execute((ROOT/'sql'/'monthly_performance.sql').read_text()).fetchall();v=variance(rows)
  self.assertEqual(sum(r[2] for r in result),sum(r['actual_revenue'] for r in v))
  self.assertEqual(sum(r[3] for r in result),sum(r['actual_ebitda'] for r in v))
 def test_empty_and_zero(self):
  self.assertEqual(reconcile([],[]),([],[]));self.assertEqual(cash_forecast([],0,0),([],0));self.assertEqual(variance([]),[])
if __name__=='__main__':unittest.main()
