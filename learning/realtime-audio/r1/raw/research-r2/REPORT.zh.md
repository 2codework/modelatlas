# 实时语音模型研究 r2

核查日：2026-10-28。有限样本：4家、4个模型/家族。**只研究，未改canonical；未运行模型、下载权重、登录、调用收费API或访问设备/Mac。** 原始字段与逐项来源见 `raw-models.json`；实际打开结果见 `source-checks.json`。

## 有价值的结论

- **必须分开模型、服务、产品。** Moshi是双工语音模型；CSM 1B是上下文语音生成，不等于Sesame完整对话产品；Voxtral Realtime 2602是流式ASR，不生成语音回答；GPT-Realtime模型通过Realtime API提供服务，不能等同ChatGPT语音客户端。
- **开放不等于免条件。** [Moshi仓库](https://github.com/kyutai-labs/moshi)对代码与权重分开许可；[CSM模型卡](https://huggingface.co/sesame/csm-1b)明确HF门控，不能写成匿名无条件下载。API账户实际可用性未验证。
- **时间轴不可只给一个发布日期。** Moshi介绍、论文、开放发布分别是2024-07-03、09-17、09-18；CSM技术文章2025-02-27与1B权重公告03-13不同；[Voxtral公告](https://mistral.ai/news/voxtral-transcribe-2/)的2026-02-04早于论文v1的02-11。准确权重首次上传时间未证明，保留null。
- **弃用精确到ID。** [官方弃用表](https://developers.openai.com/api/docs/deprecations)列出gpt-realtime及2025-08-28快照的2027-01-20计划停用；不代表2.1或整个Realtime API弃用。2.1首发日期本轮未知，不能拿别名数字推算。

## 来源边界与版本残留

[Realtime指南](https://developers.openai.com/api/docs/guides/realtime)证明实时传输与打断流程；模型目录通用Streaming字段为Not supported，保留其原作用域，不当作同接口矛盾。指南还把独立委托后端的full-duplex指向另一个产品，因此不直接把2.1标成与Moshi同一架构的full-duplex。

[Voxtral模型卡](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)保留only-vLLM旧句，但后段明确Transformers>=5.2.0；本轮登记文本残留而非认定无法支持。卡片摘要、配置范围和论文target delay分别记录，不能单凭80ms/240ms差异认定同口径矛盾；都不是独立端到端性能证据。

Kyutai最初尝试的短路径无法访问；经官方博客索引找到正确-release路径。两个历史博客页仅返回标题和日期，不能声称已读完整技术正文。官方模型卡和论文承担能力核验。

## 去重与入库建议

核对canonical生成数据242 nodes / 77 vendor records及creative-music案例：Whisper/音乐生成已覆盖，本批语音模型没有同名node。vendor的Voxtral Mini Transcribe 3不能吞并2602实时权重。保留已有Whisper案例，不因实时关键词重复添加音乐模型。

下一步若获准整合，应把4个模型/家族与托管API、demo客户端建不同实体，日期事件使用kind，不将unknown改为推测；具体运行复现另需固定commit、权重哈希和获批算力。没有复制评测题目，只登记FLEURS作者评测的链接元信息。本批不声称全球穷尽。


## 独立QA修订与冻结

已逐项处理独立QA F01–F06及Moshi范围guard（详见CHANGES.json、QA-INPUT.json）。BF16/vLLM单GPU>=16GB是官方配置条件，绝对最低显存仍未知。论文v2日期2026-02-21已补；v3目标delay为80–2400ms、80ms步长，卡推荐480ms；实际端到端还受计算、排队、网络影响。双向流式传输不等于语音对语音对话。

GPT旧快照与2.1价格/弃用按version_records隔离；未研究的GPT-Realtime-2前代明确列coverage gap。Moshi家族公告与所核Moshiko BF16变体分开，禁止当作checkpoint首次上传日。

r1全部原字节位于before-qa，含原失败记录；R1-SHA256.json覆盖r1所有文件。r2冻结后不再原地改写，后续更改另建r3。SHA256SUMS覆盖本包所有文件（清单自身除外），清单自身哈希在交接消息中提供。无canonical写入，无模型执行。
