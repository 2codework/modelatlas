# 实时语音模型 · 四个有限样本



只读来源研究 / never-run。模型、API、客户端分开；不是全球完整目录。

四家四模型/家族有限样本；不是全球完整版本史。原knowledge_graph_links_application.after为r1接纳阶段统计，不是当前全图。

当前全图统计：{
  "nodes": 246,
  "edges": 151,
  "isolated": 76,
  "weak_components": 112,
  "graph_scope": "D.nodes / D.edges only; undirected degree and weak components",
  "excluded_links": [
    "practice registry / learning_paths",
    "AgentWork cross-site links / agentwork_links",
    "source URLs / Markdown links / site navigation"
  ],
  "interpretation_zh": "内部图孤立不等于网页没有链接；边数不证明准确性提升或厂商集成。"
}



## Moshi / Moshiko BF16

开放权重语音对话家族；并行语音流支持对话双工，家族日期不代表精确checkpoint上传。

类型：model_family；版本：Moshi family; reviewed variant kyutai/moshiko-pytorch-bf16

### 精确版本（家族与checkpoint分开）

未知（未证实，不补日期）

### 已核变体

[
  {
    "exact_id": "kyutai/moshiko-pytorch-bf16",
    "parent_family": "Moshi",
    "revision_sha": null,
    "first_weights_upload_date": null,
    "source_ids": [
      "moshi-card"
    ]
  }
]

### 日期作用域

dates为Moshi家族公告/论文事件，不是所列Moshiko BF16 checkpoint首次上传或独立发布日。

### 输入模态

[
  "audio"
]

### 输出模态

[
  "audio",
  "aligned_text"
]

### 流式与双向的条件

{
  "input": true,
  "output": true,
  "full_duplex": true,
  "condition_zh": "模型并行建模用户和自身语音流；不是ASR→LLM→TTS串联。"
}

### 许可分层

{
  "weights": "CC-BY-4.0",
  "python": "MIT",
  "rust": "Apache-2.0"
}

### 运行与硬件

官方PyTorch路径要求较大显存，README给24GB；Python>=3.10建议3.12。未执行，不保证所有GPU实时。

### 账号与费用

公开模型卡；未测试权重下载或账号要求。自托管需自备算力；演示站不是托管API SLA。

### 延迟口径

官方自报理论160ms、L4约200ms；非本轮独立测速。

### 权重首次上传日期

未知（未证实，不补日期）

### 固定修订SHA

未知（未证实，不补日期）

### 不能混同的服务与客户端

[
  "Mimi音频编解码器",
  "moshi.chat演示客户端",
  "推理服务器"
]

### 日期证据（不以核验日期冒充发布）

- 2024-07-03 · Moshi / Moshiko BF16 · 介绍公告 · announcement · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2024-09-17 · Moshi / Moshiko BF16 · 论文首次提交 · paper_submission · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2024-09-18 · Moshi / Moshiko BF16 · 家族开放发布公告（非checkpoint首次上传） · announcement · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2024-10-02 · Moshi / Moshiko BF16 · 论文v2修订 · paper_revision · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

### 学习路径（未执行）

1. 先核模型/协议/产品边界与精确版本。

2. 阅读官方模型卡、论文与运行要求；保留未知与访问条件。

3. 仅设计经同意的合成音频测试；未获授权不下载、登录、收费或调用设备。

4. 如将来获批测试，分别记录目标delay、端到端P50/P95、硬件、并发、网络、版本和失败；不能拿官方自报代替实测。

### 官方学习入口

- https://github.com/kyutai-labs/moshi · opened

- https://huggingface.co/kyutai/moshiko-pytorch-bf16 · opened

- https://arxiv.org/abs/2410.00037 · opened

- https://kyutai.org/blog/2024-07-03-meet-moshi/ · opened_partial

- https://kyutai.org/blog/2024-09-18-moshi-release/ · opened_partial

- https://kyutai.org/blog/ · opened

## CSM 1B

精确1B上下文语音生成模型；不是Sesame完整对话产品，开放权重仍有访问条件。

类型：model；版本：sesame/csm-1b

### 精确版本（家族与checkpoint分开）

