# 知识图谱连接候选研究 R2

固定语义基线 `d6b2c248ee73317fcce4cca8a031b6a2722507df`；观察 HEAD `5f4f7f3ed69a62e0a601b98f3056a72ef6cb85c1`。与固定提交 `dist/data.json` 的 JSON 对象比较一致。

## 结果先行
242 节点、139 边，89 个孤立节点（36.78%）。本包提出 12 条 existing-node → existing-node 候选：1 条官方迁移关系、11 条明确标注的编辑学习对照。全部端点与 source_ids 已收录；按双向节点对检查均不重复现有边。未修改 canonical。

若未来经审核全数接纳，边数为151，孤立节点将由89降到72；这只是静态假设，不是已应用结果。不要为了消除孤立强造关系；这批仍可能形成独立学习小组，而非统一连通图。

## 统计口径：仅内部知识图谱，不是网页全部链接

本报告只统计 canonical `dist/data.json` 的 `nodes` 与 `edges`（D.nodes / D.edges）。孤立度数仅将 D.edges 的 source/target 入边与出边相加；弱连通分量仅将这些边忽略方向计算。

**明确排除** practice registry / learning_paths 实践与学习路径链接、`nodes.agentwork_links` 及其他 AgentWork 跨站链接、来源 URL、正文 Markdown 链接和网页导航链接。因此“89个孤立节点”只表示内部 D.edges 无边，**不表示节点或网页没有任何链接**；已有实践链接仍存在。增加边不等于知识准确性提升，更不能推出厂商集成。

139→151条边、孤立89→72、弱连通分量120→108均为12候选全部接纳时的**未应用静态假设复算**；当前 canonical 未改动。

## 孤立分布（仅 D.edges 的入边+出边）

| 类别 | 节点数 | 孤立数 |
|---|---:|---:|
| agent_tools | 3 | 0 |
| agents | 14 | 0 |
| alignment | 3 | 0 |
| assistant-workspaces | 8 | 8 |
| coding_agents | 3 | 0 |
| creative-design | 19 | 10 |
| creative-music | 18 | 18 |
| creative-video | 1 | 1 |
| data | 4 | 4 |
| deployment | 6 | 1 |
| evaluation | 33 | 10 |
| foundations | 8 | 0 |
| frontiers | 4 | 1 |
| inference | 2 | 0 |
| media-evaluation | 11 | 11 |
| memory | 2 | 0 |
| model-families | 10 | 0 |
| multimodal | 6 | 1 |
| office-agent-systems | 11 | 11 |
| organizations | 12 | 0 |
| quantization | 4 | 1 |
| reasoning | 3 | 1 |
| regional-office-platforms | 7 | 7 |
| retrieval | 6 | 0 |
| text-models | 14 | 0 |
| training | 2 | 0 |
| video-production | 16 | 4 |
| world-models-embodied | 12 | 0 |

office 11/11、assistant 8/8、regional 7/7 均孤立；world-model 12 个均已有边。creative-music 孤立18个，不宜靠 vendor 或“都生成音频”强连。完整89个ID及连通分量见 statistics.json。

## 候选关系与证据
编辑关系箭头仅表示建议阅读方向；官方来源支持两端的事实，不代表厂商主张二者关联。

