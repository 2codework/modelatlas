import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build
class CoverageContext(unittest.TestCase):
 def setUp(self):self.data=json.loads((ROOT/'dist/data.json').read_text())
 def test_only_one_gap_extended(self):
  old=copy.deepcopy(self.data);lines=build.coverage_gap_lines(self.data)
  self.assertEqual(self.data,old);self.assertEqual(len(lines),53)
  original='早期统计NLP、HMM/CRF、RNN/LSTM原始论文仍需单列'
  self.assertIn('- 历史研究包缺口记录（原文）：'+original,lines)
  for gap in self.data['coverage_gaps']:
   if gap!=original:self.assertIn('- '+str(gap),lines)
  self.assertTrue(any('整篇全文核验：0（full_papers_verified）' in line for line in lines))
  self.assertIn('  '+self.data['early_nlp_registry']['scope_zh'],lines)
  for name in ['BOOK.md','dist/BOOK.md','docs/BOOK.md']:
   self.assertIn('\n'.join(lines),(ROOT/name).read_text())
 def test_no_registry_original_behavior(self):
  self.data.pop('early_nlp_registry');self.assertEqual(build.coverage_gap_lines(self.data),['- '+str(g) for g in self.data['coverage_gaps']])
 def test_unknown_registry_original_behavior(self):
  self.data['early_nlp_registry']['schema_version']='unadmitted';self.assertEqual(build.coverage_gap_lines(self.data),['- '+str(g) for g in self.data['coverage_gaps']])

 def test_frozen_registry_matches_admitted_data(self):
  self.assertTrue(build.accepted_early_nlp_registry(self.data['early_nlp_registry']))
  self.assertEqual(build.EARLY_NLP_ADMITTED_REGISTRY,self.data['early_nlp_registry'])
 def test_registry_complete_negative_matrix(self):
  expected=['- '+str(g) for g in self.data['coverage_gaps']]
  valid=self.data['early_nlp_registry']
  bad=[None,False,0,'early-nlp.registry.r1',[],{}, {'schema_version':'early-nlp.registry.r1'}]
  for key in valid:
   v=copy.deepcopy(valid);del v[key];bad.append(v)
   v=copy.deepcopy(valid);v[key]=None;bad.append(v)
  for parent in ['source_counts','expected_counts']:
   for key in valid[parent]:
    v=copy.deepcopy(valid);v[parent][key]=99;bad.append(v)
    v=copy.deepcopy(valid);del v[parent][key];bad.append(v)
  for mutate in [lambda v:v.update(extra=True),lambda v:v['source_counts'].update(extra=True),lambda v:v['source_counts'].update(full_papers_verified=False),lambda v:v['node_ids'].reverse(),lambda v:v['node_ids'].append('extra'),lambda v:v.update(scope_zh='altered'),lambda v:v.update(original_bundle_sha256sums_sha256='0'*64)]:
   v=copy.deepcopy(valid);mutate(v);bad.append(v)
  for v in bad:
   with self.subTest(value=v):
    self.assertFalse(build.accepted_early_nlp_registry(v));self.data['early_nlp_registry']=v;self.assertEqual(build.coverage_gap_lines(self.data),expected)
 def test_key_order_semantic_equivalence(self):
  def reverse(v):
   if isinstance(v,dict):return {k:reverse(v[k]) for k in reversed(v)}
   if isinstance(v,list):return [reverse(x) for x in v]
   return v
  before=build.coverage_gap_lines(self.data);self.data['early_nlp_registry']=reverse(self.data['early_nlp_registry']);self.assertEqual(build.coverage_gap_lines(self.data),before)
