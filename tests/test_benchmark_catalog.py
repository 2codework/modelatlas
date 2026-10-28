import copy,hashlib,json,sys,tempfile,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import benchmark_catalog as B
class Benchmarks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.bundle=B.load(ROOT);cls.data=json.loads((ROOT/'dist/data.json').read_text());cls.rows={r['node_id']:r for r in cls.bundle['dataset_benchmark_registry']}
 def test_counts_preserve_baseline(self):
  self.assertEqual(len(self.rows),22);self.assertEqual(len({r['family'] for r in self.rows.values()}),15)
  self.assertEqual(len(self.data['dataset_benchmark_registry']),33);self.assertEqual(len(self.data['evaluation_snapshots']),3)
  systems=json.loads((ROOT/'data/research/systems.json').read_text())
  for r in systems['dataset_benchmark_registry']:self.assertEqual(r,next(x for x in self.data['dataset_benchmark_registry'] if x['node_id']==r['node_id']))
  self.assertEqual(self.data['evaluation_snapshots'],json.loads((ROOT/'data/research/evaluation-snapshots.json').read_text())['snapshots'])
 def test_raw_lossless_hashgate(self):
  for name,digest in json.loads((ROOT/'data/benchmarks/admission.json').read_text())['sha256'].items():
   raw=(ROOT/'data/benchmarks'/name).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),digest)
   for site in ['dist','docs']:self.assertEqual(raw,(ROOT/site/'benchmarks'/name).read_bytes())
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);shutil.copytree(ROOT/'data/benchmarks',root/'data/benchmarks');(root/'data/benchmarks/overlay.json').write_text('{}')
   with self.assertRaisesRegex(ValueError,'hash mismatch'):B.load(root)
 def test_access_corrections(self):
  doc=self.rows['bench-docvqa-2020-task1'];self.assertEqual(doc['access_semantics']['requires_account'],'unknown');self.assertFalse(doc['access_semantics']['download_terms_verified']);self.assertNotEqual(doc['availability'],'public_download')
  self.assertFalse(self.rows['bench-mathvista-test']['access_semantics']['full_local_scoring_access'])
  self.assertFalse(self.rows['bench-gaia']['access_semantics']['crawlable_redistribution_allowed'])
  for nid in ['bench-workarena-l1','bench-workarena-plusplus']:self.assertEqual(self.rows[nid]['access_semantics']['runtime_instance_access'],'gated_approval')
  self.assertFalse(self.rows['bench-ocrbench-v2']['access_semantics']['commercial_use_allowed'])
  self.assertTrue(all(r['availability']!='public_download' for r in self.rows.values()))
 def test_relationships_dates_scores(self):
  self.assertEqual(len(self.bundle['edges']),8)
  for e in self.bundle['edges']:self.assertIn(e['source'],self.rows);self.assertIn(e['target'],self.rows);self.assertFalse(e['score_comparable'])
  self.assertEqual(self.bundle['events'],[])
  self.assertTrue(all(not r['results_preview']['scores'] for r in self.rows.values()))
  self.assertNotEqual(self.rows['bench-mathvista-test']['split'],self.rows['bench-mathvista-testmini']['split'])
 def test_readable_and_provenanced(self):
  sources={s['id'] for s in self.data['sources']};book=(ROOT/'BOOK.md').read_text()
  for n in self.bundle['nodes']:
   self.assertTrue(n['source_ids']);self.assertTrue(set(n['source_ids'])<=sources)
   self.assertIn(n['description_zh'],book);self.assertIn(n['availability'],book)
   self.assertIn(n['version'],n['tags']);self.assertEqual(n['type'],'benchmark')

 def test_lifecycle_explicit_source_mapping(self):
  nodes={n['id']:n for n in self.bundle['nodes']}
  self.assertEqual(nodes['bench-ruler-v1-legacy']['lifecycle']['status'],'deprecated')
  for raw in self.bundle['raw_benchmark_metadata']['records']:
   self.assertEqual(nodes[raw['node_id']]['lifecycle']['status'],B.LIFECYCLE_STATUS[raw['lifecycle']['status']])
  self.assertEqual(B.lifecycle_status({'node_id':'invented-original-legacy-1-0','lifecycle':{'status':'documented'}}),'unknown')
  self.assertEqual(B.lifecycle_status({'node_id':'new-name','lifecycle':{'status':'historical_variant'}}),'historical')
  with self.assertRaisesRegex(ValueError,'unsupported benchmark lifecycle'):B.lifecycle_status({'lifecycle':{'status':'guessed'}})
