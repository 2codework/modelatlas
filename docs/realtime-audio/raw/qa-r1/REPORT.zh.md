# 实时音频模型独立 QA r1

**结论：需修正后合入；不是全球覆盖完成。** 原研究6项SHA全部通过，原始研究与canonical只读。17/20来源独立重开；2个原部分解析及1个失败状态原样保留，未重试失败页面。

## 关键修正
- Voxtral论文v2遗漏：2026-02-21。
- BF16/vLLM >=16GB只是官方指定部署条件，绝对最低硬件仍未知。
- 延迟数值按卡摘要、功能段、评测delay、公告分别保存；未建立同口径关系，不直接认定矛盾。
- GPT旧版与2.1的生命周期/价格应绑定版本；当前2.1不能标弃用，且家族史并不完整。

## speech-moshi — accept_with_scope_guard
### accept
- 模型语音输入、音频/对齐文本输出、并行双语音流及full_duplex有论文/官方仓库支持。
- 2024-07-03介绍、2024-09-17论文v1、2024-09-18开放发布公告、2024-10-02论文v2分开准确。
- 权重CC-BY-4.0、Python MIT、Rust Apache许可区分正确。
### fix
- 家族实体与精确Moshiko BF16 checkpoint保持父子/variant关系；不得把家族公告日宣称该checkpoint首次上传日。
### unknown
- 权重首次上传日期、revision SHA、全部Moshika/Moshiko量化/后端变体发布史未穷尽。
来源：[moshi-repo](https://github.com/kyutai-labs/moshi)、[moshi-card](https://huggingface.co/kyutai/moshiko-pytorch-bf16)、[moshi-paper](https://arxiv.org/abs/2410.00037)、[kyutai-index](https://kyutai.org/blog/)

## speech-csm-1b — accept
### accept
- sesame/csm-1b为上下文语音生成模型，文本/音频上下文输入和音频输出正确；不等于完整Sesame交互产品。
- 2025-02-27技术博客、03-13权重发布公告、05-20 Transformers 4.52.1支持公告分别准确。
- Apache-2.0与HF门控账户同意并存；Llama依赖访问另计。
### fix
### unknown
- 实时输入/输出及双工未证实，保持null。
- 独立论文日期、实际首次权重上传、绝对最低硬件、用户实际权限未验证。
来源：[csm-repo](https://github.com/SesameAILabs/csm)、[csm-card](https://huggingface.co/sesame/csm-1b)、[csm-post](https://www.sesame.com/journal/crossing-the-uncanny-valley-of-voice)

## speech-voxtral-realtime-2602 — fix
### accept
- 精确开放权重ID及API id区分正确；流式音频转写为文本，不是生成回答语音的双工对话。
- 2026-02-04发布/权重公告、02-11论文v1、04-06论文v3准确；Apache-2.0不等于免key/免费托管API。
- vLLM推荐与Transformers>=5.2.0段落并存，旧only-vLLM句不能覆盖后段显式版本支持；ExecuTorch/社区支持标Untested。
- 旧2602 API不支持diarize仅适用于旧版指南，不能外推Transcribe3。
### fix
- F01 补论文v2=2026-02-21（00:06:15 UTC），不得声称论文历史版本齐全而漏中间版本。
- F02 runtime补官方BF16/vLLM单GPU>=16GB部署条件；绝对最低显存仍unknown，不是独立测速。
- F03 延迟应登记段落口径：卡摘要240ms–2.4s、Features80ms–2.4s、评测delay包含160ms、公告sub-200ms。未建立算法/配置/端到端口径对应，不断言数值矛盾或最低时延保证。
### unknown
- 首次权重上传、revision SHA、独立最低显存、端到端延迟、当前用户API访问条件未验证。
来源：[vox-card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)、[vox-release](https://mistral.ai/news/voxtral-transcribe-2/)、[vox-paper](https://arxiv.org/abs/2602.11298)、[vox-api-model](https://docs.mistral.ai/models/voxtral-mini-transcribe-realtime-26-02)、[vox-api-guide](https://docs.mistral.ai/studio/audio/deprecated/speech_to_text/realtime_transcription)

## speech-gpt-realtime-family — fix_for_integration
### accept
- 旧gpt-realtime及gpt-realtime-2025-08-28于2026-07-20宣布弃用，2027-01-20为未来计划停用，不是已停用。
- 2.1当前卡/指南有效，不能随旧别名标Deprecated；文本/音频双向、图片只输入正确。
- generic Streaming=Not supported与Realtime WebRTC/WebSocket属于不同接口/字段范围，不自动构成冲突；双向传输/打断不证明独立后端式full-duplex。
- 2025-08-28模型发布与Realtime API GA分开准确；托管模型无公开权重许可，API凭据/费用另计。
### fix
- F04 合入需将旧别名/2025快照与2.1结构化为独立版本对象，日期、生命周期、价格均绑精确版本。旧版文本输出$16/百万token，2.1为$24；原2.1标注本身正确，禁止family字段继承误用。
- F05 不应以两条版本代表完整GPT-Realtime家族史：当前2.1卡明确为GPT-Realtime-2更新，应把该前代列coverage gap，不能发明其发布日期。
### unknown
- 2.1发布日、全部历史版本、独立论文、任何权重公开日期、账号实际权限/延迟未核定。
来源：[gpt-release](https://openai.com/index/introducing-gpt-realtime/)、[gpt-old-card](https://developers.openai.com/api/docs/models/gpt-realtime)、[gpt-deprecations](https://developers.openai.com/api/docs/deprecations)、[gpt-current-card](https://developers.openai.com/api/docs/models/gpt-realtime-2.1)、[gpt-guide](https://developers.openai.com/api/docs/guides/realtime)

## 去重与证据边界
canonical：242 nodes、77 vendor records；SHA256 `08b1dc2ab60f1eda3e64a65aee0034487506af8108cf44bfeec98aa8b97ef578`。
已有Voxtral Mini Transcribe 3不是Realtime2602，保持不同实体。原动态HF/GitHub资料没有revision锁定；本包source记录hash是审计记录内容hash，不是远端完整网页或权重hash。
未执行SDK、模型、权重下载、登录、密钥调用、付费、设备/Mac访问。配图未纳入本次核验。

机器可读逐模型结论：qa-findings.json；20来源状态与审计记录hash：source-checks.json；输入hash：INPUT-SHA256.json。

## 最终补充核验（覆盖上述F03，新增F06）
论文v3 [§3.2、§4、§4.2/4.3、A.2](https://arxiv.org/html/2602.11298v3)将80–2400ms定义为target delay（80ms步长），并将batch/concurrency/network的实际延迟影响另述；不可与端到端测时混同。HF摘要240ms下界与此范围关系未解释，不直接称矛盾。

F06：原full_duplex:false会误否定协议层全双工。应拆transport_bidirectional_streaming=true（vLLM）与conversational_speech_to_speech=false；转写文本不等于语音回答。新增1个官方论文HTML来源，总计21条来源记录，原20条状态未改。
