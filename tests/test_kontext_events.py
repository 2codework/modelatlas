import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class KontextEvents(unittest.TestCase):
 def setUp(self): self.p=h.load(ROOT/'curated/historical-events/zz-kontext-nov2.json')
 def test_exact_family_and_revision(self):
  a,b=h.project(self.p);self.assertEqual([a['kind'],b['kind']],['model_family_announcement','paper_revision']);self.assertEqual([a['date'],b['date']],['2025-05-29','2025-06-24']);self.assertEqual(b['raw']['timestamp_utc'],'2025-06-24T05:31:03Z');self.assertEqual(b['raw']['first_paper_submission'],'2025-06-17');self.assertIsNone(a['raw']['timestamp_utc']);self.assertEqual(a['sources'],['https://bfl.ai/blog/flux-1-kontext']);self.assertEqual(b['sources'],['https://arxiv.org/abs/2506.15742v2']);self.assertEqual([m['name'] for m in a['raw']['family_members']],['FLUX.1 Kontext [pro]','FLUX.1 Kontext [max]','FLUX.1 Kontext [dev]']);self.assertTrue(all(m['url'] is None for m in a['raw']['family_members']));self.assertIn('dev 当时仅为 private beta',a['summary']);self.assertIn('不代表报告整体最早公开',b['note']);self.assertIn('本轮未核实该链接的最早出现时间',b['note']);self.assertIn('its first link appearance was not verified',b['raw']['note']['en'])
 def test_original_228_exact_semantics_order_and_weights(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];b=json.loads((ROOT/'tests/fixtures/pre-kontext-events-digest.json').read_text());self.assertEqual(len(rows),244);self.assertEqual([r['id'] for r in rows[:228]],b['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:228],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),b['records_sha256']);self.assertEqual(sum(r['kind'] in ['weights','weights_announcement','weights_undated'] for r in rows),97)
 def test_named_members_require_valid_source_unique_name(self):
  for key,value in [('source_url',None),('source_url','https://other.example'),('url',''),('url',False),('url','javascript:alert(1)'),('name','FLUX.1 Kontext [max]')]:
   with self.subTest(key=key,value=value):
    p=copy.deepcopy(self.p);p['events'][0]['family_members'][0][key]=value
    with self.assertRaises(ValueError):h.validate(p)
  p=copy.deepcopy(self.p);del p['events'][0]['family_members'][0]['source_url']
  with self.assertRaises(ValueError):h.validate(p)
 def test_no_borrowed_weights_time_or_execution(self):
  for i in [0,1]:
   for key,val in [('first_public_weights_date','2025-05-29'),('pinned_api_revision','pinned'),('execution_status','tested'),('kind','weights')]:
    p=copy.deepcopy(self.p);p['events'][i][key]=val
    with self.assertRaises(ValueError):h.validate(p)
  p=copy.deepcopy(self.p);p['events'][0]['timestamp_utc']='2025-05-29T00:00:00Z'
  with self.assertRaises(ValueError):h.validate(p)
 def test_projection_unchanged_and_null_not_in_sources(self):
  old=copy.deepcopy(self.p);rows=h.project(self.p);self.assertEqual(old,self.p);self.assertTrue(all(None not in r['sources'] and not r['license'] and not r['nodes'] for r in rows))
 def test_snapshot_preservation_and_current_count(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-01-ltx-api/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-kontext/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],228);self.assertEqual(new['monthly']['events'],230);self.assertEqual(new['monthly']['weights_events'],97);self.assertEqual(new['checked_on'],'2026-11-02')
