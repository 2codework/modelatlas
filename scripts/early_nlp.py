"""Closed finite historical-concept admission after immutable edge stage.
No network, model execution, inferred release dates or relation edges.
"""
import copy, shutil
from realtime_audio import need, sha, digest, read
REL='learning/early-nlp/r1'
ADMISSION_SHA='1e7fca603e6cc7a05ee9310458e361bacc9681884e631bfff99bc4dc4f96ba0a'

def load(root):
 p=root/REL
 need(sha(p/'admission.json')==ADMISSION_SHA,'early NLP admission hash')
 a=read(p/'admission.json')
 for name,h in a['files_sha256'].items():need(sha(p/name)==h,'early NLP file hash '+name)
 return a,read(p/'overlay.json'),read(p/'public-research.json')

def validate_overlay(o,r):
 need(tuple(len(o[k]) for k in ('nodes','sources','events','view_nodes'))==(4,14,5,4),'early NLP finite scope')
 need(r['full_papers_read']==0,'early NLP full text boundary')
 for s,raw in zip(o['sources'],r['sources']):
  status='selected_page_regions_verified_not_full_paper' if raw.get('selected_page_visual_status') else ('primary_metadata_only' if raw['access_status'] in ('readable','readable_html_independently_opened') else 'not_accessible')
  need(s['id']=='early-nlp-src-'+raw['id'] and s['url']==raw['url'] and s['raw_record']==raw,'early NLP source identity')
  need(s['verification_status']==status and s['access_status']==raw['access_status'],'early NLP source status')
 for n,raw in zip(o['nodes'],r['nodes']):
  need(n['early_nlp']==raw and n['id']==raw['id'] and n['type']=='historical_method_concept','early NLP concept identity')
  need(n['first_release'] is None and raw['first_release'] is None,'early NLP first release unknown')
  need(n['execution_status']=='never-run' and n['runtime_verified'] is False,'early NLP never-run')
  need(n['description_zh']==raw['description_zh'],'early NLP definition scope')
 accepted=[(n,d) for n in r['nodes'] for d in n['dates'] if d['admitted']]
 for e,(n,d) in zip(o['events'],accepted):
  need(e['id']==n['id']+'-'+d['kind'] and e['node_ids']==[n['id']],'early NLP event identity')
  need(e['date']==d['value'] and e['date_precision']==d['precision'] and e['raw_record']==d,'early NLP date scope')
  need(e['source_ids']==['early-nlp-src-'+i for i in d['source_ids']],'early NLP event source')
  need(e['event_type']==('report_publication' if d['kind']=='earlier_technical_report' else 'paper_publication'),'early NLP publication not submission')
 ss={s['id']:s for s in o['sources']}
 for n in o['nodes']:
  need(all(s in ss and ss[s]['verification_status']!='not_accessible' for s in n['source_ids']),'early NLP unsupported source')
 for e in o['events']:need(all(s in ss and ss[s]['verification_status']!='not_accessible' for s in e['source_ids']),'early NLP unsupported event source')

def apply(data,root):
 a,o,r=load(root)
 need(set(data)==set(a['base_object_sha256']),'early NLP baseline fields')
 for k,v in data.items():need(digest(v)==a['base_object_sha256'][k],'early NLP baseline drift '+k)
 validate_overlay(o,r)
 for k in ('nodes','sources','events','view_nodes'):
  old=[x['id'] for x in data[k]];new=[x['id'] for x in o[k]]
  need(len(old)==len(set(old)) and len(new)==len(set(new)),'early NLP duplicate '+k)
  need(new==a['expected_ids'][k] and not set(new)&set(old),'early NLP exact IDs '+k)
  need({x['id']:digest(x) for x in o[k]}==a['expected_object_sha256'][k],'early NLP complete object '+k)
  data[k].extend(copy.deepcopy(o[k]))
 for k,v in a['expected_counts'].items():need(len(data[k])==v,'early NLP count '+k)
 need(len(data['vendor_catalog']['records'])==77,'early NLP catalog unchanged')
 data['early_nlp_registry']=read(root/REL/'registry.json')
 return data

def publish(root,out):shutil.copytree(root/REL,out/'early-nlp',dirs_exist_ok=True)