sesame/csm-1b

### 输入模态

[
  "text",
  "audio_context"
]

### 输出模态

[
  "audio"
]

### 流式与双向的条件

{
  "input": null,
  "output": null,
  "full_duplex": null,
  "condition_zh": "已核资料证明上下文语音生成，未证明开放1B checkpoint提供实时双工会话。"
}

### 许可分层

{
  "weights": "Apache-2.0",
  "code": "Apache-2.0",
  "dependencies": "Llama-3.2-1B访问及其独立条款需另核"
}

### 运行与硬件

官方CUDA兼容GPU；测试CUDA12.4/12.6，建议Python3.10，部分音频操作需要ffmpeg；显存最低值未知。

### 账号与费用

HF卡明确门控：登录并同意分享账户信息；官方代码另要求Llama-3.2-1B访问。没有登录或下载。自托管算力收费自理。

### 延迟口径

未登记实时延迟，也不以demo表现替代开放权重性能。

### 权重首次上传日期

未知（未证实，不补日期）

### 固定修订SHA

未知（未证实，不补日期）

### 独立论文日期

未知（未证实，不补日期）

### 不能混同的服务与客户端

[
  "Sesame交互语音产品使用微调变体",
  "HF Space演示",
  "Mimi codec"
]

### 日期证据（不以核验日期冒充发布）

- 2025-02-27 · CSM 1B · 技术文章公开 · report_publication · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2025-03-13 · CSM 1B · 权重发布公告（非首次上传时间核验） · weights_release · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2025-05-20 · CSM 1B · Transformers原生支持公告 · documentation_update · Transformers 4.52.1，不是模型首发

### 学习路径（未执行）

1. 先核模型/协议/产品边界与精确版本。

2. 阅读官方模型卡、论文与运行要求；保留未知与访问条件。

3. 仅设计经同意的合成音频测试；未获授权不下载、登录、收费或调用设备。

4. 如将来获批测试，分别记录目标delay、端到端P50/P95、硬件、并发、网络、版本和失败；不能拿官方自报代替实测。

### 官方学习入口

- https://huggingface.co/sesame/csm-1b · opened

- https://github.com/SesameAILabs/csm · opened

- https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice · opened

## Voxtral Mini 4B Realtime 2602

精确2602实时语音识别模型：音频流输入、文本转写输出；不是语音回答生成器。

类型：model；版本：mistralai/Voxtral-Mini-4B-Realtime-2602

### 精确版本（家族与checkpoint分开）

mistralai/Voxtral-Mini-4B-Realtime-2602

### 输入模态

[
  "audio"
]

### 输出模态

[
  "text"
]

### 流式与双向的条件

{
  "input": true,
  "output": true,
  "condition_zh": "论文A.2的full-duplex是流式音频输入/转写文本输出传输，不是会说话的双工对话模型；2602托管旧接口不兼容diarize。",
  "transport_bidirectional_streaming": true,
  "conversational_speech_to_speech": false,
  "source_ids": [
    "vox-paper-html",
    "vox-api-guide"
  ]
}

### 许可分层

{
  "weights": "Apache-2.0"
}

### 运行与硬件

官方模型卡Serve章节：BF16/vLLM可在单GPU>=16GB显存运行；这是官方部署配置条件，非独立实测或绝对最低显存。另支持Transformers>=5.2.0；部署版本、吞吐、批量和会话长度会影响资源，均未实测。

### 官方配置（非实测最低）

{
  "precision": "BF16",
  "runtime": "vLLM",
  "gpu_count": 1,
  "gpu_memory_gb_at_least": 16,
  "source_ids": [
    "vox-card"
  ],
  "section": "Usage / vLLM / Serve",
  "verified_by_execution": false
}

### 账号与费用

开放权重自托管与付费API分开。API旧2602需key，模型页0.006 USD/min（核查日）；账号/地区/额度实际未验证。

### 延迟口径

分别记录目标转写延迟、卡片推荐值及营销摘要；不把算法/目标delay当端到端时延。240ms摘要与80ms配置下限不能单凭数字不同判为同作用域矛盾；精确摘要口径关系未建立。

### 目标配置与端到端证据

