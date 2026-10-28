import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import regional_office as R
class RegionalTests(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/'learning/regional-office/r1/raw/regional-office.json').read_text())
 def test_cardinality_and_immutability(self):
  old=copy.deepcopy(self.r);b=R.adapt(self.r);self.assertEqual(old,self.r);self.assertEqual((len(b['nodes']),len(b['sources']),len(b['cases']),len(b['events'])),(7,16,7,0));self.assertEqual(b['raw_research'],old)
 def test_seals(self):self.assertEqual(len(R.load(ROOT)['nodes']),7)
 def test_types_family_and_boundaries(self):
  for n in R.adapt(self.r)['nodes']:
   self.assertFalse(n['is_model']);self.assertFalse(n['runtime_verified']);self.assertEqual(n['vendor'],R.PLATFORM_FAMILIES[n['id']]);self.assertEqual(n['regional_office']['platform_family_id'],n['vendor']);self.assertIn('never-run',n['description_zh']);self.assertTrue(n['regional_office']['source_notes']);self.assertNotIn('office_agent',n);self.assertNotIn('assistant_workspace',n)
 def test_reject_execution(self):
  self.r['entities'][0]['runtime_verified']=True
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_reject_model(self):
  self.r['entities'][0]['is_foundation_model']=True
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_reject_weak_source_upgrade(self):
  next(s for s in self.r['sources'] if s['id']=='dingtalk-delegation')['status']='opened'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_reject_naming_conflation(self):
  self.r['entities'][2]['aliases'].append('豆包工作伙伴')
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_reject_missing_eligibility(self):
  self.r['entities'][5]['exercise']['steps'][0]='跳过账户验证'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_reject_unsafe_source(self):
  self.r['sources'][0]['url']='https://user:password@example.org'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_reject_missing_source(self):
  self.r['entities'][0]['source_ids']=['absent']
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_derived_book_links_counts(self):
  d=json.loads((ROOT/'docs/data.json').read_text());self.assertEqual((len(d['nodes']),len(d['events']),len(d['vendor_catalog']['records']),len(d['dataset_benchmark_registry']),len(d['media_evaluation_registry'])),(242,166,77,33,11))
  book=(ROOT/'BOOK.md').read_text()
  for n in d['nodes']:
   if n['id'] not in R.EXPECTED:continue
   self.assertEqual(n['agentwork_links'][0]['id'],'regional-case-'+n['id'].removeprefix('regional-'));self.assertIn(n['title'],book);self.assertIn(n['license'],book);self.assertIn(n['regional_office']['tenant_requirements'],book)
  for p in ('REGIONAL_OFFICE.md','dist/REGIONAL_OFFICE.md','docs/REGIONAL_OFFICE.md'):
   self.assertEqual((ROOT/p).read_bytes(),(ROOT/'learning/regional-office/r1/raw/regional-office.zh.md').read_bytes())
if __name__=='__main__':unittest.main()
