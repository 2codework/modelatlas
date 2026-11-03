# 资料问答 Agent：离线工程实验 / Evidence QA Agent: offline engineering lab

**运行标签 / Runtime label:** Python 标准库模拟，未调用模型、API、网络或下载权重。 / Python standard-library simulation; no model, API, network call, or downloaded weights.

这不是完整 LLM 复现，不是真实模型评测，也不是生产安全认证。关键词路由代替模型规划；预审结构化事实代替文档分块与向量检索；答案必须逐字匹配证据。 / This is not a complete LLM reproduction, real-model evaluation, or production security certification. Keyword routing substitutes for model planning, reviewed structured facts substitute for document chunking and vector retrieval, and answers must exactly match evidence.

## 1. 学习目标与前置 / Goals and prerequisites

完成后能解释模型建议与程序权限的区别，并实现“计划 → 读取前人审 → 只读检索 → 生成 → 证据校验 → 发布前人审”的有限状态过程。前置：Python 函数、字典、异常；无需账号或密钥。Python 3.10+，无第三方依赖。 / After this lab, explain the difference between model proposals and program permissions, and implement a finite process: plan → pre-read human review → read-only retrieval → compose → evidence validation → pre-release human review. Prerequisites: Python functions, dictionaries, exceptions. Python 3.10+, no account, key, or third-party package.

**管理者阅读路径 / Manager path:** 先读需求、架构、失败表和生产边界，无需执行代码。 / Read requirements, architecture, failure cases, and production boundaries; running code is optional.

## 2. 需求与验收 / Requirements and acceptance

输入是一条不超过 500 字符的问题及允许读取的三份合成资料。它们不代表真实组织，也不含敏感信息。输出为状态、原因、答案、`source#section` 引用和脱敏过程日志。 / Input: one question up to 500 characters and an allowlist of three synthetic documents. These represent no real organization and contain no sensitive information. Output: status, reason, answer, `source#section` citations, and a redacted execution trace.

- `handbook#retention` 和 `policy#retention` 均写 `30 days / 30 天`。 / Both records state `30 days / 30 天`.
- `notes#owner` 写 `Research team / 研究团队`；正文同时包含故意植入的恶意指令，用于观察数据/权限隔离。 / The record states `Research team / 研究团队`; its body also contains an intentionally malicious instruction to demonstrate the data/authority boundary.
- 没有证据则拒答；不同来源值冲突则交给人处理，不多数表决、不猜。 / Refuse without evidence; escalate conflicting values rather than vote or guess.
- 人明确同意读取资料之后才调用只读工具；不支持发送邮件、访问任意路径或写外部系统。 / Call the read-only tool only after explicit human approval; sending email, arbitrary file access, and external writes are not supported.

## 3. 文件与架构 / Files and architecture

| 文件 / File | 职责 / Responsibility |
|---|---|
| `core.py` | 工具参数校验、权限关卡、状态预算、重试、证据验证 / Tool schema validation, permission gate, step budget, retries, evidence validation |
| `adapters.py` | 三份固定合成资料和确定性 FakeAdapter / Three fixed synthetic documents and deterministic FakeAdapter |
| `demo.py` | 命令行问题与明确人工确认 / CLI question and explicit human confirmation |
| `../../tests/test_qa_agent_lab.py` | 离线契约回归 / Offline contract regression |

```text
question / 问题
    ↓ FakeAdapter.plan (proposal only / 仅建议)
validated tool name / 校验工具名
    ↓ human review / 人工确认
ReadOnlySearch.search → reviewed facts / 预审事实
    ↓ no evidence → refuse / 无证据拒答
    ↓ conflicting values → needs_review / 冲突人审
FakeAdapter.compose
    ↓ exact answer + citation validation / 答案与引文校验
    ↓ human reviews candidate + citations / 人工审核候选答案和引用
answered / 返回答案
```

`Adapter` 是 Python Protocol：`plan(question)` 返回 `{tool, arguments}`；`compose(claims)` 返回 `{answer, citations}`。核心不依赖任何厂商 SDK。模型能建议调用，但仅程序决定是否执行。 / `Adapter` is a Python Protocol: `plan(question)` returns `{tool, arguments}`; `compose(claims)` returns `{answer, citations}`. The core depends on no vendor SDK. A model may propose a call, but only the program decides whether to execute it.

工具只接受 `topic` 和 `source_ids` 两个参数；类型、长度、来源白名单及重复 ID 都检查，额外字段拒绝。 / The tool accepts exactly `topic` and `source_ids`; it checks types, length, the source allowlist, and duplicate IDs, rejecting extra fields.

## 4. 运行与判读 / Run and interpret

从 ModelAtlas 仓库根目录或解压后的实验包根目录执行（需同时含 `learning/qa-agent/` 和 `tests/`）： / From the ModelAtlas repository root or extracted lab package root (containing both `learning/qa-agent/` and `tests/`):

```sh
python learning/qa-agent/demo.py
```

