import copy,hashlib,json,sys,unittest
from unittest.mock import patch
from edge_contract import ROOT,baseline,read,research,dates,validate,legacy_view
sys.path.insert(0,str(ROOT/'scripts'))
import edge_multimodal as E
class EdgeAdmission(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.live=read(ROOT/'dist/data.json')
 def reject(self,fn,pattern):
  d=copy.deepcopy(self.live);fn(d)
  with self.assertRaisesRegex(ValueError,pattern):validate(d)
 def test_closed_live(self):validate(self.live)
 def test_stage_and_old_objects(self):self.assertEqual(legacy_view(self.live),baseline())
 def test_duplicate_old(self):self.reject(lambda d:d['nodes'].append(d['nodes'][0]),'duplicate')
 def test_duplicate_new(self):self.reject(lambda d:d['sources'].append(d['sources'][-1]),'duplicate')
 def test_unknown_node(self):self.reject(lambda d:d['nodes'].append({'id':'unapproved'}),'exact ordered')
 def test_unknown_source(self):self.reject(lambda d:d['sources'].append({'id':'unapproved'}),'exact ordered')
 def test_missing_node(self):self.reject(lambda d:d['nodes'].pop(),'exact ordered')
 def test_same_count_duplicate(self):self.reject(lambda d:d['nodes'].__setitem__(0,d['nodes'][1]),'duplicate')
 def test_old_field_change(self):self.reject(lambda d:d['nodes'][0].update(title='changed'),'old complete')
 def test_old_field_delete(self):self.reject(lambda d:d['sources'][0].pop('url'),'old complete')
 def test_old_registry_change(self):self.reject(lambda d:d['vendor_catalog']['records'][0].update(title='changed'),'old complete field')
 def test_old_edges_change(self):self.reject(lambda d:d['edges'].pop(),'old complete field')
 def test_top_level(self):self.reject(lambda d:d.update(extra=[]),'top-level')
 def test_missing_collection(self):self.reject(lambda d:d.pop('sources'),'top-level')
 def test_order(self):self.reject(lambda d:d['events'].reverse(),'exact ordered')
 def test_unknown_dates_not_filled(self):self.reject(lambda d:d['events'][-1].update(date='2026-10-29'),'date scope')
 def test_failed_source_not_verified(self):
  self.reject(lambda d:next(s for s in d['sources'] if s['id']=='edge-src-gemma-failed').update(verification_status='primary_source_opened'),'source status')
 def test_failed_attempt_not_support(self):
  n=next(n for n in self.live['nodes'] if n['id']=='edge-gemma3n-e2b-it');self.assertNotIn('edge-src-gemma-failed',n['source_ids']);self.assertEqual(n['source_attempt_ids'],['edge-src-gemma-failed'])
 def test_gated_card_not_weights_access(self):
  s=next(s for s in self.live['sources'] if s['id']=='edge-src-gemma-card');self.assertEqual(s['access_status'],'public_card_read_weights_gated_not_accessed')
 def test_license_product_development_excluded(self):
  m=research()['records'][1];self.assertIn('product development',json.dumps(m['openness']).lower())
  self.reject(lambda d:d['nodes'][-3].update(license='MIT'),'license scope')
 def test_fast_backbone_not_total(self):
  m=research()['records'][1];self.assertEqual(m['parameters']['total'],'unknown');self.assertEqual(m['parameters']['llm_nominal'],500000000)
 def test_gemma_scope_unresolved(self):self.assertIn('scope_or_version_unknown',json.dumps(research()['records'][2]))
 def test_date_denominators(self):
  es=self.live['events'][len(baseline()['events']):];self.assertEqual(len(es),24);self.assertEqual(sum(e['date'] is not None for e in es),15);self.assertEqual(sum(e['date'] is None for e in es),9)
  for e in es:
   if e['date'] is None:self.assertEqual(e['verification_status'],'unknown');self.assertEqual(e['source_ids'],[])
   if e['research_event_kind']=='weights_available_by':self.assertEqual(e['event_type'],'documentation_update')
 def test_source_denominators(self):
  ss=self.live['sources'][len(baseline()['sources']):];self.assertEqual(len(ss),18);self.assertEqual(sum(s['verification_status']=='not_accessible' for s in ss),1)
 def test_no_new_catalog_edges(self):
  self.assertEqual(len(self.live['vendor_catalog']['records']),77);self.assertEqual(self.live['edges'],baseline()['edges'])
 def test_registry_drift(self):self.reject(lambda d:d['edge_multimodal_registry']['summary_counts'].update(readable_source_count=18),'registry complete')
 def test_never_run(self):self.reject(lambda d:d['nodes'][-1].update(runtime_verified=True),'never-run')
 def test_new_field(self):self.reject(lambda d:d['nodes'][-1].update(extra=True),'complete golden')
 def test_baseline_fixture_bytes(self):
  self.assertEqual(hashlib.sha256((ROOT/'tests/fixtures/edge-multimodal-baseline.json').read_bytes()).hexdigest(),'2d55feb50ce42852031a03a1992d41a1cf37b237008bf4bdcc1b70582e856cc2')
 def test_docs_dist_bytes(self):self.assertEqual((ROOT/'docs/data.json').read_bytes(),(ROOT/'dist/data.json').read_bytes())
 def test_immutable_old_adapter(self):self.assertEqual(hashlib.sha256((ROOT/'scripts/knowledge_graph_links.py').read_bytes()).hexdigest(),'b877d7655593471edf54db2341962f783cc4b1b971a6ab3b6a15e724f50e8cab')
 def test_production_exact(self):validate(E.apply(baseline(),ROOT))
 def test_production_repeated(self):
  with self.assertRaisesRegex(ValueError,'baseline fields'):E.apply(copy.deepcopy(self.live),ROOT)
 def test_production_baseline_drift(self):
  d=baseline();d['sources'][0]['title']='changed'
  with self.assertRaisesRegex(ValueError,'baseline drift'):E.apply(d,ROOT)
 def test_production_pin(self):
  with patch.object(E,'sha',return_value='0'*64):
   with self.assertRaisesRegex(ValueError,'admission hash'):E.load(ROOT)
 def test_production_raw_hash(self):
  sha=E.sha
  with patch.object(E,'sha',side_effect=lambda p:'0'*64 if p.name=='research.json' else sha(p)):
   with self.assertRaisesRegex(ValueError,'raw inventory/hash'):E.load(ROOT)
 def mutate(self,fn,pattern):
  a,o,r,d=E.load(ROOT);fn(o)
  for k in o:a['expected_object_sha256'][k]={x['id']:E.digest(x) for x in o[k]}
  with patch.object(E,'load',return_value=(a,o,r,d)):
   with self.assertRaisesRegex(ValueError,pattern):E.apply(baseline(),ROOT)
 def test_production_failure_cannot_upgrade_even_resealed(self):self.mutate(lambda o:o['sources'][13].update(verification_status='primary_source_opened'),'source status')
 def test_production_unknown_even_resealed(self):self.mutate(lambda o:o['events'][-1].update(date='2026-10-29'),'date preservation')
 def test_production_license_even_resealed(self):self.mutate(lambda o:o['nodes'][1].update(license='MIT'),'license boundary')
 def test_production_runtime_even_resealed(self):self.mutate(lambda o:o['nodes'][0].update(runtime_verified=True),'execution upgrade')
if __name__=='__main__':unittest.main()
