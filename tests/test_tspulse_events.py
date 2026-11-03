import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class TspulseEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/zzzz-tspulse-nov2.json')
 def test_exact_pinned_identity_dates_and_modality(self):
  a,b=h.project(self.p);self.assertEqual([a['kind'],b['kind']],['paper','paper_revision'])
  for i,r in enumerate([a,b],1):
   self.assertEqual(r['version'],f'arXiv:2505.13033v{i}');self.assertEqual(r['sources'],[f'https://arxiv.org/abs/2505.13033v{i}']);self.assertEqual(r['providers'],['IBM']);self.assertEqual(r['modalities'],['time_series']);self.assertIn('TSPulse: Dual Space Tiny Pre-Trained Models for Rapid Time-Series Analysis',r['summary']);self.assertEqual(r['raw']['first_paper_submission'],'2025-05-19')
  self.assertEqual([a['raw']['timestamp_utc'],b['raw']['timestamp_utc']],['2025-05-19T12:18:53Z','2025-06-25T04:59:41Z']);self.assertEqual([a['date'],b['date']],['2025-05-19','2025-06-25'])
 def test_evidence_limits_unknowns_and_pure_projection(self):
  before=copy.deepcopy(self.p);rows=h.project(self.p);self.assertEqual(before,self.p);self.assertIn('之后开放',rows[0]['note']);self.assertIn('不证明首次完整公开权重',rows[1]['note'])
  for r in rows:
   self.assertFalse(r['license']);self.assertFalse(r['nodes']);self.assertFalse(r['raw']['context_sources']);self.assertIsNone(r['raw']['first_public_weights_date']);self.assertIsNone(r['raw']['pinned_api_revision']);self.assertEqual(r['raw']['execution_status'],'not_executed');self.assertIn('不能回填历史权重许可',r['note']);self.assertIn('not two models',r['raw']['note']['en'])
 def test_original232_exact_order_and_default97(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];base=json.loads((ROOT/'tests/fixtures/pre-tspulse-events-digest.json').read_text());self.assertEqual(len(rows),244);self.assertEqual([r['id'] for r in rows[:232]],base['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:232],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),base['records_sha256']);self.assertEqual(sum(r['kind'] in ['weights','weights_announcement','weights_undated'] for r in rows),97)
 def test_rejects_weights_execution_wrong_modality_or_borrowed_dates(self):
  for index in [0,1]:
   for key,val in [('first_public_weights_date','2025-06-25'),('pinned_api_revision','tspulse'),('api_alias','tspulse'),('execution_status','tested'),('modalities',['forecasting']),('timestamp_utc','2025-01-01T00:00:00Z'),('first_paper_submission','2025-06-25')]:
    with self.subTest(index=index,key=key):
     p=copy.deepcopy(self.p);p['events'][index][key]=val
     with self.assertRaises(ValueError):h.validate(p)
 def test_first_submission_rejects_unpinned_or_wrong_version(self):
  for url in ['https://arxiv.org/abs/2505.13033','https://arxiv.org/abs/2505.13033v2']:
   p=copy.deepcopy(self.p);p['events'][0]['evidence'][0]['url']=url
   with self.assertRaises(ValueError):h.validate(p)
 def test_scoped_snapshots_preserved(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-02-afm/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-tspulse/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],232);self.assertEqual(new['monthly']['events'],234);self.assertEqual(new['monthly']['weights_events'],97)