看到只读计划后输入 `yes`。这只批准本次内存中的合成资料读取，没有授权真实服务。任何其他输入或关闭 stdin 都拒绝。 / Enter `yes` after reviewing the read-only plan. This approves only this run's in-memory synthetic source access, not any real service. Any other input or closed stdin is denied.

证据校验后会展示候选答案和引用；核对后再输入一次 `yes` 才能发布。拒绝则返回 `human_release_denied`，最终答案留空。调用核心而不提供 `approve_release` 回调时返回 `release_review_required`，不会默认批准。这里的“发布”仅指本地返回最终答案，不会发送到任何外部系统。 / After evidence validation, the CLI shows the candidate answer and citations. Review them and enter a second `yes` to release. Denial returns `human_release_denied` with no final answer. Calling the core without an `approve_release` callback returns `release_review_required`, never implicit approval. “Release” means returning a local final answer, not sending to any external system.

正常输出应包含： / Expected normal output includes:

```json
{
  "status": "answered",
  "reason": "supported_exact_fact",
  "answer": "30 days / 30 天",
  "citations": ["handbook#retention", "policy#retention"]
}
```

再尝试： / Then try:

```sh
python learning/qa-agent/demo.py --question '谁负责？'
python learning/qa-agent/demo.py --question 'What is the budget?'
python -m unittest discover -s tests -p test_qa_agent_lab.py -v
```

第一条回答研究团队，且不执行资料中的恶意指令；第二条返回 `refused / no_evidence`。第三条运行契约测试，测试使用显式布尔回调模拟人审，**不是有人逐条批准了真实操作**。 / The first answers Research team without executing the malicious document instruction; the second returns `refused / no_evidence`. The third runs contract tests using an explicit Boolean callback to simulate human review; **it does not mean a person approved real operations**.

## 5. 控制循环、重试与观测 / Control loop, retries and observation

默认最多 8 个步骤，每个可重试阶段最多重试 1 次。只重试超时和限流；无效参数、无证据、人拒绝、冲突不能靠重试解决。人工关卡不自动重试，人工等待时间不计入执行截止时间。可配置上限防止无限循环。 / By default there are at most 8 steps and one retry per retryable stage. Only timeouts and rate limits retry; invalid arguments, no evidence, human denial, and conflicts are not solved by retrying. Human review never retries automatically, and human waiting time is excluded from the execution deadline. Configuration limits prevent infinite loops.

截止时间为协作式检查：调用前后核对耗时，**不能中止阻塞调用**。模拟适配器即时完成；真实适配器必须另设网络层超时和取消机制。模拟没有 sleep/backoff；真实限流需遵守服务返回的等待时间，并受总截止时间约束。 / The deadline is cooperative: elapsed time is checked before and after calls, and **cannot interrupt a blocking call**. The fake adapter completes immediately; a real adapter must enforce transport timeouts and cancellation. This simulation has no sleep/backoff; real rate limiting must honor server retry timing within the overall deadline.

日志仅记录阶段、尝试次数、耗时和状态，不保存问题、正文、密钥。模拟不产生模型 token；不能将其运行时间、零费用或通过率当作真实 API 的延迟、价格或准确率。 / Logs record only stage, attempt, elapsed time, and status—not questions, document bodies, or keys. The simulation uses no model tokens; its runtime, zero cost, and pass rate are not real API latency, price, or accuracy measurements.

## 6. 失败与恢复 / Failure and recovery

| 原因 / Reason | 行为与下一步 / Behavior and next action |
|---|---|
| `no_evidence` | 不生成答案；补充经过许可和审核的事实后重新开始 / No answer; add permitted, reviewed facts and start again |
| `conflicting_sources` | 保留双方引文；人核对版本、适用范围和日期 / Preserve both citations; a person checks version, scope, and dates |
| `timeout`, `rate_limit` | 达到重试上限即停止；诊断适配器，勿无限重试 / Stop after retry limit; diagnose the adapter, never retry indefinitely |
| `invalid_tool_arguments`, `invalid_tool` | 拒绝未获授权的工具或参数；修正计划，不扩张权限 / Reject tool or parameters; fix the plan without expanding permissions |
| `human_release_denied`, `release_review_required` | 不返回最终答案；检查候选及引用后重新明确审核 / No final answer; review the candidate and citations and explicitly approve again |
| `human_denied` | 读取前停止；重新运行需新的明确确认 / Stop before reading; another run requires fresh explicit approval |
| `step_budget`, `deadline` | 停止并保留脱敏日志；定位耗时，不任意解除预算 / Stop and retain redacted trace; diagnose latency instead of removing limits |
| `unsupported_answer_or_citation` | 拒绝编造答案或引用；审适配器输出和证据契约 / Reject fabricated answers or citations; inspect adapter output and evidence contract |

