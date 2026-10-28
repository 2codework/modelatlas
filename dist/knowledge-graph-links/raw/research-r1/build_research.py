import json, pathlib, collections, hashlib, subprocess
ROOT=pathlib.Path('github-migration-r1/public/modelatlas'); OUT=pathlib.Path('knowledge-graph-links-research-r1')
p=json.loads((ROOT/'dist/data.json').read_text()); nodes={n['id']:n for n in p['nodes']}; sources={s['id']:s for s in p['sources']}
rows=[
('office-zapier-agents','office-ai-by-zapier','documented_migration_target','官方明确旧 Agents 向 Zap 编辑器里的 AI by Zapier 迁移；教学重点是迁移前盘点触发器、工具和审批，不将“迁移目标”误写为已停用。',['office-src-zap-migrate'],'停用日未定；每账户迁移状态、功能完全等价及实际运行均 unknown。'),
('office-n8n-ai-agent','regional-dify','editorial_learning_relation','对照工具执行前的人审与工作流 Human Input 暂停：练习画出“何处暂停、谁能批准、拒绝后如何继续”的不同边界。',['office-src-n8n-hitl','regional-src-dify-human'],'不是互相集成或等价安全保证；n8n 仅接入审核的工具受保护，Dify 邮件链接持有者可响应；未验证租户权限。'),
('regional-coze-studio','regional-dify','editorial_learning_relation','同为可自托管的 Agent/工作流平台，学习将平台、模型服务、插件凭据和部署责任拆开；源码许可不可由“开源平台”标签统一推导。',['regional-src-coze-repo','regional-src-coze-license','regional-src-dify-repo','regional-src-dify-license'],'不比较优劣、不声称兼容；两者 main 未锁定；Coze 托管产品不等同 Studio，Dify 附加条件不扩推为法律结论。'),
('assistant-chatgpt-deep-research','assistant-claude-research','editorial_learning_relation','研究助手的方法对照：来源范围、引用核验与连接器调用权限需要分开；ChatGPT Chat 研究使用应用读取动作，Claude Research 已启用连接工具可自动调用。',['assistant-src-oa-dr-help','assistant-src-cl-research'],'不推定同一模型、互通或同一权限机制；Claude mobile 与 web/desktop 来源不同，本地 MCP 不等同 Research 连接器；账户资格未知。'),
('assistant-gemini-apps-deep-research','assistant-chatgpt-deep-research','editorial_learning_relation','以“先审计划、再审来源、最后核对引文”形成跨研究助手学习路径；两者文档均支持研究计划审改。',['assistant-src-g-dr','assistant-src-oa-dr-help'],'仅 Gemini Apps 与 ChatGPT Chat 范围，不包含 API、Work 或 Workspace Studio；额度、客户端和来源接入不能相互继承。'),
('assistant-perplexity-research','assistant-perplexity-create-files-apps','editorial_learning_relation','把研究报告与可操作产物分开学习：前者主张必须可追溯，后者表格公式、文件和简单应用需要单独验收。',['assistant-src-p-pro'],'同一产品里的两功能也不推出自动交接、相同模型或审批；生成/发布具体人审机制和账户额度未知，历史 Labs 全量迁移未知。'),
('wm-genie','vid-cogvideox','editorial_learning_relation','区分可行动控制的生成环境与文本条件视频生成：Genie 以潜在动作逐帧交互，CogVideoX 论文描述视频扩散 Transformer。学会问“动作改变未来”还是“文字描述画面”。',['wm-src-paper-genie','vid-src-cogpaper'],'不是技术派生、组件依赖或同等物理真实性；Genie 限 2024 研究系统，CogVideoX 来源为论文 v3；不推广到各版本规格。'),
('wm-vjepa','vid-cogvideox','editorial_learning_relation','对照视频表征预测与像素视频生成：V-JEPA 在抽象表征空间预测遮挡部分，CogVideoX 以 3D VAE 和扩散 Transformer 生成视频。',['wm-src-vjepa-blog','vid-src-cogpaper'],'不是互相使用或性能排名；原 V-JEPA 不等于后续动作条件 V-JEPA 2；预测表征不自动构成机器人规划能力。'),
('creative-express-ai-assistant','design-canva-template','editorial_learning_relation','设计任务的两种约束方式：会话局部修改及手工接管，对照结构化品牌模板填充；用文字、版式不变量和人工验收连接，而非把二者都称生成模型。',['creative-gap-src-express-how','design-src-canva-autofill'],'无跨产品集成、素材互用或权限继承结论；Express 地域/计划与 Canva 模板资格独立核验；实际保真未知。'),
('creative-underlord','vid-kdenlive','editorial_learning_relation','把 AI 粗剪审查接到通用剪辑交付知识：Underlord 恢复需检查全项目与协作者变更，Kdenlive 代理预览与原片渲染需区分；二者共同用于讲“预览不是最终交付验收”。',['creative-gap-src-underlord-help','creative-gap-src-underlord-history-independent','creative-gap-src-kden-proxy'],'纯编辑方法对照，不保证项目格式互通、自动导入或回滚等价；未测试恢复、代理或渲染；不保证无限版本保留。'),
('music-musicgen','creative-ableton-live','editorial_learning_relation','区分音乐生成草图与录音编辑：MusicGen 是条件音乐模型，Live comping 从多个录次选择片段；教学上分别检查创意内容与接点/同步，不把 DAW 当音乐 Agent。',['music-src-musicgen','creative-gap-src-ableton-comp'],'不宣称原生集成或输出可商用；MusicGen 权重许可与 Live/录音/素材许可独立，实际导入与音质未知。'),
('creative-indesign','design-c2pa','editorial_learning_relation','区分交付打包、资产授权与内容来源凭证：InDesign Package 组织交付资产，C2PA 描述签名和来源链；有包或有效凭证都不等于拥有字体/素材版权。',['creative-gap-src-indesign-package','creative-gap-src-font-licensing-faq-independent','design-src-c2pa'],'不声称 InDesign Package 实现 C2PA 或自动附凭证；具体文件签名、完整版权与收件方许可均未验证。')]
# Historical raw source evidence reused; no upstream full text copied.
locators={
'music-src-musicgen':('本轮官方模型卡复核','Model details lines 178–184; Intended use lines 187–194','v1 为音频 token 自回归音乐模型，含文本条件与旋律引导变体；代码 MIT，权重 CC-BY-NC 4.0。'),
'office-src-zap-migrate':('本轮官方页复核','Why Agents is migrating; When to migrate; How to migrate; lines 6–18, 33–53','官方迁移目标；迁移仍保留单个 AI step，未给 Agents 关闭日期。'),
'wm-src-paper-genie':('本轮作者论文摘要复核','arXiv abstract lines 14–16; v1','无动作标签视频训练；潜在动作模型与逐帧可控生成环境。'),
'vid-src-cogpaper':('本轮作者论文摘要复核','arXiv v3 abstract lines 15–18','文本到视频扩散 Transformer，3D VAE 压缩时空维度。'),
'wm-src-vjepa-blog':('本轮官方页复核','Video JEPA in focus; lines 55–62','非生成模型，在抽象表征空间预测遮挡的视频区域。'),
'office-src-n8n-hitl':('复用已收录原始官方文档研究','Human-in-the-loop for tools; Approve/Deny; raw_office_record.confirmation_boundary','接到 human review 的工具调用前暂停，批准按给定输入执行，拒绝取消操作并通知 AI。'),
'regional-src-dify-human':('复用已收录原始官方文档研究','Human Input: pause, delivery methods, first response','工作流暂停等待输入；邮件链接持有者可响应，首个响应关闭请求。'),
'regional-src-coze-repo':('复用已收录原始官方文档研究','README: features, model setup, security warning','可视化 Agent/工作流平台，模型和插件另配置；公开部署有安全提示。'),
'regional-src-coze-license':('复用已收录原始官方文档研究','LICENSE-APACHE','该许可证文件为 Apache-2.0。'),
'regional-src-dify-repo':('复用已收录原始官方文档研究','README: features / deployment','Agent/RAG/workflow 平台，有云和自托管部署。'),
'regional-src-dify-license':('复用已收录原始官方文档研究','LICENSE: additional conditions','修改版 Apache-2.0，带多租户和前端品牌条件；非法律建议。'),
'design-src-canva-autofill':('复用已收录原始官方文档研究','Autofill guide: brand template data filling','数据填充品牌模板的文档工作流。'),
'design-src-c2pa':('复用已收录原始官方文档研究','C2PA Specification 2.5: claims, assertions, signatures, validation','签名、绑定、断言与验证用于来源链，不能单独证明内容真实或版权所有。')}
used=sorted({s for row in rows for s in row[4]}); checks=[]
for sid in used:
 s=sources[sid]; qa=s.get('independent_qa',{})
 mode,loc,claim=locators.get(sid,('复用已收录原始官方文档研究',s.get('evidence_locator') or qa.get('evidence_locator') or '原始来源记录所列章节',s.get('supported_claim') or s.get('evidence_summary_zh') or s.get('verified_claim') or s.get('claim_scope') or s.get('evidence_scope')))
 checks.append(dict(source_id=sid,url=s['url'],evidence_mode=mode,locator=loc,supported_claim_zh=claim,checked_at='2026-10-28',runtime_verified=False))
