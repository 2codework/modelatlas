import copy,hashlib,json,sys,tempfile,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import vendor_catalog as V
class CatalogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'dist/data.json').read_text());cls.catalog=V.load(ROOT,cls.data['nodes'])
 def mutate(self,fn,rehash=True):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);p=Path(tmp.name);shutil.copytree(ROOT/'data/vendor-catalog',p/'data/vendor-catalog');f=p/'data/vendor-catalog/global.json';b=json.loads(f.read_text());fn(b);f.write_text(json.dumps(b));m=p/'data/vendor-catalog/admission.json';a=json.loads(m.read_text())
  if rehash:a['accepted'][0]['sha256']=V.digest(f);m.write_text(json.dumps(a))
  return p
 def test_current_aggregate_counts_and_preserved_catalog(self):
  self.assertEqual((len(self.data['nodes']),len(self.data['edges']),len(self.data['events'])),(200,139,149));self.assertEqual(sum(bool(e['date']) for e in self.data['events']),74);self.assertEqual(len(self.catalog['records']),77)
 def test_lossless_all_fields_and_bytes(self):
  for b in self.catalog['bundles']:
   raw=json.loads((ROOT/'data/vendor-catalog'/b['file']).read_text());self.assertEqual(raw,b['raw'])
   self.assertEqual((ROOT/'data/vendor-catalog'/b['file']).read_bytes(),(ROOT/'docs/vendor-catalog'/b['file']).read_bytes())
   actual=[r['raw'] for r in self.catalog['records'] if r['source_bundle']==b['file']];self.assertEqual(raw['records'],actual)
 def test_duplicate_id_fail(self):
  with self.assertRaisesRegex(ValueError,'duplicate catalog id'):V.load(self.mutate(lambda b:b['records'].append(copy.deepcopy(b['records'][0]))),self.data['nodes'])
 def test_duplicate_identity_fail(self):
  def edit(b):r=copy.deepcopy(b['records'][0]);r['id']='other';b['records'].append(r)
  with self.assertRaisesRegex(ValueError,'duplicate catalog identity'):V.load(self.mutate(edit),self.data['nodes'])
 def test_dangling_source_fail(self):
  with self.assertRaisesRegex(ValueError,'dangling catalog source'):V.load(self.mutate(lambda b:b['records'][0]['source_ids'].append('missing')),self.data['nodes'])
 def test_bad_date_fail(self):
  with self.assertRaisesRegex(ValueError,'invalid catalog release date'):V.load(self.mutate(lambda b:b['records'][0].update(release_date='2025-02-30')),self.data['nodes'])
 def test_unknown_date_preserved(self):
  self.assertIsNone(self.catalog['records'][0]['dates']['release_date']);self.assertEqual(self.catalog['records'][0]['checked_at'],'2026-10-28')
 def test_unsafe_url_fail(self):
  with self.assertRaisesRegex(ValueError,'unsafe catalog URL'):V.load(self.mutate(lambda b:b['records'][0].update(tutorial_url='javascript:alert(1)')),self.data['nodes'])
 def test_hash_gate(self):
  with self.assertRaisesRegex(ValueError,'hash mismatch'):V.load(self.mutate(lambda b:b.update(status='changed'),False),self.data['nodes'])
 def test_links_resolve_no_merge(self):
  allids={n['id'] for n in self.data['nodes']}|{r['id'] for r in self.catalog['records']}
  for r in self.catalog['records']:
   for e in r['links']:self.assertIn(e['target'],allids)
  r=next(r for r in self.catalog['records'] if r['exact_id']=='deepseek-ai/DeepSeek-R1');self.assertNotEqual(r['id'],'deepseek-r1-2025');self.assertIn('deepseek-r1-2025',[e['target'] for e in r['links']])
 def test_weights_code_separate(self):
  r=next(r for r in self.catalog['records'] if r['exact_id']=='Qwen/Qwen2.5-Omni-3B');self.assertEqual(r['weights_license']['identifier'],'qwen-research');self.assertEqual(r['code_license']['identifier'],'Apache-2.0');self.assertIn('separate_license',r['weights_license']['commercial_use'])
 def test_kimi_minute_precision(self):
  r=next(r for r in self.catalog['records'] if r['exact_id']=='Kimi-K2-Base');self.assertEqual(r['access_observations'][-1]['checked_at'],'2026-10-28T19:46Z');self.assertIn('minute',r['access_observations'][-1]['time_precision']);self.assertEqual(r['raw']['access_observations'][-1]['checked_at'],'2026-10-28T19:46:00Z')
 def test_book_lossless(self):
  book=(ROOT/'BOOK.md').read_text()
  for r in self.catalog['records']:self.assertIn(json.dumps(r['raw'],ensure_ascii=False),book)
if __name__=='__main__':unittest.main()
