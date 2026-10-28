import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import media_evaluation as M
class MediaTests(unittest.TestCase):
 def setUp(self):self.raw=json.loads((ROOT/'learning/media-evaluation/r1/raw/media-eval-research-r1.json').read_text())
 def test_typed_and_lossless(self):
  before=copy.deepcopy(self.raw);b=M.adapt(self.raw);self.assertEqual(self.raw,before);self.assertEqual(b['raw_research'],before);self.assertEqual(len(b['nodes']),11);self.assertEqual(b['media_evaluation_registry'],before['records']);self.assertEqual(b['events'],[]);self.assertEqual(b['edges'],[])
 def test_seal(self):self.assertEqual(len(M.load(ROOT)['nodes']),11)
 def test_reject_count_conflation(self):
  self.raw['records'][2]['counts_as_dataset']=True
  with self.assertRaises(ValueError):M.adapt(self.raw)
 def test_reject_execution(self):
  self.raw['records'][0]['execution_status']='passed'
  with self.assertRaises(ValueError):M.adapt(self.raw)
 def test_reject_scores(self):
  self.raw['records'][0]['results_preview']['scores']=[1]
  with self.assertRaises(ValueError):M.adapt(self.raw)
 def test_reject_url(self):
  self.raw['records'][0]['source_urls']=['javascript:alert(1)']
  with self.assertRaises(ValueError):M.adapt(self.raw)
 def test_reject_type(self):
  self.raw['records'][2]['entity_kind']='dataset'
  with self.assertRaises(ValueError):M.adapt(self.raw)
 def test_mini_limit_scope(self):
  r=next(x for x in self.raw['records'] if x['node_id'].endswith('test-mini'));self.assertIn('不属于本条1000条test-mini',r['limitations_zh'])
 def test_book_boundaries(self):
  for r in self.raw['records']:
   s='\n'.join(M.book(r));self.assertIn('never-run',s);self.assertIn(r['entity_kind'],s);self.assertIn(r['version'],s);self.assertIn('access_semantics',s);self.assertIn('license_evidence',s)
 def test_generated_registry_counts(self):
  d=json.loads((ROOT/'docs/data.json').read_text());self.assertEqual(len(d['nodes']),230);self.assertEqual(len(d['dataset_benchmark_registry']),33);self.assertEqual(len(d['media_evaluation_registry']),11)
if __name__=='__main__':unittest.main()
