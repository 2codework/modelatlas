"""Additive, static bilingual technical learning portal. No research mutation."""
from pathlib import Path
from html import escape
import shutil

CONTENT = {}
CONTENT['zh'] = {
'nav':['系统学 AI','开发 Agent','AI 发展史','多模态技术','模型与资料','评测与方法'],
'hero':'理解 AI 的底层原理，<br>开发自己的 Agent。',
'lede':'从一个机制到一段可检查的实现。为入行者、程序员和想了解 AI 发展的管理者，把原理、工程与技术变化连起来。',
'goals':[('学原理','从模型、token 到工具调用','foundations'),('做开发','做一个有证据的资料问答 Agent','project'),('看进展','分清谁发布了什么、日期意味着什么','timeline')],
'audience':'选择阅读深度，不是给自己贴标签',
'roles':[('入行者','先读三节基础课，用自己的话解释机制，再做项目自检。','foundations'),('开发者','从输入输出契约、适配器和状态机进入离线实验。','project'),('管理者','先读发展史与多模态，再判断能力边界、风险和工程投入。','timeline')],
'path':'一条能走完的学习路径',
'pathtext':'01 区分模型与系统 → 02 理解 token 与 attention → 03 工具与记忆边界 → 04 实现资料问答 → 05 设计失败测试。无需账号；未做试学计时，不承诺学习时长。',
'projectteaser':'你的第一座实验台：资料问答 Agent',
'projecttext':'三份合成资料，一个只读检索工具，读前与答复发布前两次人工确认。学会让系统引用证据、在资料不足时拒答，并在失败时有界停止。提供 Python 标准库源码与测试；这是确定性模拟，不是大模型实测。',
'enter':'进入完整项目 →',
'changes':'三个值得理解的技术变化',
'changeitems':[('从词序列到 attention','attention 根据当前上下文计算表示，不能把权重图理解为真实因果解释。','tokens'),('从生成文本到调用工具','模型可提出动作；授权、校验与执行仍由宿主程序负责。','tools'),('从单帧生成到视频系统','时间一致性、控制条件和资源限制成为新的评估维度。','multimodal')],
'legacy':'旧版中文延伸阅读（尚未完成英文翻译）',
'legacytext':'目录、月度事件和旧课程保留原身份、日期与学习记录。它们是学习支撑，不是完整模型市场，也不是性能排行榜。',
'search':'搜索核心课程、项目与实验', 'placeholder':'例如：记忆 / attention / 拒答 / 视频', 'searchhint':'搜索双语课程与实验；空格组合词须全部匹配，支持中文片段与英文词首。历史实体请进入模型与资料。',
'market':'参考地区','language':'语言','unknown':'未指定 / 通用','regionnote':'地区只用于依赖提示：本站离线模拟不需要服务账号；真实 API 的地区、账户、费用与许可尚未逐项核验。选择地区不代表可用，也不会隐藏原理。',
'footer':'原创教学解释 · 核心中英内容等价 · 2026-11-01 教学版本，不刷新历史事实核验日期。无账号、无定位、无追踪；本地已读不等于掌握。',
'read':'标记已读','readDone':'已读（不代表掌握）','progress':'记录仅存于当前浏览器；旧版学习记录保留。',
'chapters':[
('foundations','01 · 系统学 AI','模型、应用与 Agent：到底差在哪？','前置：无。产出：能把一次资料问答拆成模型能力、应用逻辑和 Agent 控制循环。', '''
<p><strong>模型</strong>是把输入映射到输出的参数化计算系统。语言模型通常根据已有 token 序列预测后续 token；它并不天然拥有浏览器、公司资料库或付款权限。<strong>应用</strong>把模型放进产品流程，加上界面、检索、规则和权限。<strong>Agent</strong>在这里指一个受约束的系统：根据状态选择下一步动作，调用允许的工具，观察结果，再决定继续或停止。业内定义不完全统一；不能仅凭产品名字判断自主性。</p>
<div class="flow" aria-label="系统分层"><span>问题与允许资料</span><b>→</b><span>宿主：规则与循环</span><b>↔</b><span>模型 / 适配器</span><b>→</b><span>只读工具与证据</span></div>
<p>例如“报销上限是多少？”：模型可以生成流畅句子，但应用必须决定查询哪份制度、使用哪个版本。Agent 可以先检索，再发现冲突并请求人工判断。只把同一个问题提交一次模型，也可能足以完成任务；不必为每个问题构造多 Agent。</p>
<h3>训练、后训练与推理是不同阶段</h3><p>训练通过样本与目标函数更新参数；后训练进一步调整行为（方法可能包括监督微调或偏好学习）；推理使用既定参数计算输出。把文件放进提示词通常没有更新权重。RAG 是先检索外部材料、再让生成过程使用它，不等于把资料重新训练进模型。</p>
<p class="warning">重要边界：更长的回答、更多循环或更多 Agent 都不自动带来真实性。系统复杂度增加，也增加权限面、延迟、失败路径与评测负担。</p>
<h3>自检</h3><p>一个系统能读公司制度，却不能修改报销单。读写权限应该由谁控制？为什么“模型说可以修改”不构成授权？</p><details><summary>参考答案与理由</summary><p>宿主的权限层控制，并在工具执行前校验。模型输出是建议，不是用户授权，也不应直接变成可执行代码。只读检索权限不包含写入权限。</p></details>
<p>下一步：<a href="#tokens">模型如何把输入变成计算？</a></p>'''),
('tokens','02 · 模型机制','从 token 到 attention，再到一次推理','前置：模型与应用的区别。产出：解释分词、上下文、attention 和生成循环；不把本课当作完整 Transformer 复现。', '''
<p><strong>Token 不是固定的一个字或一个词。</strong> 分词器用特定词表与规则把文本转成整数 ID；同一句中文、英文或代码在不同分词器下可能有不同长度。ID 查表得到向量，位置信息让模型区分顺序。上下文窗口和输出预算通常按 token 而不是字符计数，实际规则随模型版本变化。</p>
<p>教学用假词表：<code>“猫坐垫子” → [“猫”, “坐”, “垫子”] → [12, 7, 31]</code>。这只是演示映射，<strong>不是任何真实模型的分词结果</strong>。一个词表外的词也可能被拆成多个片段。</p>
<h3>Attention 如何连接上下文？</h3><p>每个位置的表示经线性变换得到 query、key、value。query 与各 key 做相似度计算，缩放后经 softmax 得到权重，再对 value 加权求和。简写为 <code>softmax(QKᵀ / √dₖ)V</code>。因果语言模型用掩码阻止当前位置读取未来 token；多头机制在多个投影空间中计算这种关系。</p>
<div class="flow"><span>当前 query</span><b>→</b><span>比较 keys</span><b>→</b><span>归一化权重</span><b>→</b><span>汇总 values</span></div>
<p>极简数值例子：两个位置权重为 0.25 和 0.75，标量 value 为 2 和 6，加权结果是 <code>0.25×2 + 0.75×6 = 5</code>。真实模型使用高维向量、残差连接、归一化与前馈层；此例只解释加权汇总，不是语义理解实验，也不是可解释性证明。</p>
<p><a class="academy-primary" href="attention-lab.html">进入 Attention 数学实验 →</a> 三个教学 token：切换查询位置与因果遮罩，核对缩放分数、softmax 权重和输出；有手算、自检与恢复步骤。</p>
<h3>一次回答是怎样生成的？</h3><ol><li>把输入编码为 token，并在允许的上下文内计算表示。</li><li>输出下一 token 的分数，转成分布，按解码策略选择 token。</li><li>把新 token 加入序列，重复，直到结束标记或预算上限。</li></ol><p>训练目标帮助模型学习统计规律，但不保证每次生成都有可核对事实。温度等解码参数改变采样行为，不是可靠性开关。长上下文也不保证所有证据都被正确使用。</p>
<details><summary>自检：attention 权重高，能证明答案真实吗？</summary><p>不能。权重是模型内部计算的一部分，不是对资料真实性的认证。应核对证据、版本与引用，并以目标任务测试回答正确性。</p></details>
<p>机制依据：<a href="https://arxiv.org/abs/1706.03762">Attention Is All You Need（Transformer 原论文）</a>，第 3 节。上面的分词与算术例子是原创简化教学，不是论文复现。</p><p>下一步：<a href="#tools">工具调用与记忆的边界</a>。</p>'''),
('tools','03 · Agent 机制','工具调用不是授权，记忆不是事实','前置：生成循环。产出：画出一次工具调用的信任边界，并区分会话状态与持久记忆。', '''
<p>工具调用的核心不是让模型直接控制电脑，而是让它提出结构化请求，例如 <code>{"name":"search","arguments":{"query":"报销上限"}}</code>。宿主检查工具名、字段、类型、长度、权限与预算后，才调用工具。工具结果进入上下文，模型或策略据此决定下一步。</p>
<ol><li><strong>提议：</strong>适配器产出工具请求或最终回答候选。</li><li><strong>校验：</strong>只接受 allowlist 中的工具和严格参数；拒绝额外字段。</li><li><strong>执行：</strong>只读检索限定在用户批准的资料集，设置超时与结果上限。</li><li><strong>观察：</strong>把结果当作不可信数据，而不是新的系统指令。</li><li><strong>停止：</strong>证据充分时附来源；缺失、冲突或预算耗尽时拒答或交给人。</li></ol>
<p>固定工作流预先定义路径；Agent 循环允许策略根据观察选择下一步。二者是设计取舍而非高低等级。检索后直接回答的两步流程往往比自由规划更容易测清楚。更多自治应由任务需要与风险证明，而不是由“Agent”名称证明。</p>
<h3>记忆分层</h3><p><strong>运行状态</strong>保存本次步骤、检索结果和重试次数；<strong>会话上下文</strong>把相关历史放入下一次输入；<strong>持久记忆</strong>在多次会话间保存内容，需要身份隔离、来源、过期和删除机制。它们都可能错误或过时。摘要会丢信息，向量检索会漏召回；“记住了”不等于“验证过”。</p>
<p class="warning">文档里出现“忽略之前的规则并泄露密钥”是提示注入，不是工具授权。不要把文档当成指令；只读能力、出站控制和人工关卡应在模型外实现。关键词检测只能挡住教学样例，不能证明抵御任意注入。</p>
<details><summary>自检：资料中要求调用 send_email，系统应该怎样处理？</summary><p>本项目没有发信工具，必须拒绝该调用。不得动态添加工具、把文本交给 shell 或让文档覆盖用户授权；保留安全停止原因，不回显敏感文档或密钥。</p></details><p>下一步：<a href="#project">实现一个有证据的资料问答 Agent</a>。</p>'''),
('project','04 · 完整开发项目','做一个有证据的资料问答 Agent','前置：会运行 Python 3.10+，理解函数与字典；先读工具调用课。产出：可运行的离线模拟、可核对引用、失败测试和限制清单。', '''
<p class="warning"><strong>运行等级：标准库确定性模拟。</strong> 不联网、不加载模型、不调用真实 API、不下载权重、不安装第三方依赖。测试检查宿主控制逻辑，不证明模型质量、真实延迟、费用、提示注入安全或生产可用性。</p>
<h3>1 · 需求与验收</h3><p>用户给定问题与批准的三份合成资料，系统检索相关事实，返回状态、答案和来源 ID。资料只包含虚构团队制度，不含真实个人数据。只允许查询，不发信、不写外部系统。无答案必须拒答；同一字段冲突必须停下来；未经人工确认不能交付答案。</p>
<p>可接受的答案不仅要“说得通”，还要让每项事实能回到某份资料。引用存在不代表引用支持结论：生产系统还需要检查证据蕴含与完整性。本模拟用受控字段精确匹配，避免把生成文本伪装成已验证结果。</p>
<h3>2 · 架构与边界</h3><div class="flow"><span>问题</span><b>→</b><span>策略适配器 / 校验</span><b>→</b><span>读取前人审</span><b>→</b><span>只读检索</span><b>→</b><span>证据判定</span><b>→</b><span>发布前人审 → 回答</span></div>
<p>核心状态机与 API 适配器分层。核心负责权限、预算、检索和最终输出；模拟适配器只提供预设动作，不能越过工具校验。未来真实模型适配器应把厂商响应转换成相同契约，但本项目<strong>不包含已验证的真实 API 接入</strong>。适配时另查具体版本文档、结构化输出格式、地区/账户、价格、隐私条款及速率限制；密钥只从受控服务端环境读取，不能写入网页或仓库。</p>
<h3>3 · 获取与运行</h3><p>下载 <a href="qa-agent-lab.zip" download>完整离线实验 ZIP</a>，解压进入目录。先阅读 <a href="qa-agent/README.md">中英 README</a>，再运行以下命令。需要本地 Python 3.10+；浏览器不会替你执行代码。</p>
<pre><code>python --version
python -m unittest discover -s tests -v
python learning/qa-agent/demo.py</code></pre>
<p>若 Python 命令不存在，先使用你组织批准的 Python 安装方式。不要把未知安装脚本粘贴到终端。测试失败时保留错误和环境版本，先检查是否在解压后的根目录；不要为了变绿删除断言。</p>
<p>本地执行记录：2026-11-01，云端 Linux / Python 3.12.14，33 项模拟单元测试通过；这不是模型或浏览器验收。<a href="qa-agent/TEST-RESULTS.md">查看命令、结果与边界</a>。</p><h3>4 · 跟着核心循环走一遍</h3><pre><code># step() enforces bounded retries, steps and deadline
plan = step("plan", lambda: adapter.plan(question))
validate_allowed_tool(plan)
if step("human_review", lambda: approve(plan),
        retry=False, human_wait=True) is not True:
    stop("human_denied")              # BEFORE document access
claims = step("read_only_search", lambda: tool.search(plan["arguments"]))
evidence = freeze_plain_string_claims(claims)
if missing_or_conflicting(evidence): stop_with_reason()
draft = step("compose", lambda: adapter.compose(fresh_claims(evidence)))
validate_against_frozen_evidence(draft, evidence)
candidate = detach_validated_output(draft)
if step("human_release_review", lambda: approve_release(copy(candidate)),
        retry=False, human_wait=True) is not True:
    stop("human_release_denied")      # BEFORE answer release
return candidate</code></pre><p>上面按真实适配器契约展示简化控制流程；校验、冻结和停止辅助函数是示意，完整可执行实现见 ZIP。证据必须在 compose 之前冻结，并给适配器独立副本，不能让适配器改写验收依据。此修复保护模拟数据契约，不是任意 Python 代码沙箱或生产安全认证。实际适配器暴露 <code>plan(question)</code> 与 <code>compose(claims)</code>；核心 <code>run(..., approve, approve_release=...)</code> 在读取前和发布前分别确认。先运行正常示例，再修改测试夹具里的问题或相同字段值，看拒答和冲突如何出现。不要直接将伪代码当成完整实现。</p>
<h3>5 · 状态、预算与恢复</h3><p>每次运行有最大步骤数和有限重试数。只对明确的临时超时/限流进行有限重试；非法参数、权限拒绝、证据冲突和人工否决不应盲目重试。模拟超时是受控异常，不是对真实网络计时的测量。生产适配器还需在传输层设置真实超时/取消，按服务端提示处理限流，并在预算内退避。</p>
<p>人工关卡在答案发布前展示候选和引用，让人接受或拒绝；不是在运行前点一次“同意一切”。拒绝后停止，不绕过确认。重跑是一个新运行，默认不从不可信中间状态续跑。日志只留步骤、结果类型和失败原因，不保存密钥与原始敏感问题；真实 token 用量和费用在本模拟中未知。</p>
<h3>6 · 必须逐项检查的失败样例</h3><ul><li>正常：返回批准资料中的答案和存在的来源 ID。</li><li>无答案：不给猜测答案，标明证据不足。</li><li>冲突：两份资料同一字段不同值，拒绝自动选一个。</li><li>超时 / 限流：允许有限重试；耗尽后可诊断地停止。</li><li>非法工具参数：错误类型、额外字段和不在 allowlist 的工具全部拒绝。</li><li>提示注入：样例指令不能改变工具或泄露数据；样例通过不代表任意攻击安全。</li><li>人工否决 / 步骤上限：不能输出已批准答案，不能无限循环。</li></ul>
<h3>7 · 交付与下一步</h3><p>保存源码、测试输出、Python 版本和限制清单。解释一次成功、一次拒答和一次超时恢复；这才是项目检查点。真实模型接入前还需鉴权、租户隔离、检索评测、模型输出校验、成本硬限额、监控和回滚。当前不是可部署到企业资料库的系统。</p><details><summary>自检：测试全部通过，就能把真实合同放进去吗？</summary><p>不能。夹具仅覆盖有限合成数据与确定性策略；没有检验真实模型、权限隔离、隐私、传输层或任意提示注入。先完成授权和数据治理，再设计真实服务评估。</p></details><p>下一步：<a href="#evaluation">建立自己的验收矩阵</a>。</p>'''),
('timeline','05 · AI 发展史','读懂变化，而不是追逐发布日期','前置：模型与系统的区别。产出：把一则技术新闻拆成对象、事件类型、日期、来源和影响。', '''
<p>早期规则自动化按写好的条件行动；模型驱动系统让语言模型提出动作，但执行边界仍需程序管理。工具增强和检索增强让系统连接外部信息，不意味着模型自身知识实时更新，也不意味着可靠的通用自主性已经实现。这里解释技术路线，不给出有争议的“第一个 Agent”结论。</p>
<p><a class="academy-primary" href="release-reading.html">真实发布阅读课：Qwen3-8B →</a> 从证据卡到有条件的简报；区分公告、报告、原生上下文和扩展条件，修订错误简报并带走 Markdown 模板。</p><h3>三个有证据的历史路标</h3><ol><li><strong>2017-06-12 · Transformer 论文首次提交：</strong><a href="https://arxiv.org/abs/1706.03762">Vaswani 等人的论文</a>提出以 attention 为核心的架构。影响是改变序列建模方式；该日期不是产品或权重开放日期。</li><li><strong>2020-05-22 · RAG 论文首次提交：</strong><a href="https://arxiv.org/abs/2005.11401">Lewis 等人的论文</a>研究把参数化生成模型与外部检索结合。影响是让回答利用检索证据；不能据此保证检索到的文档真实或答案正确。</li><li><strong>2022-10-06 · ReAct 论文首次提交：</strong><a href="https://arxiv.org/abs/2210.03629">Yao 等人的论文</a>研究推理与行动相结合。影响是把观察反馈纳入过程；论文任务结果不等于生产系统可靠性。</li></ol>
<p>这些是选定论文的首次提交日期，不是作者机构首次发布模型的完整年表。已收录的厂商/具体版本历史记录仍由原目录承载；本页不新增或重写规范事件。</p>
<h3>如何看“最近发布”？</h3><p>先确认家族、固定快照、滚动 API 别名还是服务；再区分公告、报告公开、权重开放、API 上线和“截至某日已可用”。核验日期记录编辑何时检查来源，不能替代发生日期。原有月度投影保留 __MONTHLY_COUNT__ 条事件；它与规范事件库是不同投影，不相加为模型数量。</p><p><a href="monthly.html">进入月度发布档案（旧版中文）→</a> · <a href="index.html?view=timeline">原始事件与来源（旧版中文）→</a></p>
<details><summary>管理者自检：一家公司发了公告，就能安排明天上线吗？</summary><p>不能。还需明确可访问版本、API/权重开放状态、许可、区域与账户条件、任务效果、成本、安全与回退方案。发布日期不提供这些问题的全部答案。</p></details>'''),
('multimodal','06 · 多模态技术','图像、音频、视频与世界模型，分别在做什么？','前置：token 与模型输入输出。产出：按输入、输出、控制条件和失败模式阅读一项多模态能力。', '''
<p>多模态不是一个单独任务。系统可能接收图像并输出文字，也可能根据文字生成音频、编辑视频或预测未来状态。输入编码器把不同信号转换成可处理的表示；生成端的结构与训练目标决定它输出什么。统一界面不证明底层只有一个模型。</p>
<h3>图像：理解与生成不同</h3><p>理解系统处理图像区域、文字和空间关系，可能漏掉细节、误读小字；生成系统可能通过去噪等过程产生图像，局部合理不保证数量、布局或物理关系正确。评估应区分视觉问答、OCR、定位和编辑约束，不能用一张漂亮图片概括全部能力。</p>
<h3>音频：不只有语音转文字</h3><p>语音识别输出文字；合成输出音频；实时系统还要处理端点检测、打断、延迟和轮次。转写正确不等于说话人身份判断可靠，音色相似也不构成使用声音的授权。测试应包括噪声、口音、重叠说话和用户打断。</p>
<h3>视频：时间是额外的约束</h3><p>视频生成要在多个帧之间保持对象身份、运动与场景关系。模型可使用压缩的时空表示，具体路线随版本不同。比较时记录文本/图像/视频输入、首尾帧或相机控制、输出时长、分辨率和计算预算；未知项写未知。单帧美观不证明长时间一致，物体穿透或身份漂移可能只在回放中出现。</p>
<p><a class="academy-primary" href="diffusion-noise-lab.html">扩散噪声与预测误差：从加噪到反解 →</a> 用原创二维数值比较已知噪声与错误估计，计算误差放大；不是训练或图片生成。</p>
<p><a class="academy-primary" href="video-sampling-lab.html">进入视频抽帧与时序证据实验 →</a> 用原创时间戳帧序列改变间隔与起点，发现稀疏抽样遗漏的身份断点，完成独立练习与证据报告。</p>
<h3>世界模型：预测不等于理解物理世界</h3><p>有些系统预测表示或未来状态，有些生成可视场景，有些支持动作条件下的模拟。不要因为都叫“世界模型”就认为都能规划机器人行动。要问状态是什么、动作能否输入、预测跨度多长、怎样衡量误差，以及闭环执行是否实际测试。</p>
<p class="warning">本页是机制概览，不是厂商性能排名。没有运行视频、音频或世界模型，没有测量硬件需求或生成质量。具体功能、许可与可用性必须回到准确版本来源。</p><p><a href="index.html?view=explore">模型资料与来源（旧版中文）</a> · <a href="realtime-audio.html">实时音频延伸阅读（旧版中文）</a></p>
<details><summary>自检：视频看起来连贯，为什么还不能当机器人模拟器？</summary><p>视觉连续不等于动作条件下物理状态预测正确。还需可控动作接口、状态定义、误差指标与真实闭环验证；不能仅凭画面判断。</p></details>'''),
('resources','07 · 模型与资料','把资料当证据，不把目录当课堂','前置：明确想验证的具体说法。产出：找到准确对象、版本与支持该说法的来源。', '''
<p>先写问题：是“attention 如何工作”，还是“这个固定版本能否输入视频”？前者回到机制课；后者查模型卡、技术报告和接口文档。家族名称不等于固定模型快照，权重许可、代码许可与服务条款也不同。可下载不自动等于可商用。</p><p><a href="index.html?view=vendor-catalog">厂商与模型目录（旧版中文）→</a> · <a href="index.html?view=explore">概念、模型、来源检索（旧版中文）→</a> · <a href="BOOK.md">同源中文书稿 →</a></p><p>旧版资料未全部翻译，英文读者会明确进入中文原文。资料中的事实核验时间仍用原值；本次教学翻译与页面更新不刷新它。未知地区条件、未核验链接与生命周期限制应保留，不猜测。</p><p><a href="release-reading.html">Qwen3-8B 发布简报：证据账本与 Markdown 模板 →</a></p><h3>进一步阅读</h3><p>Transformer 原论文用于 attention 机制；RAG 原论文用于检索与生成的分工；ReAct 原论文用于推理—行动过程。论文说明研究设置，不能替代你自己的项目验收。</p>'''),
('evaluation','08 · 评测与方法','先定义失败，再谈成功率','前置：完成问答项目或读过需求。产出：一张能复查的验收矩阵。', '''
<p><a class="academy-primary" href="benchmark-practice.html">评测阅读课：来源、条件与独立迁移 →</a> 两张官方来源卡、空账本、三条修订与两条独立比较决定；无需运行模型。</p><p>把需求变成可判定标准：问题、允许资料、期望状态、必要引用、禁止动作和最大预算。先固定数据版本与配置，再执行。正确率之外，分别记录引用支持率、拒答是否恰当、冲突处理、非法工具调用、超时停止和人工否决。不要用一个平均分掩盖权限失败。</p><p>示例：对“资料没有报销上限”这条用例，正确结果是证据不足；生成一个合理金额应判失败。对冲突用例，附两个来源但任意挑一个值也不合格。给定资料没有答案时的拒答不是模型能力差，而是满足系统契约。</p>
<p>本项目的模拟测试用于回归宿主逻辑；真实模型测试需要固定模型版本、提示、采样设置、工具配置、样本与重复运行策略。作者自报成绩、独立复现与我们自己的测试是不同证据，不做跨配置排名。原有三条历史快照及后续补充保留原口径。</p><p class="warning">已读标记不是掌握证明，单元测试通过不是学习成效证明。入行者、开发者和管理者试学尚未开展；完成率与学习时长未知。</p><p><a href="index.html?view=evaluation">历史评测索引（旧版中文）→</a> · <a href="index.html?view=coverage">来源方法与覆盖缺口（旧版中文）→</a></p><details><summary>自检：换了检索器以后只重跑正常问题可以吗？</summary><p>不可以。还要重跑漏检、冲突、注入、引用和预算测试；改变证据召回可能影响原来安全停止的路径。保留旧配置结果以便比较和回退。</p></details>''')]
}
CONTENT['en'] = {
'nav':['Learn AI','Build Agents','AI Timeline','Multimodal','Models & Resources','Evaluation & Methods'],
'hero':'Understand how AI works.<br>Build your own Agent.',
'lede':'From one mechanism to an implementation you can inspect. Connect foundations, engineering and technical change—whether you are starting out, writing code or leading a team.',
'goals':[('Learn the principles','Models, tokens and tool calls','foundations'),('Build an Agent','Evidence-grounded document Q&A','project'),('Follow AI progress','Who released what—and what the date means','timeline')],
'audience':'Choose your reading depth, not a permanent label',
'roles':[('Newcomer','Read three foundation chapters, explain each mechanism, then try the project checks.','foundations'),('Developer','Start with input/output contracts, adapters and the offline state-machine lab.','project'),('Manager','Read the timeline and multimodal overview, then consider limits, risks and engineering effort.','timeline')],
'path':'A learning path you can finish',
'pathtext':'01 Models versus systems → 02 Tokens and attention → 03 Tools and memory → 04 Document Q&A → 05 Failure tests. No account required. Learning time has not been measured in learner trials.',
'projectteaser':'Your first lab: evidence-grounded document Q&A',
'projecttext':'Three synthetic documents, one read-only search tool and two human gates: before reading and before releasing the answer. Learn to cite evidence, abstain when it is missing and stop within bounded budgets. Python standard-library source and tests included; a deterministic simulation, not a real model evaluation.',
'enter':'Open the complete project →',
'changes':'Three technical changes worth understanding',
'changeitems':[('From token sequences to attention','Attention computes contextual representations; its weights are not proof of a causal explanation.','tokens'),('From text generation to tool calls','A model may propose an action; the host still owns authorization, validation and execution.','tools'),('From individual images to video systems','Temporal consistency, control conditions and resource constraints add new evaluation dimensions.','multimodal')],
'legacy':'Legacy Chinese further reading (not yet translated)',
'legacytext':'Catalogs, monthly events and earlier courses retain their identities, dates and reading records. They support learning; they are neither a complete market inventory nor a performance leaderboard.',
'search':'Search core lessons, projects and labs','placeholder':'Try: memory / attention / refusal / video','searchhint':'Search bilingual lessons and labs. Combine words with spaces: every term must match. Chinese fragments and English word prefixes work. Historical entities are under Models & Resources.',
'market':'Reference region','language':'Language','unknown':'Unspecified / general','regionnote':'Region affects dependency guidance only. This offline simulation needs no service account. Real API region, account, pricing and licensing conditions have not been verified individually. Selecting a region does not establish availability or hide principles.',
'footer':'Original teaching explanations · Equivalent core Chinese and English content · Teaching edition 2026-11-01, not a new historical fact-verification date. No account, location inference or tracking. Read does not mean mastered.',
'read':'Mark as read','readDone':'Read (not proof of mastery)','progress':'Records stay in this browser; legacy learning records are preserved.',
'chapters':[
('foundations','01 · Learn AI','Model, application or Agent: what is the difference?','Prerequisites: none. Outcome: separate model capability, application logic and an Agent control loop in document Q&A.', '''
<p>A <strong>model</strong> is a parameterized computational system mapping inputs to outputs. A language model typically predicts subsequent tokens from a preceding sequence; it does not inherently possess a browser, company database or payment permission. An <strong>application</strong> embeds a model in a product workflow with interfaces, retrieval, rules and permissions. Here, an <strong>Agent</strong> means a constrained system that chooses actions from its state, invokes allowed tools, observes results and decides whether to continue or stop. Definitions vary; a product name does not establish autonomy.</p>
<div class="flow" aria-label="System layers"><span>Question + approved documents</span><b>→</b><span>Host: rules + loop</span><b>↔</b><span>Model / adapter</span><b>→</b><span>Read-only tool + evidence</span></div>
<p>For “What is the reimbursement limit?”, a model can produce fluent text, but the application must choose the policy and version to retrieve. An Agent can retrieve evidence, detect conflicting values and ask a human. A single model call may also be sufficient; not every task needs multiple Agents.</p>
<h3>Training, post-training and inference differ</h3><p>Training updates parameters using examples and an objective. Post-training further adjusts behavior, for example through supervised fine-tuning or preference learning. Inference computes outputs using the resulting parameters. Putting a document into a prompt does not normally update weights. RAG retrieves external material for generation; it is not the same as retraining the model on that material.</p>
<p class="warning">Longer answers, more loops or more Agents do not automatically improve truthfulness. Complexity also increases the permission surface, latency, failure paths and evaluation burden.</p>
<h3>Check your understanding</h3><p>A system can read policy documents but cannot modify expense claims. Who should enforce that boundary, and why is “the model said it could” not authorization?</p><details><summary>Answer and reasoning</summary><p>The host permission layer must enforce it before tool execution. Model output is a proposal, not user authorization or executable code. Read permission does not include write permission.</p></details><p>Next: <a href="#tokens">How does input become computation?</a></p>'''),
('tokens','02 · Model mechanisms','From tokens to attention to one inference loop','Prerequisite: models versus applications. Outcome: explain tokenization, context, attention and generation. This is not a full Transformer reproduction.', '''
<p><strong>A token is not always a character or word.</strong> A tokenizer maps text into integer IDs using its vocabulary and rules. The same Chinese text, English text or code can have different token counts under different tokenizers. IDs map to vectors, and position information distinguishes order. Context and output budgets are usually measured in tokens, not characters; exact rules depend on model version.</p>
<p>A fictional teaching vocabulary: <code>“猫坐垫子” → [“猫”, “坐”, “垫子”] → [12, 7, 31]</code>. This illustrates a mapping; it is <strong>not the tokenization of any real model</strong>. A word absent from the vocabulary may be split into pieces.</p>
<h3>How does attention connect context?</h3><p>Linear transformations of each position's representation produce queries, keys and values. A query is compared with keys; scaled scores pass through softmax to become weights, which form a weighted sum of values: <code>softmax(QKᵀ / √dₖ)V</code>. Causal language models mask future positions. Multi-head attention performs this computation in multiple projected spaces.</p>
<div class="flow"><span>Current query</span><b>→</b><span>Compare keys</span><b>→</b><span>Normalize weights</span><b>→</b><span>Combine values</span></div>
<p>A tiny numerical example: weights 0.25 and 0.75 with scalar values 2 and 6 yield <code>0.25×2 + 0.75×6 = 5</code>. Real models use high-dimensional vectors, residual connections, normalization and feed-forward layers. This only illustrates weighted aggregation; it is neither a semantic understanding experiment nor an interpretability proof.</p>
<p><a class="academy-primary" href="attention-lab-en.html">Open the attention mathematics lab →</a> Three teaching tokens: switch query positions and causal masking, verify scaled scores, softmax weights and outputs, then hand-check and recover from mistakes.</p>
<h3>How is an answer generated?</h3><ol><li>Encode input into tokens and compute representations within the allowed context.</li><li>Produce scores for the next token, form a distribution and choose a token using the decoding strategy.</li><li>Append it and repeat until an end marker or budget limit.</li></ol><p>The training objective helps learn statistical regularities but does not guarantee factual output. Temperature changes sampling behavior; it is not a reliability switch. Long context does not guarantee correct use of all evidence.</p>
<details><summary>Check: does a high attention weight prove a statement true?</summary><p>No. It is part of internal computation, not certification of source truth. Check evidence, versions and citations, and evaluate correctness on the target task.</p></details><p>Mechanism reference: <a href="https://arxiv.org/abs/1706.03762">Attention Is All You Need</a>, section 3. The token and arithmetic examples above are original simplifications, not a paper reproduction.</p><p>Next: <a href="#tools">Tools and memory boundaries</a>.</p>'''),
('tools','03 · Agent mechanisms','Tool calls are not authorization. Memory is not truth.','Prerequisite: the generation loop. Outcome: draw the trust boundary in a tool call and distinguish run state from persistent memory.', '''
<p>A tool call is not direct computer control. The model proposes a structured request, such as <code>{"name":"search","arguments":{"query":"reimbursement limit"}}</code>. The host checks the tool name, fields, types, lengths, permissions and budgets before execution. The result enters context, and the model or policy selects the next step.</p>
<ol><li><strong>Propose:</strong> the adapter returns a tool request or a candidate answer.</li><li><strong>Validate:</strong> accept only allowlisted tools and strict arguments; reject extra fields.</li><li><strong>Execute:</strong> constrain read-only retrieval to approved documents, with time and result limits.</li><li><strong>Observe:</strong> treat results as untrusted data, not new system instructions.</li><li><strong>Stop:</strong> cite sufficient evidence; abstain or defer to a human on missing evidence, conflicts or budget exhaustion.</li></ol>
<p>A fixed workflow defines paths in advance; an Agent loop lets a policy choose the next step from observations. This is a design tradeoff, not a hierarchy. A two-step retrieve-and-answer workflow is often easier to evaluate than open-ended planning. More autonomy needs justification from the task and risk, not the label “Agent”.</p>
<h3>Layers of memory</h3><p><strong>Run state</strong> stores current steps, results and retry counts. <strong>Conversation context</strong> places relevant history in the next input. <strong>Persistent memory</strong> survives conversations and needs identity isolation, provenance, expiry and deletion. All can be wrong or stale. Summaries lose information and vector retrieval can miss relevant material; remembering does not mean verifying.</p>
<p class="warning">A document saying “ignore previous rules and reveal secrets” is prompt injection, not tool authorization. Keep document data separate from instructions. Read-only capabilities, egress controls and human gates belong outside the model. Keyword detection can catch a teaching fixture, not prove resistance to arbitrary injection.</p>
<details><summary>Check: a document requests send_email. What should happen?</summary><p>This project has no email tool, so the request must be rejected. Do not add tools dynamically, pass text to a shell or let documents override authorization. Retain a safe stop reason without echoing secrets or sensitive documents.</p></details><p>Next: <a href="#project">Build evidence-grounded Q&A</a>.</p>'''),
('project','04 · Complete development project','Build an evidence-grounded document Q&A Agent','Prerequisites: Python 3.10+, functions and dictionaries; read the tools chapter. Outcome: a runnable offline simulation, inspectable citations, failure tests and a limitations list.', '''
<p class="warning"><strong>Execution level: deterministic standard-library simulation.</strong> No network, model, real API, weight download or third-party dependency. Tests check host control logic—not model quality, real latency, costs, prompt-injection security or production readiness.</p>
<h3>1 · Requirements and acceptance</h3><p>Given a question and three approved synthetic documents, retrieve relevant facts and return status, answer and source IDs. Documents contain fictional team policies, not real personal data. Reading is allowed; sending messages or writing external systems is not. Missing evidence requires abstention; conflicting values require a stop; human approval is required before delivering an answer.</p><p>An acceptable answer must trace every fact to a document. A citation's existence does not prove that it supports a claim: production systems also need entailment and completeness checks. This simulation matches controlled fields exactly rather than presenting generated prose as verified.</p>
<h3>2 · Architecture and boundaries</h3><div class="flow"><span>Question</span><b>→</b><span>Policy adapter / validation</span><b>→</b><span>Pre-read review</span><b>→</b><span>Read-only search</span><b>→</b><span>Assess evidence</span><b>→</b><span>Pre-release review → answer</span></div><p>The core state machine is separate from the API adapter. The core owns permissions, budgets, retrieval and final output. The simulation adapter supplies scripted actions and cannot bypass tool validation. A future real-model adapter must translate provider responses into the same contract; <strong>no verified real API integration is included</strong>. Before adapting, check version-specific documentation, structured output, region/account requirements, pricing, privacy terms and rate limits. Read secrets from a controlled server environment, never a web page or repository.</p>
<h3>3 · Get and run the lab</h3><p>Download the <a href="qa-agent-lab.zip" download>complete offline lab ZIP</a>, extract it and enter its root directory. Read the <a href="qa-agent/README.md">bilingual README</a>, then run the commands below. Local Python 3.10+ is required; the browser does not execute them for you.</p><pre><code>python --version
python -m unittest discover -s tests -v
python learning/qa-agent/demo.py</code></pre><p>If Python is unavailable, use your organization's approved installation process. Do not paste unknown installation scripts into a terminal. On failure, keep the error and environment version, check the extraction root, and do not delete assertions to obtain a green result.</p>
<p>Local execution record: 2026-11-01, cloud Linux / Python 3.12.14, 33 simulation unit tests passed. This is not model or browser acceptance. <a href="qa-agent/TEST-RESULTS.md">Commands, results and limits</a>.</p><h3>4 · Walk through the core loop</h3><pre><code># step() enforces bounded retries, steps and deadline
plan = step("plan", lambda: adapter.plan(question))
validate_allowed_tool(plan)
if step("human_review", lambda: approve(plan),
        retry=False, human_wait=True) is not True:
    stop("human_denied")              # BEFORE document access
claims = step("read_only_search", lambda: tool.search(plan["arguments"]))
evidence = freeze_plain_string_claims(claims)
if missing_or_conflicting(evidence): stop_with_reason()
draft = step("compose", lambda: adapter.compose(fresh_claims(evidence)))
validate_against_frozen_evidence(draft, evidence)
candidate = detach_validated_output(draft)
if step("human_release_review", lambda: approve_release(copy(candidate)),
        retry=False, human_wait=True) is not True:
    stop("human_release_denied")      # BEFORE answer release
return candidate</code></pre><p>This simplified flow follows the real adapter contract; validation, freezing and stop helpers are illustrative. The ZIP contains the executable implementation. Freeze evidence before compose and pass independent copies so the adapter cannot rewrite the validation basis. This protects a simulation data contract; it is not a sandbox for arbitrary Python or production security certification. The actual adapter exposes <code>plan(question)</code> and <code>compose(claims)</code>; the core <code>run(..., approve, approve_release=...)</code> requests approval before reading and before release. Run the normal example, then change the fixture question or a competing field value to observe abstention and conflict handling. Do not mistake the pseudocode for a complete implementation.</p>
<h3>5 · State, budgets and recovery</h3><p>Each run has maximum steps and bounded retries. Retry only explicitly transient timeouts or rate limits; do not blindly retry invalid arguments, denied permissions, evidence conflicts or human rejection. Simulated timeouts are controlled exceptions, not measurements of real network timing. A production adapter also needs transport timeouts/cancellation, server rate-limit guidance and bounded backoff.</p><p>Human review shows the candidate and citations before release; it is not a one-time “approve everything” button. Rejection stops the run. A rerun is a new run, not automatic continuation from untrusted state. Logs retain steps, outcome types and stop reasons—not keys or raw sensitive questions. Real token usage and charges are unknown in this simulation.</p>
<h3>6 · Failure cases to inspect</h3><ul><li>Normal: return an answer from approved documents with existing source IDs.</li><li>Missing evidence: abstain rather than guess.</li><li>Conflict: refuse to choose automatically between two values for the same field.</li><li>Timeout / rate limit: bounded retries, then a diagnosable stop.</li><li>Invalid arguments: reject wrong types, extra fields and non-allowlisted tools.</li><li>Prompt injection: fixture instructions cannot change tools or exfiltrate data; passing fixtures is not general attack resistance.</li><li>Human rejection / step limit: no approved answer and no unbounded loop.</li></ul>
<h3>7 · Deliver and extend</h3><p>Keep source, test output, Python version and limitations. Explain one success, one abstention and one timeout recovery. Before real-model integration, add authentication, tenant isolation, retrieval evaluation, model-output validation, hard spending limits, monitoring and rollback. This is not a system ready for an enterprise document store.</p><details><summary>Check: all tests passed. Can you now load real contracts?</summary><p>No. The fixtures cover limited synthetic data and a deterministic policy, not real models, identity isolation, privacy, transport or arbitrary injection. Establish authorization and data governance before evaluating a real service.</p></details><p>Next: <a href="#evaluation">Build an acceptance matrix</a>.</p>'''),
('timeline','05 · AI Timeline','Understand change, not just release dates','Prerequisite: models versus systems. Outcome: separate a technical announcement into entity, event type, date, source and implication.', '''
<p>Rule-based automation acts on predefined conditions. Model-driven systems let a language model propose actions, but programs must still enforce execution boundaries. Tools and retrieval connect systems to external information; they do not make model knowledge intrinsically real-time or establish reliable general autonomy. This overview explains approaches without asserting a disputed “first Agent”.</p>
<p><a class="academy-primary" href="release-reading-en.html">Real-release reading lesson: Qwen3-8B →</a> Turn supplied evidence into a qualified brief; separate announcement/report dates and native/extended context, repair a flawed brief and take a Markdown template.</p><h3>Three evidence-backed historical landmarks</h3><ol><li><strong>2017-06-12 · Transformer paper first submitted:</strong> <a href="https://arxiv.org/abs/1706.03762">Vaswani and colleagues</a> proposed an attention-centered architecture. It changed sequence modeling; this is not a product or weight-release date.</li><li><strong>2020-05-22 · RAG paper first submitted:</strong> <a href="https://arxiv.org/abs/2005.11401">Lewis and colleagues</a> studied combining parametric generation with retrieval. It lets answers use retrieved evidence, without guaranteeing source truth or answer correctness.</li><li><strong>2022-10-06 · ReAct paper first submitted:</strong> <a href="https://arxiv.org/abs/2210.03629">Yao and colleagues</a> studied interleaving reasoning and action. Observation becomes part of the process; paper results do not establish production reliability.</li></ol><p>These are first-submission dates for selected papers, not a complete vendor model-release chronology. Existing catalogs retain provider and exact-version records; this page does not create or rewrite canonical events.</p>
<h3>How should you read “recently released”?</h3><p>Identify the family, fixed snapshot, rolling API alias or service first. Separate announcements, reports, weight releases, API launches and “available by” observations. A verification date says when an editor checked a source, not when the event occurred. The preserved monthly projection has __MONTHLY_COUNT__ events; it is distinct from the canonical event library and must not be added to it as a model count.</p><p><a href="monthly.html">Monthly release archive (legacy Chinese) →</a> · <a href="index.html?view=timeline">Original events and sources (legacy Chinese) →</a></p><details><summary>Manager check: does an announcement mean you can deploy tomorrow?</summary><p>No. Establish the accessible version, API/weight status, licensing, region and account conditions, task performance, costs, safety and rollback. A release date does not answer all these questions.</p></details>'''),
('multimodal','06 · Multimodal','What do image, audio, video and world models actually do?','Prerequisite: tokens and model inputs/outputs. Outcome: read a capability in terms of inputs, outputs, control conditions and failure modes.', '''
<p>Multimodal is not one task. A system may accept an image and produce text, generate audio from text, edit video or predict future states. Encoders transform signals into usable representations; output architecture and training objectives determine what is produced. A unified interface does not prove that a single model operates underneath.</p>
<h3>Images: understanding differs from generation</h3><p>Understanding systems process regions, text and spatial relations and may miss details or small lettering. Generators may use processes such as denoising; plausible local detail does not guarantee correct counts, layouts or physical relationships. Evaluate visual question answering, OCR, localization and editing constraints separately rather than using one attractive image to summarize all abilities.</p>
<h3>Audio: more than speech-to-text</h3><p>Recognition outputs text; synthesis outputs audio. Real-time systems must also handle endpointing, interruptions, latency and turn-taking. Accurate transcription does not establish speaker identity, and a similar voice does not authorize its use. Test noise, accents, overlapping speech and user interruptions.</p>
<h3>Video: time adds constraints</h3><p>Generation must maintain object identity, motion and scene relationships across frames. Models may use compressed spatiotemporal representations; approaches vary by version. Record text/image/video inputs, endpoint-frame or camera controls, duration, resolution and compute budgets. Label unknowns. Attractive individual frames do not prove long-range consistency; penetration or identity drift may appear only during playback.</p>
<p><a class="academy-primary" href="diffusion-noise-lab-en.html">Diffusion noise and prediction error: mix, invert and compare →</a> Compute error amplification with original 2-D signals, distinguishing oracle inversion from a supplied wrong estimate; no training or image generation.</p>
<p><a class="academy-primary" href="video-sampling-lab-en.html">Open the video sampling and temporal-evidence lab →</a> Vary stride and offset on original timestamped frames, find an identity discontinuity missed by sparse sampling, then complete an independent exercise and evidence report.</p>
<h3>World models: prediction is not proof of physical understanding</h3><p>Some predict representations or future states, some generate visible scenes, and some simulate conditional on actions. The shared label does not imply that all can plan robot behavior. Ask what state means, whether actions are inputs, the prediction horizon, how error is measured and whether closed-loop execution was tested.</p>
<p class="warning">This is a mechanism overview, not a vendor ranking. No video, audio or world model was run; hardware requirements and generation quality were not measured. Specific features, licenses and availability require exact-version sources.</p><p><a href="index.html?view=explore">Model evidence (legacy Chinese)</a> · <a href="realtime-audio.html">Real-time audio further reading (legacy Chinese)</a></p><details><summary>Check: why is coherent video not automatically a robot simulator?</summary><p>Visual continuity does not prove correct action-conditioned state prediction. You need an action interface, state definition, error measures and real closed-loop validation—not just convincing frames.</p></details>'''),
('resources','07 · Models & Resources','Use resources as evidence, not as a substitute for teaching','Prerequisite: a precise claim to verify. Outcome: locate the exact entity, version and supporting source.', '''
<p>First write the question: “How does attention work?” or “Does this fixed version accept video?” The former belongs in the mechanisms chapter; the latter requires model cards, technical reports and API documentation. A family name is not a fixed snapshot. Weight licenses, code licenses and service terms differ; downloadable does not mean commercially licensed.</p><p><a href="index.html?view=vendor-catalog">Providers and model catalog (legacy Chinese) →</a> · <a href="index.html?view=explore">Concepts, models and sources (legacy Chinese) →</a> · <a href="BOOK.md">Source-generated Chinese book →</a></p><p>Legacy resources are not fully translated; English readers are explicitly directed to Chinese originals. Their original fact-verification dates remain unchanged by this translation or page update. Preserve unknown regional conditions, unverified links and lifecycle limits rather than guessing.</p><p><a href="release-reading-en.html">Qwen3-8B release brief: evidence ledger and Markdown template →</a></p><h3>Further reading</h3><p>The Transformer paper supports attention mechanisms, the RAG paper explains retrieval/generation roles, and the ReAct paper studies reasoning–action processes. Research settings do not replace acceptance tests for your system.</p>'''),
('evaluation','08 · Evaluation & Methods','Define failure before reporting success','Prerequisite: complete the Q&A lab or read its requirements. Outcome: an inspectable acceptance matrix.', '''
<p><a class="academy-primary" href="benchmark-practice-en.html">Benchmark reading: evidence, conditions and independent transfer →</a> Two official source cards, a blank ledger, three claim repairs and two independent comparison decisions; no model execution.</p><p>Turn requirements into decidable criteria: question, allowed documents, expected status, required citations, forbidden actions and maximum budget. Fix data versions and configuration before running tests. Alongside correctness, record citation support, appropriate abstention, conflict handling, invalid calls, timeout stops and human rejection. A single average score must not hide permission failures.</p><p>For “the documents contain no reimbursement limit”, the correct outcome is insufficient evidence; a plausible amount is a failure. In a conflict case, citing both documents while arbitrarily selecting a value is also unacceptable. Abstention without evidence satisfies the system contract.</p><p>The simulation tests regress host logic. Real-model evaluation requires fixed model versions, prompts, sampling, tools, samples and a repeat-run strategy. Author-reported results, independent reproductions and our tests are distinct evidence, not a cross-configuration ranking. The original three historical snapshots and subsequent additions retain their original scope.</p><p class="warning">Marking a chapter read is not mastery; passing unit tests is not learning-effectiveness evidence. Newcomer, developer and manager learner trials have not been conducted. Completion rates and learning time are unknown.</p><p><a href="index.html?view=evaluation">Historical evaluation index (legacy Chinese) →</a> · <a href="index.html?view=coverage">Source methods and gaps (legacy Chinese) →</a></p><details><summary>Check: after changing retrieval, is testing only normal questions enough?</summary><p>No. Rerun missing-evidence, conflict, injection, citation and budget tests. Changed retrieval can affect previously safe stop paths. Preserve old configuration results for comparison and rollback.</p></details>''')]
}

