import unittest,json,sys,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import monthly_releases as m
class MonthlyTests(unittest.TestCase):
 def test_real_projection_is_readonly(self):
  d=json.loads((ROOT/'dist/data.json').read_text());before=copy.deepcopy(d);p=m.project(d);self.assertEqual(d,before);rows=p['records'];self.assertTrue(rows);self.assertEqual(len(rows),len({r['id'] for r in rows}));self.assertEqual(sum(r['kind']=='weights' and bool(r['month']) for r in rows),8);self.assertEqual(sum(r['kind']=='weights_announcement' for r in rows),2)
 def test_no_date_provider_license_inference(self):
  d={'nodes':[{'id':'x','type':'model','title':'X','publication_date':'2025-01-01','checked_at':'2026-10-30'}],'sources':[],'events':[{'id':'e','event_type':'weights_release','node_ids':['x'],'date':None,'source_urls':['https://example.org/download']}]};r=m.project(d)['records'][0];self.assertIsNone(r['month']);self.assertEqual(r['providers'],['未登记']);self.assertEqual(r['license'],[])
 def test_semantic_overrides_and_year(self):
  d={'nodes':[{'id':'x','type':'model','title':'X'}],'sources':[],'events':[{'id':k,'event_type':'documentation_update','research_event_kind':k,'node_ids':['x'],'date':'2025','date_precision':'year'} for k in ['repo_first_public','weights_available_by']]};r=m.project(d)['records'];self.assertEqual([x['kind'] for x in r],['code','weights_available_by']);self.assertTrue(all(x['month'] is None for x in r))

 def test_curated_history_preserves_family_and_license_scope(self):
  package=json.loads((ROOT/'curated/monthly/history.json').read_text());before=copy.deepcopy(package);rows=m.curated_rows(package);self.assertEqual(package,before);self.assertEqual(len(rows),6);self.assertTrue(all(r['kind']=='weights_announcement' for r in rows));self.assertTrue(all(r['date_details']['first_upload'] is None for r in rows));q=next(r for r in rows if 'qwen2-' in r['id']);self.assertGreater(len(q['curated_licenses']),1);self.assertEqual(q['raw']['included_models'],next(e for e in package['events'] if 'qwen2-' in e['id'])['included_models'])
 def test_curated_rejects_weight_date_without_evidence(self):
  with self.assertRaises(AssertionError):m.curated_rows({'records':[{'id':'bad','model_name':'Bad','weights_release_date':'2026-01-02','evidence':[]}]})

 def test_calendar_and_future_dates(self):
  for date,precision in [('2026-02-30','day'),('2026-13','month'),('2026','year'),(None,'day')]:self.assertIsNone(m.event_month(date,precision,'2026-10-30'))
  self.assertIsNone(m.event_month('2026-12-01','day','2026-10-30'))
  self.assertEqual(m.event_month('2026-09','month','2026-10-30'),'2026-09')
  with self.assertRaises(AssertionError):m.curated_rows({'records':[{'id':'bad','model_name':'Bad','weights_release_date':'2026-02-30','evidence':[{'supports':['weights_release_date']}]}]})

 def test_2026_exact_records_and_missing_weight_dates(self):
  p=json.loads((ROOT/'curated/monthly/2026.json').read_text());rows=m.curated_rows(p);self.assertEqual(len(rows),10);self.assertEqual(sum(bool(r['month']) for r in rows),8);self.assertEqual(sum(r['month'] is None for r in rows),2);self.assertTrue(all('家族开放声明' in r['note'] for r in rows if 'ifm-k2' in r['id']));self.assertTrue(all(r['curated_licenses'] for r in rows));self.assertTrue(all(r['kind']==('weights_announcement' if r['date'] else 'weights_undated') for r in rows))

 def test_homepage_monthly_entry_is_visible_in_beginner_mode(self):
  self.assertIn('<a class="beginner-nav" href="monthly.html">每月模型发布</a>',(ROOT/'web/index.html').read_text())
  self.assertIn(':not(.beginner-nav)',(ROOT/'web/start.css').read_text())
