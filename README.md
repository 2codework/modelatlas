# ModelAtlas

**把模型放回知识的坐标系。** 可追溯的大模型知识地图与中文学习书稿，v0.2.2。

这是代表性研究起点，不是全球所有厂商、所有版本或截至今天的完整清单，也不是性能排行榜。

## 本地使用

需要 Python 3.10+；前端无需依赖安装。Node 18+ 仅用于纯函数测试。

```sh
python scripts/build.py
python -m unittest discover -s tests -v
node --check web/app.js
node --test tests/core.test.js
python -m http.server 8000 --directory dist
```

然后在浏览器打开 `http://localhost:8000`。不要直接双击 HTML（浏览器可能阻止本地 fetch）。
构建不联网、不安装第三方代码。`dist/` 是静态站点；项目路径相对资源适合 GitHub Pages。

## 能做什么

- 中文关键词搜索；按节点类型、类别、机构与可获得性组合筛选。
- 节点详情、原始来源、核验日期/版本/证据等级、误区、操作学习步骤。
- 原创 SVG 一跳关联图（最多显示12个邻居）；下方完整等价关系列表支持键盘操作。
- 独立事件时间轴：论文首次提交、报告公开、公告、权重开放、API 上线绝不互相替代。
- 未知日期单列；保留年/月/日精度，不补造日期。
- 学习路径、浏览器本地已读记录、可导入导出进度；损坏文件不覆盖原进度。
- 数据集/评测注册表只展示介绍、口径、来源及外链。不提供题目、答案或受限数据。
- 历史报告成绩卡片：固定报告版本、表/页证据、shot、统计口径与作者自报限定；不是独立复现、不是当前排行榜、不跨配置横比。
- 同源 `BOOK.md` 由研究数据生成，而非另一套手工摘要。
- 生命周期、固定版本、替代节点与操作检查路径：历史知识不直接充当当前部署推荐。

## 数据及证据

`data/research/` 保留研究者提交的完整原始 JSON。`scripts/build.py` 验证引用并生成站点视图；原研究包同时保留在 `dist/research/` 与 `data.json.research_bundles`。不得直接修改生成文件。

模型家族、具体发布、机构、概念、运行时、协议和评测是不同实体。不同来源中同词不自动合并。JEV 暂未消歧，不映射 JEPA；RSI 是受限研究概念，不宣称通用递归自改进已经实现。

“已核验”仅说明研究者检查原始页面/论文摘要或元数据支持对应摘要，不说明全部论文经过精读、教程经过执行、许可证经过法律审查或结果经过独立复现。前端明确保留未知值。详见 [SOURCE_METHOD.md](SOURCE_METHOD.md)、[QUALITY.md](QUALITY.md)。

## 仓库结构

```
data/research/    不丢字段的研究输入
web/              无依赖 HTML/CSS/JavaScript
scripts/build.py  标准库校验、规范化、同源书稿生成
tests/            内容完整性与浏览器纯逻辑测试
ci-drafts/        保留旧禁用草案；当前只读门禁在 .github/workflows/checks.yml
dist/             生成后的静态网页
BOOK.md           同源生成的中文书稿
```

## 发布与许可

包含 push/PR 只读 CI 配置。此仓库维护源码；线上对应提交以 Actions / Pages 结果为准，本地测试不等于线上验收。部署步骤见 [DEPLOYMENT.md](DEPLOYMENT.md)。

本轮采用代码 MIT、原创编辑文本与原创图形 CC BY 4.0 的许可方案。第三方模型、论文、数据、网页、商标及引用的事实来源不受本项目重新许可。详见 [LICENSE-CONTENT.md](LICENSE-CONTENT.md)。

## 创作专题与历史时间轴

网站：https://2codework.github.io/modelatlas/ 。新增设计、音乐、视频资料以官方文档审阅为依据，未运行模型/付费 API/第三方工具，不承诺全量市场覆盖。

实践与技术使用经 ID 校验的 `?case=<id>` / `?node=<id>` 双向链接；模型、工具接口、标准、普通软件分别保留类型。书稿和网站由同一研究 JSON 构建。旧节点与案例保留；许可、费用、生命周期、来源和未实测状态不可省略。

## 日期证据

事件总数与已知/未知日期分布以网站时间轴统计及生成的 `dist/data.json` / `docs/data.json` 为准。`timeline-dates.json` 是追加式证据覆盖层；构建时核对 `expected_before`，不重写历史研究包。BLOOM API 的 `available_by=2022-07-12` 只说明截至该日可用，不替代精确首发日期。GPT-3 API 限 private beta，Gemini 1.0 Pro / Pro Vision 限 Vertex AI Preview，不标作 GA。时区未声明则保留 null。

## MCP、Skill 与提示词 · 十二课

新增 12 个原创深教程：角色、历史初始化、工具调用、资源与模板、错误、取消、权限、提示注入、Skill、调试、迁移与现行消息。每课在网站和同源书稿中完整保留目标、前置、输入输出、提示词、步骤、验收、错误、权限、来源与版本。MCP 2025-11-25 的 initialize 是历史教学；2026-07-28 对照采用逐请求元数据。Skills 扩展已发布、SEP-2640 Final；具体宿主支持仍待逐版本验证。

