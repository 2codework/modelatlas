"""Pinned, additive graph admission. Local metadata only; never execute retained evidence."""
import copy, hashlib, json, shutil
ADMISSION_SHA='eb489097baa065a20c2b239e76b0b7801b2a01cfcfb97ce590b1e478a7ec6846'
REL='learning/knowledge-graph-links/r1'
def need(ok,msg):
 if not ok:raise ValueError('knowledge graph links: '+msg)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def object_sha(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def statistics(data):
 adj={n['id']:set() for n in data['nodes']}
 for e in data['edges']:adj[e['source']].add(e['target']);adj[e['target']].add(e['source'])
 seen=set();components=0
 for n in adj:
  if n in seen:continue
  components+=1;queue=[n];seen.add(n)
  while queue:
   for k in adj[queue.pop()]-seen:seen.add(k);queue.append(k)
 return {'nodes':len(adj),'edges':len(data['edges']),'isolated':sum(not x for x in adj.values()),'weak_components':components,'graph_scope':'D.nodes / D.edges only; undirected degree and weak components','excluded_links':['practice registry / learning_paths','AgentWork cross-site links / agentwork_links','source URLs / Markdown links / site navigation'],'interpretation_zh':'内部图孤立不等于网页没有链接；边数不证明准确性提升或厂商集成。'}
def load(root):
 folder=root/REL;need(sha(folder/'admission.json')==ADMISSION_SHA,'admission hash mismatch')
 a=json.loads((folder/'admission.json').read_text());actual={str(p.relative_to(folder)) for p in (folder/'raw').rglob('*') if p.is_file()}
 need(actual==set(a['raw_files_sha256']),'raw file-set mismatch')
 for name,digest in a['raw_files_sha256'].items():need(sha(folder/name)==digest,'raw hash mismatch: '+name)
 raw=json.loads((folder/'raw/research-r2/candidates.json').read_text());qa=json.loads((folder/'raw/qa-r2/FINAL-VALIDATION.json').read_text())
 need(qa['status']=='PASS-source-and-semantics-r2','QA not accepted')
 need(qa['input_hashes']['manifest.json']==a['research_manifest_sha256'],'QA manifest binding')
 need(sha(folder/'raw/qa-r2/FINAL-VALIDATION.json')==a['qa_sha256'],'QA hash binding')
 return a,raw

def apply(data,root):
 a,raw=load(root)
 # Full object fingerprints fail closed on baseline drift; no original fields are rewritten.
 need(set(data)==set(a['base_object_sha256']),'baseline field-set drift')
 for k,h in a['base_object_sha256'].items():need(object_sha(data[k])==h,'baseline object drift: '+k)
 edges=raw['edges'];need(len(edges)==12,'candidate count')
 need([e['id'] for e in edges]==a['accepted_candidate_ids'],'candidate identity/order')
 nodes={n['id'] for n in data['nodes']};sources={s['id']:s for s in data['sources']};pairs={frozenset((e['source'],e['target'])) for e in data['edges']};derived=[];records=[]
 for i,e in enumerate(edges):
  need(e['source'] in nodes and e['target'] in nodes and e['source']!=e['target'],'endpoint/self-loop')
  pair=frozenset((e['source'],e['target']));need(pair not in pairs,'duplicate pair');pairs.add(pair)
  need(e['integration_status']=='candidate_only_not_applied','raw status rewritten')
  need(e['verification_status']=='documentation_review_not_runtime_verified','runtime upgrade')
  need(e['type']==('documented_migration_target' if i==0 else 'editorial_learning_relation'),'relation type')
  need(e['evidence_type']==('official_documented_product_migration' if i==0 else 'editorial_learning_relation_not_vendor_integration_claim'),'evidence type')
  need(e['unknown_boundary_zh'] and e['direction_semantics'],'missing direction/unknown')
  for sid in e['source_ids']:need(sid in sources and object_sha(sources[sid])==a['source_object_sha256'][sid],'source drift')
  need([x['source_id'] for x in e['official_evidence']]==e['source_ids'],'evidence mapping')
  for ev in e['official_evidence']:need(ev['url']==sources[ev['source_id']]['url'],'source URL mismatch')
  d=copy.deepcopy(e);d.pop('integration_status');d['application_status']='accepted_into_derived_graph_not_product_execution';d['candidate_status_at_research']='candidate_only_not_applied';d['admission_id']='knowledge-graph-links-r1';derived.append(d)
  records.append({'candidate_id':e['id'],'candidate_object_sha256':object_sha(e),'source_ids':e['source_ids'],'source_object_sha256':{sid:a['source_object_sha256'][sid] for sid in e['source_ids']},'application_status':d['application_status']})
 before=statistics(data);need((before['nodes'],before['edges'],before['isolated'],before['weak_components'])==(242,139,89,120),'before statistics')
 data['edges'].extend(derived)
 after=statistics(data);need((after['nodes'],after['edges'],after['isolated'],after['weak_components'])==(242,151,72,108),'after statistics')
 data['knowledge_graph_links_application']={'schema_version':'knowledge-graph-links.application.r1','baseline_commit':a['baseline_commit'],'admission_sha256':ADMISSION_SHA,'research_manifest_sha256':a['research_manifest_sha256'],'qa_sha256':a['qa_sha256'],'status':'applied_to_local_derived_graph_only','boundary_zh':a['boundary_zh'],'raw_candidate_status':'candidate_only_not_applied','relation_counts':{'official_documented_migration':1,'editorial_learning_relation':11},'before':before,'after':after,'records':records}
 return data

def book(data):
 from pathlib import Path
 def book_edges(data):
  """Select this admitted stage only; not an admission gate for later graph stages."""
  app=data.get('knowledge_graph_links_application')
  if app is None:
   need(not any(e.get('admission_id')=='knowledge-graph-links-r1' for e in data['edges']),'book missing application')
   return []
  a,raw=load(Path(__file__).resolve().parents[1])
  need(isinstance(app,dict) and app.get('admission_sha256')==ADMISSION_SHA,'book application binding')
  for key in ('qa_sha256','research_manifest_sha256','baseline_commit'):
   need(app.get(key)==a[key],'book application identity binding: '+key)
  need(app.get('schema_version')=='knowledge-graph-links.application.r1' and
       app.get('status')=='applied_to_local_derived_graph_only' and
       app.get('raw_candidate_status')=='candidate_only_not_applied','book application identity/status')
  referenced={sid for candidate in raw['edges'] for sid in candidate['source_ids']}
  source_objects={}
  for source in data['sources']:
   sid=source.get('id')
   if sid not in referenced:continue
   need(sid not in source_objects,'book duplicate referenced source: '+sid)
   need(object_sha(source)==a['source_object_sha256'][sid],'book referenced source content mismatch: '+sid)
   source_objects[sid]=source
  need(set(source_objects)==referenced,'book missing referenced source')
  records=app.get('records');ids=a['accepted_candidate_ids']
  need(isinstance(records,list) and len(records)==len(ids) and
       all(isinstance(r,dict) for r in records),'book application records')
  need([r.get('candidate_id') for r in records]==ids,'book candidate identity/order')
  selected={}
  for e in data['edges']:
   eid=e.get('id')
   if eid not in ids:
    need(e.get('admission_id')!='knowledge-graph-links-r1','book unregistered stage edge')
    continue
   need(eid not in selected,'book duplicate stage edge: '+eid)
   need(e.get('admission_id')=='knowledge-graph-links-r1','book stage binding: '+eid)
   selected[eid]=e
  need(set(selected)==set(ids),'book missing stage edge')
  for record,candidate in zip(records,raw['edges']):
   eid=record['candidate_id'];e=selected[eid]
   need(candidate['id']==eid and record.get('candidate_object_sha256')==object_sha(candidate),'book candidate hash binding: '+eid)
   need(record.get('source_ids')==e.get('source_ids') and
        record.get('source_object_sha256')=={sid:a['source_object_sha256'][sid] for sid in candidate['source_ids']},'book source binding: '+eid)
   need(e.get('application_status')==record.get('application_status')=='accepted_into_derived_graph_not_product_execution' and
        e.get('candidate_status_at_research')=='candidate_only_not_applied','book application status: '+eid)
   original=copy.deepcopy(e)
   for key in ('application_status','candidate_status_at_research','admission_id'):original.pop(key)
   need('integration_status' not in original,'book raw status overwritten: '+eid)
   original['integration_status']='candidate_only_not_applied'
   need(object_sha(original)==record['candidate_object_sha256'],'book candidate content mismatch: '+eid)
  return [selected[eid] for eid in ids]
 edges=book_edges(data)
 if not edges:return []
 lines=['','## 新增12条知识关联 · 接纳状态与阅读边界','1条官方文档迁移目标、11条编辑学习对照。迁移目标不表示迁移已完成、旧服务已关闭或功能完全等价；编辑箭头仅为阅读对照，不是厂商整合、模型派生或权限继承。','接纳到本地构建关系不代表产品运行或网站部署。原始研究candidate_only_not_applied保留原状，派生应用索引单独记录候选ID及来源对象哈希。','只统计D.edges内部图：139→151边，89→72孤立，120→108弱连通分量。排除practice registry、AgentWork跨站、来源与网页导航链接；孤立不等于网页无链接。']
 for e in edges:
  lines+=['','### '+e['id']+' · '+('官方文档迁移关系（非运行核验）' if e['type']=='documented_migration_target' else '编辑学习对照（非厂商集成）'),e['source']+' → '+e['target'],e['explanation_zh'],'- 方向：'+e['direction_semantics'],'- 未知边界：'+e['unknown_boundary_zh']]
  for ev in e['official_evidence']:lines+=['- 来源 '+ev['source_id']+'：'+ev['url']+' · '+ev['locator']]
 return lines

def publish(root,out,data):
 shutil.copytree(root/REL,out/'knowledge-graph-links',dirs_exist_ok=True)
 (out/'knowledge-graph-links/application.json').write_text(json.dumps(data['knowledge_graph_links_application'],ensure_ascii=False,separators=(',',':'))+'\n')
