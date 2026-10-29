"""Defense in depth after intentionally replacing admission trust anchors.
These are NOT exploits of the frozen pinned input: changing the trusted pin is
necessary for a modified real file to pass load. Do not alter baseline semantics.
"""
import copy,json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from runtime_contract import ROOT,baseline
sys.path.insert(0,str(ROOT/'scripts'))
import inference_runtime as I
class RuntimeSemanticSchema(unittest.TestCase):
 def reject(self,mutate):
  a,o,r=I.load(ROOT);mutate(o,r)
  for k in o:a['expected_object_sha256'][k]={x['id']:I.digest(x) for x in o[k]}
  with patch.object(I,'load',return_value=(a,o,r)):
   with self.assertRaises(ValueError):I.apply(baseline(),ROOT)
 def test_direct_schema_source_fields(self):
  _,_,r=I.load(ROOT)
  for field in ['title','kind','access_status']:
   for value in [None,False,0,[],{},'']:
    source=copy.deepcopy(r['sources'][0]);source[field]=value
    with self.subTest(field=field,value=value),self.assertRaises(ValueError):I.validate_source(source)
   source=copy.deepcopy(r['sources'][0]);source.pop(field)
   with self.assertRaises(ValueError):I.validate_source(source)
 def test_direct_schema_access_kind_scope(self):
  _,_,r=I.load(ROOT)
  for field,value in [('kind','secondary'),('access_status','executed_verified'),('access_status','not_accessible'),('reading_revision','r2_reverified'),('execution_evidence',0)]:
   source=copy.deepcopy(r['sources'][0]);source[field]=value
   with self.assertRaises(ValueError):I.validate_source(source)
 def test_resealed_overlay_source_projection(self):
  for field,value in [('title',{}),('title','Invented'),('kind','secondary'),('access_status','executed_verified'),('execution_evidence',0)]:
   self.reject(lambda o,r,f=field,v=value:o['sources'][0].update({f:v}))
  for field in ['title','kind','access_status']:self.reject(lambda o,r,f=field:o['sources'][0].pop(f))
 def test_resealed_raw_source_schema(self):
  for field,value in [('title',{}),('kind','secondary'),('access_status','executed_verified'),('execution_evidence',0)]:
   def mutate(o,r):
    r['sources'][0][field]=value;o['sources'][0][field]=value;o['sources'][0]['raw_record']=copy.deepcopy(r['sources'][0])
   self.reject(mutate)
 def test_nested_boolean_zero_is_not_false(self):
  self.reject(lambda o,r:o['nodes'][0]['inference_runtime'].update(is_model=0))
  def both(o,r):
   r['nodes'][0]['is_model']=0;o['nodes'][0]['inference_runtime']=copy.deepcopy(r['nodes'][0])
  self.reject(both)
 def test_other_raw_boolean_types(self):
  for field in ['runtime_verified','weights_downloaded']:
   def mutate(o,r):
    if field=='weights_downloaded':r['nodes'][0]['artifact_pin'][field]=0
    else:r['nodes'][0][field]=0
    o['nodes'][0]['inference_runtime']=copy.deepcopy(r['nodes'][0])
   self.reject(mutate)
  self.reject(lambda o,r:r['execution_policy'].update(local_validation_only=1))
 def test_nested_source_boolean_zero_is_not_false(self):self.reject(lambda o,r:o['sources'][0]['raw_record'].update(execution_evidence=0))
 def test_exact_four_measurement_keys(self):
  for metrics in [{'speed':'unknown'},{'minimum_memory':'unknown','speed':'unknown','cost':'unknown','accuracy_delta':'unknown','extra':'unknown'},{},None,[]]:
   def mutate(o,r):
    r['nodes'][0]['independent_measurements']=metrics;o['nodes'][0]['inference_runtime']=copy.deepcopy(r['nodes'][0])
   self.reject(mutate)
 def test_exact_measurement_value_types(self):
  for value in [None,0,False,{},[],1,'measured']:
   def mutate(o,r):
    r['nodes'][0]['independent_measurements']['speed']=value;o['nodes'][0]['inference_runtime']=copy.deepcopy(r['nodes'][0])
   self.reject(mutate)
 def test_real_files_trust_anchor_resealed_source_negatives(self):
  for field,value in [('title',{}),('kind',None),('access_status','executed_verified')]:
   with tempfile.TemporaryDirectory() as t:
    root=Path(t);p=root/I.REL;shutil.copytree(ROOT/I.REL,p)
    a=I.read(p/'admission.json');o=I.read(p/'overlay.json')
    if value is None:o['sources'][0].pop(field)
    else:o['sources'][0][field]=value
    (p/'overlay.json').write_text(json.dumps(o,ensure_ascii=False))
    a['files_sha256']['overlay.json']=I.sha(p/'overlay.json')
    for k in o:a['expected_object_sha256'][k]={x['id']:I.digest(x) for x in o[k]}
    (p/'admission.json').write_text(json.dumps(a,ensure_ascii=False))
    # Original pin rejects modified admission before semantic validation.
    with self.assertRaisesRegex(ValueError,'admission hash'):I.apply(baseline(),root)
    # Deliberately new pin: semantic check independently rejects bad projection.
    with patch.object(I,'ADMISSION_SHA',I.sha(p/'admission.json')):
     with self.assertRaisesRegex(ValueError,'source projection'):I.apply(baseline(),root)
if __name__=='__main__':unittest.main()