`learning/mcp/raw/` 原字节保留研究采集历史；`overlay.json` 是经核验的补充说明。页面默认展示显式适配后的教学正文，而非内部状态。ZIP 下载内含原包与 `VERIFIED-OVERLAY.json`；请同时阅读。只有原创标准库模拟契约经过测试，不是 MCP SDK、真实服务器、OAuth、模型或行业效果验证。没有安装、账号、付费或真实调用。

```sh
python learning/mcp/raw/validate.py
python -m unittest discover -s learning/mcp/raw/tests -v
```

不新增未经核验的版本事件或模型能力断言。保留全部旧案例、节点、日期覆盖层与互链；源网页的权利与适用条件不因本教程而改变。此仓库维护源码；线上对应提交以 Actions / Pages 结果为准，本地测试不等于线上验收。

## 厂商目录（可追溯记录）

新增独立目录视图与 `?catalog=<id>` 深链接，支持厂商、实体类型、输入/输出模态、生命周期与全字段搜索。目录记录数以网站目录统计及生成的 `dist/data.json` / `docs/data.json` 为准，目录记录不等同于新增模型；历史知识图与事件独立保留。原始数据、QA修订、覆盖缺口、许可差异与官方教程链接完整保留。详见 [CATALOG.md](CATALOG.md)；不生成价格/性能排名，不运行模型或SDK。

## 评测介绍扩充（22条版本/分片记录）

原11项登记与3条历史成绩不变，新增22条介绍来自15个家族。搜索名称、版本或分片，或使用 `?node=bench-docvqa-2020-task1` 等深链接；详情展示口径、聚合量及官方入口。版本/分片分别保留，8条关系明确不代表成绩可比。没有新增题目、答案或成绩。

`data/benchmarks/raw/` 原字节保留历史研究；`overlay.json` 明确访问修订，`admission.json` 固定SHA-256。DocVQA下载账户/条款未知；MathVista test标签不公开；WorkArena运行实例需审批；GAIA门控且禁止可爬重发；OCRBench v2仅研究非商业。任何公开入口都不自动等于匿名下载、完整本地复现或商用许可。下游下载未逐项测试。

网站与书稿同源生成；没有据核验日期添加发布日期或外部配图。未执行benchmark、登录、下载受限包或访问真实设备。

## 区域办公平台补包

[7条区域办公平台与人监督练习](REGIONAL_OFFICE.md)：Dify、Coze Studio、飞书 aily 企业工作伙伴、钉钉宜搭 AI 助理、Zoho Zia Agents、百炼智能体应用、腾讯云智能体开发平台。均为 documentation-only / never-run；保留许可、地域/租户条件、命名关系未知及较弱来源说明，不是7个基础模型。原始包与独立QA位于 `learning/regional-office/r1/`。

## 知识图谱关联补充 r1

新增12条现有节点间关系：1条官方文档迁移目标、11条编辑学习对照。网页用显式分类区分来源文档关系、编辑对照与未知；来源审阅不是产品运行验证，迁移目标不是迁移完成。

原始R1/R2研究与独立QA完整保留于 `learning/knowledge-graph-links/r1/raw/`，仍为研究时 `candidate_only_not_applied`；`admission.json` 固定字节与来源对象哈希，派生 `knowledge_graph_links_application` / `knowledge-graph-links/application.json` 单独记录接纳到本地构建。151边、72孤立、108弱连通分量只统计D.edges内部图，不计实践、AgentWork跨站及网页导航链接；孤立不等于网页无链接，不表示知识覆盖完整或准确性提升。未运行产品或发布本候选。

维护边界：本批采用整份基线顶层对象哈希的 fail-closed 接纳，不是自动兼容未来目录增量的通用适配器。后续任何模块改变基线对象都会阻断构建，须重新审核并更新 admission 中的基线对象哈希及适配器固定 admission SHA，再完整复跑保真与负面门禁；不可跳过校验或覆盖原始研究状态。

## 实时语音模型 · 有限样本 r1

[可读学习页](https://2codework.github.io/modelatlas/realtime-audio.html) / [专题书稿](REALTIME_AUDIO.md)：Moshi家族、CSM 1B、Voxtral Realtime 2602、GPT-Realtime分版本家族。只有4个新模型实体，不把托管API、演示客户端或量化后端另算模型；不代表全球完整音频模型史。新节点无新增关系边。

后置 `realtime_audio.apply` 在固定r1知识图接纳之后执行，**未修改旧graph adapter/admission**。其封存输入仍为242节点、151边；当前全站246节点、151边、373来源、182事件（107有日期、75未知）。旧知识图 application.after 只表示历史接纳阶段；当前全图76孤点/112弱分量，不等于网站无链接。

`learning/realtime-audio/r1/`封存R1/R2及两轮独立QA原字节；新admission严格检查旧顶层对象完整哈希、新ID、对象哈希及来源清单。测试在验证封闭增量后才向旧模块测试提供独立封存旧阶段，旧fixture及断言不削弱。GPT2前代历史仍是覆盖缺口；2.1无已证实首发日期，不补事件；2027停用仅为指定旧ID的未来计划，列表和详情显著标记。

所有模型均never-run；没有登录、权重下载、SDK执行、收费或设备访问。新的离线DOM测试只验证自编展示程序，不是浏览器渲染或语音性能测试。
