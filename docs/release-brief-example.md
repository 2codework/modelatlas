# 发布阅读课：把 Qwen3-8B 公告写成有条件的简报

Qwen 团队在 2025-04-29 的公告中将 Qwen/Qwen3-8B 列入开放权重的稠密模型（A）。不要把公告表中的 128K 直接写成原生上限；准确模型卡区分原生与 YaRN 扩展（B）。2025-05-14 是家族报告 v1 提交日（C），不是本课证明的首次上传日。权重列表与许可文件可见（D/E），但这不能证明特定地区服务可用或部署就绪。

## 已填写账本

- **对象**: Qwen/Qwen3-8B；提供方 Qwen / Alibaba；不是整个家族、Base 变体或 API 别名。 [A/B]
- **日期**: 2025-04-29：有日期的官方公告；2025-05-14：报告 v1；2026-11-01：本课核验。首次上传仍未知。 [A/C]
- **特点与条件**: 稠密文本生成模型，不因家族含 MoE 就变成 MoE。原生 32,768 / YaRN 131,072；扩展条件不能省略。 [A/B]
- **权重与许可**: 开放权重列表 + Apache 2.0 文件。main 可变，未固定权重修订、未下载、未审计；开放权重不自动等于开源。 [D/E]
- **未知与边界**: 首次上传、模型卡原始发表/更新日期、API 上线、地区与账号条件、延迟、硬件需求、任务质量均未独立确立。无最新、全球完整或基准冠军结论。 [本课范围]

编辑核验日期：2026-11-01

证据模式：本课提供的编辑释义。学习者独立核验日期：未独立核验；不要把编辑日期当作自己打开原始来源的日期。

## 来源定位（编辑释义，非原文摘录）

- A: [Introduction / dense-model table](https://qwenlm.github.io/blog/qwen3/)
- B: [Model Overview / Processing Long Texts](https://huggingface.co/Qwen/Qwen3-8B)
- C: [Abstract / Submission history [v1]](https://arxiv.org/abs/2505.09388v1)
- D: [Files / safetensors shards and index](https://huggingface.co/Qwen/Qwen3-8B/tree/main)
- E: [LICENSE / heading](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE)

结论：可以进入任务评估规划，不能直接批准部署。先确定任务、授权、运行条件和验收标准；本课没有运行模型、API、MCP 或宿主工具。