[
  {
    "scope": "model_card_summary",
    "value": "240ms–2.4s",
    "source_ids": [
      "vox-card"
    ]
  },
  {
    "scope": "model_card_features",
    "value": "80ms–2.4s",
    "source_ids": [
      "vox-card"
    ]
  },
  {
    "scope": "model_card_recommended_configuration",
    "value": "480ms recommended; transcription_delay_ms: multiples of 80ms from 80 through 1200 plus 2400",
    "source_ids": [
      "vox-card"
    ]
  },
  {
    "scope": "paper_v3_section_3_2_training_target_delay",
    "value": "80–2400ms in 80ms steps; delay conditioning",
    "source_ids": [
      "vox-paper-html"
    ]
  },
  {
    "scope": "announcement_marketing",
    "value": "sub-200ms configurable",
    "source_ids": [
      "vox-release"
    ]
  },
  {
    "scope": "end_to_end_observed_latency",
    "value": null,
    "note_zh": "没有测试；论文区分理论delay与batch/concurrency/network开销。80ms帧步长和lookahead/目标delay不等于保证每个用户80ms见字。",
    "source_ids": [
      "vox-paper-html"
    ]
  }
]

### 权重首次上传日期

未知（未证实，不补日期）

### 固定修订SHA

未知（未证实，不补日期）

### 不能混同的服务与客户端

[
  "API id voxtral-mini-transcribe-realtime-2602",
  "Voxtral Mini Transcribe V2 batch",
  "Voxtral Mini Transcribe 3",
  "Mistral Studio playground"
]

### 日期证据（不以核验日期冒充发布）

- 2026-02-04 · Voxtral Mini 4B Realtime 2602 · 介绍公告 · announcement · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2026-02-04 · Voxtral Mini 4B Realtime 2602 · 权重发布公告（非首次上传时间核验） · weights_release · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2026-02-11 · Voxtral Mini 4B Realtime 2602 · 论文首次提交 · paper_submission · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2026-02-21 · Voxtral Mini 4B Realtime 2602 · 论文v2修订 · paper_revision · arXiv submission history；不是新权重发布

- 2026-04-06 · Voxtral Mini 4B Realtime 2602 · 论文v3修订 · paper_revision · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

### 学习路径（未执行）

1. 先核模型/协议/产品边界与精确版本。

2. 阅读官方模型卡、论文与运行要求；保留未知与访问条件。

3. 仅设计经同意的合成音频测试；未获授权不下载、登录、收费或调用设备。

4. 如将来获批测试，分别记录目标delay、端到端P50/P95、硬件、并发、网络、版本和失败；不能拿官方自报代替实测。

### 官方学习入口

- https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602 · opened

- https://mistral.ai/news/voxtral-transcribe-2/ · opened

- https://arxiv.org/abs/2602.11298 · opened

- https://docs.mistral.ai/models/voxtral-mini-transcribe-realtime-26-02 · opened

- https://docs.mistral.ai/studio/audio/deprecated/speech_to_text/realtime_transcription · opened

- https://arxiv.org/html/2602.11298v3 · opened

## GPT-Realtime family (2025-08-28 / 2.1)

托管语音模型家族的有限版本对照；旧快照与2.1的生命周期、价格分开，非完整版本史。

类型：model_family；版本：gpt-realtime-2025-08-28 / gpt-realtime-2.1 (分别见版本表)

### 精确版本（家族与checkpoint分开）

[
  "gpt-realtime-2025-08-28",
  "gpt-realtime-2.1"
]

### 输入模态

[
  "audio",
  "text",
  "image"
]

### 输出模态

[
  "audio",
  "text"
]

### 流式与双向的条件

{
  "input": true,
  "output": true,
  "full_duplex": null,
  "condition_zh": "Realtime协议可双向音频及打断；通用Streaming字段原值Not supported另存，不视为同接口冲突。不能据此宣称GPT-Live独立后端式full-duplex。"
}

### 许可分层

{
  "weights": "not publicly released in reviewed sources",
  "service": "proprietary API terms; no open-weight license"
}

### 运行与硬件

模型运行在托管服务；客户端WebRTC/WebSocket，SIP另有指南。无本地GPU需求证据。