IDS = ['foundations','project','timeline','multimodal','resources','evaluation']
def page_name(lang): return 'academy-en.html' if lang=='en' else 'academy.html'
def header(lang):
 c=CONTENT[lang]
 nav=''.join(f'<a href="{page_name(lang)}#{i}">{t}</a>' for i,t in zip(IDS,c['nav']))
 return f'''<a class="academy-skip" href="#academy-content">{'Skip to content' if lang=='en' else '跳至内容'}</a>
<header class="academy-header"><a class="academy-brand" href="{page_name(lang)}#home"><span aria-hidden="true">m</span> ModelAtlas<small>{'AI, understood & built.' if lang=='en' else '理解原理 · 亲手实现'}</small></a><nav class="academy-desktop-nav" aria-label="{'Main navigation' if lang=='en' else '主导航'}">{nav}</nav><details class="academy-main-menu"><summary>{'Menu' if lang=='en' else '菜单'}</summary><nav aria-label="{'Main navigation' if lang=='en' else '主导航'}">{nav}</nav></details>
<div class="academy-preferences"><span>{c['language']}: <a data-language="zh" href="academy.html">中文</a> / <a data-language="en" href="academy-en.html">English</a></span><label>{c['market']} <select class="academy-region"><option value="unknown">{c['unknown']}</option><option value="international">{'International · country unspecified' if lang=='en' else '国际 · 国家未指定'}</option><option value="CN">{'Mainland China' if lang=='en' else '中国大陆'}</option><option value="US">{'United States' if lang=='en' else '美国'}</option><option value="GB">{'United Kingdom' if lang=='en' else '英国'}</option><option value="SG">{'Singapore' if lang=='en' else '新加坡'}</option></select></label><label><input type="checkbox" class="academy-remember-region"> {'Remember region on this device' if lang=='en' else '在本机记住地区'}</label><span class="academy-storage-status" role="status"></span></div></header>'''