cm={c['source_id']:c for c in checks}; candidates=[]
for i,(a,b,t,ex,ss,unknown) in enumerate(rows,1):
 candidates.append(dict(id=f'kgl-r1-{i:02}',source=a,target=b,type=t,explanation_zh=ex,evidence_type='official_documented_product_migration' if i==1 else 'editorial_learning_relation_not_vendor_integration_claim',source_ids=ss,official_evidence=[cm[s] for s in ss],unknown_boundary_zh=unknown,verification_status='documentation_review_not_runtime_verified',integration_status='candidate_only_not_applied',direction_semantics='旧入口到文档迁移目标' if i==1 else '建议阅读顺序；非技术依赖方向'))
deg=collections.Counter(x[k] for x in p['edges'] for k in ['source','target']); cat=collections.defaultdict(lambda:dict(total=0,isolated_ids=[]))
for n in nodes.values():
 cat[n['category']]['total']+=1
 if not deg[n['id']]:cat[n['category']]['isolated_ids'].append(n['id'])
def components(edges):
 adj={i:set() for i in nodes}
 for e in edges:adj[e['source']].add(e['target']);adj[e['target']].add(e['source'])
 seen=set();sizes=[]
 for i in adj:
  if i in seen:continue
  q=[i];seen.add(i);z=0
  while q:
   j=q.pop();z+=1
   for k in adj[j]-seen:seen.add(k);q.append(k)
  sizes.append(z)
 return sorted(sizes,reverse=True)
