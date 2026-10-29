"""Full JSON wire overflow and representation parity; no product execution."""
import copy,json,unittest
from images_contract import ROOT,legacy_view,json_value
from runtime_contract import validate
DATA=json.loads((ROOT/'dist/data.json').read_text())
PATHS=[['nodes',0,'publication_date'],['nodes',258,'exact_backend_model'],['nodes',258,'architecture'],['nodes',258,'first_feature_release_date'],['nodes',258,'weights_release_date'],['sources',421,'unknown_boundary'],['chatgpt_images_feature_registry','runtime_verified']]
def set_value(d,path,value):
 n=d
 for k in path[:-1]:n=n[k]
 n[path[-1]]=value
class JSONValues(unittest.TestCase):
 def test_complete_wire_overflow_standalone_chain(self):
  for path in PATHS:
   for token in ['1e400','-1e400']:
    for combo in [False,True]:
     d=copy.deepcopy(DATA);set_value(d,path,'__WIRE_NUMBER_SENTINEL__')
     if combo:d['nodes'][0]['title']='unauthorized'
     raw=json.dumps(d,ensure_ascii=False).replace('"__WIRE_NUMBER_SENTINEL__"',token);self.assertNotIn('__WIRE_NUMBER_SENTINEL__',raw);d=json.loads(raw)
     for check in [legacy_view,validate]:
      with self.subTest(path=path,token=token,combo=combo),self.assertRaisesRegex(ValueError,'non-finite'):check(d)
 def test_non_json_values_rejected(self):
  for value in [float('inf'),float('-inf'),float('nan'),(),set(),lambda:None]:
   d=copy.deepcopy(DATA);d['extra']=value
   for check in [legacy_view,validate]:
    with self.assertRaises(ValueError):check(d)
  for value in [{1:'not string'},{}]:
   if not value:value['cycle']=value
   with self.assertRaises(ValueError):json_value(value)
 def test_finite_and_normal_graph(self):
  for value in [0,-0.0,1,0.1,1e300,1e-300,None,True,'text',[],{}]:json_value(value)
  before=json.dumps(DATA);legacy_view(DATA);validate(DATA);self.assertEqual(json.dumps(DATA),before)