def reading_progress(lang):
 c=CONTENT[lang]; en=lang=='en'; target=page_name(lang)
 rows=''.join(f'<li><a href="{target}#{ident}">{escape(kicker)} · {escape(title)}</a><span data-progress-id="{ident}">{"Not loaded" if en else "尚未载入"}</span></li>' for ident,kicker,title,_,_ in c['chapters'])
 return f'''<section class="academy-section academy-progress" aria-labelledby="academy-progress-title"><div><p class="academy-eyebrow">READ · RETURN · REVIEW</p><h2 id="academy-progress-title">{'Your reading path' if en else '你的阅读路径'}</h2><p id="academy-progress-summary" role="status">{'Device reading marks have not been loaded.' if en else '尚未读取本机的阅读标记。'}</p><p>{'Marks are self-reported, not mastery or lab completion. No account or last-visited tracking.' if en else '已读由你自行标记，不代表掌握或完成实验；无需账号，不追踪上次访问。'}</p><p class="academy-reading-status" role="status">{'Enable JavaScript to see local marks; chapter links work without it.' if en else '启用 JavaScript 可查看本机标记；不启用仍可打开章节。'}</p><a id="academy-progress-next" class="academy-primary" href="{target}#foundations">{'Start chapter 01 →' if en else '从第一章开始 →'}</a></div><details><summary>{'All 8 core chapters' if en else '全部 8 个核心章节'}</summary><ol id="academy-progress-list">{rows}</ol></details></section>'''