### kgl-r1-01 · Zapier Agents → AI by Zapier（agentic step）
- source / target / type：`office-zapier-agents` → `office-ai-by-zapier` / `documented_migration_target`
- 解释：官方明确旧 Agents 向 Zap 编辑器里的 AI by Zapier 迁移；教学重点是迁移前盘点触发器、工具和审批，不将“迁移目标”误写为已停用。
- 证据类型：`official_documented_product_migration`
- unknown 边界：官方未定 Agents 停用日；每账户迁移状态及实际运行均 unknown，不宣称迁移完成或全部功能等价。工具默认不暂停，须逐工具开启 Require approval；聊天 on-demand 暂无直接等价触发；组织级 BYOM 未支持。HubSpot/Asana/Zendesk/Zoom/Jira 知识源尚未支持，Q4 2026 仅为计划；已支持来源仍有规模、加载和权限差异。
- 已收录 `office-src-zap-migrate`：[官方来源](https://help.zapier.com/hc/en-us/articles/47402591569805-Migrating-from-Agents-to-AI-by-Zapier)；定位：Why Agents is migrating; When to migrate; How to migrate; lines 6–18, 33–53；官方迁移目标；迁移仍保留单个 AI step，未给 Agents 关闭日期。（本轮官方页复核）

### kgl-r1-02 · n8n AI Agent node + human review → Dify
- source / target / type：`office-n8n-ai-agent` → `regional-dify` / `editorial_learning_relation`
- 解释：对照工具执行前的人审与工作流 Human Input 暂停：练习画出“何处暂停、谁能批准、拒绝后如何继续”的不同边界。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不是互相集成或等价安全保证；n8n 仅接入审核的工具受保护，Dify 邮件链接持有者可响应；未验证租户权限。
- 已收录 `office-src-n8n-hitl`：[官方来源](https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md)；定位：Human-in-the-loop for tools; Approve/Deny; raw_office_record.confirmation_boundary；接到 human review 的工具调用前暂停，批准按给定输入执行，拒绝取消操作并通知 AI。（复用已收录原始官方文档研究）
- 已收录 `regional-src-dify-human`：[官方来源](https://docs.dify.ai/en/cloud/use-dify/nodes/human-input)；定位：Human Input: pause, delivery methods, first response；工作流暂停等待输入；邮件链接持有者可响应，首个响应关闭请求。（复用已收录原始官方文档研究）

### kgl-r1-03 · Coze Studio → Dify
- source / target / type：`regional-coze-studio` → `regional-dify` / `editorial_learning_relation`
- 解释：同为可自托管的 Agent/工作流平台，学习将平台、模型服务、插件凭据和部署责任拆开；源码许可不可由“开源平台”标签统一推导。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不比较优劣、不声称兼容；两者 main 未锁定；Coze 托管产品不等同 Studio，Dify 附加条件不扩推为法律结论。
- 已收录 `regional-src-coze-repo`：[官方来源](https://github.com/coze-dev/coze-studio)；定位：README: features, model setup, security warning；可视化 Agent/工作流平台，模型和插件另配置；公开部署有安全提示。（复用已收录原始官方文档研究）
- 已收录 `regional-src-coze-license`：[官方来源](https://github.com/coze-dev/coze-studio/blob/main/LICENSE-APACHE)；定位：LICENSE-APACHE；该许可证文件为 Apache-2.0。（复用已收录原始官方文档研究）
- 已收录 `regional-src-dify-repo`：[官方来源](https://github.com/langgenius/dify)；定位：README: features / deployment；Agent/RAG/workflow 平台，有云和自托管部署。（复用已收录原始官方文档研究）
- 已收录 `regional-src-dify-license`：[官方来源](https://github.com/langgenius/dify/blob/main/LICENSE)；定位：LICENSE: additional conditions；修改版 Apache-2.0，带多租户和前端品牌条件；非法律建议。（复用已收录原始官方文档研究）

### kgl-r1-04 · Deep research in ChatGPT → Research in Claude
- source / target / type：`assistant-chatgpt-deep-research` → `assistant-claude-research` / `editorial_learning_relation`
- 解释：研究助手的方法对照：来源范围、引用核验与连接器调用权限需要分开；ChatGPT Chat 研究使用应用读取动作，Claude Research 已启用连接工具可自动调用。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不推定同一模型、互通或同一权限机制；Claude mobile 与 web/desktop 来源不同，本地 MCP 不等同 Research 连接器；账户资格未知。
- 已收录 `assistant-src-oa-dr-help`：[官方来源](https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt)；定位：L15–24; L31–59; L62–88；Chat 研究可审改计划、限定站点、核验引用；连接应用仅使用读取动作。套餐/地区/角色决定来源和额度。（复用已收录原始官方文档研究）
- 已收录 `assistant-src-cl-research`：[官方来源](https://support.claude.com/en/articles/11088861-use-research-on-claude)；定位：Availability; Use research; FAQ；Research需付费及web search；移动端仅web，web/desktop可用已连接工具。研究调用连接工具不逐次确认，不支持桌面本地MCP。（复用已收录原始官方文档研究）

### kgl-r1-05 · Deep Research in Gemini Apps → Deep research in ChatGPT
- source / target / type：`assistant-gemini-apps-deep-research` → `assistant-chatgpt-deep-research` / `editorial_learning_relation`
- 解释：以“先审计划、再审来源、最后核对引文”形成跨研究助手学习路径；两者文档均支持研究计划审改。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：仅 Gemini Apps 与 ChatGPT Chat 范围，不包含 API、Work 或 Workspace Studio；额度、客户端和来源接入不能相互继承。
- 已收录 `assistant-src-g-dr`：[官方来源](https://support.google.com/gemini/answer/15719111?hl=en)；定位：L19–55; L64–104；18岁以上登录用户；可改计划后启动研究；默认Search，可选择其他来源。Pro/Ultra有较高额度；Workspace来源须连接。（复用已收录原始官方文档研究）
- 已收录 `assistant-src-oa-dr-help`：[官方来源](https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt)；定位：L15–24; L31–59; L62–88；Chat 研究可审改计划、限定站点、核验引用；连接应用仅使用读取动作。套餐/地区/角色决定来源和额度。（复用已收录原始官方文档研究）

### kgl-r1-06 · Perplexity Research / Deep Research → Perplexity Create files and apps（原 Labs）
- source / target / type：`assistant-perplexity-research` → `assistant-perplexity-create-files-apps` / `editorial_learning_relation`
- 解释：把研究报告与可操作产物分开学习：前者主张必须可追溯，后者表格公式、文件和简单应用需要单独验收。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：同一产品里的两功能也不推出自动交接、相同模型或审批；生成/发布具体人审机制和账户额度未知，历史 Labs 全量迁移未知。
- 已收录 `assistant-src-p-pro`：[官方来源](https://www.perplexity.ai/help-center/en/articles/10352901-what-is-perplexity-pro)；定位：Research Mode; Create files and apps；Research自动选模型做深入报告；Create files and apps可生成报告、表格、仪表板、简单web应用。（复用已收录原始官方文档研究）

### kgl-r1-07 · Genie（2024 研究系统） → CogVideoX
- source / target / type：`wm-genie` → `vid-cogvideox` / `editorial_learning_relation`
- 解释：区分可行动控制的生成环境与文本条件视频生成：Genie 以潜在动作逐帧交互，CogVideoX 论文描述视频扩散 Transformer。学会问“动作改变未来”还是“文字描述画面”。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不是技术派生、组件依赖或同等物理真实性；Genie 限 2024 研究系统，CogVideoX 来源为论文 v3；不推广到各版本规格。
- 已收录 `wm-src-paper-genie`：[官方来源](https://arxiv.org/abs/2402.15391)；定位：arXiv abstract lines 14–16; v1；无动作标签视频训练；潜在动作模型与逐帧可控生成环境。（本轮作者论文摘要复核）
- 已收录 `vid-src-cogpaper`：[官方来源](https://arxiv.org/abs/2408.06072)；定位：arXiv v3 abstract lines 15–18；文本到视频扩散 Transformer，3D VAE 压缩时空维度。（本轮作者论文摘要复核）

### kgl-r1-08 · V-JEPA → CogVideoX
- source / target / type：`wm-vjepa` → `vid-cogvideox` / `editorial_learning_relation`
- 解释：对照视频表征预测与像素视频生成：V-JEPA 在抽象表征空间预测遮挡部分，CogVideoX 以 3D VAE 和扩散 Transformer 生成视频。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不是互相使用或性能排名；原 V-JEPA 不等于后续动作条件 V-JEPA 2；预测表征不自动构成机器人规划能力。
- 已收录 `wm-src-vjepa-blog`：[官方来源](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)；定位：Video JEPA in focus; lines 55–62；非生成模型，在抽象表征空间预测遮挡的视频区域。（本轮官方页复核）
- 已收录 `vid-src-cogpaper`：[官方来源](https://arxiv.org/abs/2408.06072)；定位：arXiv v3 abstract lines 15–18；文本到视频扩散 Transformer，3D VAE 压缩时空维度。（本轮作者论文摘要复核）

### kgl-r1-09 · Adobe Express AI Assistant → Canva模板数据填充与导出
- source / target / type：`creative-express-ai-assistant` → `design-canva-template` / `editorial_learning_relation`
- 解释：设计任务的两种约束方式：会话局部修改及手工接管，对照结构化品牌模板填充；用文字、版式不变量和人工验收连接，而非把二者都称生成模型。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：无跨产品集成、素材互用或权限继承结论；Express 地域/计划与 Canva 模板资格独立核验；实际保真未知。
- 已收录 `creative-gap-src-express-how`：[官方来源](https://helpx.adobe.com/express/web/ai-assistant/get-started-with-the-adobe-express-ai-assistant.html)；定位：L712–750；主页提示、补信息、四候选、对话修改/手工编辑/Download；Chats不共享给协作者。（复用已收录原始官方文档研究）
- 已收录 `design-src-canva-autofill`：[官方来源](https://www.canva.dev/docs/apps/rest-apis/autofill-guide/)；定位：Autofill guide: brand template data filling；数据填充品牌模板的文档工作流。（复用已收录原始官方文档研究）

### kgl-r1-10 · Descript Underlord → Kdenlive 字幕与转录剪辑
- source / target / type：`creative-underlord` → `vid-kdenlive` / `editorial_learning_relation`
- 解释：把 AI 粗剪审查接到通用剪辑交付知识：Underlord 恢复需检查全项目与协作者变更，Kdenlive 代理预览与原片渲染需区分；二者共同用于讲“预览不是最终交付验收”。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：纯编辑方法对照，不保证项目格式互通、自动导入或回滚等价；未测试恢复、代理或渲染；不保证无限版本保留。
- 已收录 `creative-gap-src-underlord-help`：[官方来源](https://help.descript.com/getting-started/underlord-beta-your-ai-co-editor-in-descript)；定位：L249–269；Beta co-editor；项目右侧入口；可选底层模型；提示推理及工具均计积分，成本非确定。（复用已收录原始官方文档研究）
- 已收录 `creative-gap-src-underlord-history-independent`：[官方来源](https://help.descript.com/working-in-projects/version-history)；定位：L249–252；可预览版本，Restore出现协作者冲突确认；恢复影响项目所有compositions/files，必须先审查协作者变更。（复用已收录原始官方文档研究）
- 已收录 `creative-gap-src-kden-proxy`：[官方来源](https://docs.kdenlive.org/en/user_interface/menu/media_menu.html)；定位：Proxy Clip lines 352–359；26.08手册：启用项目代理后创建Proxy Clip；P标记；最终渲染使用原素材。（复用已收录原始官方文档研究）

### kgl-r1-11 · MusicGen v1 → Ableton Live comping / linked-track editing
- source / target / type：`music-musicgen` → `creative-ableton-live` / `editorial_learning_relation`
- 解释：区分音乐生成草图与录音编辑：MusicGen 是条件音乐模型，Live comping 从多个录次选择片段；教学上分别检查创意内容与接点/同步，不把 DAW 当音乐 Agent。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不宣称原生集成或输出可商用；MusicGen 权重许可与 Live/录音/素材许可独立，实际导入与音质未知。
- 已收录 `music-src-musicgen`：[官方来源](https://github.com/facebookresearch/audiocraft/blob/main/model_cards/MUSICGEN_MODEL_CARD.md)；定位：Model details lines 178–184; Intended use lines 187–194；v1 为音频 token 自回归音乐模型，含文本条件与旋律引导变体；代码 MIT，权重 CC-BY-NC 4.0。（本轮官方模型卡复核）
- 已收录 `creative-gap-src-ableton-comp`：[官方来源](https://help.ableton.com/hc/en-us/articles/360019092580-Comping-in-Live-FAQ)；定位：Comping FAQ lines 13–27, 59–61；Comping自Live 11起；Take Lanes/Draw Mode；Intro/Standard/Suite支持comping，linked-track editing限Standard/Suite。（复用已收录原始官方文档研究）

### kgl-r1-12 · Adobe InDesign Package / Preflight → C2PA素材来源链
- source / target / type：`creative-indesign` → `design-c2pa` / `editorial_learning_relation`
- 解释：区分交付打包、资产授权与内容来源凭证：InDesign Package 组织交付资产，C2PA 描述签名和来源链；有包或有效凭证都不等于拥有字体/素材版权。
- 证据类型：`editorial_learning_relation_not_vendor_integration_claim`
- unknown 边界：不声称 InDesign Package 实现 C2PA 或自动附凭证；具体文件签名、完整版权与收件方许可均未验证。
- 已收录 `creative-gap-src-indesign-package`：[官方来源](https://helpx.adobe.com/indesign/desktop/print/preflight/package-files-for-output.html)；定位：body lines 1414–1439；File Package前预检；可包含链接、IDML、PDF；Adobe Fonts激活字体不拷入；隐藏非打印资产有可选包含项。（复用已收录原始官方文档研究）
- 已收录 `creative-gap-src-font-licensing-faq-independent`：[官方来源](https://helpx.adobe.com/fonts/web/font-licensing/font-licensing.html)；定位：lines 116–117,128–130,137–152；不同官方页面独立支持：Adobe Fonts文件不能转移/打包；直接编辑需收件人自有许可；正确嵌入PDF与传递字体文件不同；本地其他字体依各自EULA。不是失败原页成功。（复用已收录原始官方文档研究）
- 已收录 `design-src-c2pa`：[官方来源](https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html)；定位：C2PA Specification 2.5: claims, assertions, signatures, validation；签名、绑定、断言与验证用于来源链，不能单独证明内容真实或版权所有。（复用已收录原始官方文档研究）

## 研究边界与复核方式
- 先读取 canonical 原始研究（office raw_office_record、assistant raw/research.json、regional raw_regional_office、world-model raw_research、creative-gaps r2）及派生 source 映射。原始材料只摘要，不搬运网页全文。
- 本轮重新打开5个来源：Zapier迁移页、Genie摘要、CogVideoX摘要、Meta V-JEPA公告、MusicGen官方模型卡。其余严格复用同日原始官方文档核验，不伪称重新访问。原有 unknown/版本限制均保留。
- 未执行任何 SDK、模型、产品、账户、网络服务写操作；未操作 Mac、密钥、发布、仓库改动。
- 不增加节点，不重写原始研究，不把全部产品称为模型或 Agent，不推断权限继承、底层模型、vendor关系或产品互操作。
- source-checks.json 为每条来源保留精确 URL、章节/原核验行号、证据摘要、复用/重查状态；旧行号仅定位当时观察，滚动网页可能变化。
- 未来整合前应重新查端点和已有边，显式保留 editorial 标记，不使用技术依赖箭头解释教学对照；评测/运行效果必须另立证据。

## R2 独立 QA 修订
- r1 原包保持原字节，完整副本保存在 `before-qa/`；修订只澄清统计口径及 Zapier 迁移边界，不改变12条 source/target/type/source_ids。
- Zapier 官方迁移页由独立 QA 再次打开：L35、L40–53、L69、L90、L120、L125、L127–132。默认审批、on-demand、BYOM 和知识源差异已写入第1条 unknown 边界；厂商未来计划不作现行事实。
- 独立 QA 复算242/139/89/120及假设151/72/108吻合；第10条Kdenlive代理来源已在全局sources且官方页支持，虽不直接列于该节点source_ids，不能视为缺失来源或据此重写节点。

## 原始研究状态与未来派生应用记录

本包候选的 `integration_status=candidate_only_not_applied` 是研究产生时的真实状态，原始研究不得在未来被改写成“已部署”或“已应用”。若后续整合12条关系，必须另建派生应用/接纳记录，记录实际接纳的候选ID、目标提交、构建与验证结果；实时图关系和构建统计从该派生层取得，不能覆盖本包的历史候选状态。本轮未应用任何边。

## 文件
- candidates.json：12条结构化候选与逐条证据。
- statistics.json：全量类别、孤立ID、弱连通分量及假设影响。
- source-checks.json：本轮与复用官方来源摘要。
- validation.json：固定语义基线、端点、来源及双向去重检查。
- before-qa/build_research.py：原r1生成脚本，仅作为原字节存档，不应在r2下运行。
- changes.json / manifest.json：修订说明与原字节完整性。
