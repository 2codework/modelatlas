"""Finite regional office research adapter; offline only, never product execution."""
import copy,json,hashlib,shutil
from urllib.parse import urlsplit
PLATFORM_FAMILIES={'regional-dify':'Dify','regional-coze-studio':'Coze','regional-feishu-aily-enterprise':'Feishu','regional-dingtalk-yida-assistant':'DingTalk','regional-zoho-zia-agents':'Zoho','regional-bailian-agent-app':'Alibaba Cloud','regional-tencent-agent-platform':'Tencent Cloud'}
EXPECTED=set(PLATFORM_FAMILIES)
KINDS={'self-hostable-agent-application-platform','self-hostable-agent-development-platform','hosted-enterprise-agent-feature','hosted-low-code-office-assistant-feature','hosted-agent-platform','hosted-agent-application-platform','hosted-agent-development-platform'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def adapt(research):
 r=copy.deepcopy(research);ss=r['sources'];sm={s['id']:s for s in ss};items=r['entities']
 require(len(items)==7 and {x['id'] for x in items}==EXPECTED,'regional entity cardinality')
 require(len(sm)==len(ss)==16,'regional source cardinality')
 for s in ss:
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password and not any(c.isspace() for c in s['url']),'regional unsafe source')
 require(sm['dingtalk-delegation']['status']=='search-excerpt-open-failed','regional weak source upgraded')
 nodes=[];cases=[]
 for x in items:
  nid=x['id'];lab=x['exercise'];require(x['runtime_status']=='never-run' and x['runtime_verified'] is False and x['is_foundation_model'] is False,'regional execution/model claim')
  require(lab['status']=='never-run' and lab['origin']=='original-synthetic','regional exercise claim')
  require(x['entity_type'] in KINDS,'regional type');require(x['source_ids'] and all(s in sm for s in x['source_ids']),'regional source reference')
  if nid=='regional-feishu-aily-enterprise':require('豆包工作伙伴' not in x['aliases'] and '关系未知' in x['version_lifecycle'],'regional identity conflation')
  if nid=='regional-bailian-agent-app':require('2025-04-21' in lab['steps'][0] and '预览' in lab['steps'][0],'regional eligibility gate missing')
  notes=['来源核验：'+sm[s]['title']+'；'+sm[s]['status']+'；'+sm[s]['supported_claim']+'；限制：'+sm[s]['limits'] for s in x['source_ids']]
  boundary=dict(entity_type=x['entity_type'],platform_family_id=PLATFORM_FAMILIES[nid],execution_status='never-run',proof_level='documentation-only',permission_boundary=x['permission_boundary'],confirmation_boundary=lab['human_gate'],tenant_requirements=x['tenant_connector_requirements'],lifecycle_note=x['version_lifecycle'],synthetic_input='；'.join(lab['inputs']),expected_not_observed='预期而非实测：'+'；'.join(lab['output_acceptance']),source_notes=notes,failure_risks=lab['failure_risks'],unknowns=x['unknowns'])
  nodes.append(dict(id=nid,title=x['name'],type=x['entity_type'],category='regional-office-platforms',vendor=PLATFORM_FAMILIES[nid],platform_family_id=PLATFORM_FAMILIES[nid],search_aliases=x['aliases'],tags=x['aliases'],description_zh=x['documented_capability']+'；documentation-only / never-run；'+x['region_context'],version=x['version_lifecycle'],checked_at=x['verified_at'][:10],verification_status='source_reviewed_not_replicated',execution_status='never-run',runtime_verified=False,proof_level='documentation-only',is_model=False,source_ids=['regional-src-'+s for s in x['source_ids']],lifecycle='unknown',availability=x['regional_availability']+'；'+x['tenant_connector_requirements'],license=x['license'],cost=x['pricing'],historical_context=x['version_lifecycle'],steps_zh=lab['steps'],misconceptions=['风险：'+v for v in lab['failure_risks']]+['未知：'+v for v in x['unknowns']]+['宽别名仅用于搜索，不能据此合并产品身份。'],regional_office=boundary,raw_regional_office=x))
  cases.append(dict(id='regional-case-'+nid.removeprefix('regional-'),title=lab['title'],modelatlas_node_ids=[nid]))
 return dict(schema_version='regional-office.adapted.r1',checked_at=r['checked_at'][:10],nodes=nodes,edges=[],events=[],sources=[dict(s,id='regional-src-'+s['id'],checked_at=s['checked_at'][:10],evidence_scope=s['supported_claim']+'；核验：'+s['status']+'；限制：'+s['limits']) for s in ss],cases=cases,raw_research=r,coverage_gaps=['7条区域办公平台/功能文档补包，不是7个模型，也不是全球市场完整清单；价格、租户资格与实际权限拒绝效果未实测。'])
def load(root):
 p=root/'learning/regional-office/r1';qa=json.loads((p/'qa/qa.json').read_text());require(qa['status']=='sealed-independent-documentation-qa','regional QA status')
 require(qa['verdict_counts']['accept']==7 and qa['verdict_counts']['fix']==0,'regional QA disposition')
 for name,digest in qa['input_sha256'].items():
  require(not name.startswith('/') and '..' not in name.split('/') and '\\' not in name,'regional unsafe seal path')
  require(hashlib.sha256((p/'raw'/name).read_bytes()).hexdigest()==digest,'regional raw seal mismatch: '+name)
 return adapt(json.loads((p/'raw/regional-office.json').read_text()))
def publish(root,out):
 shutil.copytree(root/'learning/regional-office/r1',out/'regional-office/r1',dirs_exist_ok=True)
 shutil.copy2(root/'REGIONAL_OFFICE.md',out/'REGIONAL_OFFICE.md')
