"""Bounded bilingual editorial lesson. No catalog mutation or model execution."""
from html import escape
from pathlib import Path

CHECKED = '2026-11-01'
SOURCES = [
 ('A', 'https://qwenlm.github.io/blog/qwen3/', 'Introduction / dense-model table', '公告日期为 2025-04-29，开放权重名单包含 Qwen3-8B；表中上下文简写为 128K。', 'The announcement is dated 2025-04-29, includes Qwen3-8B among open weights, and abbreviates its context as 128K.'),
 ('B', 'https://huggingface.co/Qwen/Qwen3-8B', 'Model Overview / Processing Long Texts', '准确模型：稠密因果语言模型，8.2B 参数、36 层、GQA 32 个 Q 头 / 8 个 KV 头。上下文：原生 32,768；使用 YaRN 时 131,072 token。', 'Exact model: dense causal LM, 8.2B parameters, 36 layers, GQA with 32 Q / 8 KV heads. Context: 32,768 native; 131,072 tokens with YaRN.'),
 ('C', 'https://arxiv.org/abs/2505.09388v1', 'Abstract / Submission history [v1]', 'Qwen3 家族技术报告 v1 提交于 2025-05-14T13:41:34 UTC；不是 8B 专属发布公告。', 'The family technical report v1 was submitted on 2025-05-14T13:41:34 UTC; it is not an 8B-only release announcement.'),
 ('D', 'https://huggingface.co/Qwen/Qwen3-8B/tree/main', 'Files / safetensors shards and index', '公开文件列表可见权重分片与索引；本课未下载权重。', 'The public listing shows weight shards and an index; this lesson downloaded no weights.'),
 ('E', 'https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE', 'LICENSE / heading', '准确仓库的 LICENSE 显示 Apache 2.0；只记录可见许可证据，不作法律批准。', 'The exact repository LICENSE displays Apache 2.0; this records visible evidence, not legal approval.'),
]

