import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build',ROOT/'scripts/build.py');B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
class Integrity(unittest.TestCase):
 def setUp(self): self.bs=sorted([json.loads(p.read_text()) for p in sorted((ROOT/'data/research').glob('*.json'))],key=lambda b:'nodes' not in b)
 def test_complete_and_lossless(self):
  old=copy.deepcopy(self.bs);d=B.normalize(self.bs)
  self.assertGreaterEqual(len(d['nodes']),100);self.assertEqual(self.bs,old);self.assertEqual(d['research_bundles'],old)
 def test_duplicate_ids(self):
  self.bs[0]['nodes'].append(copy.deepcopy(self.bs[0]['nodes'][0]))
  with self.assertRaisesRegex(ValueError,'duplicate'): B.normalize(self.bs)
 def test_dangling_edge(self):
  self.bs[0]['edges'][0]['target']='missing'
  with self.assertRaisesRegex(ValueError,'dangling'): B.normalize(self.bs)
 def test_missing_source(self):
  self.bs[0]['nodes'][0]['source_ids']=['missing']
  with self.assertRaisesRegex(ValueError,'missing source'): B.normalize(self.bs)
 def test_dated_requires_source(self):
  e=next(b for b in self.bs if b.get('events'))['events'][0];e['source_ids']=[];e['source_urls']=[]
  with self.assertRaisesRegex(ValueError,'without source'): B.normalize(self.bs)
 def test_invalid_date(self):
  next(b for b in self.bs if b.get('events'))['events'][0]['date']='2025-02-30'
  with self.assertRaisesRegex(ValueError,'invalid date'): B.normalize(self.bs)
 def test_unknown_does_not_invent_date(self):
  d=B.normalize(self.bs);unknown=[e for e in d['events'] if e['date'] is None]
  self.assertGreater(len(unknown),0);self.assertTrue(all(e.get('date_precision') in (None,'unknown') for e in unknown))
 def test_claim_without_evidence(self):
  n=self.bs[0]['nodes'][0];n['source_ids']=[];n['source_urls']=[]
  with self.assertRaisesRegex(ValueError,'without evidence'): B.normalize(self.bs)
 def test_url_protocols(self):
  for u in ['javascript:alert(1)','data:text/html,test','file:///tmp/x','https://user:pass@example.org','https://example.org/ a']:self.assertFalse(B.url_ok(u))
  self.assertTrue(B.url_ok('https://example.org/a'))
 def test_unsafe_source_rejected(self):
  self.bs[0]['sources'][0]['url']='javascript:alert(1)'
  with self.assertRaisesRegex(ValueError,'unsafe'): B.normalize(self.bs)
 def test_bad_prerequisite(self):
  self.bs[0]['nodes'][0]['prerequisites']=['missing']
  with self.assertRaisesRegex(ValueError,'prerequisite'): B.normalize(self.bs)
 def test_precision(self):
  self.assertTrue(B.date_ok('2024','year'));self.assertTrue(B.date_ok('2024-02','month'));self.assertFalse(B.date_ok('2024-13','month'));self.assertFalse(B.date_ok('2024','day'))
 def test_static_security(self):
  html=(ROOT/'web/index.html').read_text();js=(ROOT/'web/app.js').read_text()
  self.assertIn('Content-Security-Policy',html);self.assertNotIn('innerHTML',js);self.assertNotIn('eval(',js);self.assertNotIn('unsafe-inline',html)
 def test_book_has_every_node(self):
  d=B.normalize(self.bs);book=B.book(d)
  for n in d['nodes']:self.assertIn('## '+n['title'],book)
 def test_book_resolves_source_ids(self):
  d=B.normalize(self.bs)
  for n in d['nodes']:
   fragment=B.book({**d,'nodes':[n]})
   for sid in n.get('source_ids',[]):
    url=next(s['url'] for s in d['sources'] if s['id']==sid)
    self.assertIn('- 来源：'+url,fragment)
 def test_registry_unsafe_url(self):
  next(b for b in self.bs if b.get('dataset_benchmark_registry'))['dataset_benchmark_registry'][0]['access_url']='javascript:alert(1)'
  with self.assertRaisesRegex(ValueError,'unsafe'):B.normalize(self.bs)
 def test_score_import_disabled(self):
  next(b for b in self.bs if b.get('dataset_benchmark_registry'))['dataset_benchmark_registry'][0]['results_preview']['scores']=[99]
  with self.assertRaisesRegex(ValueError,'score import unsupported'):B.normalize(self.bs)
 def test_bad_source_checked_date(self):
  self.bs[0]['sources'][0]['checked_at']='2024-02-30'
  with self.assertRaisesRegex(ValueError,'checked_at'):B.normalize(self.bs)
 def test_historical_snapshots_scoped(self):
  d=B.normalize(self.bs)
  self.assertGreaterEqual(len(d['evaluation_snapshots']),3)
  for snap in d['evaluation_snapshots']:
   self.assertTrue(snap['evidence_locator']);self.assertTrue(snap['limitations_zh'])
 def test_snapshot_requires_source(self):
  bundle=next(b for b in self.bs if b.get('snapshots'));bundle['snapshots'][0]['source_url']='javascript:alert(1)'
  with self.assertRaisesRegex(ValueError,'evaluation source'):B.normalize(self.bs)
 def test_snapshot_requires_limitations(self):
  bundle=next(b for b in self.bs if b.get('snapshots'));bundle['snapshots'][0]['limitations_zh']=''
  with self.assertRaisesRegex(ValueError,'limitations'):B.normalize(self.bs)
 def test_snapshot_nonfinite_rejected(self):
  bundle=next(b for b in self.bs if b.get('snapshots'));bundle['snapshots'][0]['value']=float('nan')
  with self.assertRaisesRegex(ValueError,'finite'):B.normalize(self.bs)
 def test_snapshot_percentage_range(self):
  bundle=next(b for b in self.bs if b.get('snapshots'));bundle['snapshots'][0]['value']=101
  with self.assertRaisesRegex(ValueError,'out of range'):B.normalize(self.bs)
 def test_snapshot_unknown_version_requires_note(self):
  bundle=next(b for b in self.bs if b.get('snapshots'));bundle['snapshots'][0]['model_version_note']=''
  with self.assertRaisesRegex(ValueError,'version requires'):B.normalize(self.bs)
 def test_registry_no_unverified_ranking(self):
  d=B.normalize(self.bs)
  for row in d['dataset_benchmark_registry']:self.assertEqual(row['results_preview']['scores'],[])
if __name__=='__main__':unittest.main()
