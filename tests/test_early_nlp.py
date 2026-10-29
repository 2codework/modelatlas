"""Offline implementation tests; do not constitute independent research review."""
import copy,json,unittest,sys
from unittest.mock import patch
from early_nlp_contract import ROOT,baseline,validate,legacy_view
sys.path.insert(0,str(ROOT/'scripts'))
import early_nlp as E
class EarlyNLP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.live=json.loads((ROOT/'dist/data.json').read_text())
 def reject(self,fn):
  d=copy.deepcopy(self.live);fn(d)
  with self.assertRaises(ValueError):validate(d)
 def test_closed_live(self):validate(self.live)
 def test_old_stage_exact(self):self.assertEqual(legacy_view(self.live),baseline())
 def test_node_identity(self):self.assertEqual([n['id'] for n in self.live['nodes'][250:]],['early-nlp-hmm','early-nlp-crf','early-nlp-rnn','early-nlp-lstm'])
 def test_five_dates_only(self):
  es=self.live['events'][206:];self.assertEqual(sorted((e['date'],e['date_precision']) for e in es),[('1989-02','month'),('1990-03','month'),('1995-08','month'),('1997','year'),('2001','year')])
  self.assertTrue(all(e['source_ids'] for e in es));self.assertTrue(all(e['date_precision']!='day' for e in es))
 def test_no_first_release_guess(self):
  for n in self.live['nodes'][250:]:self.assertIsNone(n['first_release']);self.assertNotEqual(n['type'],'model');self.assertNotIn('tutorial_markdown',n)
 def test_source_scope_denominators(self):
  ss=self.live['sources'][391:]
  self.assertEqual({v:sum(s['verification_status']==v for s in ss) for v in ('primary_metadata_only','selected_page_regions_verified_not_full_paper','not_accessible')},{'primary_metadata_only':7,'selected_page_regions_verified_not_full_paper':2,'not_accessible':5})
  failed={s['id'] for s in ss if s['verification_status']=='not_accessible'}
  for n in self.live['nodes'][250:]:self.assertFalse(set(n['source_ids'])&failed)
  for e in self.live['events'][206:]:self.assertFalse(set(e['source_ids'])&failed)
 def test_projection_accepted_facts(self):
  r=json.loads((ROOT/'learning/early-nlp/r1/public-research.json').read_text())
  self.assertEqual(r['original_bundle_sha256sums_sha256'],'a03b78b1fc42a4a6bc5d1ff20d0fcdfa8d797eaa9a224f11f0e4aabf67d1ad44')
  self.assertEqual([n['early_nlp'] for n in self.live['nodes'][250:]],r['nodes'])
  self.assertEqual([s['raw_record'] for s in self.live['sources'][391:]],r['sources'])
  accepted=[d for n in r['nodes'] for d in n['dates'] if d['admitted']]
  self.assertEqual([e['raw_record'] for e in self.live['events'][206:]],accepted)
  self.assertTrue(all(not n['full_paper_verified'] for n in r['nodes']))
  for n in r['nodes']:
   if 'selected_page_evidence' in n:self.assertEqual(n['selected_page_evidence']['viewed_regions'],['page 1 top','page 1 bottom','page 2 top'])
 def test_unknown_node(self):self.reject(lambda d:d['nodes'].append({'id':'unapproved'}))
 def test_duplicate(self):self.reject(lambda d:d['nodes'].__setitem__(-1,d['nodes'][-2]))
 def test_old_object_change(self):self.reject(lambda d:d['nodes'][0].update(title='changed'))
 def test_old_top_level_change(self):self.reject(lambda d:d['coverage_gaps'].append('changed'))
 def test_unapproved_registry(self):self.reject(lambda d:d['early_nlp_registry'].update(extra=True))
 def test_new_extra_field(self):self.reject(lambda d:d['nodes'][-1].update(extra=True))
 def test_date_day_upgrade(self):self.reject(lambda d:d['events'][-1].update(date='1997-11-15',date_precision='day'))
 def test_date_source_swap(self):self.reject(lambda d:d['events'][-1].update(source_ids=[d['sources'][-1]['id']]))
 def test_failed_source_upgrade(self):self.reject(lambda d:d['sources'][-1].update(verification_status='primary_source_opened'))
 def test_first_release_upgrade(self):self.reject(lambda d:d['nodes'][-1].update(first_release='1997-11-15'))
 def test_new_edge(self):self.reject(lambda d:d['edges'].append({'id':'invented'}))
 def test_candidate_as_event(self):self.reject(lambda d:d['events'].append({'id':'unaccepted','date':'1997-11-15'}))
 def test_missing_registry(self):self.reject(lambda d:d.pop('early_nlp_registry'))
 def test_production_exact(self):validate(E.apply(baseline(),ROOT))
 def test_production_base_drift(self):
  d=baseline();d['nodes'][0]['title']='changed'
  with self.assertRaisesRegex(ValueError,'baseline drift'):E.apply(d,ROOT)
 def test_production_repeat(self):
  with self.assertRaisesRegex(ValueError,'baseline fields'):E.apply(copy.deepcopy(self.live),ROOT)
 def test_production_admission_pin(self):
  with patch.object(E,'sha',return_value='0'*64):
   with self.assertRaisesRegex(ValueError,'admission hash'):E.load(ROOT)
 def mutate_overlay(self,fn,pattern):
  a,o,r=E.load(ROOT);fn(o)
  for k in o:a['expected_object_sha256'][k]={x['id']:E.digest(x) for x in o[k]}
  with patch.object(E,'load',return_value=(a,o,r)):
   with self.assertRaisesRegex(ValueError,pattern):E.apply(baseline(),ROOT)
 def test_resealed_source_upgrade(self):self.mutate_overlay(lambda o:next(s for s in o['sources'] if s['verification_status']=='not_accessible').update(verification_status='primary_metadata_only'),'source status')
 def test_resealed_date_day_upgrade(self):self.mutate_overlay(lambda o:o['events'][-1].update(date='1995-08-28',date_precision='day'),'date scope')
 def test_resealed_source_swap(self):self.mutate_overlay(lambda o:o['events'][-1].update(source_ids=[]),'event source')
 def test_resealed_first_release(self):self.mutate_overlay(lambda o:o['nodes'][-1].update(first_release='1997'),'first release')
 def test_resealed_runtime(self):self.mutate_overlay(lambda o:o['nodes'][-1].update(runtime_verified=True),'never-run')
 def test_resealed_first_submission(self):self.mutate_overlay(lambda o:o['events'][0].update(event_type='paper_first_submitted'),'publication not submission')
if __name__=='__main__':unittest.main()
