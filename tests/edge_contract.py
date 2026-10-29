"""Closed reviewed edge stage; old stage returned only after full admission.
Independent raw research/date fixtures are pinned; production is not the oracle.
"""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='2d55feb50ce42852031a03a1992d41a1cf37b237008bf4bdcc1b70582e856cc2'
NODE_IDS=['edge-smolvlm2-500m-video-instruct','edge-fastvlm-05b-stage3','edge-gemma3n-e2b-it','edge-phi4-multimodal-instruct']
SOURCE_IDS=['edge-src-'+s for s in ['smol-card','smol-launch','smol-paper','fast-repo','fast-paper','fast-license-code','fast-license-model','fast-export','fast-app','fast-highlight','fast-hf','gemma-card','gemma-launch','gemma-failed','phi-card','phi-launch','phi-paper','phi-onnx']]
def need(ok,msg):
 if not ok:raise ValueError('independent edge: '+msg)
def read(p):
 def pairs(rows):
  d={}
  for k,v in rows:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite')))
def pinned(name,sha):
 p=ROOT/'tests/fixtures'/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==sha,'fixture hash '+name);return read(p)
def baseline():return pinned('edge-multimodal-baseline.json',BASE_SHA)
def research():return pinned('edge-multimodal-research-r2.json','0d42b558e49640d5b0aa6f142e08956b820edcb698baafb154332f2da9a1c0a5')
def dates():return pinned('edge-multimodal-dates-r2.json','b04b993da945ca7fe27d2556fb590a4a479d743bfd8082ddf93ee2bfe9f3da85')['events']
def validate(data):
 if "early_nlp_registry" in data:
  from early_nlp_contract import legacy_view
  data=legacy_view(data)
 b=baseline();r=research();ds=dates()
 need(set(data)==set(b)|{'edge_multimodal_registry'},'top-level fields')
 extras={'nodes':NODE_IDS,'sources':SOURCE_IDS,'events':['edge-event-'+e['model_id']+'-'+e['event'] for e in ds],'view_nodes':NODE_IDS}
 for k,ids in extras.items():
  actual=[x['id'] for x in data[k]];need(len(actual)==len(set(actual)),'duplicate '+k)
  need(actual==[x['id'] for x in b[k]]+ids,'exact ordered '+k)
  need(data[k][:len(b[k])]==b[k],'old complete object '+k)
 for k in set(b)-set(extras):need(data[k]==b[k],'old complete field '+k)
 o={k:data[k][len(b[k]):] for k in extras}
 for n,m in zip(o['nodes'],r['records']):
  need(n['edge_multimodal']==m,'full raw model')
  need(n['title']==m['exact_id'] and n['version']==m['exact_id'] and n['type']=='model','exact identity')
  need(n['source_ids']==['edge-src-'+s for s in m['source_ids'] if s!='gemma-failed'],'node source')
  need(n['source_attempt_ids']==['edge-src-'+s for s in m['source_ids'] if s=='gemma-failed'],'failed attempt separation')
  need(n['license']==m['openness']['terms'] and n['availability']==m['openness']['weights'],'license scope')
  need(n['execution_status']=='never-run' and n['runtime_verified'] is False,'never-run')
 for s,raw in zip(o['sources'],r['sources']):
  expected={'id':'edge-src-'+raw['id'],'url':raw['url'],'title':raw['id'],'checked_at':raw['checked_at'],'evidence_scope':raw['evidence_summary_zh'],'verification_status':'not_accessible' if raw['status']=='failed_tool_access' else 'primary_source_opened','access_status':raw['status'],'research_source_id':raw['id'],'raw_record':raw}
  need(s==expected,'source status/full object')
 for e,raw in zip(o['events'],ds):
  need(e['raw_record']==raw and e['date']==raw['date'] and e['date_precision']==raw['precision'],'date scope')
  need(e['source_ids']==(['edge-src-'+raw['source_id']] if raw['source_id'] else []),'event source')
  need(e['node_ids']==[raw['model_id']],'event node')
  need(e['verification_status']==('primary_sources_reviewed_not_executed' if raw['date'] else 'unknown'),'unknown date status')
 for v,n in zip(o['view_nodes'],o['nodes']):need(v=={'id':n['id'],'lifecycle':'unknown','vendor':n['organization'],'availability':n['availability'],'license':n['license']},'view object')
 golden=pinned('edge-multimodal-reviewed-golden.json','e0f8edca9cdc4a4057e6cc19cd97830bfc1f37647f33ad6296b1dc354f9f0e02')
 need(o==golden,'complete golden object')
 reg=pinned('edge-multimodal-registry.json','c7fe6a0b5b29f7f21cdfa64183da5f53f7369b7c1b6d45b889c4f73981a5a898');need(data['edge_multimodal_registry']==reg,'registry complete object')
 need(tuple(len(data[k]) for k in ('nodes','sources','events','edges'))==(250,391,206,151),'current snapshot counts')
 need(sum(bool(e['date']) for e in data['events'])==122,'dated snapshot count')
 return data
def legacy_view(data):
 validate(data);return copy.deepcopy(baseline())
