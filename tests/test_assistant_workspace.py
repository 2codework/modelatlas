from audio_contract import legacy_view
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import assistant_workspace as A
class AssistantTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'learning/assistant-workspace/r1/raw';self.r=json.loads((p/'research.json').read_text());self.s=json.loads((p/'sources.json').read_text())
 def test_cardinality_preservation(self):
  old=copy.deepcopy((self.r,self.s));b=A.adapt(self.r,self.s);self.assertEqual(old,(self.r,self.s));self.assertEqual((len(b['nodes']),len(b['sources']),len(b['cases']),len(b['events'])),(8,16,8,0));self.assertEqual(b['raw_research'],self.r)
 def test_source_seals(self):self.assertEqual(len(A.load(ROOT)['nodes']),8)
 def test_visible_boundaries_no_office_count_conflation(self):
  for n in A.adapt(self.r,self.s)['nodes']:
   self.assertNotIn('office_agent',n);self.assertNotIn('tutorial_markdown',n);self.assertFalse(n['is_model']);self.assertTrue(n['assistant_workspace']['permission_boundary']);self.assertIn('never-run',n['description_zh']);self.assertTrue(any(t.startswith('未知：') for t in n['misconceptions']));self.assertEqual(n['lifecycle'],'unknown')
 def test_reject_execution(self):
  self.r['items'][0]['execution']['model_called']=True
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_retirement(self):
  self.r['items'][0]['dates']['retirement']='2026-10-28'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_normalized_date(self):
  self.r['items'][5]['dates']['normalized_date']='2026-08-04'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_source_date(self):
  next(s for s in self.s if s['id']=='p-feb-change')['event_date']='2026-02-05'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_upgrade_failed_source(self):
  next(s for s in self.s if s['id']=='p-labs')['evidence_status']='verified'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_missing_source(self):
  self.r['items'][0]['source_ids']=['missing']
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_unsafe_source(self):
  self.s[0]['url']='https://u:p@example.org'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_derived_book_links_and_counts(self):
  d=legacy_view(json.loads((ROOT/'docs/data.json').read_text()));self.assertEqual((len(d['nodes']),len(d['events']),len(d['media_evaluation_registry']),len(d['dataset_benchmark_registry']),len(d['vendor_catalog']['records'])),(242,166,11,33,77));self.assertEqual(len([n for n in d['nodes'] if 'office_agent' in n]),11)
  for n in [n for n in d['nodes'] if n['id'] in A.EXPECTED]:
   self.assertEqual(n['agentwork_links'][0]['id'],'assistant-case-'+n['id'].removeprefix('assistant-'));self.assertIn(n['title'],(ROOT/'BOOK.md').read_text());self.assertEqual(n['assistant_workspace']['execution_status'],'never-run')
if __name__=='__main__':unittest.main()
