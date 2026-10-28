"""Finite official-document assistant/workspace adapter. Offline; never runs products."""
import copy, hashlib, json, shutil
from urllib.parse import urlsplit
EXPECTED={'assistant-chatgpt-agent','assistant-chatgpt-deep-research','assistant-claude-cowork','assistant-claude-research','assistant-gemini-apps-deep-research','assistant-perplexity-projects','assistant-perplexity-research','assistant-perplexity-create-files-apps'}
KINDS={'historical_executable_agent_surface','research_feature','executable_agent_product_surface','research_workspace','artifact_creation_feature'}
def require(ok,message):
 if not ok: raise ValueError(message)
def adapt(research,sources):
 r=copy.deepcopy(research);ss=copy.deepcopy(sources);items=r['items'];sm={s['id']:s for s in ss}
 require(len(items)==8 and {n['id'] for n in items}==EXPECTED,'assistant entity cardinality')
 require(len(sm)==len(ss)==16,'assistant source cardinality')
 for s in ss:
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'assistant unsafe source URL')
 for sid in ('p-projects-change','p-feb-change'):
  require(sm[sid]['event_date'] is None and sm[sid]['normalized_date'] is None,'assistant ambiguous event date normalized')
 require(sm['p-projects-change']['raw_date']=='08/04/26' and sm['p-feb-change']['raw_date']=='02/05/26','assistant raw date changed')
 require(sm['p-labs']['evidence_status']=='unknown','assistant failed source upgraded')
 nodes=[];cases=[]
 for x in items:
  nid=x['id'];case_id='assistant-case-'+nid.removeprefix('assistant-');lab=x['learning_task'];kind=x['entity_type'];ex=x['execution']
  require(kind in KINDS,'assistant invalid entity kind')
  require(ex['status']=='never-run' and all(ex[k] is False for k in ('model_called','account_login','real_automation','user_files_uploaded','user_mac_operated')),'assistant execution claim')
  require(lab['original_synthetic'] is True and lab['steps_zh'] and lab['acceptance_zh'],'assistant synthetic task missing')
  require(x['source_ids'] and all(s in sm for s in x['source_ids']),'assistant missing source')
  require(x['permissions_and_human_confirmation_zh'] and x['unknowns_zh'],'assistant boundary missing')
  if nid=='assistant-chatgpt-agent':
   require(x['lifecycle_status']=='documentation_unavailability_notice_with_conflicting_legacy_text' and x['dates']['retirement'] is None,'assistant agent conflict/retirement boundary')
  if nid.startswith('assistant-perplexity-'):
   require(x['dates']['normalized_date'] is None and x['dates']['date_status']=='unknown','assistant ambiguous entity date normalized')
  vendor='OpenAI' if 'chatgpt' in nid else 'Anthropic' if 'claude' in nid else 'Google' if 'gemini' in nid else 'Perplexity'
  permission='；'.join(x['permissions_and_human_confirmation_zh'])
  confirmation='仅纸面设计；不登录、开通、上传用户数据、调用模型或执行自动化。平台审批不是一律逐次确认；具体配置按下列权限说明。'+permission+'；停止条件：'+lab['stop_condition_zh']
  dates=json.dumps(x['dates'],ensure_ascii=False)
  source_notes=['文档观察：'+sm[s]['title']+'；'+str(sm[s]['document_updated'] or '更新日未知')+'；'+sm[s]['evidence_summary_zh']+'；事件日期与文档观察不同。' for s in x['source_ids']]
  boundary=dict(entity_type=kind,platform_family_id=vendor,execution_status='never-run',proof_level='documentation-only',permission_boundary=permission,confirmation_boundary=confirmation,lifecycle_note=x['lifecycle_status']+'；'+x['version_scope_zh']+'；'+dates,synthetic_input=lab['title_zh']+'；'+lab['input_policy'],expected_not_observed='预期验收（不是实测）：'+'；'.join(lab['acceptance_zh']),source_notes=source_notes,limitations=x['limitations_zh'],unknowns=x['unknowns_zh'])
  nodes.append(dict(id=nid,title=x['name'],type=kind,category='assistant-workspaces',vendor=vendor,description_zh=x['version_scope_zh']+'；'+x['availability_zh']+'；documentation-only / never-run。功能、工作区容器、客户端表面与模型分开，不把检索或写作都称自主Agent。',version=x['version_scope_zh'],checked_at=r['checked_at'],verification_status='source_reviewed_not_replicated',execution_status='never-run',runtime_verified=False,proof_level='documentation-only',is_model=False,source_ids=['assistant-src-'+s for s in x['source_ids']],lifecycle='unknown',availability=x['availability_zh'],license='本批未核验服务合同/许可；不推定开源或免费。',cost='价格未知，未核实；套餐条件不等于账号已可用，不开通或购买。',historical_context='原始与QA文档观察分别保留；访问/更新日不是产品事件日。日期范围：'+dates,steps_zh=lab['steps_zh'],misconceptions=['限制：'+v for v in x['limitations_zh']]+['未知：'+v for v in x['unknowns_zh']]+['8项有限补包，不是全球完整目录；产品和练习均未运行。'],assistant_workspace=boundary,raw_assistant_workspace=copy.deepcopy(x)))
  cases.append(dict(id=case_id,title=lab['title_zh'],modelatlas_node_ids=[nid]))
 return dict(schema_version='assistant-workspace.adapted.r1',checked_at=r['checked_at'],nodes=nodes,edges=[],events=[],sources=[dict(s,id='assistant-src-'+s['id'],checked_at=s['accessed_at'],evidence_scope=s['evidence_summary_zh']+'；官方文档观察，不是产品实测；更新时间不当事件日。') for s in ss],cases=cases,raw_research=r,raw_sources=ss,coverage_gaps=['通用助手/研究工作区已有8项有限文档补包；功能、工作区、历史执行表面不是8个模型或8个自主Agent。账号可用性、实际效果和更广市场仍未覆盖。'])
def load(root):
 p=root/'learning/assistant-workspace/r1';qa=json.loads((p/'qa/REVISION-RECHECK.json').read_text())
 require(qa['verdict']=='accept_with_documented_unknowns','assistant QA verdict')
 for name,digest in qa['revised_input_sha256'].items():
  require('/' not in name and name not in ('.','..'),'assistant unsafe seal path')
  require(hashlib.sha256((p/'raw'/name).read_bytes()).hexdigest()==digest,'assistant approved source changed: '+name)
 for name,digest in json.loads((p/'raw/before-qa/sha256.json').read_text()).items():
  require('/' not in name and name not in ('.','..'),'assistant unsafe history seal path')
  require(hashlib.sha256((p/'raw/before-qa'/name).read_bytes()).hexdigest()==digest,'assistant original changed: '+name)
 return adapt(json.loads((p/'raw/research.json').read_text()),json.loads((p/'raw/sources.json').read_text()))
def publish(root,out):shutil.copytree(root/'learning/assistant-workspace/r1',out/'assistant-workspace/r1',dirs_exist_ok=True)
