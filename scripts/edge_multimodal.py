"""Pinned finite metadata admission after the immutable realtime-audio stage."""
import copy, json, shutil
from realtime_audio import need, sha, digest, read
import knowledge_graph_links as graph
REL='learning/edge-multimodal/r1'
ADMISSION_SHA='0beca167e4ad56635d5110e1dbba78e167f52908ccf15bd5ea300e1017e7747c'

def load(root):
 p=root/REL
 need(sha(p/'admission.json')==ADMISSION_SHA,'edge admission hash')
 a=read(p/'admission.json')
 need({str(f.relative_to(p)):sha(f) for f in (p/'raw').rglob('*') if f.is_file()}==a['raw_files_sha256'],'edge raw inventory/hash')
 need(sha(p/'overlay.json')==a['overlay_sha256'],'edge overlay hash')
 return a,read(p/'overlay.json'),read(p/'raw/research-r2/research.json'),read(p/'raw/research-r2/date-evidence.json')

def validate_overlay(o,r,dates):
 need(r['summary_counts']=={'source_record_count':18,'readable_source_count':17,'historical_failed_source_count':1,'date_event_slot_count':24,'known_date_count':15,'unknown_date_count':9},'edge summary denominator')
 need(len(o['sources'])==18 and len(o['nodes'])==4 and len(o['events'])==24,'edge finite scope')
 for s,raw in zip(o['sources'],r['sources']):
  need(s['raw_record']==raw and s['id']=='edge-src-'+raw['id'] and s['url']==raw['url'],'edge source mapping')
  expected='not_accessible' if raw['status']=='failed_tool_access' else 'primary_source_opened'
  need(s['verification_status']==expected and s['access_status']==raw['status'],'edge source status')
 for n,raw in zip(o['nodes'],r['records']):
  need(n['edge_multimodal']==raw and n['version']==raw['exact_id'] and n['id']==raw['id'],'edge exact model record')
  need(n['execution_status']=='never-run' and n['runtime_verified'] is False,'edge execution upgrade')
  need(n['license']==raw['openness']['terms'] and n['availability']==raw['openness']['weights'],'edge license boundary')
  need(n['source_ids']==['edge-src-'+x for x in raw['source_ids'] if x!='gemma-failed'],'edge model source mapping')
  need(n['source_attempt_ids']==['edge-src-'+x for x in raw['source_ids'] if x=='gemma-failed'],'edge failed attempt separation')
 for e,raw in zip(o['events'],dates['events']):
  need(e['raw_record']==raw and e['date']==raw['date'] and e['date_precision']==raw['precision'],'edge date preservation')
  need(e['node_ids']==[raw['model_id']] and e['research_event_kind']==raw['event'],'edge event identity')
  need(e['source_ids']==(['edge-src-'+raw['source_id']] if raw['source_id'] else []),'edge event source')
  need(e['verification_status']==('primary_sources_reviewed_not_executed' if raw['date'] else 'unknown'),'edge unknown date status')
  if raw['event']=='weights_available_by':need(e['event_type']=='documentation_update','edge available-by is not first upload')
 sources={s['id'] for s in o['sources']};nodes={n['id'] for n in o['nodes']}
 for n in o['nodes']:need(set(n['source_ids'])<=sources,'edge unresolved node sources')
 for e in o['events']:need(set(e['source_ids'])<=sources and set(e['node_ids'])<=nodes,'edge unresolved events')

def registry(data,a,r):
 return {'schema_version':'edge-multimodal.registry.r1','admission_sha256':ADMISSION_SHA,'node_ids':a['expected_ids']['nodes'],'catalog_record_ids':[],'new_edge_ids':[],'summary_counts':r['summary_counts'],'execution_status':'never-run','scope_zh':'4模型/4组织有限样本，非全球全集、非排名；节点与厂商目录身份分开，本批目录仍77条。旧图接纳及实时语音统计仅描述各自固定历史阶段。18来源=17可读+1历史失败；24日期槽=15已知+9未知。','graph_statistics_current':graph.statistics(data)}

def apply(data,root):
 a,o,r,dates=load(root)
 need(set(data)==set(a['base_object_sha256']),'edge baseline fields')
 for k,v in data.items():need(digest(v)==a['base_object_sha256'][k],'edge baseline drift '+k)
 validate_overlay(o,r,dates)
 need(a['new_edges']==[] and a['new_catalog_records']==[],'edge unexpected relation/catalog')
 for k in ('nodes','sources','events','view_nodes'):
  old=[x['id'] for x in data[k]];new=[x['id'] for x in o[k]]
  need(len(old)==len(set(old)) and len(new)==len(set(new)),'edge duplicate ID '+k)
  need(new==a['expected_ids'][k] and not set(new)&set(old),'edge addition IDs '+k)
  need({x['id']:digest(x) for x in o[k]}==a['expected_object_sha256'][k],'edge addition objects '+k)
  data[k].extend(copy.deepcopy(o[k]))
 for k,count in a['expected_counts'].items():need(len(data[k])==count,'edge count '+k)
 need([x['id'] for x in data['nodes']]==[x['id'] for x in data['view_nodes']],'edge view pairing')
 data['edge_multimodal_registry']=registry(data,a,r)
 return data

def publish(root,out):
 shutil.copytree(root/REL,out/'edge-multimodal',dirs_exist_ok=True)
