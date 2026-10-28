# 全球代表厂商目录核验：第一批

核验日：2026-10-28。40条独立研究记录；未合并或修改发布仓库。不是“全球全部完成”。

## 可直接采用的结论

- 原公开数据148节点偏重家族/历史代表；版本、API别名和训练阶段需要另建记录。
- 固定版本不一定带日期：Claude 4.6起的无日期ID由版本文档说明为固定版本。
- 已关闭API仍有历史价值；不能因为当前目录缺失就删历史模型。
- 当前目录与历史报告不能互相替代，研究记录保留未知日期和许可。

## 实际覆盖矩阵

| 厂商 | 实际已读 | 尚未核验 |
|---|---|---|
| OpenAI | catalog；deprecation；image model page；live model page | 全部历史snapshot；gpt-oss许可/权重；embedding/moderation全表；每版发布公告/报告 |
| Anthropic | catalog；versioning；deprecation | 全部旧版逐条入库；每版system card；合作云生命周期逐条核验 |
| Google Gemini | catalog；4 Argon；3.8 Live；Nano Banana 2.1；Omni Flash | 历史Gemini/Imagen/Veo/Lyria完整目录；完整弃用日志；逐版报告 |
| Google Gemma | catalog；Gemma4 model card；Apache2页面；Gemma4 report摘要 | 五尺寸精确checkpoint；旧Gemma/3n/PaliGemma/ShieldGemma全谱系 |
| Meta | Llama4 model card；download entry | 全部Llama1/2/3与Guard/PromptGuard/CodeLlama checkpoint；license正文细则；全套教程 |
| Mistral | catalog；Small4；Voxtral Mini Transcribe3；lifecycle page | 历史模型完整列表；每版权重仓库/报告/许可证；第三方托管去重 |
| Cohere | catalog；deprecation page；Command A report | Aya/Embed/Rerank/North/Parse/Transcribe逐项录入；checkpoint许可证 |
| AI21 | Jamba catalog；platform matrix；docs index | Jurassic历史；Jamba权重许可证；全部报告与旧版状态 |
| Ai2 | Olmo catalog；Olmo3 base card；release notes搜索摘要 | Olmo3.1/Hybrid/Molmo/ASR等逐条核验；所有训练checkpoint/revision；完整release notes正文 |

## 已整理记录

| 厂商 | 名称 / exact ID | 实体类型 | 生命周期 |
|---|---|---|---|
| OpenAI | gpt-6-astra | api_model_id | catalog_listed |
| OpenAI | gpt-6.1-sol | api_model_id | catalog_listed |
| OpenAI | gpt-6.1-terra | api_model_id | catalog_listed |
| OpenAI | gpt-6-luna | api_model_id | catalog_listed |
| OpenAI | gpt-image-2.5-sunburst | api_model_id | catalog_listed |
| OpenAI | gpt-live-1 | api_model_id | catalog_listed |
| OpenAI | sora-2 | api_alias | retired |
| OpenAI | sora-2-2025-10-06 | fixed_snapshot | retired |
| OpenAI | Videos API | api_service | retired |
| OpenAI | gpt-4o-2024-05-13 | fixed_snapshot | retired |
| Anthropic | claude-fable-5-1 | fixed_api_version | active |
| Anthropic | claude-opus-5-5 | fixed_api_version | active |
| Anthropic | claude-sonnet-5-5 | fixed_api_version | active |
| Anthropic | claude-haiku-5-5 | fixed_api_version | active |
| Anthropic | claude-sonnet-4-5-20250929 | fixed_snapshot | deprecated |
| Google | gemini-4-argon | api_model_id | stable |
| Google | gemini-3.8-live | api_model_id | stable |
| Google | gemini-nano-banana-2.1 | api_model_id | stable |
| Google | gemini-omni-1.1-flash | api_model_id | stable |
| Google | gemini-omni-flash-preview | api_model_id | retired |
| Google | Gemma 4 | model_family | open_weights_documented |
| Google | arXiv:2607.02770 | technical_report | published |
| Meta | Llama 4 Scout (17Bx16E) | model_variant | static_release |
| Meta | Llama 4 Maverick (17Bx128E) | model_variant | static_release |
| Mistral | mistral-small-2603 | api_model_id | GA |
| Mistral | voxtral-mini-transcribe-3-0 | api_model_id | public_preview |
| Mistral | Mistral Large 4 | model_family | catalog_listed |
| Cohere | command-a-plus-05-2026 | api_model_id | live |
| Cohere | command-a-03-2025 | api_model_id | live |
| Cohere | command-a-vision-07-2025 | api_model_id | live |
| Cohere | command-r | api_alias | deprecated |
| AI21 | jamba-large | api_alias | catalog_listed |
| AI21 | jamba-large-1.7-2025-07 | fixed_snapshot | catalog_listed |
| AI21 | jamba-mini-2-2026-01 | fixed_snapshot | catalog_listed |
| AI21 | Jamba2 3B | model_variant | catalog_listed |
| AI21 | jamba-mini-1.7-2025-08 | fixed_snapshot | deprecated |
| Ai2 | allenai/Olmo-3-1025-7B | open_weight_checkpoint | open_weights_documented |
| Ai2 | allenai/Olmo-3-7B-Think-DPO | open_weight_checkpoint | open_weights_documented |
| Ai2 | allenai/Olmo-3-7B-Think | open_weight_checkpoint | open_weights_documented |
| Ai2 | allenai/Olmo-3-7B-Instruct | open_weight_checkpoint | open_weights_documented |

