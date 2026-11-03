"""Pinned Nile-Chat paper: one event, no release or licensing inference."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class NileChatEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/zzzzzzz-nile-chat-paper-nov2.json')
 def test_identity_date_and_scope(self):
  self.assertEqual(len(self.p['events']),1);e=self.p['events'][0]
  for k,v in {'kind':'paper','provider':'MBZUAI Institute of Foundation Models (IFM)','version':'arXiv:2507.04569v1','date':'2025-07-06','timestamp_utc':'2025-07-06T22:53:41Z','checked_at':'2026-11-02','modalities':['text']}.items():self.assertEqual(e[k],v)
  for lang in ['zh','en']:
   for text in ['Nile-Chat: Egyptian Language Models for Arabic and Latin Scripts','Guokan Shang','Hadi Abdine','Ahmad Chamma','Amr Mohamed','Mohamed Anwar','Abdelaziz Bounhar','Omar El Herraoui','Preslav Nakov','Michalis Vazirgiannis','Eric Xing','22:53:41 UTC','3x4B-A6B','Arabizi']:self.assertIn(text,e['summary'][lang])
   for text in ['2505.18383','3B','MBZUAI-Paris','MBZUAI-IFM Paris Lab']:self.assertIn(text,e['note'][lang])
  self.assertIn('not a model, API or weights release',e['note']['en']);self.assertIn('commits do not prove',e['note']['en'])
 def test_exact_old241_prefix_and_counts(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];base=json.loads((ROOT/'tests/fixtures/pre-nile-chat-events-digest.json').read_text());self.assertEqual(len(rows),244);self.assertEqual(base['count'],241);self.assertEqual([e['id'] for e in rows[:241]],base['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:241],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),base['records_sha256']);self.assertEqual(rows[241:242],h.project(self.p));self.assertEqual(len({e['id'] for e in rows}),244)
  weights=[e for e in rows if e['kind'] in ['weights','weights_announcement','weights_undated']];self.assertEqual(len(weights),97);self.assertEqual(sum(bool(e['month']) for e in weights),76);self.assertEqual(len(json.loads((ROOT/'dist/data.json').read_text())['nodes']),259)
 def test_no_release_license_execution_inference(self):
  before=copy.deepcopy(self.p);e=h.project(self.p)[0];self.assertEqual(e['license'],[]);self.assertEqual(e['nodes'],[]);self.assertEqual(e['sources'],['https://arxiv.org/abs/2507.04569v1']);self.assertNotIn('weight_entries',e)
  for k in ['api_alias','first_public_weights_date','pinned_api_revision']:self.assertIsNone(e['raw'][k])
  self.assertEqual(e['raw']['execution_status'],'not_executed');self.assertEqual(self.p,before)
 def test_reject_borrowed_dates_release_and_unpinned_sources(self):
  for k,v in [('kind','weights_release'),('first_public_weights_date','2025-05-29'),('date','2025-05-23'),('api_alias','nile-chat'),('pinned_api_revision','v1'),('execution_status','tested'),('timestamp_utc','2025-07-06T22:53:41+08:00'),('version','arXiv:2505.18383v1')]:
   with self.subTest(k=k):
    p=copy.deepcopy(self.p);p['events'][0][k]=v
    with self.assertRaises(ValueError):h.validate(p)
  for url in ['https://arxiv.org/abs/2507.04569','https://arxiv.org/abs/2505.18383v1']:
   p=copy.deepcopy(self.p);p['events'][0]['evidence'][0]['url']=url
   with self.assertRaises(ValueError):h.validate(p)
 def test_coverage_current_artifacts_and_historical_scope(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-02-speakstream-paper/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-nile-chat-paper/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],241);self.assertEqual(new['monthly']['events'],242);self.assertEqual(old['catalog'],new['catalog']);self.assertEqual(new['catalog']['records'],77);self.assertEqual(old['practice'],new['practice'])
  self.assertEqual(hashlib.sha256((ROOT/'learning/coverage/2026-11-02-nile-chat-paper/snapshot.json').read_bytes()).hexdigest(), '57a018658c401ad94218a55aecf32b7ec5cd10f9e9ec169ec7284c60f54e6d13')
if __name__=='__main__':unittest.main()