isolated=[i for i in nodes if not deg[i]]; touched=set(x[k] for x in candidates for k in ['source','target'])
stats=dict(node_count=len(nodes),edge_count=len(p['edges']),isolated_count=len(isolated),isolated_percentage=round(100*len(isolated)/len(nodes),2),isolated_ids=isolated,by_category=dict(cat),weak_component_sizes=components(p['edges']),hypothetical_only=dict(candidate_edges=len(candidates),previously_isolated_touched=sorted(touched&set(isolated)),remaining_isolated=len(set(isolated)-touched),component_sizes=components(p['edges']+candidates)))
head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
baseline=dict(requested_semantic_head='d6b2c248ee73317fcce4cca8a031b6a2722507df',observed_head=head,note='父任务说明新 HEAD 5f4f7f3ed69a62e0a601b98f3056a72ef6cb85c1 仅紧凑 JSON 排版且对象相同；本研究另在 validation 中检查固定提交对象。',data_sha256=hashlib.sha256((ROOT/'dist/data.json').read_bytes()).hexdigest())
# Compare actual JSON objects against pinned semantic baseline, independent of parent statement.
old=json.loads(subprocess.check_output(['git','-C',str(ROOT),'show','d6b2c248ee73317fcce4cca8a031b6a2722507df:dist/data.json']))
existing={frozenset((e['source'],e['target'])) for e in p['edges']}
validation=dict(baseline_json_object_equal=(old==p),counts_match=(len(nodes)==242 and len(p['edges'])==139),all_endpoints_existing=all(e[k] in nodes for e in candidates for k in ['source','target']),all_source_ids_existing=all(s in sources for e in candidates for s in e['source_ids']),no_existing_edge_either_direction=all(frozenset((e['source'],e['target'])) not in existing for e in candidates),candidate_pairs_unique=len({frozenset((e['source'],e['target'])) for e in candidates})==len(candidates),canonical_worktree_clean=(subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain'],text=True)==''),canonical_modified=False,product_sdk_model_account_executed=False)
assert all(validation[k] for k in ['baseline_json_object_equal','counts_match','all_endpoints_existing','all_source_ids_existing','no_existing_edge_either_direction','candidate_pairs_unique'])
for name,obj in [('candidates.json',dict(schema_version='knowledge-graph-links-research-r1',baseline=baseline,scope='有限代表性关系候选；非全集，未整合，非运行验证',edges=candidates)),('statistics.json',stats),('source-checks.json',checks),('validation.json',validation)]: (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
lines=['# 知识图谱连接候选研究 R1','',f'固定语义基线 `{baseline["requested_semantic_head"]}`；观察 HEAD `{head}`。与固定提交 `dist/data.json` 的 JSON 对象比较一致。','',f'## 结果先行\n242 节点、139 边，89 个孤立节点（{stats["isolated_percentage"]}%）。本包提出 12 条 existing-node → existing-node 候选：1 条官方迁移关系、11 条明确标注的编辑学习对照。全部端点与 source_ids 已收录；按双向节点对检查均不重复现有边。未修改 canonical。','',f'若未来经审核全数接纳，边数为151，孤立节点将由89降到{stats["hypothetical_only"]["remaining_isolated"]}；这只是静态假设，不是已应用结果。不要为了消除孤立强造关系；这批仍可能形成独立学习小组，而非统一连通图。','', '## 孤立分布（度数按入边+出边，忽略方向判断孤立）','', '| 类别 | 节点数 | 孤立数 |','|---|---:|---:|']
for c,v in sorted(cat.items()):lines.append(f'| {c} | {v["total"]} | {len(v["isolated_ids"])} |')
lines+=['','office 11/11、assistant 8/8、regional 7/7 均孤立；world-model 12 个均已有边。creative-music 孤立18个，不宜靠 vendor 或“都生成音频”强连。完整89个ID及连通分量见 statistics.json。','', '## 候选关系与证据','编辑关系箭头仅表示建议阅读方向；官方来源支持两端的事实，不代表厂商主张二者关联。']
for e in candidates:
 lines += ['',f'### {e["id"]} · {nodes[e["source"]]["title"]} → {nodes[e["target"]]["title"]}',f'- source / target / type：`{e["source"]}` → `{e["target"]}` / `{e["type"]}`',f'- 解释：{e["explanation_zh"]}',f'- 证据类型：`{e["evidence_type"]}`',f'- unknown 边界：{e["unknown_boundary_zh"]}']
 for ev in e['official_evidence']:lines.append(f'- 已收录 `{ev["source_id"]}`：[官方来源]({ev["url"]})；定位：{ev["locator"]}；{ev["supported_claim_zh"]}（{ev["evidence_mode"]}）')
lines+=['','## 研究边界与复核方式','- 先读取 canonical 原始研究（office raw_office_record、assistant raw/research.json、regional raw_regional_office、world-model raw_research、creative-gaps r2）及派生 source 映射。原始材料只摘要，不搬运网页全文。','- 本轮重新打开5个来源：Zapier迁移页、Genie摘要、CogVideoX摘要、Meta V-JEPA公告、MusicGen官方模型卡。其余严格复用同日原始官方文档核验，不伪称重新访问。原有 unknown/版本限制均保留。','- 未执行任何 SDK、模型、产品、账户、网络服务写操作；未操作 Mac、密钥、发布、仓库改动。','- 不增加节点，不重写原始研究，不把全部产品称为模型或 Agent，不推断权限继承、底层模型、vendor关系或产品互操作。','- source-checks.json 为每条来源保留精确 URL、章节/原核验行号、证据摘要、复用/重查状态；旧行号仅定位当时观察，滚动网页可能变化。','- 未来整合前应重新查端点和已有边，显式保留 editorial 标记，不使用技术依赖箭头解释教学对照；评测/运行效果必须另立证据。','', '## 文件','- candidates.json：12条结构化候选与逐条证据。','- statistics.json：全量类别、孤立ID、弱连通分量及假设影响。','- source-checks.json：本轮与复用官方来源摘要。','- validation.json：固定语义基线、端点、来源及双向去重检查。','- build_research.py：仅使用本地 JSON 与只读 git 的复核脚本；只写本研究目录。']
(OUT/'REPORT.zh-CN.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'validation':validation,'isolated':len(isolated),'remaining_hypothetical':stats['hypothetical_only']['remaining_isolated'],'components_before':len(stats['weak_component_sizes']),'components_hypothetical':len(stats['hypothetical_only']['component_sizes'])},ensure_ascii=False))
