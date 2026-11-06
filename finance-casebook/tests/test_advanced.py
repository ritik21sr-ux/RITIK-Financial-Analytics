import unittest,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from advanced import *
class AdvancedTests(unittest.TestCase):
 def test_age_boundaries(self):
  rows=[dict(id=str(i),amount=100,paid=20,due=d) for i,d in enumerate(['2026-11-06','2026-10-07','2026-10-06','2026-09-07','2026-09-06','2026-08-08','2026-08-07'])]
  a=aging(rows,'2026-11-06');self.assertEqual([r['bucket'] for r in a],['Current','1-30','31-60','31-60','61-90','61-90','90+']);self.assertEqual(sum(r['outstanding'] for r in a),560)
 def test_inventory_lower_value(self):
  a=inventory([dict(sku='x',units=10,cost=20,nrv=15,annual_units=100)])
  self.assertEqual(a[0]['write_down'],50);self.assertEqual(a[0]['carrying_value'],150)
 def test_saas_excludes_new_from_retention(self):
  a=saas([dict(opening=100,new=50,expansion=10,contraction=5,churn=15)])[0]
  self.assertEqual(a['ending_mrr'],140);self.assertAlmostEqual(a['nrr'],.9);self.assertAlmostEqual(a['grr'],.8)
 def test_capex_time_zero(self):
  self.assertAlmostEqual(npv(.1,[-100,110]),0);self.assertEqual(capex([-100,40,40,40],.1)['undiscounted_payback_years'],2.5)
 def test_no_payback(self):self.assertIsNone(capex([-100,10],.1)['undiscounted_payback_years'])
 def test_forecast_no_future_leakage(self):
  a=backtest([10,20,30,100],3);self.assertEqual(a['rows'][0]['forecast'],20);self.assertEqual(a['mae'],80)
 def test_forecast_zero_denominator(self):self.assertIsNone(backtest([0,0,0,0],3)['wape'])
 def test_journal_control(self):
  rows=[dict(journal='J',debit=10,credit=0,date='2026-11-01',preparer='A',approver='A')]
  self.assertEqual(set(journal_controls(rows)[0]['reasons']),{'unbalanced','approval_conflict','weekend_review'})
 def test_statements_balance_and_cash(self):
  a=json.loads((ROOT/'data'/'10_three_statements.json').read_text());s=statements(a)
  self.assertAlmostEqual(s['balance_check'],0,places=7)
  self.assertAlmostEqual(s['closing_cash'],a['opening_cash']+s['cfo']-a['capex']-a['repayment']-a['dividends'])
  self.assertAlmostEqual(s['net_income'],1875000)
 def test_dso_sensitivity(self):
  a=json.loads((ROOT/'data'/'10_three_statements.json').read_text());base=statements(a);a['dso']+=10;stress=statements(a)
  self.assertAlmostEqual(base['closing_cash']-stress['closing_cash'],a['revenue']*10/365);self.assertAlmostEqual(stress['balance_check'],0,places=7)