def render(root):
 for en in (False, True):
  def t(zh,eng): return eng if en else zh
  suffix = '-en' if en else ''
  other = '' if en else '-en'
  title = t('发布阅读课：把 Qwen3-8B 公告写成有条件的简报','Release reading: turn a Qwen3-8B announcement into a qualified brief')
  template = t('''# 模型发布简报模板

- 准确对象 / 提供方 / 家族（不要合并服务、别名、checkpoint）：
- 证据模式：仅使用本课编辑释义 / 自己打开并核对原始来源（逐项注明）：
- 编辑核验日期：2026-11-01（仅指本课证据卡；其他模型另填）：
- 学习者独立核验日期：未独立核验（仅在自己核对后填写；不要继承编辑日期）：
- 公告日期 + 事件类型 + 来源定位：
- 论文日期 + 版本 + 来源定位：
- 首次上传 / 权重开放 / API 上线（分别记录；缺证据写未知）：
- 特点：输入输出、架构、参数；每项绑定准确对象与来源：
- 条件：原生限制 / 扩展上限 / 额外配置；不要只抄最大数字：
- 权重与许可：列表、许可文件、可变分支或固定版本；未验证事项：
- 未知：模型卡原始发表/更新日期、地区、账号、延迟、硬件、任务质量：
- 一句判断：支持什么决策？还不支持什么决策？
- 下一步：要补的证据、成功条件与停止条件：

## 证据账本

| 主张 | 对象/事件 | 来源与章节 | 条件 | 已知/未知 | 编辑核验日 / 学习者核验日 |
| --- | --- | --- | --- | --- | --- |
| 待填写 | | | | | |

## 发布前自查

- 日期是否带事件名？是否把核验日当发布日？
- 家族特性是否误套到某个成员？
- 最大值是否丢失配置条件？
- 开放权重是否被误写成开源、无条件商用或部署就绪？
- 是否把工具能力写成宿主授权或自动执行？
- 不知道的项目是否明确保留未知？

练习用模板；不是法律审查、性能测试或掌握证明。
''','''# Model release brief template

- Exact entity / provider / family (do not merge services, aliases and checkpoints):
- Evidence mode: supplied editorial summaries / independently opened and checked primary sources (state per claim):
- Editor check date: 2026-11-01 (this lesson’s cards only; fill anew for another model):
- Learner verification date: not independently checked (fill only after your own check; do not inherit the editor date):
- Announcement date + event type + source locator:
- Paper date + version + source locator:
- First upload / weight release / API launch (separate; unknown without evidence):
- Characteristics: inputs/outputs, architecture, parameters; bind each to the exact entity and source:
- Conditions: native limit / extended limit / extra configuration; do not copy only the largest number:
- Weights and license: listing, license file, mutable branch or pinned revision; unverified aspects:
- Unknowns: original model-card publication/update date, region, account, latency, hardware, task quality:
- Decision sentence: what does this support, and what does it not support?
- Next step: missing evidence, success condition and stopping condition:

## Evidence ledger

| Claim | Entity/event | Source and section | Condition | Known/unknown | Editor check / learner verification |
| --- | --- | --- | --- | --- | --- |
| Fill in | | | | | |

## Pre-release review

- Does each date name an event? Is a check date being mistaken for a release?
- Are family characteristics being assigned to a specific member?
- Has a maximum lost its configuration condition?
- Have open weights become an unsupported claim of open source, unconditional commercial use or deployment readiness?
- Has tool capability become host authorization or autonomous execution?
- Are unknowns explicitly retained?

Practice template; not legal review, performance testing or proof of mastery.
''')
  brief = t('''Qwen 团队在 2025-04-29 的公告中将 Qwen/Qwen3-8B 列入开放权重的稠密模型（A）。不要把公告表中的 128K 直接写成原生上限；准确模型卡区分原生与 YaRN 扩展（B）。2025-05-14 是家族报告 v1 提交日（C），不是本课证明的首次上传日。权重列表与许可文件可见（D/E），但这不能证明特定地区服务可用或部署就绪。''','''Qwen’s dated 2025-04-29 announcement includes Qwen/Qwen3-8B as dense open weights (A). Do not turn the table’s 128K into a native limit: the exact card distinguishes native context from YaRN extension (B). 2025-05-14 is the family report v1 submission date (C), not a first-upload date established here. Listing and license evidence are visible (D/E), without establishing regional service access or deployment readiness.''')
  rows = [
   (t('对象','Identity'),t('Qwen/Qwen3-8B；提供方 Qwen / Alibaba；不是整个家族、Base 变体或 API 别名。','Qwen/Qwen3-8B; Qwen / Alibaba; not the whole family, a Base variant or an API alias.'),'A/B'),
   (t('日期','Dates'),t('2025-04-29：有日期的官方公告；2025-05-14：报告 v1；2026-11-01：本课核验。首次上传仍未知。','2025-04-29: dated official announcement; 2025-05-14: report v1; 2026-11-01: lesson check. First upload remains unknown.'),'A/C'),
   (t('特点与条件','Characteristics and conditions'),t('稠密文本生成模型，不因家族含 MoE 就变成 MoE。原生 32,768 / YaRN 131,072；扩展条件不能省略。','Dense text-generation model, not MoE merely because the family includes MoE. Native 32,768 / YaRN 131,072; keep the extension condition.'),'A/B'),
   (t('权重与许可','Weights and license'),t('开放权重列表 + Apache 2.0 文件。main 可变，未固定权重修订、未下载、未审计；开放权重不自动等于开源。','Open-weight listing + Apache 2.0 file. Mutable main, no pinned weight revision, download or audit; open weights do not automatically mean open source.'),'D/E'),
   (t('未知与边界','Unknowns and boundaries'),t('首次上传、模型卡原始发表/更新日期、API 上线、地区与账号条件、延迟、硬件需求、任务质量均未独立确立。无最新、全球完整或基准冠军结论。','First upload, original model-card publication/update date, API launch, regional/account conditions, latency, hardware needs and task quality are not independently established. No latest, globally complete or benchmark-winner claim.'),t('本课范围','Lesson scope')),
  ]
  example = '# '+title+'\n\n'+brief+'\n\n'+t('## 已填写账本','## Completed ledger')+'\n\n'+'\n'.join('- **'+a+'**: '+b+' ['+c+']' for a,b,c in rows)+'\n\n'+t('编辑核验日期：','Editor check date: ')+CHECKED+'\n\n'+t('证据模式：本课提供的编辑释义。学习者独立核验日期：未独立核验；不要把编辑日期当作自己打开原始来源的日期。','Evidence mode: supplied editorial summaries. Learner verification date: not independently checked; do not treat the editor date as your own primary-source check.')+'\n\n'+t('## 来源定位（编辑释义，非原文摘录）','## Source locators (editorial paraphrases, not excerpts)')+'\n\n'+'\n'.join(f'- {sid}: [{locator}]({url})' for sid,url,locator,zh,eng in SOURCES)+'\n\n'+t('结论：可以进入任务评估规划，不能直接批准部署。先确定任务、授权、运行条件和验收标准；本课没有运行模型、API、MCP 或宿主工具。','Decision: proceed to evaluation planning, not deployment approval. Establish the task, authorization, runtime conditions and acceptance criteria first. No model, API, MCP or host tools ran in this lesson.')+'\n'
  for kind,content in [('template',template),('example',example)]:
   (root/'web'/f'release-brief-{kind}{suffix}.md').write_text(content)
  cards=''.join(f'<article class="evidence-card" id="evidence-{sid}"><h3>{sid} · {escape(locator)}</h3><p>{escape(eng if en else zh)}</p><p><a href="{url}">{t("官方原始来源（可选外链）","Primary source (optional external link)")}</a> · {t("编辑核验","Editor checked")} {CHECKED}</p></article>' for sid,url,locator,zh,eng in SOURCES)
  ledger=''.join(f'<dt>{a} <small>· {c}</small></dt><dd>{b}</dd>' for a,b,c in rows)
  html=f'''<!doctype html><html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>{title} · ModelAtlas</title><link rel="stylesheet" href="academy.css"><link rel="stylesheet" href="release-reading.css"><script src="release-reading.js" defer></script></head><body class="academy-page"><main class="release-lesson"><header><a href="academy{suffix}.html#timeline">← {t('返回 AI 发展史','Back to AI Timeline')}</a><a data-release-language href="release-reading{other}.html" lang="{'zh-CN' if en else 'en'}">{t('English','中文')}</a></header>
<p class="academy-eyebrow">MODELATLAS · {t('真实模型 / 编辑释义 / 无代码练习','REAL MODEL / EDITORIAL PARAPHRASES / NO-CODE PRACTICE')}</p><h1>{title}</h1>
<p>{t('前置：知道模型不等于应用或 Agent。产出：一份能保留条件与未知项的发布简报。路线：读证据卡 → 看推理示范 → 独立修订 → 按量规回查。无需账号；下方材料足够完成，外链只是进一步核对。','Prerequisite: distinguish a model from an application or Agent. Outcome: a release brief preserving conditions and unknowns. Read evidence → follow the worked reasoning → repair independently → review against the rubric. No account required; supplied material is sufficient and external links are optional.')}</p>
<p class="scope">{t('这是一个有界的真实模型阅读案例，不是最新榜单或完整发布史。核验日 2026-11-01；旧目录记录仍为 2026-10-28，不因本课刷新。main 分支与模型卡会变化，未固定权重修订。没有下载权重、运行真实模型、调用 API/MCP、执行宿主动作或保存学习记录。','This is one bounded real-model reading case, not a latest ranking or complete release history. Checked 2026-11-01; the legacy catalog retains 2026-10-28. The main branch and model card are mutable; no weight revision is pinned. No weights downloaded, real model run, API/MCP call, host action or learning-record storage.')}</p>
<p class="scope">{t('证据模式：本页使用编辑提供的原始来源释义，编辑核验日为 2026-11-01。只读本页的学习者应填写“未独立核验”；只有自己打开并核对原始来源后，才能记录自己的核验日期。编辑日期不是模型卡原始发表/更新日期，后者在本课中未独立确立。','Evidence mode: this page supplies editorial primary-source summaries, checked by the editor on 2026-11-01. A learner using only this page should write “not independently checked”; record a learner verification date only after personally opening and checking the primary sources. The editor date is not the original model-card publication/update date, which is not independently established here.')}</p><nav aria-label="{t('本课目录','Lesson contents')}"><a href="#evidence">1 · {t('证据','Evidence')}</a><a href="#worked">2 · {t('示范','Worked brief')}</a><a href="#practice">3 · {t('独立修订','Independent repair')}</a><a href="#reference">4 · {t('参考与回查','Review')}</a><a href="#template">5 · {t('带走模板','Take the template')}</a></nav>
<section id="evidence"><h2>1 · {t('先区分证据能回答什么','First ask what each source can establish')}</h2><p>{t('下面是精简的编辑释义，不是网页全文或运行结果。A 定事件，B 限定准确对象与条件，C 定报告日期，D/E 检查可见文件与许可；没有一张卡能单独证明部署就绪。','These are concise editorial paraphrases, not full pages or execution results. A identifies an event; B narrows entity and conditions; C dates the report; D/E establish visible files and licensing evidence. None alone establishes deployment readiness.')}</p>{cards}<h3>{t('只需读懂这四个术语','Four terms needed for this brief')}</h3><dl><dt>{t('稠密 / MoE','Dense / MoE')}</dt><dd>{t('这是架构分类，不是质量排名。MoE 按路由选择部分专家；不能只凭家族名判断某个成员。','These describe architecture, not a quality ranking. MoE routes work to selected experts; a family name alone cannot classify a member.')}</dd><dt>{t('因果语言模型','Causal language model')}</dt><dd>{t('按已有上下文预测后续 token；不表示理解或输出必然正确。','Predicts subsequent tokens from preceding context; the label does not guarantee understanding or correctness.')}</dd><dt>GQA</dt><dd>{t('多个 query 头共享较少的 key/value 头。头数描述内部结构，不直接说明速度或质量。','Multiple query heads share fewer key/value heads. Head counts describe structure, not a measured speed or quality result.')}</dd><dt>{t('原生 / YaRN 扩展','Native / YaRN extension')}</dt><dd>{t('前者与需要额外扩展方法的长度不是同一条件。这里把 YaRN 视为必须保留的配置限定，不演示部署，也不保证任意长文本任务质量。','Native and extension-dependent lengths are different conditions. Here YaRN is a required configuration qualifier, not a deployment demonstration or a guarantee of arbitrary long-context task quality.')}</dd></dl></section>
<section id="worked"><h2>2 · {t('示范：先修饰主张，再写简报','Worked example: qualify the claim before summarizing')}</h2><ol><li>{t('先固定对象为准确仓库，不把家族中的所有能力合并。','Fix the exact repository first; do not pool every family capability.')}</li><li>{t('公告与模型卡不是简单二选一：保留公告的历史事件，用模型卡给最大数字补上运行条件。','Do not simply choose announcement or card: retain the historical event and use the card to qualify the maximum.')}</li><li>{t('报告晚于公告不冲突，因为它们不是同一种事件。核验时间也不是首次发布时间。','A report following an announcement is not a contradiction: they are different events. A check date is not a first-release date either.')}</li><li>{t('许可线索与能力描述都不能替代授权、性能评测或上线验收。','License evidence and capability descriptions cannot replace authorization, evaluation or acceptance checks.')}</li></ol><blockquote>{brief}</blockquote><h3>{t('身份 / 日期 / 条件 / 许可 / 未知账本','Identity / date / condition / license / unknown ledger')}</h3><dl>{ledger}</dl></section>
<section id="practice"><h2>3 · {t('独立修订：给同事的简报哪里会误导？','Independent repair: what would mislead a colleague?')}</h2><p>{t('先别展开参考答案。以下是本站原创的错误简报，不是厂商原话。','Do not open the reference yet. This deliberately flawed brief is original teaching material, not a vendor quotation.')}</p><blockquote class="flawed">{t('“Qwen3-8B 于 2025-05-14 发布，原生支持 128K。Qwen3 家族有 MoE，所以 8B 也是 MoE。支持 Agent 就表示模型能自主执行宿主操作；既然开放权重，就能直接部署。”','“Qwen3-8B was released on 2025-05-14 and natively supports 128K. The Qwen3 family includes MoE, so 8B is MoE too. Agent capability means the model autonomously executes host actions; open weights mean we can deploy immediately.”')}</blockquote><ol><li>{t('逐句写“保留 / 改写 / 证据不足”，为每个修改标 A–E 或“本课推理边界”。','Mark each sentence keep / revise / insufficient evidence; tag each correction A–E or “lesson reasoning boundary”.')}</li><li>{t('用自己的话写三至五句替代简报，并在账本中单列原生与扩展条件。','Write a replacement in three to five sentences; separate native and extended conditions in the ledger.')}</li><li>{t('至少保留三项未知，并提出一个下一步证据问题。可用纸笔或下方 Markdown，不必提交任何内容。','Retain at least three unknowns and propose one next evidence question. Use paper or the Markdown below; nothing needs submitting.')}</li></ol></section>
<section id="reference"><h2>4 · {t('参考答案、量规与失败恢复','Reference, rubric and recovery')}</h2><details><summary>{t('完成独立修订后展开参考答案','Open the reference after your independent repair')}</summary><ol><li>{t('日期句改为带事件名的日期：A 是有日期的公告，C 是报告 v1；首次上传不在本课证据中。','Replace the date claim with named events: A is the dated announcement, C is report v1; first upload is not established here.')}</li><li>{t('上下文句要引用 B 的原生 / YaRN 两档，而不是把 A 的简写当成无条件原生值。','Use B’s native / YaRN distinction rather than treating A’s shorthand as an unconditional native limit.')}</li><li>{t('架构句改为准确成员的稠密模型；不能从家族包含 MoE 推断所有成员都是 MoE（A/B）。','Use the exact member’s dense architecture; family membership does not imply MoE for every member (A/B).')}</li><li>{t('自主执行句删去：这是能力到权限的错误推理。模型提出动作不等于宿主已批准并执行；授权和工具校验属于系统边界。','Remove autonomous execution: it confuses capability with authority. A model proposing an action does not mean the host approved and executed it; authorization and tool validation are system boundaries.')}</li><li>{t('部署结论改为“可以规划评估，尚不能批准上线”；D/E 不回答地区、账号、硬件、延迟或任务质量。','Replace deployment approval with “ready to plan evaluation, not approve deployment”; D/E do not establish region, account, hardware, latency or task quality.')}</li></ol></details>
<h3>{t('回查量规（不是掌握认证）','Review rubric (not a mastery certificate)')}</h3><ul><li>{t('对象：准确 ID 不丢，家族 / 服务 / 模型不混。','Identity: exact ID retained; family, service and model kept separate.')}</li><li>{t('时间：事件带日期；公告、报告、核验和未知的首次上传分开。','Time: dates name events; announcement, report, check and unknown first upload remain distinct.')}</li><li>{t('条件：原生与扩展同时出现，保留 YaRN；不把能力当授权。','Conditions: native and extended limits both appear, with YaRN retained; capability is not authorization.')}</li><li>{t('证据：每项修订有卡片 ID / 推理边界；至少三项未知和一个补证问题。','Evidence: every correction has a card ID / reasoning boundary; at least three unknowns and one evidence question.')}</li><li>{t('结论：不从许可和权重直接跳到上线，也不声称最新、完整或冠军。','Decision: no leap from license/weights to deployment, and no latest, completeness or winner claim.')}</li></ul><p>{t('漏掉任一项，先回到相应卡片重写，而不是重复背日期。混淆对象→A/B；最大值丢条件→B；日期混淆→A/C；许可外推→D/E。完成只是一次可检查的练习，不证明已掌握所有发布阅读。','If any item fails, revisit its evidence and rewrite rather than memorizing dates. Entity confusion → A/B; unqualified maximum → B; date confusion → A/C; license overreach → D/E. Completion is one reviewable exercise, not proof of general mastery.')}</p></section>
<section id="template"><h2>5 · {t('复用简报，而不是复制结论','Reuse the brief structure, not the conclusion')}</h2><p><a download href="release-brief-template{suffix}.md">{t('下载 Markdown 模板','Download Markdown template')}</a> · <a download href="release-brief-example{suffix}.md">{t('下载本课填写示例','Download worked Markdown example')}</a></p><details><summary>{t('在浏览器中阅读 / 复制完整模板','Read / copy the full template in your browser')}</summary><pre>{escape(template)}</pre></details><p>{t('下一次换模型时重新核对准确版本、事件和条件，不继承这里的数值与许可。若要真正部署，先提出任务与授权范围，另做环境、可用性和质量评估；本课到简报修订为止。','For another model, recheck its exact version, events and conditions; do not inherit these numbers or license. Real deployment needs a defined task and authorization, plus separate environment, availability and quality evaluation. This lesson stops at a revised brief.')}</p><p><a href="academy{suffix}.html#resources">{t('返回模型与资料','Back to Models & Resources')}</a> · <a href="academy{suffix}.html#tools">{t('补课：工具与授权边界','Review: tools and authorization boundaries')}</a> · <a href="academy{suffix}.html#evaluation">{t('下一步：评测方法','Next: evaluation methods')}</a></p></section>
<footer><p>{t('语言不等于地区。链接携带地区选择，但本课未核验任何地区服务可用性；离线阅读内容在各地区相同。','Language is not region. Links carry the region choice, but no regional service availability is verified; offline lesson content is the same across regions.')}</p><noscript>{t('JavaScript 已关闭：全部材料与下载仍可读；切换页面时地区参数不会自动携带。','JavaScript is off: all material and downloads remain readable; region parameters are not automatically carried between pages.')}</noscript></footer></main></body></html>'''
  (root/'web'/f'release-reading{suffix}.html').write_text(html)

if __name__ == '__main__':
 render(Path(__file__).resolve().parents[1])
