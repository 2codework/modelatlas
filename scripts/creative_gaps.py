"""Explicit, fail-closed creative-learning adapter. No product or API execution."""
import copy, hashlib, html, json, re, shutil
from urllib.parse import urlsplit
MAPPING={
 'gap-underlord-review':('creative-underlord','agentic_application_feature'),
 'gap-express-targeted':('creative-express-ai-assistant','conversational_ai_assistant'),
 'gap-ableton-comp':('creative-ableton-live','deterministic_software_workflow'),
 'gap-muse-parts':('creative-musescore-studio','deterministic_software_workflow'),
 'gap-kden-proxy':('vid-kdenlive','deterministic_software_workflow'),
 'gap-indesign-preflight':('creative-indesign','deterministic_software_workflow')}
PREFIX='creative-gap-src-'
NOTICE='六项代表性教学，不是全集。资料核验≠产品效果；所有练习never-run。两项AI应用能力不是基础模型；另四项普通创作软件不是Agent。通过稳定案例ID关联AgentWork的对应练习。'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def safe(url):
 u=urlsplit(url);return u.scheme=='https' and bool(u.hostname) and not u.username and not u.password and not any(c.isspace() for c in url)
def adapt(raw):
 d=copy.deepcopy(raw);need(d['schema_version']=='creative-learning-gap-research-r2.v1','schema')
 need(len(d['candidates'])==6 and len(d['sources'])==23,'cardinality')
 src={s['id']:s for s in d['sources']};need(len(src)==23,'duplicate source')
 for s in src.values():
  need(safe(s['url']),'unsafe URL');need(s['checked_at']=='2026-10-28','unchecked source')
  need(s['status'] in {'opened_primary','tool_open_error','redirect_with_search_body_conflict','independently_opened_primary'},'source evidence upgrade')
 cases=[];nodes=[];seen=set()
 for c in d['candidates']:
  cid=c['id'];need(cid in MAPPING and cid not in seen,'mapping/duplicate case');seen.add(cid);nid,kind=MAPPING[cid]
  need(c['entity_type']==kind and c['is_foundation_model'] is False,'wrong entity type')
  need(c['lifecycle']['release_date'] is None,'invented release date')
  need(c['original_exercise']['status']=='proposed_not_executed','execution upgrade')
  need(c['verification']=={'documentation_review':True,'product_run':False,'account_login':False,'api_key_used':False,'output_quality_verified':False},'verification upgrade')
  need(c['source_ids'] and all(s in src for s in c['source_ids']),'missing source')
  for field in ['visible_documented_path']:
   need(isinstance(c[field],list) and c[field] and all(isinstance(x,str) and x for x in c[field]),'missing steps')
  need(len(c['original_exercise']['acceptance_checks'])>=3,'missing acceptance')
  for field in ['gap_vs_existing','access_and_payment','license_and_rights','automation_boundary']:
   need(isinstance(c[field],str) and c[field],'missing boundary')
  if cid=='gap-underlord-review':
   text=json.dumps(c,ensure_ascii=False)
   need(all(x in text for x in ['当前session','Version history','compositions/files','协作者','批准','刷新']),'rollback scope missing')
  if cid=='gap-express-targeted':need(all(x in json.dumps(c,ensure_ascii=False) for x in ['中国','Chats','Teams/Enterprise/Education','未列中文','未确认']),'Express boundary missing')
  case=dict(c,modelatlas_node_id=nid,agentwork_case_id=cid,execution_status='never-run',proof_level='documentation-only',mapping_relation='editorial_learning_relation',modelatlas_url='index.html?node='+nid,local_exercise_url='creative-learning.html#'+cid,agentwork_link={'url':'https://2codework.github.io/agentwork/?case='+cid,'status':'declared_stable_id_mapping'},source_ids=[PREFIX+s for s in c['source_ids']])
  cases.append(case)
  if nid!='vid-kdenlive':
   nodes.append(dict(id=nid,title=c['product_name'],type='application_feature' if kind!='deterministic_software_workflow' else 'tool',entity_type=kind,category={'音乐':'creative-music','视频':'creative-video','设计':'creative-design'}[c['domain']],vendor={'gap-underlord-review':'Descript','gap-express-targeted':'Adobe','gap-ableton-comp':'Ableton','gap-muse-parts':'MuseScore','gap-indesign-preflight':'Adobe'}[cid],description_zh=c['gap_vs_existing']+' '+c['automation_boundary'],checked_at=d['checked_at'],version='以2026-10-28核验的帮助页为依据，非固定产品安装快照',verification_status='source_reviewed_not_replicated',lifecycle='unknown',availability=c['access_and_payment'],cost=c['access_and_payment'],license=c['license_and_rights'],source_ids=case['source_ids'],steps_zh=c['visible_documented_path'],misconceptions=[NOTICE,c['lifecycle']['history'],'首发日期unknown；文档日期不是产品发布日期。'],creative_gap_case_id=cid))
 need(seen==set(MAPPING),'missing case')
 sources=[dict(s,id=PREFIX+s['id'],title=s['id'],evidence_scope=s['supported_claim']+'；原观察 '+s['status']+'；独立QA '+s.get('independent_qa',{}).get('qa_status','unknown')+'；限制 '+s.get('limitations','')) for s in d['sources']]
 bundle={'schema_version':'creative.gaps.integrated.r1','checked_at':d['checked_at'],'nodes':nodes,'sources':sources,'events':[],'edges':[],'raw_research':d,'coverage_gaps':[NOTICE]}
 registry={'schema_version':'creative.learning.registry.r1','notice':NOTICE,'cases':cases,'node_to_cases':{nid:[cid for cid,(n,_) in MAPPING.items() if n==nid] for nid,_ in MAPPING.values()},'source_ids':[s['id'] for s in sources],'verification_status':'documentation_and_id_contract_only'}
 return bundle,registry