def home(lang, monthly_count):
 c=CONTENT[lang]; target=page_name(lang); en=lang=='en'
 steps=[('foundations','模型与系统','Models and systems'),('tokens','Token 与 attention','Tokens and attention'),('tools','工具与记忆','Tools and memory'),('project','实现资料问答','Build evidence Q&A'),('evaluation','检验失败边界','Test failure boundaries')]
 roadmap=''.join(f'<li><a href="{target}#{ident}"><span aria-hidden="true">{n:02d}</span><strong>{english if en else chinese}</strong></a></li>' for n,(ident,chinese,english) in enumerate(steps,1))
 cards=lambda items: ''.join(f'<a class="academy-card" href="{target}#{i}"><h3>{t} <span aria-hidden="true">↗</span></h3><p>{d}</p></a>' for t,d,i in items)
 return f'''<main id="academy-content"><section class="academy-hero" id="home"><div><p class="academy-eyebrow">MODEL ATLAS / LEARN • BUILD • UNDERSTAND</p><h1>{c['hero']}</h1><p class="academy-lede">{c['lede']}</p><div class="academy-hero-actions"><a class="academy-primary" href="{target}#foundations">{'Start with the foundations →' if en else '从基础开始学 →'}</a><a class="academy-secondary" href="{target}#project">{'Build the Q&A project' if en else '动手做问答 Agent'}</a></div><p class="academy-hero-note">{'Read without an account. Practice with inspectable, offline examples.' if en else '无需账号阅读；用可检查的离线例子练习。'}</p></div><div class="academy-diagram" aria-label="{'Learning loop' if lang=='en' else '学习循环'}"><span>01 / {'Understand' if lang=='en' else '先理解'}</span><strong>token → attention</strong><span>02 / {'Implement' if lang=='en' else '看实现'}</span><strong>state → tool → evidence</strong><span>03 / {'Test boundaries' if lang=='en' else '验边界'}</span><strong>{'answer · abstain · stop' if lang=='en' else '回答 · 拒答 · 停止'}</strong><small>{'A learning map, not a model benchmark.' if lang=='en' else '学习路径示意，不是模型性能图。'}</small></div></section>
<nav class="academy-quicklinks" aria-label="{'On this learning home' if en else '学习首页内导航'}"><span>{'Find your next step' if en else '找到下一步'}</span><a href="#academy-paths">{'Learning paths' if en else '学习路径'}</a><a href="#academy-practice">{'Hands-on practice' if en else '动手实践'}</a><a href="#academy-discover">{'Search lessons' if en else '搜索课程'}</a><a href="#academy-evidence">{'Evidence & history' if en else '资料与历史'}</a></nav>
<div class="academy-grid academy-goals">{cards(c['goals'])}</div>
{reading_progress(lang)}
<section class="academy-section" id="academy-paths"><h2>{c['audience']}</h2><div class="academy-grid">{cards(c['roles'])}</div></section>
<section class="academy-section academy-path" id="academy-practice"><div><p class="academy-eyebrow">FOUNDATIONS → ENGINEERING</p><h2>{c['path']}</h2><ol class="academy-roadmap">{roadmap}</ol><p class="academy-path-note">{'No account needed. Learning times have not been measured.' if en else '无需账号；未做试学计时，不承诺学习时长。'}</p><a href="{target}#foundations">{'Start chapter 01 →' if lang=='en' else '从第一章开始 →'}</a><p><a href="tokenization-lab{'-en' if lang=='en' else ''}.html">{'Start with text: a tiny BPE tokenizer →' if lang=='en' else '从文本开始：微型 BPE 分词器 →'}</a></p><p><a href="tiny-training{'-en' if lang=='en' else ''}.html">{'Developer practice: train nine parameters →' if lang=='en' else '开发者实践：训练九个参数 →'}</a></p></div><div><p><a href="retrieval-lab{'-en' if lang=='en' else ''}.html">{'Developer practice: source-to-citation retrieval →' if lang=='en' else '开发者实践：从原文到检索引用 →'}</a></p><h2>{c['projectteaser']}</h2><p>{c['projecttext']}</p><a class="academy-primary" href="{target}#project">{c['enter']}</a></div></section>
<section class="academy-section"><h2>{c['changes']}</h2><div class="academy-grid">{cards(c['changeitems'])}</div></section>
<section class="academy-section academy-search" id="academy-discover"><label for="academy-search">{c['search']}</label><div class="academy-search-controls"><input id="academy-search" maxlength="200" type="search" placeholder="{c['placeholder']}" aria-describedby="academy-search-hint"><button id="academy-search-clear" type="button" hidden>{"Clear search" if lang == "en" else "清除搜索"}</button></div><p id="academy-search-status" role="status"></p><p id="academy-search-hint">{c['searchhint']} {'Search terms are kept in the page URL, up to 200 characters. Avoid private information.' if lang == 'en' else '检索词保留在页面网址中，最多 200 个字符；请勿输入隐私信息。'}</p><ul id="academy-search-results" aria-live="polite"></ul></section>
<section class="academy-section" id="academy-evidence"><h2>{c['legacy']}</h2><p>{c['legacytext']}</p><div class="academy-links"><a href="index.html?view=explore">{'Knowledge library · Chinese' if lang=='en' else '知识资料库'}</a><a href="monthly.html">{str(monthly_count)+' monthly events · Chinese' if lang=='en' else str(monthly_count)+' 条月度事件'}</a><a href="index.html?view=learn">{'Legacy learning records · Chinese' if lang=='en' else '旧版学习路线与记录'}</a></div></section></main>'''

