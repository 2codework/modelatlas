"""Independent closed admission used by historical-stage tests, not production.
The immutable fixture is the approved 4b959116 canonical output, not a new
output with its suffix removed. Every live object is checked before projection.
"""
import copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='08b1dc2ab60f1eda3e64a65aee0034487506af8108cf44bfeec98aa8b97ef578'
NODE_IDS=['speech-moshi','speech-csm-1b','speech-voxtral-realtime-2602','speech-gpt-realtime-family']
SOURCE_IDS=['audio-src-'+s for s in ['moshi-repo','moshi-card','moshi-paper','moshi-intro','moshi-release','kyutai-index','moshi-failed','csm-repo','csm-card','csm-post','vox-card','vox-release','vox-paper','vox-api-model','vox-api-guide','gpt-release','gpt-old-card','gpt-deprecations','gpt-current-card','gpt-guide','vox-paper-html']]
EVENT_DATES={}
EVENT_NODES={}
for model,events in [
 ('speech-moshi',[('announcement','2024-07-03'),('paper_v1','2024-09-17'),('open_release_announcement','2024-09-18'),('paper_v2','2024-10-02')]),
 ('speech-csm-1b',[('technical_blog','2025-02-27'),('weights_release_announcement','2025-03-13'),('transformers_integration_announcement','2025-05-20')]),
 ('speech-voxtral-realtime-2602',[('announcement','2026-02-04'),('weights_release_announcement','2026-02-04'),('paper_v1','2026-02-11'),('paper_v2','2026-02-21'),('paper_v3','2026-04-06')]),
 ('speech-gpt-realtime-family',[('model_announcement','2025-08-28'),('realtime_api_ga','2025-08-28'),('old_snapshot_deprecation_announced','2026-07-20'),('old_snapshot_scheduled_shutdown','2027-01-20')])]:
 for kind,date in events:
  EVENT_DATES['audio-event-'+model+'-'+kind]=date
  EVENT_NODES['audio-event-'+model+'-'+kind]=model

def need(ok,msg):
 if not ok:raise ValueError('independent audio admission: '+msg)
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:
   need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite')))
def baseline():
 raw=(ROOT/'tests/fixtures/realtime-audio-baseline.json').read_bytes()
 need(hashlib.sha256(raw).hexdigest()==BASE_SHA,'baseline fixture hash')
 return strict(raw)
def unique(rows,label):
 ids=[x['id'] for x in rows];need(len(ids)==len(set(ids)),'duplicate '+label)
 return ids
def validate(data):
 old=baseline();need(set(data)==set(old)|{'realtime_audio_registry'},'top-level fields')
 extras={'nodes':NODE_IDS,'sources':SOURCE_IDS,'events':list(EVENT_DATES),'view_nodes':NODE_IDS}
 for key in extras:
  ids=unique(data[key],key);oldids=unique(old[key],'old '+key)
  need(ids==oldids+extras[key],'exact ordered '+key+' IDs')
  need(data[key][:len(old[key])]==old[key],'old '+key+' complete object/order preservation')
 for key in set(old)-set(extras):need(data[key]==old[key],'old complete field '+key)
 for event in data['events'][len(old['events']):]:
  need(event['date']==EVENT_DATES[event['id']],'event date')
  need(event['node_ids']==[EVENT_NODES[event['id']]],'event node')
  need(bool(event.get('source_ids')) and set(event['source_ids'])<=set(SOURCE_IDS),'event source')
 need((len(data['nodes']),len(data['edges']),len(data['events']),len(data['sources']))==(246,151,182,373),'release counts')
 need(sum(bool(e['date']) for e in data['events'])==107,'dated event count')
 return data

def legacy_view(data):
 if "edge_multimodal_registry" in data:
  from edge_contract import legacy_view as edge_legacy
  data=edge_legacy(data)
 validate(data)
 # Return the separately sealed stage only after full closed validation of live.
 return copy.deepcopy(baseline())

# This reviewed delta fixture is a byte-stable acceptance snapshot. Its semantics
# are separately checked against the independently sealed research r2 in
# test_realtime_audio.py, rather than trusting production adapter output alone.
GOLDEN_SHA='246db58481bd5179dbd52d7e22aca3f5458b5d7f66b758616ead34e893b72246'
_validate_baseline=validate
def validate(data):
 _validate_baseline(data)
 raw=(ROOT/'tests/fixtures/realtime-audio-reviewed-golden.json').read_bytes()
 need(hashlib.sha256(raw).hexdigest()==GOLDEN_SHA,'reviewed golden fixture hash')
 golden=strict(raw);old=baseline()
 for key in golden:need(data[key][len(old[key]):]==golden[key],'new '+key+' complete golden object')
 need(set(data['realtime_audio_registry'])=={'schema_version','admission_sha256','node_ids','coverage_gaps','scope_zh','execution_status','graph_statistics_current'},'registry exact fields')
 raw_research=(ROOT/'tests/fixtures/realtime-audio-research-r2.json').read_bytes()
 need(hashlib.sha256(raw_research).hexdigest()=='a05361a48710722d564d18757e5404ddb8d7103ca9541d28078429a723f2f9c2','research fixture hash')
 graph=copy.deepcopy(old['knowledge_graph_links_application']['after'])
 graph.update(nodes=246,edges=151,isolated=76,weak_components=112)
 expected={'schema_version':'realtime-audio.registry.r1','admission_sha256':'5de29a453d196dc5ccd47376248f8898e10e8694d43c8cca18d5a4038ce4b74f','node_ids':NODE_IDS,'coverage_gaps':strict(raw_research)['coverage_gaps'],'scope_zh':'四家四模型/家族有限样本；不是全球完整版本史。原knowledge_graph_links_application.after为r1接纳阶段统计，不是当前全图。','execution_status':'never-run','graph_statistics_current':graph}
 need(data['realtime_audio_registry']==expected,'registry complete object')
 return data