资料正文是数据，不是系统指令。本实验只访问预审 facts，恶意 body 根本不交给模型，因此测试证明的是这个狭窄隔离方式，**不证明真实模型抵抗提示注入**。若把自由文本送给模型，需独立隔离、最小权限、内容来源标记、对抗评测与人工升级；过滤一个关键词不足以解决注入。 / Document text is data, not a system instruction. This lab accesses reviewed facts only and sends no malicious body to a model. The test verifies this narrow isolation design, **not a real model's resistance to prompt injection**. Passing free text to a model requires separate isolation, least privilege, provenance labels, adversarial evaluations, and escalation; filtering one keyword is not sufficient.

## 7. 接真实 API 前的分层工作 / Before adding a real API adapter

本实验**未提供、未调用真实适配器**。以后可实现同一 Protocol，但不得将模拟运行自动升级为真实调用。 / This lab **neither provides nor calls a real API adapter**. A future implementation may satisfy the same Protocol, but simulation must never silently turn into a real call.

1. 明确厂商、具体版本、地区/账号/条款与费用，未核验则写未知；语言不代表市场可用性。 / Establish vendor, exact version, region/account/terms, and cost; label unverified facts unknown. Language does not establish regional availability.
2. 用户明确授权后再配置密钥与允许资料；从安全配置注入密钥，不写入代码或日志。 / Obtain explicit authorization before configuring keys and source access; inject keys securely, never in code or logs.
3. 在适配层做响应 schema、token 上限、传输超时、有限重试和真实用量记录；核心仍独立校验工具权限与引文。 / Put response schema, token limits, transport timeouts, bounded retries, and actual usage recording in the adapter; keep tool permission and citation validation in the core.
4. 不能直接用精确字符串测试评估自然语言答案；另建带标准答案、证据支持、引用准确率与拒答质量的真实模型评测，并报告配置和失败。 / Exact-string tests do not evaluate natural-language answers; build real-model evaluations for gold answers, evidence support, citation accuracy, and refusal quality, reporting configuration and failures.
5. 生产部署还需鉴权、文档权限/删除与保留策略、隔离、审计、监控、回滚和隐私审查。本样例不具备这些保障。 / Production also needs authentication, document access/deletion/retention controls, isolation, audit, monitoring, rollback, and privacy review. This sample provides none of those guarantees.

## 8. 自检与下一步 / Self-check and next step

- 为什么工具调用不能直接信任？ / Why not trust a tool call directly? **模型输出是建议，不是授权；程序校验参数、来源及人审。 / Model output is a proposal, not authorization; the program validates arguments, sources, and approval.**
- 找到两份资料是否就可靠？ / Do two retrieved documents establish reliability? **还需检查是否独立、同一版本、范围一致；冲突不能多数表决。 / Check independence, version, and scope; conflicts are not settled by voting.**
- 本测试能证明模型聪明吗？ / Does this test prove a model is capable? **没有运行模型，只验证控制逻辑。 / No model ran; only controller logic was tested.**

练习：复制合成资料到测试内，把第二份保留期改成 `90 days`，确认程序返回 `needs_review` 且不输出答案。接着为新的失败模式写测试，再改逻辑；不要先去掉安全关卡来让演示成功。 / Exercise: copy the synthetic corpus in a test, change the second retention value to `90 days`, and confirm `needs_review` with no answer. Then write a new failure test before changing logic; do not remove safety gates merely to make a demo succeed.

**证据口径 / Evidence scope:** 原创教学设计及本地代码；运行记录见 `TEST-RESULTS.md`。资料、日期和机构均为合成练习，不增加 ModelAtlas 历史事件或模型记录。 / Original teaching design and local code; see `TEST-RESULTS.md` for execution. Documents and organizations are synthetic fixtures and add no ModelAtlas historical event or model records.

## 证据快照与变异回归 / Evidence snapshots and mutation regressions

`compose` 调用前，宿主把证据字段验证为非空纯字符串，再保存不可变 tuple 和允许引文 frozenset；每次尝试只把新列表和新 Claim 对象传给适配器。嵌套列表/字典不是本模拟的合法字段，直接拒绝。适配器替换列表、修改副本或原资料、在重试前变异输入，都不能改变验收依据。发布审核前，已验证答案和引文也脱离适配器拥有的可变输出；审核不是编辑接口。截止时间只接受有限 int/float 且 0 < 值 ≤ 30，排除 bool，错误输入安全拒绝。

Before `compose`, the host validates evidence fields as nonempty plain strings and stores immutable tuples and an allowed-citation frozenset. Every attempt receives a fresh list and fresh Claim objects. Nested lists/dictionaries are outside this simulation schema and are rejected. Replacing the list, mutating copied objects or source documents, and mutating before a retry cannot change the validation basis. Before release review, validated answers and citations are detached from adapter-owned mutable output; review is not an editing interface. Deadlines accept only finite int/float values with 0 < value ≤ 30, excluding bool; invalid inputs fail closed.

这是离线模拟数据契约修复，不是任意 Python 适配器的安全沙箱，也不是生产安全认证。 / This is an offline simulation data-contract fix, not a sandbox for arbitrary Python adapters or production security certification.
