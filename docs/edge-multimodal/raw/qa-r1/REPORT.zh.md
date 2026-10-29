# 端侧多模态 r1 独立 QA

**结论：accept（研究主体），revise（两项摘要精度）；不是集成／发布批准。**

2026-10-29 实际通过 web 重开17个官方公开正文。第18条是原包保留的 Google docs 访问失败记录，本轮遵守已有失败边界，未重试；不是成功核验来源。24个日期事件槽位实际为15个有日期、9个unknown。原包 SHA256SUMS 7/7通过。

## 接受项

- **SmolVLM2-500M**：官方500M标签、图像/视频/文本输入而仅文本输出、Apache-2.0、1.8GB为缺完整条件的官方自报，均正确。公告2025-02-20、家族论文2025-04-07分列正确。[模型卡](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct)、[公告](https://huggingface.co/blog/smolvlm2)、[论文](https://arxiv.org/abs/2504.05299)。
- **FastVLM stage3**：0.5B是LLM主干，不能写成整机总量；stage2/stage3确实分开。模型仅限非商业科研，代码许可另列；LLM 4/8-bit不等于视觉编码器全量化。HF约0.8B不是所选stage3字节身份证明。论文v1/v2及介绍/更新日期正确，TTFT不是GUI执行耗时。[仓库](https://github.com/apple-aiml-research/ml-fastvlm)、[模型许可](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/LICENSE_MODEL)、[论文](https://arxiv.org/abs/2412.13303)、[导出](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/model_export/README.md)。
- **Gemma 3n E2B IT**：两份官方作者正文确实分别写raw6B/raw5B；原包保留scope_or_version_unknown是正确决策，不能擅自挑一个或相加。effective2B是内存/驻留相关口径而非通用active计数。launch不是preview，2025-06-26正确，HF文件同意门禁可见但未访问。[HF正文](https://huggingface.co/google/gemma-3n-E2B-it)、[发布正文](https://developers.googleblog.com/en/introducing-gemma-3n-developer-guide/)。
- **Phi-4 multimodal**：5.6B完整多模态模型，MIT，文本/图像/音频入而文本出。官方ONNX INT4支持CUDA/DirectML例程，CPU页仍说待续或自行转换。公告2025-02-26、论文2025-03-03/03-07、模型卡2025-02月精度分开正确。[卡](https://huggingface.co/microsoft/Phi-4-multimodal-instruct)、[ONNX](https://huggingface.co/microsoft/Phi-4-multimodal-instruct-onnx)、[公告](https://azure.microsoft.com/en-us/blog/empowering-innovation-the-next-generation-of-the-phi-family/)、[论文](https://arxiv.org/abs/2503.01743)。

## 两项 revise

1. **统计文案**明确“18个来源条目（17可读、1失败），24个日期事件槽位（15有日期、9未知）”。原包结构本身保留失败/unknown是优点，不得在简卡或状态汇总抹掉。
2. **FastVLM许可摘要**不要把独立的“产品开发”排除项缩成仅“商业产品开发”。建议：限非商业科研及学术开发；排除商业利用、产品开发、商业产品/服务用途。以[原条款 License Scope](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/LICENSE_MODEL)为准，非法律意见。

## 可选准确补充，不要求扩范围

Gemma发布时音频实现有30秒片段限制，不能拿流式架构潜力冒充发布实现或所有当前后端能力；Phi卡将语言覆盖按模态分开，视觉列英语，不能将文本多语言数套到视觉。详见 findings.json 的直接官方定位。

## 去重与边界

canonical HEAD仍为 `11c74bc780688f4c489e710404e52789fe4a10b4`；246 nodes，77 catalog records。对节点和目录完整记录做忽略大小写/空格/标点的家族词扫描，四候选均无命中。Gemma4不应合并为Gemma3n。具体散列见 dedup-review.json。

仅写此QA目录，未更改原研究/canonical、未集成或发布、未下载权重/执行模型、未用账号密钥或Mac。当前滚动页面不等于固定commit快照；weights_available_by不是首上传日期，且家族公告不证明stage3字节身份。完整来源URL/工具定位、24项日期判定、原文件hash均随包保存。不能据本研究声称全球完整、真实速度排名或可复现部署已验证。
