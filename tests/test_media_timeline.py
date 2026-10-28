import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import media_timeline as M
import build as B
class MediaTimelineTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'learning/media-evaluation-timeline/r1';self.p=json.loads((p/'proposal/proposal.json').read_text());self.q=json.loads((p/'qa/audit.json').read_text())
 def test_lossless_inputs(self):
  before=copy.deepcopy((self.p,self.q));b=M.adapt(self.p,self.q);self.assertEqual(before,(self.p,self.q));self.assertEqual(b['raw_proposal'],self.p);self.assertEqual(b['raw_qa'],self.q);self.assertEqual(b['nodes'],[]);self.assertEqual(b['sources'],[])
 def test_types_explicit(self):
  self.assertIn('paper_revision',B.EVENT_TYPES);self.assertIn('platform_migration',B.EVENT_TYPES)
 def test_approved_hashes(self):self.assertEqual(len(M.load(ROOT)['events']),17)
 def test_date_change_rejected(self):
  self.p['events'][0]['date']='2020-01-01'
  with self.assertRaises(ValueError):M.adapt(self.p,self.q)
 def test_timezone_upgrade_rejected(self):
  self.p['events'][0]['timezone']='UTC'
  with self.assertRaises(ValueError):M.adapt(self.p,self.q)
 def test_run_claim_rejected(self):
  self.p['events'][0]['execution_status']='passed'
  with self.assertRaises(ValueError):M.adapt(self.p,self.q)
 def test_type_conflation_rejected(self):
  self.p['events'][-1]['event_type']='benchmark_release'
  with self.assertRaises(ValueError):M.adapt(self.p,self.q)
 def test_observation_not_full_history(self):
  for e in M.adapt(self.p,self.q)['events']:
   self.assertEqual(e['checked_at'],'2026-10-28');self.assertIsNone(e['timezone'])
   if e['event_type']=='paper_revision':self.assertIn('不代表完整修订历史',e['observation_scope_zh']);self.assertIsNone(e['version'])
 def test_shared_paper_and_migration(self):
  es=M.adapt(self.p,self.q)['events'];paper=next(e for e in es if '2410-19168-v1' in e['id']);self.assertEqual(len(paper['node_ids']),2);migration=next(e for e in es if e['event_type']=='platform_migration');self.assertEqual(migration['node_ids'],['bench-mmau-v051525-test'])
 def test_actual_generated_counts_and_book(self):
  d=json.loads((ROOT/'docs/data.json').read_text());self.assertEqual(len(d['events']),166);self.assertEqual(sum(bool(e['date']) for e in d['events']),91);self.assertEqual(len(d['nodes']),230);self.assertEqual(len(d['media_evaluation_registry']),11)
  book=(ROOT/'BOOK.md').read_text()
  for e in M.adapt(self.p,self.q)['events']:
   self.assertIn(e['evidence_locator'],book);self.assertIn(e['source_urls'][0],book);self.assertIn(e['observation_scope_zh'],book)
if __name__=='__main__':unittest.main()
