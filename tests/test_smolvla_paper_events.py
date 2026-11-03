"""Pinned SmolVLA paper: one event, no release or licensing inference."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class SmolVLAPaperEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/zzzzzzzz-smolvla-paper-nov2.json')
 def test_identity_date_and_scope(self):
  self.assertEqual(len(self.p['events']),1);e=self.p['events'][0]
  for k,v in {'kind':'paper','provider':'Hugging Face','version':'arXiv:2506.01844v1','date':'2025-06-02','timestamp_utc':'2025-06-02T16:30:19Z','checked_at':'2026-11-02','modalities':['image','text']}.items():self.assertEqual(e[k],v)
  for lang in ['zh','en']:
   for text in ['SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics','Mustafa Shukor','Dana Aubakirova','Francesco Capuano','Pepijn Kooijmans','Steven Palma','Adil Zouitine','Michel Aractingi','Caroline Pascal','Martino Russi','Andres Marafioti','Simon Alibert','Matthieu Cord','Thomas Wolf','Remi Cadene','16:30:19 UTC']:self.assertIn(text,e['summary'][lang])
   for text in ['2025-06-03','2025-06-02','Hugging Face','Sorbonne University','valeo.ai','École Normale Supérieure Paris-Saclay']:self.assertIn(text,e['note'][lang])
  self.assertIn('not a general office agent',e['summary']['en']);self.assertIn('robot sensorimotor state',e['summary']['en']);self.assertIn('not a model, API or weights release',e['note']['en']);self.assertIn('historical weights and code licenses',e['note']['en'])
 def test_exact_old242_prefix_and_counts(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];base=json.loads((ROOT/'tests/fixtures/pre-smolvla-paper-events-digest.json').read_text());self.assertEqual(len(rows),244);self.assertEqual(base['count'],242);self.assertEqual([e['id'] for e in rows[:242]],base['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:242],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),base['records_sha256']);self.assertEqual(rows[242:243],h.project(self.p));self.assertEqual(len({e['id'] for e in rows}),244)
  weights=[e for e in rows if e['kind'] in ['weights','weights_announcement','weights_undated']];self.assertEqual(len(weights),97);self.assertEqual(sum(bool(e['month']) for e in weights),76);self.assertEqual(len(json.loads((ROOT/'dist/data.json').read_text())['nodes']),259)
 def test_no_release_license_execution_inference(self):
  before=copy.deepcopy(self.p);e=h.project(self.p)[0];self.assertEqual(e['license'],[]);self.assertEqual(e['nodes'],[]);self.assertEqual(e['sources'],['https://arxiv.org/abs/2506.01844v1']);self.assertNotIn('weight_entries',e)
  for k in ['api_alias','first_public_weights_date','pinned_api_revision']:self.assertIsNone(e['raw'][k])
  self.assertEqual(e['raw']['execution_status'],'not_executed');self.assertEqual(self.p,before)
 def test_reject_borrowed_dates_release_and_unpinned_sources(self):
  for k,v in [('kind','weights_release'),('first_public_weights_date','2025-05-29'),('date','2025-06-03'),('api_alias','smolvla'),('pinned_api_revision','v1'),('execution_status','tested'),('timestamp_utc','2025-06-02T16:30:19+08:00'),('version','arXiv:2505.18383v1')]:
   with self.subTest(k=k):
    p=copy.deepcopy(self.p);p['events'][0][k]=v
    with self.assertRaises(ValueError):h.validate(p)
  for url in ['https://arxiv.org/abs/2506.01844','https://arxiv.org/abs/2505.18383v1']:
   p=copy.deepcopy(self.p);p['events'][0]['evidence'][0]['url']=url
   with self.assertRaises(ValueError):h.validate(p)
 def test_coverage_current_artifacts_and_historical_scope(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-02-nile-chat-paper/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-smolvla-paper/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],242);self.assertEqual(new['monthly']['events'],243);self.assertEqual(old['catalog'],new['catalog']);self.assertEqual(new['catalog']['records'],77);self.assertEqual(old['practice'],new['practice'])
  self.assertEqual(next(v['sha256'] for v in new['provenance'] if v['path'].endswith('dist/monthly-releases.json')),'b43ecf96835a99d444e0146c12b9d5b2f1b20b4879fd5f8ca782b85d7a824a86')
if __name__=='__main__':unittest.main()