def render(root, monthly_count):
 if type(monthly_count) is not int or monthly_count < 0: raise ValueError('invalid monthly count')
 import build_release_reading
 build_release_reading.render(root)
 import build_attention_lab
 build_attention_lab.render(root)
 import build_video_sampling_lab
 build_video_sampling_lab.render(root)
 for lang,c in CONTENT.items():
  chapters=''
  for ident,kicker,title,prereq,body in c['chapters']:
   body=body.replace('__MONTHLY_COUNT__',str(monthly_count))
   if ident=='tokens':
    bpe_name='tokenization-lab-en.html' if lang=='en' else 'tokenization-lab.html'
    bpe_label='Before attention: learn and freeze a tiny BPE tokenizer →' if lang=='en' else '先于 attention：学习并冻结微型 BPE 分词规则 →'
    body=f'<p><a class="academy-primary" href="{bpe_name}">{bpe_label}</a></p>'+body
   if ident in ('project','evaluation'):
    retrieval_name='retrieval-lab-en.html' if lang=='en' else 'retrieval-lab.html'
    retrieval_label='From raw text to retrieval and verifiable citations →' if lang=='en' else '从原文到检索与可核对的引用 →'
    body+=f'<p><a class="academy-primary" href="{retrieval_name}">{retrieval_label}</a></p>'
   if ident in ('foundations','tokens'):
    training_name='tiny-training-en.html' if lang=='en' else 'tiny-training.html'
    training_label='Nine parameters: loss, gradient, update and frozen inference →' if lang=='en' else '九个参数：损失、梯度、更新与冻结推理 →'
    body+=f'<p><a class="academy-primary" href="{training_name}">{training_label}</a></p>'
   chapters+=f'<article id="{ident}" class="academy-chapter"><p class="academy-eyebrow">{kicker}</p><h2>{title}</h2><p class="academy-outcome">{prereq}</p>{body}<div class="academy-read"><button type="button" data-read="{ident}" data-unread-label="{c["read"]}" data-read-label="{c["readDone"]}" aria-pressed="false">{c["read"]}</button><small data-read-status>{c["progress"]}</small></div><a href="#home">↑ {"Back to learning home" if lang=="en" else "返回学习首页"}</a></article>'
  toc=''.join(f'<a href="#{i}">{k} · {t}</a>' for i,k,t,_,_ in c['chapters'])
  content=header(lang)+home(lang, monthly_count)+f'<div class="academy-reader"><aside><details class="academy-chapter-disclosure" open><summary>{"Chapters" if lang=="en" else "章节目录"}</summary><nav>{toc}</nav></details></aside><div>{chapters}</div></div>'
  content+=f'<footer class="academy-footer"><p>{c["regionnote"]}</p><p>{c["footer"]}</p></footer>'
  html=f'''<!doctype html><html lang="{'en' if lang=='en' else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>ModelAtlas · {'Understand AI, build Agents' if lang=='en' else '理解 AI，开发 Agent'}</title><meta name="description" content="{escape(c['lede'])}"><link rel="stylesheet" href="academy.css"><script src="academy.js" defer></script></head><body class="academy-page"><div class="academy" data-language="{lang}">{content}</div></body></html>'''
  (root/'web'/page_name(lang)).write_text(html)
 # Home is static and readable without JavaScript; legacy DOM remains untouched.
 path=root/'web/index.html'; original=path.read_text()
 import re
 original=re.sub(r'<!-- ACADEMY HOME BEGIN -->.*?<!-- ACADEMY HOME END -->','',original,flags=re.S)
 original=original.replace('</head>','<link rel="stylesheet" href="academy.css"><script src="academy.js" defer></script></head>') if 'href="academy.css"' not in original else original
 markup='<div id="academy-home" class="academy" data-language="zh">'+header('zh')+home('zh', monthly_count)+f'<footer class="academy-footer"><p>{CONTENT["zh"]["regionnote"]}</p><p>{CONTENT["zh"]["footer"]}</p></footer></div>'
 original=original.replace('<a class="skip"', '<!-- ACADEMY HOME BEGIN -->'+markup+'<!-- ACADEMY HOME END --><a class="skip"',1)
 original=original.replace('class="atlas-workspace campus"','class="atlas-workspace campus portal-home"')
 original=original.replace('ModelAtlas · 从第一件小事学会用 AI','ModelAtlas · 理解 AI，开发 Agent')
 path.write_text(original)

def publish(root,out):
 import zipfile
 lab=root/'learning/qa-agent'
 shutil.copytree(lab,out/'qa-agent',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 # Git checkouts change mtimes and may change permissions. Do not serialize
 # filesystem metadata or zlib-dependent compressed bytes into the release.
 members=[('learning/qa-agent/'+p.name,p) for p in sorted(lab.iterdir()) if p.is_file()]
 members.append(('tests/test_qa_agent_lab.py',root/'tests/test_qa_agent_lab.py'))
 with zipfile.ZipFile(out/'qa-agent-lab.zip','w',compression=zipfile.ZIP_STORED) as z:
  for name,path in members:
   info=zipfile.ZipInfo(name,date_time=(2026,11,1,0,0,0))
   info.create_system=3
   info.create_version=20
   info.extract_version=20
   info.compress_type=zipfile.ZIP_STORED
   info.external_attr=(0o100644 << 16)
   info.internal_attr=0
   info.extra=b''
   info.comment=b''
   z.writestr(info,path.read_bytes())
if __name__=='__main__': render(Path(__file__).resolve().parents[1])