def load(root):
 folder=root/'learning/creative-gaps';manifest=json.loads((folder/'raw-sha256.json').read_text());raw=folder/'raw'
 actual={p.relative_to(raw).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in raw.rglob('*') if p.is_file()}
 need(actual==manifest,'raw byte manifest mismatch')
 bundle,registry=adapt(json.loads((raw/'creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text()))
 plans=json.loads((folder/'exercise-plans.json').read_text());need(plans['execution_status']=='never-run' and set(plans['plans'])==set(MAPPING),'exercise plan coverage/state')
 for c in registry['cases']:
  plan=plans['plans'][c['id']];need(plan['task'] and len(plan['steps'])==4 and plan['expected_artifacts'] and plan['stop_conditions'],'incomplete exercise plan');c['exercise_plan']=plan;c['exercise_plan_note']=plans['note']
 return bundle,registry

def validate_registry(data):
 r=data['creative_learning_registry'];nodes={n['id'] for n in data['nodes']};sources={s['id'] for s in data['sources']}
 need(len(r['cases'])==6,'registry cardinality')
 for c in r['cases']:
  need(c['modelatlas_node_id'] in nodes,'dangling mapped node');need(set(c['source_ids'])<=sources,'dangling source');need(c['id'] in r['node_to_cases'][c['modelatlas_node_id']],'reverse mapping')
  need(c['agentwork_link']['status']=='declared_stable_id_mapping','premature publication')

def book(registry):
 lines=['','## 创意学习工作台 · 六项未执行练习','',NOTICE]
 for c in registry['cases']:
  lines+=['','### '+c['title'],'- 类型：'+c['entity_type'],'- 产品节点：'+c['modelatlas_node_id'],'- case ID：'+c['id'],'- 状态：documentation-only / never-run','- 为什么补：'+c['gap_vs_existing'],'- 原创输入：'+c['original_exercise']['fixture'],'#### 文档操作路径（不是执行结果）']
  lines += [str(i)+'. '+s for i,s in enumerate(c['visible_documented_path'],1)]
  lines += ['#### 原创练习验收（预期，未观察）']+['- '+s for s in c['original_exercise']['acceptance_checks']]
  for label,key in [('账号与费用','access_and_payment'),('许可与权利','license_and_rights'),('权限与自动化边界','automation_boundary')]:lines+=['- '+label+'：'+c[key]]
  if 'exercise_plan' in c:
   p=c['exercise_plan'];lines+=['#### 原创操作练习（未执行）',c['exercise_plan_note'],p['task']]+[str(i)+'. '+x for i,x in enumerate(p['steps'],1)]+['- 预期交付物：'+'；'.join(p['expected_artifacts']),'- 停止条件：'+'；'.join(p['stop_conditions'])]
  lines+=['- 历史与版本：'+c['lifecycle']['history'],'- 精确首发日期：unknown','- [对应AgentWork练习]('+c['agentwork_link']['url']+')']
 return '\n'.join(lines)+'\n'

def publish(root,out,registry,sources):
 shutil.copytree(root/'learning/creative-gaps',out/'creative-learning-evidence',dirs_exist_ok=True)
 esc=html.escape
 parts=['<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'none\'; style-src \'self\'; img-src \'self\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'"><title>创意学习工作台 · ModelAtlas</title><link rel="stylesheet" href="style.css"></head><body><a href="index.html">返回ModelAtlas</a><main><h1>创意学习工作台</h1><p>'+esc(NOTICE)+'</p><nav aria-label="六项练习">']
 for c in registry['cases']:parts.append('<p><a href="#'+c['id']+'">'+esc(c['title'])+'</a></p>')
 parts.append('</nav>');sm={s['id']:s for s in sources}
 for c in registry['cases']:
  parts.append('<section id="'+c['id']+'"><h2>'+esc(c['title'])+'</h2><p>分类：'+esc(c['entity_type'])+'；documentation-only / never-run</p><p><a href="'+c['modelatlas_url']+'">技术/工具节点：'+esc(c['modelatlas_node_id'])+'</a></p>')
  for title,text in [('学习目标与去重',c['gap_vs_existing']),('原创输入',c['original_exercise']['fixture']),('账号与费用',c['access_and_payment']),('许可与权利',c['license_and_rights']),('权限/自动化边界',c['automation_boundary']),('历史/未知日期',c['lifecycle']['history']+'；精确首发日期unknown')]:parts.append('<h3>'+title+'</h3><p>'+esc(text)+'</p>')
  for title,steps in [('文档操作路径（未执行）',c['visible_documented_path']),('原创练习验收（预期，不是实测）',c['original_exercise']['acceptance_checks'])]:parts.append('<h3>'+title+'</h3><ol>'+''.join('<li>'+esc(s)+'</li>' for s in steps)+'</ol>')
  if 'exercise_plan' in c:
   p=c['exercise_plan'];parts.append('<h3>原创操作练习（未执行）</h3><p>'+esc(c['exercise_plan_note'])+'</p><p>'+esc(p['task'])+'</p><ol>'+''.join('<li>'+esc(x)+'</li>' for x in p['steps'])+'</ol><p>预期交付物：'+esc('；'.join(p['expected_artifacts']))+'</p><p>停止条件：'+esc('；'.join(p['stop_conditions']))+'</p>')
  parts.append('<p><a href="'+esc(c['agentwork_link']['url'],quote=True)+'" rel="noopener noreferrer">对应AgentWork练习</a> · case ID：<code>'+c['id']+'</code></p><h3>来源与核验强弱</h3><ul>')
  for sid in c['source_ids']:
   s=sm[sid];parts.append('<li><a href="'+esc(s['url'],quote=True)+'" rel="noopener noreferrer">'+esc(s['title'])+'</a><p>'+esc(s['evidence_scope'])+'</p></li>')
  parts.append('</ul></section>')
 parts.append('<section><h2>证据包</h2><p><a href="creative-learning-evidence/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json">修订研究JSON</a> · <a href="creative-learning-evidence/raw/creative-learning-gap-qa-r2/creative-learning-gap-qa-r2.md">最终独立QA</a> · <a href="creative-learning-evidence/raw-sha256.json">原始字节SHA256清单</a></p></section></main></body></html>')
 (out/'creative-learning.html').write_text('\n'.join(parts)+'\n')