### 账号与费用

版本特定价格和生命周期见version_records，不向family继承；账号、地区、额度与收费未实际验证。

### 延迟口径

未量化测速；2.1官方注明更高reasoning effort可增加时延和输出token。

### 精确版本、价格与生命周期表

[
  {
    "exact_id": "gpt-realtime-2025-08-28",
    "related_alias": "gpt-realtime",
    "announcement_date": "2025-08-28",
    "deprecation_announced": "2026-07-20",
    "scheduled_shutdown": "2027-01-20",
    "lifecycle_as_of": "2026-10-28",
    "status": "deprecated_not_yet_scheduled_shutdown",
    "inputs": [
      "text",
      "audio",
      "image"
    ],
    "outputs": [
      "text",
      "audio"
    ],
    "pricing_per_million_tokens_usd": {
      "text_input": 4,
      "text_output": 16,
      "audio_input": 32,
      "audio_output": 64
    },
    "source_ids": [
      "gpt-old-card",
      "gpt-release",
      "gpt-deprecations"
    ]
  },
  {
    "exact_id": "gpt-realtime-2.1",
    "immutable_dated_snapshot": null,
    "release_date": null,
    "status": "current_guide_example_not_marked_deprecated_in_reviewed_sources",
    "lifecycle_as_of": "2026-10-28",
    "inputs": [
      "text",
      "audio",
      "image"
    ],
    "outputs": [
      "text",
      "audio"
    ],
    "pricing_per_million_tokens_usd": {
      "text_input": 4,
      "text_output": 24,
      "audio_input": 32,
      "audio_output": 64
    },
    "free_tier": "not supported",
    "source_ids": [
      "gpt-current-card",
      "gpt-guide"
    ]
  }
]

### 2.1首发日期

未知（未证实，不补日期）

### 固定修订SHA

未知（未证实，不补日期）

### 独立论文日期

未知（未证实，不补日期）

### 不能混同的服务与客户端

[
  "Realtime API传输/会话服务",
  "ChatGPT语音客户端",
  "GPT-Live不同架构"
]

### 日期证据（不以核验日期冒充发布）

- 2025-08-28 · GPT-Realtime family (2025-08-28 / 2.1) · 旧版模型发布公告 · announcement · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2025-08-28 · GPT-Realtime family (2025-08-28 / 2.1) · Realtime API GA（服务事件） · api_launch · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2026-07-20 · GPT-Realtime family (2025-08-28 / 2.1) · 旧版快照弃用公告（尚未到停用日） · documentation_update · 事件日期由官方来源证明，不用核查日替代；权重首传日期仍未知。

- 2027-01-20 · GPT-Realtime family (2025-08-28 / 2.1) · 【计划·尚未发生】旧快照计划停止服务 · scheduled_shutdown · 未来计划，非已停用

### 学习路径（未执行）

1. 先核模型/协议/产品边界与精确版本。

2. 阅读官方模型卡、论文与运行要求；保留未知与访问条件。

3. 仅设计经同意的合成音频测试；未获授权不下载、登录、收费或调用设备。

4. 如将来获批测试，分别记录目标delay、端到端P50/P95、硬件、并发、网络、版本和失败；不能拿官方自报代替实测。

### 官方学习入口

- https://openai.com/index/introducing-gpt-realtime/ · opened

- https://developers.openai.com/api/docs/models/gpt-realtime · opened

- https://developers.openai.com/api/docs/deprecations · opened

- https://developers.openai.com/api/docs/models/gpt-realtime-2.1 · opened

- https://developers.openai.com/api/docs/guides/realtime · opened

## 覆盖缺口

[
  {
    "entity": "GPT-Realtime-2",
    "reason_zh": "2.1模型卡提及其前代；本轮未研究该前代精确发布、快照、许可/生命周期，不将两条版本说成完整家族史。",
    "source_ids": [
      "gpt-current-card"
    ]
  },
  {
    "entity": "Moshi backend/quantization variants",
    "reason_zh": "未穷尽Moshika/Moshiko所有后端、量化及checkpoint历史。",
    "source_ids": [
      "moshi-repo"
    ]
  }
]
