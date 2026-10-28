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

包含 push/PR 只读 CI 配置；线上状态以对应提交的 Actions 与 Pages 结果为准。部署步骤见 [DEPLOYMENT.md](DEPLOYMENT.md)。

本轮采用代码 MIT、原创编辑文本与原创图形 CC BY 4.0 的许可方案。第三方模型、论文、数据、网页、商标及引用的事实来源不受本项目重新许可。详见 [LICENSE-CONTENT.md](LICENSE-CONTENT.md)。

## 创作专题与历史时间轴

网站：https://2codework.github.io/modelatlas/ 。新增设计、音乐、视频资料以官方文档审阅为依据，未运行模型/付费 API/第三方工具，不承诺全量市场覆盖。

实践与技术使用经 ID 校验的 `?case=<id>` / `?node=<id>` 双向链接；模型、工具接口、标准、普通软件分别保留类型。书稿和网站由同一研究 JSON 构建。旧节点与案例保留；许可、费用、生命周期、来源和未实测状态不可省略。

## 日期证据

87 条事件中 50 条有日期、37 条日期未知。`timeline-dates.json` 是追加式证据覆盖层；构建时核对 `expected_before`，不重写历史研究包。BLOOM API 的 `available_by=2022-07-12` 只说明截至该日可用，不替代精确首发日期。GPT-3 API 限 private beta，Gemini 1.0 Pro / Pro Vision 限 Vertex AI Preview，不标作 GA。时区未声明则保留 null。

## MCP、Skill 与提示词 · 十二课候选

新增 12 个原创深教程：角色、历史初始化、工具调用、资源与模板、错误、取消、权限、提示注入、Skill、调试、迁移与现行消息。每课在网站和同源书稿中完整保留目标、前置、输入输出、提示词、步骤、验收、错误、权限、来源与版本。MCP 2025-11-25 的 initialize 是历史教学；2026-07-28 对照采用逐请求元数据。Skills 扩展已发布、SEP-2640 Final；具体宿主支持仍待逐版本验证。

`learning/mcp/raw/` 原字节保留研究采集历史；`overlay.json` 是经核验的补充说明。页面默认展示显式适配后的教学正文，而非内部状态。ZIP 下载内含原包与 `VERIFIED-OVERLAY.json`；请同时阅读。只有原创标准库模拟契约经过测试，不是 MCP SDK、真实服务器、OAuth、模型或行业效果验证。没有安装、账号、付费或真实调用。

```sh
python learning/mcp/raw/validate.py
python -m unittest discover -s learning/mcp/raw/tests -v
```

不新增未经核验的版本事件或模型能力断言。保留全部旧案例、节点、日期覆盖层与互链；源网页的权利与适用条件不因本教程而改变。此目录是待独立审阅的候选，不能据此推定线上已发布。