## 来源与变更注意

- 总表alias行重列当前ID；版本专页明确4.6起dateless ID固定。按专页标fixed_api_version，不套用旧alias规则。 [claude_catalog](https://platform.claude.com/docs/en/models/overview) [claude_versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)
- 数据类型表写Text和audio输出，迁移段说response modality仅audio；文字需output audio transcription，保留两段语义。 [gemini_live](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live)
- Mini1.7 snapshot列2025-07而API ID为2025-08；不能改写或用于发布日期。 [ai21_catalog](https://docs.ai21.com/docs/jamba-foundation-models)
- 教程DPO段重复7B-Think final名称；模型卡列独立Think-DPO，采用模型卡标识。 [ai2_catalog](https://docs.allenai.org/models/olmo/index.html) [ai2_card](https://huggingface.co/allenai/Olmo-3-1025-7B)
- 现有弃用历史的推荐替代随文档更新，记录核验日建议而不倒填原公告建议。 [openai_deprecations](https://developers.openai.com/api/docs/deprecations)
- Mistral目录也含第三方Z.ai/DeepSeek，托管目录不等于原创厂商。 [mistral_catalog](https://docs.mistral.ai/models)

## 去重与关系建议

- `gpt`、`gemini`、`llama`、`mistral`保留为家族；新版本挂member_of_family，不覆盖历史节点。
- `gemini-1-report`、`gpt-3`属于历史论文/报告；不能重命名为当前API。
- `llama-2`与`mistral-7b-v0-1`独立保留；`org-aya`不能自动等同整个Cohere组织谱系。
- alias_of和recommended_replacement必须附平台、来源、核验日；推荐替代不等于训练派生关系。
- 当前API可用性仅依据文档，未实际调用；open_weight_checkpoint未锁commit，不能称不可变权重。

## 尚未完成

未覆盖名单、逐厂商缺口、空字段、教程状态都写入JSON。下一步应逐厂商枚举历史发布日志和checkpoint，而不是增加几个代表名字后宣称全量。

## 失败/恢复记录

AI21旧 `/docs/jamba-models` 返回404；改读官方llms索引找到 `/docs/jamba-foundation-models`。`.md`入口被工具content-type限制，改HTML成功。无授权拒绝、无模型执行、无账号访问。

## 官方来源清单

- [openai_catalog](https://developers.openai.com/api/docs/models)（已读页面；不代表完整全文逐字审计）
- [openai_deprecations](https://developers.openai.com/api/docs/deprecations)（已读页面；不代表完整全文逐字审计）
- [openai_image](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)（已读页面；不代表完整全文逐字审计）
- [openai_live](https://developers.openai.com/api/docs/models/gpt-live-1)（已读页面；不代表完整全文逐字审计）
- [claude_catalog](https://platform.claude.com/docs/en/models/overview)（已读页面；不代表完整全文逐字审计）
- [claude_versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)（已读页面；不代表完整全文逐字审计）
- [claude_deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（已读页面；不代表完整全文逐字审计）
- [gemini_catalog](https://ai.google.dev/gemini-api/docs/models)（已读页面；不代表完整全文逐字审计）
- [gemini_argon](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)（已读页面；不代表完整全文逐字审计）
- [gemini_live](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live)（已读页面；不代表完整全文逐字审计）
- [gemini_image](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)（已读页面；不代表完整全文逐字审计）
- [gemini_video](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash)（已读页面；不代表完整全文逐字审计）
- [gemma_catalog](https://ai.google.dev/gemma/docs)（已读页面；不代表完整全文逐字审计）
- [gemma_card](https://ai.google.dev/gemma/docs/core/model_card_4)（已读页面；不代表完整全文逐字审计）
- [gemma_license](https://ai.google.dev/gemma/apache_2)（已读页面；不代表完整全文逐字审计）
- [gemma_report](https://arxiv.org/abs/2607.02770)（已读页面；不代表完整全文逐字审计）
- [meta_card](https://raw.githubusercontent.com/meta-llama/llama-models/refs/heads/main/models/llama4/MODEL_CARD.md)（已读页面；不代表完整全文逐字审计）
- [meta_access](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)（仅搜索摘要）
- [mistral_catalog](https://docs.mistral.ai/models)（已读页面；不代表完整全文逐字审计）
- [mistral_small](https://docs.mistral.ai/models/mistral-small-4-0-26-03)（已读页面；不代表完整全文逐字审计）
- [mistral_audio](https://docs.mistral.ai/models/voxtral-mini-transcribe-3-0)（已读页面；不代表完整全文逐字审计）
- [mistral_lifecycle](https://docs.mistral.ai/inference/model-lifecycle)（已读页面；不代表完整全文逐字审计）
- [cohere_catalog](https://docs.cohere.com/docs/models)（已读页面；不代表完整全文逐字审计）
- [cohere_deprecations](https://docs.cohere.com/docs/deprecations)（已读页面；不代表完整全文逐字审计）
- [cohere_report](https://cohere.com/research/papers/command-a-technical-report.pdf)（已读页面；不代表完整全文逐字审计）
- [ai21_catalog](https://docs.ai21.com/docs/jamba-foundation-models)（已读页面；不代表完整全文逐字审计）
- [ai21_platforms](https://docs.ai21.com/docs/model-availability-across-platforms)（已读页面；不代表完整全文逐字审计）
- [ai21_index](https://docs.ai21.com/llms.txt)（已读页面；不代表完整全文逐字审计）
- [ai2_catalog](https://docs.allenai.org/models/olmo/index.html)（已读页面；不代表完整全文逐字审计）
- [ai2_card](https://huggingface.co/allenai/Olmo-3-1025-7B)（已读页面；不代表完整全文逐字审计）
- [ai2_release](https://docs.allenai.org/release_notes/olmo-release-notes/index.html)（仅搜索摘要）

补充生命周期差异：Mistral Public Preview允许静默更新，不能视为固定snapshot；Cohere deprecated不等于shutdown，既有客户可能仍能访问。见[生命周期政策](https://docs.mistral.ai/inference/model-lifecycle)与[Cohere弃用记录](https://docs.cohere.com/docs/deprecations)。

验证：40条唯一ID、JSON可解析、全部非空发布日期均有独立明示证据、原148节点数据SHA-256未变化。

## 独立审计更正：Mistral Small 4 输入模态（2026-10-28）

`mistral-small-2603` 的 `modality.input` 从 `["text"]` 更正为 `["text", "image"]`。首版整理遗漏图像输入，不是本次新增模型能力。官方[发布文](https://mistral.ai/news/mistral-small-4/)在“A new standard for multimodal, reasoning-optimized models”首段及“Key architectural details → Native multimodality”均明确文本和图像输入（本轮网页定位L31、L41）。JSON已补来源和字段证据；其余39条记录经结构深比较完全不变，其他字段也未改。
