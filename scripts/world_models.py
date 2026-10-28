"""Bounded world-model teaching adapter; retained source pack + independent QA overlay.
No training, network, checkpoint loading, or robot execution.
"""
import copy,json,shutil
from urllib.parse import urlsplit
EXPECTED={'wm-world-models-2018','wm-planet','wm-dreamer','wm-dreamerv2','wm-jepa-concept','wm-dreamerv3','wm-ijepa','wm-vjepa','wm-genie','wm-openvla','wm-cosmos-2025','wm-vjepa2'}
SUBTYPES={'wm-jepa-concept':'architecture_concept','wm-ijepa':'static_representation_predictor','wm-vjepa':'video_representation_predictor','wm-openvla':'action_policy_not_world_state_predictor','wm-cosmos-2025':'world_foundation_model_platform','wm-vjepa2':'video_predictor_and_action_conditioned_variant'}
LABELS={'paper_first_submitted':('paper_submission','论文首次投稿'),'publication':('report_publication','出版记录（来源限定）'),'announcement':('announcement','官方公告'),'repo_initial_release':('documentation_update','仓库初始发布记录'),'weights_first_available':('announcement','官方权重可用性公告（非独立核实首次文件时间）'),'concept_proposed':('announcement','概念年份（官方回顾，非精确首发）'),'repo_release_label':('documentation_update','当前 README 发布标签（与公告分开）')}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def adapt(raw,qa):
 r=copy.deepcopy(raw);q=copy.deepcopy(qa)
 require({n['id'] for n in r['nodes']}==EXPECTED and len(r['nodes'])==12,'world node cardinality')
 require(q['overall'].startswith('accept_'),'unaccepted QA')
 require({n['id'] for n in q['records']}==EXPECTED and len(q['records'])==12,'QA identity mismatch')
 require(all(n['verdict']=='accept_with_explicit_unknowns' for n in q['records']),'QA not accepted')
 require(all(r['execution_boundary'][k] is False for k in ['weights_downloaded','datasets_downloaded','models_executed','robot_execution','credentials_used','paid_api_used']),'unreviewed execution claim')
 source_map={s['id']:'wm-src-'+s['id'] for s in r['sources']}
 require(len(source_map)==len(r['sources']),'duplicate source')
 sources=[]
 for s in r['sources']:
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password and not any(c.isspace() for c in s['url']),'unsafe source')
  sources.append(dict(s,id=source_map[s['id']],title=s['id'],evidence_scope=s['evidence_zh'],revision_id=None,revision_note='live page observed on checked_at; historical revision not pinned'))
 def refs(ids):
  require(all(s in source_map for s in ids),'missing source');return [source_map[s] for s in ids]
 nodes=[];events=[]
 for raw_node in r['nodes']:
  n=copy.deepcopy(raw_node);nid=n['id'];review=next(a for a in q['records'] if a['id']==nid)
  require(n['type'] in {'concept','research_system','model_release'},'invalid taxonomy')
  require(n['dates']['paper_first_submitted']['date']==review['paper_first_submitted'],'QA date mismatch')
  require(n['exercise_status']=='original_conceptual_exercise_not_executed','exercise execution claim')
  if nid=='wm-ijepa':require(n['dates']['publication']['date'] is None,'unresolved venue must stay unknown')
  n['source_ids']=refs(n['source_ids']);n['semantic_subtype']=SUBTYPES.get(nid,'world_model_research_system');n['lifecycle']='unknown';n['version']='本节点限定原始研究/初始发布；非当前整个系列';n['availability']='仅文档核验；未下载或执行';n['prerequisites']=[]
  n['steps_zh']=['前置概念：'+'、'.join(n['prerequisites_zh']),'纯离线纸面练习（未执行）：'+n['offline_exercise_zh'],'验收：标清输入、输出、假设与未知；不把教学假值记作跑分，不连接机器人。']
  n['misconceptions']=['集合名称不代表所有节点都是世界状态预测器；语义子类：'+n['semantic_subtype'],'可用性公告不是独立核实首次权重文件时间；unknown 不表示从未发布。','当前仓库许可/参数页面未固定 revision，不追溯套用至全部历史版本。']+review['unknowns']
  if nid=='wm-ijepa':n['misconceptions'].append(q['additional_unknowns'][0])
  n['world_model_learning']={'semantic_subtype':n['semantic_subtype'],'prerequisites_zh':n['prerequisites_zh'],'parameters':n['parameters'],'license_scope':n['license'],'diagram':'world-model-learning.svg','diagram_note':'原创教学示意，不是论文原图或实测架构复原；箭头是教学数据流。','qa_verdict':review['verdict'],'unknowns':review['unknowns'],'best_practices':r['best_practices_zh']}
  # Raw provenance retained intact below; visible references are namespaced for aggregate uniqueness.
  n['raw_world_model_record']=copy.deepcopy(raw_node)
  for key,e in n['dates'].items():
   require(key in LABELS,'unknown date event');require(e['time'] is None and e['timezone'] is None,'unreviewed timestamp')
   typ,label=LABELS[key];sid=refs(e['source_ids']);date=e['date'];precision=e['precision']
   require((date is None and precision=='unknown') or (date is not None and sid and precision in {'day','year','month'}),'event provenance')
   note='官方来源日期；不推断同日其他事件。' if date else '未核验；不是从未发布。'
   if key=='weights_first_available':note='官方当日可用性声明，未下载验证，也未穷尽首次文件历史；不是首次权重时间的独立结论。'
   if key=='repo_release_label':note='当前 README 标签与 2025-06-11 公告并列；原因与时区未知，不静默合并。'
   events.append(dict(id=nid+'-'+key.replace('_','-'),node_ids=[nid],event_type=typ,title=n['title']+' · '+label,date=date,date_precision=precision,source_ids=sid,time=None,timezone=None,verification_status='source_reviewed_not_replicated' if date else 'not_checked',evidence_locator='research dates.'+key+'; '+e['status'],note_zh=note,availability_scope='official_dated_availability_claim' if key=='weights_first_available' else 'source_specific_event',raw_event_key=key))
  for field in ['parameters','license','weights_availability']:
   if 'source_ids' in n[field]:n[field]['source_ids']=refs(n[field]['source_ids'])
  for event in n['dates'].values():event['source_ids']=refs(event['source_ids'])
  n['dates']['weights_availability_announcement']=n['dates'].pop('weights_first_available')
  nodes.append(n)
 paths=[];edges=[]
 for p in r['reading_paths']:
  require(all(i in EXPECTED for i in p['nodes']),'path missing node')
  paths.append(dict(id='wm-path-'+p['id'],title=p['goal_zh'],node_ids=p['nodes'],acceptance='编辑阅读顺序，不是历史因果；纯离线教学练习未执行。'))
  for a,b in zip(p['nodes'],p['nodes'][1:]):
   edges.append(dict(source=a,target=b,type='editorial_learning_order',evidence_type='editorial_learning_order',verification_status='editorial_learning_relation',source_ids=next(n['source_ids'] for n in nodes if n['id']==b),note_zh='编辑阅读关系；来源支持主题内容，不证明直接历史传承。'))
 for a,b in [('embeddings','wm-jepa-concept'),('transformer','wm-ijepa'),('multimodal','wm-openvla'),('agents','wm-dreamer')]:
  edges.append(dict(source=a,target=b,type='editorial_learning_order',evidence_type='editorial_learning_order',verification_status='editorial_learning_relation',source_ids=next(n['source_ids'] for n in nodes if n['id']==b),note_zh='跨专题编辑学习入口，不证明直接因果或模型继承。'))
 return dict(schema_version='world-models.adapted.v1',title='世界模型 / JEPA / 具身 · 12 节点有限补包',scope='代表性历史与教学对照，非全球完整覆盖；JEV 无等同关系；未执行模型或机器人。',checked_at=r['checked_at'],nodes=nodes,events=events,edges=edges,sources=sources,tutorial_paths=paths,coverage_gaps=['本轮已增加12个世界模型/JEPA/具身对照节点；旧研究包缺口保留为历史记录，不能解读为当前零覆盖。']+r['unknowns']+q['additional_unknowns'],raw_research=r,qa_overlay=q)
def load(root):
 p=root/'learning/world-models/r1';return adapt(json.loads((p/'world-model-research-r1.json').read_text()),json.loads((p/'qa-overlay.json').read_text()))
def publish(root,out):shutil.copytree(root/'learning/world-models/r1',out/'world-models/r1',dirs_exist_ok=True)
