import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class AfmEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/zzz-apple-afm-nov2.json')
 def test_two_distinct_dated_events(self):
  a,b=h.project(self.p);self.assertEqual([a['kind'],b['kind']],['model_family_announcement','paper']);self.assertEqual([a['date'],b['date']],['2025-06-09','2025-07-17']);self.assertIsNone(a['raw']['timestamp_utc']);self.assertEqual(b['raw']['timestamp_utc'],'2025-07-17T23:37:19Z');self.assertEqual(b['version'],'arXiv:2507.13575v1');self.assertEqual(b['sources'],['https://arxiv.org/abs/2507.13575v1']);self.assertEqual(len(a['raw']['family_members']),2)
 def test_mutable_page_caveat_and_unknowns(self):
  a,b=self.p['events'];self.assertIn('2025-07-17 更新图表',a['note']['zh']);self.assertIn('not a June announcement snapshot',a['note']['en']);self.assertIn('不证明报告在所有渠道的最早公开时刻',b['note']['zh']);self.assertIn('paper license is not a weights license',b['note']['en'])
  for r in self.p['events']:
   self.assertIsNone(r['first_public_weights_date']);self.assertIsNone(r['pinned_api_revision']);self.assertEqual(r['execution_status'],'not_executed')
 def test_old230_exact_order_and_weights(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];base=json.loads((ROOT/'tests/fixtures/pre-afm-events-digest.json').read_text());self.assertEqual(len(rows),244);self.assertEqual([r['id'] for r in rows[:230]],base['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:230],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),base['records_sha256']);self.assertEqual(sum(r['kind'] in ['weights','weights_announcement','weights_undated'] for r in rows),97)
 def test_first_submission_rejects_borrowed_or_missing_identity(self):
  for key,val in [('first_paper_submission','2025-06-09'),('timestamp_utc',None),('timestamp_utc','2025-07-18T23:37:19Z'),('version','arXiv:2507.13575v3'),('version','arXiv:2507.13575'),('api_alias','afm'),('first_public_weights_date','2025-07-17'),('pinned_api_revision','fixed'),('execution_status','tested'),('kind','paper_revision')]:
   with self.subTest(key=key,val=val):
    p=copy.deepcopy(self.p);p['events'][1][key]=val
    with self.assertRaises(ValueError):h.validate(p)
 def test_first_submission_rejects_unpinned_or_unrelated_evidence(self):
  for url in ['https://arxiv.org/abs/2507.13575','https://arxiv.org/abs/2507.13575v3','https://example.org/report']:
   p=copy.deepcopy(self.p);p['events'][1]['evidence'][0]['url']=url
   with self.assertRaises(ValueError):h.validate(p)
 def test_paper_rejects_api_context_and_projection_is_pure(self):
  p=copy.deepcopy(self.p);p['events'][1]['context_sources']=[dict(url='https://example.org',role='api_alias',date='2025-07-17')]
  with self.assertRaises(ValueError):h.validate(p)
  before=copy.deepcopy(self.p);rows=h.project(self.p);self.assertEqual(before,self.p);self.assertTrue(all(not r['license'] and not r['nodes'] and None not in r['sources'] for r in rows))
 def test_old_snapshot_and_current_snapshot(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-02-kontext/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-afm/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],230);self.assertEqual(new['monthly']['events'],232);self.assertEqual(new['monthly']['weights_events'],97)
