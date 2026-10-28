import pathlib,json,hashlib
out=pathlib.Path('knowledge-graph-links-research-r2');old=pathlib.Path('knowledge-graph-links-research-r1')
p=out/'candidates.json';v=json.loads(p.read_text());e=v['edges'][0]
e['unknown_boundary_zh']='官方未定 Agents 停用日；每账户迁移状态及实际运行均 unknown，不宣称迁移完成或全部功能等价。工具默认不暂停，须逐工具开启 Require approval；聊天 on-demand 暂无直接等价触发；组织级 BYOM 未支持。HubSpot/Asana/Zendesk/Zoom/Jira 知识源尚未支持，Q4 2026 仅为计划；已支持来源仍有规模、加载和权限差异。'
check={'reviewer':'independent QA / audit_regional_platform_sources','checked_at':'2026-10-28','status':'official_page_independently_opened','url':'https://help.zapier.com/hc/en-us/articles/47402591569805-Migrating-from-Agents-to-AI-by-Zapier','locator':'L35; L40–53; L69; L90; L120; L125; L127–132','supported_claim_zh':'未定停用日；单个AI step；默认工具不暂停，须逐工具启用批准；on-demand无直接等价触发；组织级BYOM未支持；列出的五种知识源未支持，Q4 2026为计划；支持源仍有规模/加载/权限差异。','scope':'只补迁移限制；不扩大迁移关系，不把计划当已上线。'}
e['official_evidence'][0]['independent_qa_r2']=check;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
p=out/'source-checks.json';sc=json.loads(p.read_text());next(x for x in sc if x['source_id']=='office-src-zap-migrate')['independent_qa_r2']=check;p.write_text(json.dumps(sc,ensure_ascii=False,indent=2)+'\n')
p=out/'REPORT.zh-CN.md';s=p.read_text();before=json.loads((old/'candidates.json').read_text())['edges'][0]['unknown_boundary_zh'];s=s.replace(before,e['unknown_boundary_zh']);s=s.replace('## 文件','## R2 独立 QA 修订\n- r1 原包保持原字节，完整副本保存在 `before-qa/`；修订只澄清统计口径及 Zapier 迁移边界，不改变12条 source/target/type/source_ids。\n- Zapier 官方迁移页由独立 QA 再次打开：L35、L40–53、L69、L90、L120、L125、L127–132。默认审批、on-demand、BYOM 和知识源差异已写入第1条 unknown 边界；厂商未来计划不作现行事实。\n- 独立 QA 复算242/139/89/120及假设151/72/108吻合；第10条Kdenlive代理来源已在全局sources且官方页支持，虽不直接列于该节点source_ids，不能视为缺失来源或据此重写节点。\n\n## 文件')
s=s.replace('- build_research.py：仅使用本地 JSON 与只读 git 的复核脚本；只写本研究目录。','- before-qa/build_research.py：原r1生成脚本，仅作为原字节存档，不应在r2下运行。\n- changes.json / manifest.json：修订说明与原字节完整性。');p.write_text(s)
# Verify original byte retention and identities.
retained={str(p.relative_to(old)):hashlib.sha256(p.read_bytes()).hexdigest() for p in old.rglob('*') if p.is_file()}
assert all((out/'before-qa'/k).read_bytes()==(old/k).read_bytes() for k in retained)
a=json.loads((old/'candidates.json').read_text());b=json.loads((out/'candidates.json').read_text());keys=['id','source','target','type','source_ids','explanation_zh','evidence_type']
assert [[e[k] for k in keys] for e in a['edges']]==[[e[k] for k in keys] for e in b['edges']]
p=out/'validation.json';valid=json.loads(p.read_text());valid.update(r1_bytes_preserved=True,candidate_identity_and_relation_claims_unchanged=True,only_edge_01_unknown_and_source_qa_enriched=True,graph_scope_explicit=True,independent_qa_statistics_agree=True,revision_status='frozen_after_independent_qa_comments');p.write_text(json.dumps(valid,ensure_ascii=False,indent=2)+'\n')
changes={'from':'knowledge-graph-links-research-r1','to':'knowledge-graph-links-research-r2','changes':['新增graph_scope/excluded_links，孤立及弱连通分量仅D.edges内部关系','明确已有practice registry/AgentWork等链接不计入，孤立不代表网页无链接','全部after指标明确未应用假设，不据增加边宣称准确性提升','边01仅补Zapier迁移默认审批/on-demand/BYOM/知识源限制和独立QA来源定位'],'unchanged':['12条关系source/target/type/source_ids与解释','全部图统计值','canonical仓库与原始研究'],'r1_preserved_sha256':retained}
(out/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(out/'DRAFT_STATUS.txt').unlink()
manifest={'status':'frozen','revision':'r2','root_files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']},'before_qa_sha256':retained}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS'))
print((out/'SHA256SUMS').read_text())
