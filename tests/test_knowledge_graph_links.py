import copy, json, pathlib, sys, unittest
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import knowledge_graph_links as K
class KnowledgeLinks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.applied=json.loads((ROOT/'dist/data.json').read_text());cls.base=copy.deepcopy(cls.applied);cls.base['edges']=cls.base['edges'][:139];cls.base.pop('knowledge_graph_links_application');cls.admission,cls.raw=K.load(ROOT)
 def test_exact_preservation(self):
  d=copy.deepcopy(self.base);K.apply(d,ROOT)
  for k in self.base:
   self.assertEqual(d[k][:139] if k=='edges' else d[k],self.base[k])
  self.assertEqual(d,self.applied);self.assertEqual(len(d['nodes']),242);self.assertEqual(len(d['sources']),352);self.assertEqual(len(d['events']),166)
 def test_internal_graph_stats(self):
  b=K.statistics(self.base);a=K.statistics(self.applied);self.assertEqual((b['isolated'],b['weak_components']),(89,120));self.assertEqual((a['isolated'],a['weak_components']),(72,108));self.assertIn('AgentWork cross-site links / agentwork_links',a['excluded_links'])
 def test_original_candidate_status(self):
  self.assertTrue(all(e['integration_status']=='candidate_only_not_applied' for e in self.raw['edges']));self.assertTrue(all('integration_status' not in e for e in self.applied['edges'][139:]));self.assertEqual(len(self.applied['knowledge_graph_links_application']['records']),12)
 def test_repeated_application_fails(self):
  with self.assertRaisesRegex(ValueError,'baseline field-set'):K.apply(copy.deepcopy(self.applied),ROOT)
 def test_baseline_drift_fails(self):
  for field in ['nodes','edges','sources','events']:
   d=copy.deepcopy(self.base);d[field][0]['unexpected']='mutation'
   with self.assertRaisesRegex(ValueError,'baseline object drift'):K.apply(d,ROOT)
 def changed(self,change,regex):
  r=copy.deepcopy(self.raw);change(r)
  with patch.object(K,'load',return_value=(self.admission,r)):
   with self.assertRaisesRegex(ValueError,regex):K.apply(copy.deepcopy(self.base),ROOT)
 def test_missing_endpoint(self):self.changed(lambda r:r['edges'][0].update(target='missing'),'endpoint')
 def test_duplicate_pair(self):self.changed(lambda r:r['edges'][1].update(source=r['edges'][0]['source'],target=r['edges'][0]['target']),'duplicate pair')
 def test_source_url_drift(self):self.changed(lambda r:r['edges'][0]['official_evidence'][0].update(url='https://wrong.example/'),'source URL')
 def test_missing_source(self):self.changed(lambda r:r['edges'][0].update(source_ids=['missing']),'source drift')
 def test_runtime_upgrade(self):self.changed(lambda r:r['edges'][0].update(verification_status='runtime_verified'),'runtime upgrade')
 def test_original_status_upgrade(self):self.changed(lambda r:r['edges'][0].update(integration_status='deployed'),'raw status')
 def test_editorial_upgrade(self):self.changed(lambda r:r['edges'][1].update(evidence_type='official_documented_product_migration'),'evidence type')
 def test_unknown_required(self):self.changed(lambda r:r['edges'][0].update(unknown_boundary_zh=''),'missing direction/unknown')
 def test_admission_hash_fails(self):
  with patch.object(K,'sha',return_value='0'*64):
   with self.assertRaisesRegex(ValueError,'admission hash mismatch'):K.load(ROOT)
 def test_raw_hash_fails(self):
  original=K.sha
  with patch.object(K,'sha',side_effect=lambda p:'0'*64 if str(p).endswith('raw/research-r2/candidates.json') else original(p)):
   with self.assertRaisesRegex(ValueError,'raw hash mismatch'):K.load(ROOT)
 def test_book_semantics(self):
  text='\n'.join(K.book(self.applied));self.assertIn('1条官方文档迁移目标、11条编辑学习对照',text);self.assertIn('不表示迁移已完成',text);self.assertIn('孤立不等于网页无链接',text)
if __name__=='__main__':unittest.main()
