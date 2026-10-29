"""Offline metadata and negative gates; no runtime/SDK or product execution."""
import copy,json,sys,unittest
from unittest.mock import patch
from runtime_contract import ROOT,baseline,validate,legacy_view,golden
sys.path.insert(0,str(ROOT/'scripts'))
import inference_runtime as I
class RuntimeAdmission(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.live=json.loads((ROOT/'dist/data.json').read_text())
 def test_live_and_complete_old_stage(self):validate(self.live);self.assertEqual(legacy_view(self.live),baseline())
 def test_production(self):validate(I.apply(baseline(),ROOT))
 def test_exact_counts(self):self.assertEqual([len(self.live[k]) for k in ['nodes','sources','events','edges']],[258,421,211,151])
 def test_preserved_book_stability(self):
  import relation_book_contract
  relation_book_contract.validate()
 def test_three_reread_thirteen_inherited(self):
  p=ROOT/I.REL;ledger=json.loads((p/'raw/research-r2/reading-ledger.json').read_text())
  reread=[s for e in ledger['entries'] for s in e['read_in_r2']];inherited=[s for e in ledger['entries'] for s in e['inherited_r1']]
  self.assertEqual((len(reread),len(inherited)),(3,13));self.assertFalse(set(reread)&set(inherited));self.assertEqual(set(reread+inherited),{s['id'] for s in golden()['sources']})
 def test_raw_qa_acceptance(self):
  q=json.loads((ROOT/I.REL/'raw/qa-r2/validation.json').read_text());self.assertEqual(q['status'],'passed');self.assertFalse(q['errors']);self.assertTrue(all(c['passed'] for c in q['checks']))
 def test_learning_and_unknowns(self):
  for n in self.live['nodes'][254:]:
   self.assertFalse(n['is_model']);self.assertEqual(n['type'],'runtime');self.assertIsNone(n['first_release']);self.assertIn('未执行',n['tutorial_markdown']);self.assertIn('unknown',n['tutorial_markdown'])
 def test_dedup_current_base(self):
  d=json.loads((ROOT/I.REL/'dedup.json').read_text());self.assertEqual(d['baseline_counts'],{'nodes':254,'sources':405})
  for k in ['node_id_collisions','source_id_collisions','normalized_url_collisions','alias_matches']:self.assertEqual(d[k],[])
 def test_negatives_complete_stage(self):
  mutations=[lambda d:d['nodes'][0].update(title='drift'),lambda d:d['nodes'][-1].update(is_model=True),lambda d:d['nodes'][-1].update(runtime_verified=True),lambda d:d['nodes'][-1].update(first_release='2026-10-29'),lambda d:d['sources'][-1].update(reading_revision='read_in_r2'),lambda d:d['edges'].append({'id':'extra'}),lambda d:d['events'].append({'id':'fabricated'}),lambda d:d['nodes'].append(d['nodes'][-1]),lambda d:d['inference_runtime_registry'].update(extra=1),lambda d:d['nodes'][-1]['inference_runtime']['independent_measurements'].update(speed=1)]
  for mutate in mutations:
   d=copy.deepcopy(self.live);mutate(d)
   with self.assertRaises(ValueError):validate(d)
 def test_baseline_drift(self):
  b=baseline();b['sources'][0]['title']='drift'
  with self.assertRaisesRegex(ValueError,'baseline drift'):I.apply(b,ROOT)
 def test_repeat(self):
  with self.assertRaisesRegex(ValueError,'baseline fields'):I.apply(copy.deepcopy(self.live),ROOT)
 def test_admission_pin(self):
  with patch.object(I,'sha',return_value='0'*64):
   with self.assertRaisesRegex(ValueError,'admission hash'):I.load(ROOT)
 def test_resealed_semantic_negatives(self):
  for mutate in [lambda o:o['nodes'][-1].update(is_model=True),lambda o:o['nodes'][-1].update(first_release='2026'),lambda o:o['nodes'][-1].update(runtime_verified=True),lambda o:o['sources'][-1].update(reading_revision='read_in_r2'),lambda o:o['events'].append({'id':'fake'}),lambda o:o['nodes'][-1].update(source_ids=[])]:
   a,o,r=I.load(ROOT);mutate(o)
   for k in o:a['expected_object_sha256'][k]={x['id']:I.digest(x) for x in o[k]}
   with patch.object(I,'load',return_value=(a,o,r)):
    with self.assertRaises(ValueError):I.apply(baseline(),ROOT)
if __name__=='__main__':unittest.main()
