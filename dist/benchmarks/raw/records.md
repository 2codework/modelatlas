# ModelAtlas 评测目录扩充候选（metadata only）

核验日期：2026-10-28。新增 22 条版本/分片记录；原11项不变。不是完整全球目录，也不是排行榜。

## 先看重要边界
- MMMU test答案已公开；MathVista test标签仍声明不公开。公开入口与完整可复现不是同一概念。
- GAIA须门控并禁止可爬重发；WorkArena代码公开而运行实例需审批。
- OSWorld原版/Verified、WebLINX 1.0/1.1、LongBench v1/v2独立记录；RULER历史pipeline已deprecated仍保留。
- OCRBench v2明确研究用途、非商业，不能把根仓库MIT当全部数据授权。
- 全部成绩为空，只链接官方结果；没有下载题库、答案、受限包，未执行代码或使用账号/设备。

## 目录
### MMMU
跨学科图文理解；不同split不得混成一个成绩。
- 版本/分片：original; snapshot 2026-10-28；dev / validation / test
- 任务/模态：多学科视觉问答；image, text
- 访问：public。test答案已于2026-02-12公开；仍不在本站镜像。
- 指标/口径：accuracy。固定学科聚合、答案解析、few-shot与图片处理
- 数据许可：Apache-2.0（数据卡声明；原始素材权利另核）；代码许可：Apache-2.0
- [官方来源](https://github.com/MMMU-Benchmark/MMMU) · [论文](https://arxiv.org/abs/2311.16502) · [官方结果入口](https://mmmu-benchmark.github.io/)

### MMMU-Pro
去除可只靠文本回答的问题并加强选项及纯视觉设置，不能与MMMU直接比较。
- 版本/分片：Pro；standard / vision-only；配置须分别标记
- 任务/模态：增强多模态推理；image, text
- 访问：public。公开数据卡；未获取文件。
- 指标/口径：accuracy。明确standard/vision-only配置及选项设置
- 数据许可：Apache-2.0（数据卡声明）；代码许可：Apache-2.0
- [官方来源](https://github.com/MMMU-Benchmark/MMMU) · [论文](https://arxiv.org/abs/2409.02813) · [官方结果入口](https://mmmu-benchmark.github.io/)

### MathVista testmini
小规模开发验证分片，不能当作完整test成绩。
- 版本/分片：original；testmini
- 任务/模态：视觉数学推理；image, text
- 访问：public。可公开获取；只登记入口。
- 指标/口径：accuracy。记录答案抽取器及模型、数值精度、工具与CoT；第三方解析器不保证与官方等价
- 数据许可：unknown；多来源素材不可由仓库许可推定统一授权；代码许可：CC-BY-SA-4.0（仓库标记）
- [官方来源](https://github.com/lupantech/MathVista) · [官方结果入口](https://mathvista.github.io/)

### MathVista test
标准评测分片；官方说明test标签不公开，不能声称可完整本地复现。
- 版本/分片：original；test
- 任务/模态：视觉数学推理；image, text
- 访问：public。问题公开，test答案非公开；仅公开metadata和结果入口。
- 指标/口径：accuracy。答案提取与提交评分流程须固定；不使用testmini替代
- 数据许可：unknown；多来源素材另核；代码许可：CC-BY-SA-4.0（仓库标记）
- [官方来源](https://github.com/lupantech/MathVista) · [官方结果入口](https://mathvista.github.io/)

### DocVQA（单文档）
从文档图像回答问题；不混同文档集合检索或2026新挑战。
- 版本/分片：2020 Challenge Task 1；train / validation / test；分片量未复核
- 任务/模态：单页文档问答；document_image, text
- 访问：public。官方提供RRC下载入口；账户/下载条款未实测，不声称匿名下载。
- 指标/口径：ANLS。大小写不敏感、空格敏感；固定OCR、答案格式及RRC规则
- 数据许可：unknown；代码许可：unknown
- [官方来源](https://www.docvqa.org/datasets/docvqa) · [官方结果入口](https://www.docvqa.org/challenges/2020)

### ChartQA
图表视觉与逻辑推理，需区分人工和机器生成题及是否提供表格。
- 版本/分片：full with annotations；train / val / test；human / augmented
- 任务/模态：图表问答；image, text
- 访问：public。仓库列出初版与含标注完整版入口。
- 指标/口径：官方任务评测；具体容差本轮未逐行核验。固定human/augmented子集、图像/表格输入与答案归一化；评分实现需二次锁定
- 数据许可：unknown；不能据代码GPL推定全部图表素材许可；代码许可：GPL-3.0（仓库标记）
- [官方来源](https://github.com/vis-nlp/ChartQA) · [论文](https://aclanthology.org/2022.findings-acl.177/)

### OCRBench
文字识别、文档问答等五类能力；不要将论文Full Test和OCRBench子集混用。
- 版本/分片：v1；OCRBench；非Full Test
- 任务/模态：OCR综合评测；image, text
- 访问：public。公开下载链接；不下载题库。
- 指标/口径：官方OCRBench分数；细项匹配规则待锁定。采用官方scripts；第三方VLMEvalKit/lmms-eval须标revision和评分差异
- 数据许可：unknown；底层多来源数据权利另核；代码许可：MIT（根仓库标记）
- [官方来源](https://github.com/Yuliang-Liu/MultimodalOCR/tree/main/OCRBench) · [官方结果入口](https://github.com/Yuliang-Liu/MultimodalOCR/tree/main/OCRBench)

### OCRBench v2
中英双语文字密集视觉任务，扩展定位、版面及复杂推理。
- 版本/分片：v2；EN_part / CN_part
- 任务/模态：文字定位与推理；image, text
- 访问：public。公开下载入口不等于可商用。
- 指标/口径：0–100总分；分任务指标由官方eval_scripts聚合。eval.py逐样本评分后get_score.py聚合；固定中英文子集
- 数据许可：研究用途、非商业；子目录Copyright Statement，非标准SPDX；代码许可：MIT（根仓库标记）
- [官方来源](https://github.com/Yuliang-Liu/MultimodalOCR/tree/main/OCRBench_v2) · [论文](https://arxiv.org/abs/2501.00321) · [官方结果入口](https://github.com/Yuliang-Liu/MultimodalOCR/tree/main/OCRBench_v2#leaderboard)

### LongBench
中英问答、摘要、少样本、合成与补全任务的集合；各任务评分不同。
- 版本/分片：v1；21 task test splits；不混LongBench-E
- 任务/模态：长上下文理解；text, code
- 访问：public。公开数据集入口。
- 指标/口径：按任务自动评分，分类均值；非统一accuracy。固定任务清单、模板、输出上限与中间截断策略
- 数据许可：unknown；混合任务数据来源需分别核权；代码许可：MIT（根仓库标记）
- [官方来源](https://github.com/THUDM/LongBench/blob/main/LongBench/README.md) · [论文](https://aclanthology.org/2024.acl-long.172) · [官方结果入口](https://github.com/THUDM/LongBench/blob/main/LongBench/README.md)

### LongBench v2
更长上下文的多项选择任务；直接回答、CoT、RAG不可混算。
- 版本/分片：v2；HF train（用于评测，不代表训练授权）
- 任务/模态：长上下文推理；text, code
- 访问：public。官方README旧THUDM数据链接重定向zai-org。
- 指标/口径：multiple-choice accuracy。固定cot/no_context/rag开关、上下文长度及结果导出器
- 数据许可：unknown；本轮未核验数据卡许可正文；代码许可：MIT（仓库标记）
- [官方来源](https://github.com/THUDM/LongBench) · [论文](https://arxiv.org/abs/2412.15204) · [官方结果入口](https://longbench2.github.io/)

### RULER（历史pipeline）
用多类合成任务观察长度退化；官方已将原pipeline标为deprecated，历史保留。
- 版本/分片：v1 legacy main pipeline；synthetic；按任务与上下文长度生成
- 任务/模态：有效长上下文测量；text
- 访问：public。旧pipeline deprecated；官方另指rulerv1-ns/rulerv2-ns，新版需另行核验。
- 指标/口径：按任务/长度得分与平均分；有效长度依阈值。固定生成seed、tokenizer、长度、任务复杂度、one-shot设置；勿把配置窗口当实测能力
- 数据许可：unknown；外部语料条款另核；代码许可：unknown
- [官方来源](https://github.com/NVIDIA/RULER) · [官方结果入口](https://github.com/NVIDIA/RULER)

### MBPP
入门编程任务；手工校验sanitized版本不是同一测试集合。
- 版本/分片：original + sanitized variant described；test IDs 11–510；prompt 1–10；val 511–600；train 601–974
- 任务/模态：基础Python程序合成；text, code
- 访问：public。公开仓库；不复制题目或参考代码。
- 指标/口径：测试用例通过情况；pass@k实现本轮未审计。原论文three-shot使用IDs 2/3/4；固定原始或sanitized、采样与隔离测试环境
- 数据许可：unknown；代码许可：unknown
- [官方来源](https://github.com/google-research/google-research/tree/master/mbpp)

### OSWorld（原版）
真实桌面环境中的开放式任务，执行式验收；历史版本不能混入Verified榜单。
- 版本/分片：2024 original；原始论文任务；锁定旧revision
- 任务/模态：桌面GUI多步任务；screenshot, text, accessibility_tree
- 访问：public。公开环境与任务定义；运行需要隔离VM及资源，本轮未运行。
- 指标/口径：execution-based task success。固定VM镜像、初始状态、动作空间、步数、观察方式、重试与评测器
- 数据许可：unknown；应用及素材条款独立；代码许可：Apache-2.0
- [官方来源](https://github.com/xlang-ai/OSWorld) · [论文](https://arxiv.org/abs/2404.07972) · [官方结果入口](https://os-world.github.io/)

### OSWorld-Verified
修订任务及验收器的版本；应与同版本结果比较，而非原版横向排名。
- 版本/分片：2025-07-28 Verified update；Verified任务与修订评测器
- 任务/模态：桌面GUI多步任务；screenshot, text, accessibility_tree
- 访问：public。代码环境公开；不授权访问用户真实机器或账户。
- 指标/口径：execution-based task success。锁定Verified revision、镜像、动作预算与判分实现；记录失败原因和重复实验
- 数据许可：unknown；应用素材独立；代码许可：Apache-2.0（对应官方仓库）
- [官方来源](https://xlang.ai/blog/osworld-verified) · [论文](https://arxiv.org/abs/2404.07972) · [官方结果入口](https://os-world.github.io/)

### AndroidWorld
模拟器中参数化任务；116是任务模板数，不是唯一可运行实例数。
- 版本/分片：original; current README snapshot；参数化tasks；seed实例
- 任务/模态：Android代理操作；screenshot, text, accessibility_tree
- 访问：public。需Android模拟器；不使用真实设备或账户。
- 指标/口径：task success / reward。固定随机参数seed、20 apps版本、模拟器API与动作预算
- 数据许可：unknown；app许可另核；代码许可：Apache-2.0
- [官方来源](https://github.com/google-research/android_world) · [论文](https://arxiv.org/abs/2405.14573) · [官方结果入口](https://google-research.github.io/android_world/)

### WebArena
可自托管的真实风格网站任务；评测终态，不只比较文本答案。
- 版本/分片：v0.2.0 annotation baseline；canonical tasks；环境快照固定
- 任务/模态：网页代理操作；text, DOM, screenshot
- 访问：public。推荐AgentLab/BrowserGym不等于改变原始benchmark版本。
- 指标/口径：execution-based success。记录网站/容器版本、URL映射、状态reset、观察/动作空间、步数与harness
- 数据许可：unknown；站点内容与镜像条款另核；代码许可：Apache-2.0
- [官方来源](https://github.com/web-arena-x/webarena) · [论文](https://arxiv.org/abs/2307.13854) · [官方结果入口](https://webarena.dev/)

### VisualWebArena
引入视觉信息依赖的网页操作，沿用执行式验收思路；独立于WebArena计分。
- 版本/分片：2024 original；full tasks
- 任务/模态：视觉网页代理；image, text, DOM, screenshot
- 访问：public。公开任务和自托管环境入口。
- 指标/口径：execution-based success。固定截图、caption/SoM等额外工具、网页状态、评测器与步数
- 数据许可：unknown；第三方图像及站点内容另核；代码许可：MIT
- [官方来源](https://github.com/web-arena-x/visualwebarena) · [论文](https://arxiv.org/abs/2401.13649) · [官方结果入口](https://jykoh.com/vwa)

### WorkArena L1
ServiceNow日常工作原子任务；源码公开不表示托管实例可自由使用。
- 版本/分片：L1 atomic；33 task types；实例采样
- 任务/模态：知识工作网页任务；text, DOM, screenshot
- 访问：gated。运行实例须HF申请、接受条款并等待批准；源码公开。
- 指标/口径：task success（BrowserGym reward）。固定实例版本、seed、任务清单与AgentLab/BrowserGym revision
- 数据许可：unknown；实例使用条款需批准；代码许可：unknown；仓库自定义License待全文审阅
- [官方来源](https://github.com/ServiceNow/WorkArena) · [论文](https://arxiv.org/abs/2403.07718) · [官方结果入口](https://servicenow.github.io/WorkArena/)

### WorkArena++
将原子任务组合成更长工作流程，不能与L1原子成功率直接比较。
- 版本/分片：compositional 2024；组合任务；固定level与curriculum
- 任务/模态：规划推理知识工作；text, DOM, screenshot
- 访问：gated。同WorkArena运行实例审批，不提交申请或登录。
- 指标/口径：task success（BrowserGym reward）。记录level、curriculum、seed、预算及ServiceNow实例版本
- 数据许可：unknown；实例使用条款需批准；代码许可：unknown；自定义License待全文审阅
- [官方来源](https://github.com/ServiceNow/WorkArena) · [论文](https://arxiv.org/abs/2407.05291) · [官方结果入口](https://servicenow.github.io/WorkArena/)

### WebLINX 1.0
基于记录的操作演示评测下一步，不等同在线端到端成功率。
- 版本/分片：1.0 initial release；原版划分；需固定split
- 任务/模态：对话式网页导航（离线）；text, DOM, screenshot
- 访问：public。公开数据入口；初版仍保留用于历史比较。
- 指标/口径：离线动作评测；具体指标实现待锁定。固定动作类型、元素定位、分片和原版评测器；不混1.1
- 数据许可：unknown；演示和网页素材许可另核；代码许可：Apache-2.0
- [官方来源](https://github.com/McGill-NLP/weblinx) · [论文](https://arxiv.org/abs/2402.05930) · [官方结果入口](https://mcgill-nlp.github.io/weblinx/)

### WebLINX 1.1 / BrowserGym
由1.0派生，移除少量演示并改变评测steps；官方要求以1.1/BG单独报分。
- 版本/分片：1.1；BrowserGym评测steps；新增tab动作
- 任务/模态：对话式网页导航（离线）；text, DOM, screenshot
- 访问：public。公开派生数据入口；未新增演示并不意味着评测等价。
- 指标/口径：离线动作评测；不能标作在线任务完成率。固定weblinx-browsergym revision、动作集合、分片；与1.0严格分列
- 数据许可：unknown；数据卡许可尚未单独核验；代码许可：Apache-2.0
- [官方来源](https://github.com/McGill-NLP/weblinx) · [论文](https://arxiv.org/abs/2402.05930) · [官方结果入口](https://mcgill-nlp.github.io/weblinx/)

### GAIA
任务要求不同程度的工具与自主性；test答案和metadata非公开。
- 版本/分片：2023 benchmark; 2025-10 parquet format；validation / test；level 1/2/3
- 任务/模态：通用助理工具任务；text, image, audio, document
- 访问：gated。需同意HF信息分享；禁止在可爬页面重发validation/test；本轮未接受条款。
- 指标/口径：答案正确性；标准化细节待榜单规则锁定。声明搜索、浏览、代码和文件工具，预算、运行日期及level；动态网络会影响复现
- 数据许可：unknown；gating/不重发条件已明确；代码许可：unknown
- [官方来源](https://huggingface.co/datasets/gaia-benchmark/GAIA) · [论文](https://arxiv.org/abs/2311.12983) · [官方结果入口](https://huggingface.co/spaces/gaia-benchmark/leaderboard)

## 集成建议（父任务QA后再做）
1. 沿用node_id唯一引用；新增bench-*节点和bench-src-*来源，不覆盖原11项。此文件未写生产registry。
2. 当前registry availability为public_download；本研究public建议映射为public_download，但同时保留访问细分，避免把MathVista test隐藏标签或DocVQA未实测登录说成完全开放。
3. 现有registry支持的metric/protocol/contamination/reproducibility/source_ids/results_preview可直接映射；新增family/version/modality/relations/license_evidence/dataset_sizes应扩schema或挂metadata扩展，不静默丢字段。
4. repo/data/leaderboard可能共享官方入口：页面会链接下游资源；null表示未核验，不生成猜测链接。
5. scoring.implementation_verified=false、harness.revision=null是刻意保留的证据缺口：本轮只介绍，不声称复跑或实现完全审计。
6. 数据大小附split/date/source；空数组是未知，不以网页下载数或近似范围代替样本量。
7. 搜索引擎可能渲染公开数据卡预览，本地交付未保存任何样题/答案或受限文件。

## 共同比较条件
模型精确版本、训练截止、数据和harness revision、prompt/shot/CoT、工具、预算、seed、采样、输出/上下文截断、环境初态和日期都需可追溯。GUI任务另外锁定VM/app/网站状态及动作空间；公开题、素材与轨迹存在污染风险，私有标签并不保证无污染。
