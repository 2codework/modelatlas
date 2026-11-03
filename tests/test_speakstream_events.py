"""One pinned paper event; preserved history, no inferred availability/license."""
import copy, hashlib, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class SpeakStreamEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/zzzzzz-speakstream-paper-nov2.json')
 def test_exact_identity_date_authors_scope(self):
  self.assertEqual(len(self.p['events']),1);e=self.p['events'][0]
  for k,v in {'kind':'paper','provider':'Apple','version':'arXiv:2505.19206v1','date':'2025-05-25','timestamp_utc':'2025-05-25T16:11:10Z','checked_at':'2026-11-02','modalities':['text','audio']}.items():self.assertEqual(e[k],v)
  for lang in ['zh','en']:
   for text in ['SpeakStream: Streaming Text-to-Speech with Interleaved Data','Richard He Bai','Zijin Gu','Tatiana Likhomanenko','Navdeep Jaitly','16:11:10 UTC']:self.assertIn(text,e['summary'][lang])
  self.assertIn('not a model, API or weights release',e['note']['en']);self.assertIn('not full-paper verification',e['note']['en'])
 def test_no_licenses_execution_or_weight_fields(self):
  before=copy.deepcopy(self.p);e=h.project(self.p)[0]
  self.assertEqual(e['license'],[]);self.assertEqual(e['nodes'],[]);self.assertNotIn('weight_entries',e)
  for k in ['api_alias','first_public_weights_date','pinned_api_revision']:self.assertIsNone(e['raw'][k])
  self.assertEqual(e['raw']['execution_status'],'not_executed');self.assertEqual(self.p,before)
 def test_old240_exact_prefix_and_counts(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];base=json.loads((ROOT/'tests/fixtures/pre-speakstream-events-digest.json').read_text())
  self.assertEqual(len(rows),244);self.assertEqual(base['count'],240);self.assertEqual([e['id'] for e in rows[:240]],base['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:240],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),base['records_sha256']);self.assertEqual(rows[240:241],h.project(self.p));self.assertEqual(len({e['id'] for e in rows}),244)
  weights=[e for e in rows if e['kind'] in ['weights','weights_announcement','weights_undated']];self.assertEqual(len(weights),97);self.assertEqual(sum(bool(e['month']) for e in weights),76)
  data=json.loads((ROOT/'dist/data.json').read_text());self.assertEqual(len(data['nodes']),259)
 def test_reject_inferred_or_unpinned_mutations(self):
  for k,v in [('kind','weights_release'),('first_public_weights_date','2025-05-25'),('api_alias','speakstream'),('pinned_api_revision','v1'),('execution_status','tested'),('timestamp_utc','2025-05-25T16:11:10+08:00'),('version','arXiv:2505.19206v2')]:
   with self.subTest(k=k):
    p=copy.deepcopy(self.p);p['events'][0][k]=v
    with self.assertRaises(ValueError):h.validate(p)
  for url in ['https://arxiv.org/abs/2505.19206','https://arxiv.org/abs/2505.19206v2']:
   p=copy.deepcopy(self.p);p['events'][0]['evidence'][0]['url']=url
   with self.assertRaises(ValueError):h.validate(p)
 def test_coverage_and_publication_parity(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-02-microsoft-paper/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-speakstream-paper/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],240);self.assertEqual(new['monthly']['events'],241);self.assertEqual(old['catalog'],new['catalog']);self.assertEqual(new['catalog']['records'],77);self.assertEqual(old['practice'],new['practice'])
  self.assertEqual(hashlib.sha256((ROOT/'learning/coverage/2026-11-02-speakstream-paper/snapshot.json').read_bytes()).hexdigest(), '79ae9dc8a1d0d3cc47ec4a4a4c5ce477b7160bbb2f651271c6d34b89ae5ac13a')
if __name__=='__main__':unittest.main()
