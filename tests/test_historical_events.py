import copy,hashlib,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
import monthly_releases as m

class HistoricalEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/deepseek-nov1.json')
 def test_exact_event_dates_and_types(self):
  rows=h.project(self.p);self.assertEqual([r['kind'] for r in rows],['paper_revision','api_ga_announcement','api_availability_announcement']);self.assertEqual([r['date'] for r in rows],['2025-07-18','2026-08-13','2026-08-21'])
  self.assertEqual(rows[0]['raw']['timestamp_utc'],'2025-07-18T08:20:23Z');self.assertEqual(rows[0]['raw']['first_paper_submission'],'2025-04-30')
  self.assertTrue(all(not r['license'] and not r['nodes'] and 'weight_entries' not in r for r in rows));self.assertIn('https://api-docs.deepseek.com/updates/',rows[2]['sources'])
 def test_original_222_records_preserved_and_weights_unchanged(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];old=[r for r in rows if not r.get('historical_typed')];expected=json.loads((ROOT/'tests/fixtures/pre-typed-events-digest.json').read_text())
  self.assertEqual(len(rows),244);self.assertEqual(len(old),expected['count']);self.assertEqual(hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),expected['records_sha256'])
  weights=[r for r in rows if r['kind'] in ['weights','weights_announcement','weights_undated']];self.assertEqual(len(weights),97);self.assertEqual(sum(bool(r['month']) for r in weights),76);self.assertEqual(sum(not r['month'] for r in weights),21)
 def test_projection_is_readonly_and_deterministic(self):
  before=copy.deepcopy(self.p);one=h.project(self.p);two=h.project(self.p);self.assertEqual(one,two);self.assertEqual(self.p,before)
 def test_semantic_boundary_rejections(self):
  changes=[('kind','weights_release'),('kind',[]),('date','2026-11-02'),('date','2025-02-30'),('checked_at','2026-10-31'),('first_public_weights_date','2025-07-18'),('pinned_api_revision','abc'),('execution_status','tested'),('timestamp_utc','2025-07-19T08:20:23Z'),('first_paper_submission','2025-07-18'),('api_alias','borrowed'),('modalities',['text',{}])]
  for key,value in changes:
   with self.subTest(key=key,value=value):
    p=copy.deepcopy(self.p);p['events'][0][key]=value
    with self.assertRaises(ValueError):h.validate(p)
 def test_api_paper_date_mixing_and_source_support_rejected(self):
  for key,value in [('timestamp_utc','2026-08-13T00:00:00Z'),('first_paper_submission','2026-08-13'),('api_alias',None)]:
   p=copy.deepcopy(self.p);p['events'][1][key]=value
   with self.assertRaises(ValueError):h.validate(p)
  for key,value in [('date','2026-08-16'),('kind','weights_release'),('supports',['event_date']),('url','http://example.org'),('url','https://user:pass@example.org'),('url','javascript:alert(1)'),('url','https://example.org bad')]:
   p=copy.deepcopy(self.p);p['events'][1]['evidence'][0][key]=value
   with self.assertRaises(ValueError):h.validate(p)
 def test_closed_fields_duplicate_ids_and_identities(self):
  for level in ['package','event','evidence']:
   p=copy.deepcopy(self.p);target=p if level=='package' else p['events'][0] if level=='event' else p['events'][0]['evidence'][0];target['weights_release_date']='2025-07-18'
   with self.assertRaises(ValueError):h.validate(p)
  p=copy.deepcopy(self.p);p['events'].append(copy.deepcopy(p['events'][0]))
  with self.assertRaises(ValueError):h.validate(p)
  p['events'][-1]['id']='another-id'
  with self.assertRaises(ValueError):h.validate(p)
 def test_strict_json_loader(self):
  for payload in ['{"schema":1,"schema":2}','{"x":NaN}']:
   with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'bad.json';p.write_text(payload)
    with self.assertRaises(ValueError):h.load(p)
 def test_cross_package_duplicate_and_collision_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'a.json').write_text(json.dumps(self.p));(p/'b.json').write_text(json.dumps(self.p))
   with self.assertRaises(ValueError):h.collect(p,set())
   (p/'b.json').unlink()
   with self.assertRaises(ValueError):h.collect(p,{'historical-'+self.p['events'][0]['id']})
 def test_old_snapshot_retained_and_new_snapshot_current(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-01/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-01-nonweight/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],222);self.assertEqual(new['monthly']['events'],225);self.assertEqual(new['monthly']['weights_events'],97)
