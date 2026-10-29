"""Closed additive runtime metadata admission. No install, network or execution."""
import copy, shutil
from realtime_audio import need, sha, digest, read
REL='learning/inference-runtime/r1'
ADMISSION_SHA='ee9078aa31789fa4eb2d19a77cf6c877b50b65621055081ce85a118ec355dd2c'
def load(root):
 p=root/REL
 need(sha(p/'admission.json')==ADMISSION_SHA,'runtime admission hash')
 a=read(p/'admission.json')
 actual={str(f.relative_to(p)):sha(f) for f in p.rglob('*') if f.is_file() and f!=p/'admission.json' and '__pycache__' not in f.parts and f.suffix!='.pyc'}
 need(actual==a['files_sha256'],'runtime exact file inventory/hash')
 return a,read(p/'overlay.json'),read(p/'raw/research-r2/runtime-learning.json')
def same_json(a,b):
 # JSON canonical digests preserve scalar types: false != 0, true != 1.
 return digest(a)==digest(b)
def validate_source(raw):
 required={'id','url','title','kind','checked_at','access_status','web_evidence_ref','execution_evidence','reading_revision'}
 need(type(raw) is dict and required<=set(raw)<=required|{'prior_web_evidence_ref'},'runtime source schema fields')
 need(all(type(raw[k]) is str and raw[k].strip() for k in set(raw)-{'execution_evidence'}),'runtime source text field type')
 need(raw['kind']=='official_primary' and raw['access_status']=='opened_content_read','runtime source kind/access status')
 need(raw['execution_evidence'] is False,'runtime raw source execution claim')
 reread={'irt-src-trt-license','irt-src-trt-release','irt-src-ort-install'}
 expected='r2_reverified' if raw['id'] in reread else 'inherited_r1_not_reopened_r2'
 need(raw['reading_revision']==expected,'runtime source reading partition')
 need(('prior_web_evidence_ref' in raw)==(raw['id'] in reread),'runtime prior source evidence scope')
def validate_overlay(o,r):
 need(type(r) is dict and type(r.get('nodes')) is list and len(r['nodes'])==4 and type(r.get('sources')) is list and len(r['sources'])==16,'runtime raw cardinality')
 need(type(r.get('execution_policy')) is dict and r['execution_policy'].get('local_validation_only') is True,'runtime local validation policy type')
 need(set(o)=={'nodes','sources','events','view_nodes'},'runtime overlay fields')
 need(tuple(len(o[k]) for k in ('nodes','sources','events','view_nodes'))==(4,16,0,4),'runtime finite scope/no fabricated events')
 need([n['id'] for n in o['nodes']]==['irt-sg-lang','irt-trt-llm','irt-ort-core','irt-ov-core'],'runtime identity')
 for n,raw in zip(o['nodes'],r['nodes']):
  need(same_json(n['inference_runtime'],raw) and n['id']==raw['id'],'runtime full raw record')
  need(raw.get('is_model') is False and raw.get('runtime_verified') is False and raw.get('execution_status')=='never-run' and raw.get('type')=='runtime','runtime raw model/execution types')
  need(type(raw.get('artifact_pin')) is dict and raw['artifact_pin'].get('weights_downloaded') is False,'runtime raw download flag type')
  need(n['type']=='runtime' and n['is_model'] is False,'runtime not model')
  need(n['execution_status']=='never-run' and n['runtime_verified'] is False,'runtime execution claim')
  need(n['first_release'] is None and raw['first_release_date'] is None and raw['representative_release']['date_iso'] is None,'runtime unknown dates')
  metrics=raw.get('independent_measurements')
  need(type(metrics) is dict and set(metrics)=={'minimum_memory','speed','cost','accuracy_delta'} and all(type(v) is str and v=='unknown' for v in metrics.values()),'runtime exact unknown measurement map')
  need(n['source_ids']==raw['source_ids'],'runtime source mapping')
  need(n['description_zh']==raw['description_zh'] and n['steps_zh']==raw['steps_zh'],'runtime teaching scope')
 for s,raw in zip(o['sources'],r['sources']):
  validate_source(raw)
  expected=dict(raw,verification_status='primary_sources_reviewed_not_executed',evidence_scope='官方文档阅读，非执行证据；'+raw['reading_revision'],raw_record=raw)
  need(same_json(s,expected),'runtime truthful complete source projection')
 ss={s['id'] for s in o['sources']}
 for n in o['nodes']:need(set(n['source_ids'])<=ss,'runtime dangling source')
def apply(data,root):
 a,o,r=load(root)
 need(set(data)==set(a['base_object_sha256']),'runtime baseline fields')
 for k,v in data.items():need(digest(v)==a['base_object_sha256'][k],'runtime baseline drift '+k)
 validate_overlay(o,r)
 for k in o:
  old=[x['id'] for x in data[k]];new=[x['id'] for x in o[k]]
  need(len(old)==len(set(old)) and len(new)==len(set(new)) and not set(new)&set(old),'runtime duplicate '+k)
  need(new==a['expected_ids'][k],'runtime exact IDs '+k)
  need({x['id']:digest(x) for x in o[k]}==a['expected_object_sha256'][k],'runtime exact objects '+k)
  data[k].extend(copy.deepcopy(o[k]))
 for k,count in a['expected_counts'].items():need(len(data[k])==count,'runtime counts '+k)
 data['inference_runtime_registry']=read(root/REL/'registry.json')
 return data
def publish(root,out):
 need(sha(root/'INFERENCE_RUNTIME.md')==sha(root/REL/'raw/research-r2/README.zh-CN.md'),'runtime readable guide drift')
 shutil.copytree(root/REL,out/'inference-runtime',dirs_exist_ok=True)
 shutil.copy2(root/'INFERENCE_RUNTIME.md',out/'INFERENCE_RUNTIME.md')
