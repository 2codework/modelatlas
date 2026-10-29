# 端侧／小型多模态模型：有限候选批次 r2

核验日：2026-10-29。**4个精确候选、4个组织；不是全球全集、不是最新性能排行。** 来源记录18条：17条可读、1条历史访问失败；日期事件槽位24条：15条已知日期、9条unknown。 仅研究资料，未修改canonical、未实现UI、未发布，未下载权重、安装或运行SDK/模型、访问设备、登录或接受许可。

## 可直接用于简卡的结论

| 候选 | 输入 → 输出 | 参数口径 | 最重要限制 |
|---|---|---|---|
| HuggingFaceTB/SmolVLM2-500M-Video-Instruct | 文本／图像／多图／视频帧 → 文本 | 官方500M名义整体规模；精确总量及active未知 | Apache-2.0权重；不是视频生成模型 |
| Apple fastvlm_0.5b_stage3 | 文本／图像 → 文本 | 0.5B指LLM，不是全VLM；stage3总量未知 | 权重仅非商业科研；不是可商用手机控制器 |
| Google gemma-3n-E2B-it，正式launch版 | 文本／图像／视频／音频 → 文本 | effective2B≠总量；两官方正文raw5B/6B口径或版本待确认 | Gemma自定义条款，HF文件需登录同意；本轮未访问 |
| Microsoft Phi-4-multimodal-instruct | 文本／图像／音频 → 文本 | 官方完整模型名义5.6B；active未知 | MIT；官方ONNX INT4 CUDA/DirectML不等于手机通用支持 |

### 1. SmolVLM2：先理解小模型的模态边界

从[官方模型卡](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct)开始，再读[发布与MLX学习入口](https://huggingface.co/blog/smolvlm2)。2025-02-20公告声明模型已可用；[家族论文](https://arxiv.org/abs/2504.05299)首次提交是2025-04-07，不能倒填为权重发布日期。模型卡展示CUDA BF16推理，视频需decord；发布文的MLX转换件未量化。精确官方量化件、全机型最低内存未知。视频GPU RAM 1.8GB只是模型卡自报，缺完整帧数、批量、硬件配置，不作为通用门槛或本地实测。

### 2. FastVLM：公开权重不等于开放商用

[官方repo](https://github.com/apple-aiml-research/ml-fastvlm)区分0.5B stage2/stage3。[模型许可](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/LICENSE_MODEL)限非商业科研及学术开发；排除商业利用、产品开发、商业产品/服务用途，与[软件许可](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/LICENSE)分开。官方HF页的约0.8B元数据没有证明与所选stage3同字节，不据此补齐总量。[导出文档](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/model_export/README.md)的4/8-bit针对LLM，视觉编码器另用CoreML，不能称整模型全4-bit。[视觉问答demo](https://github.com/apple-aiml-research/ml-fastvlm/blob/main/app/README.md)列iOS18.2+/macOS15.2+，不是OS操作代理。

[论文](https://arxiv.org/abs/2412.13303)首次提交2024-12-17，修订2025-05-15；[官方介绍](https://machinelearning.apple.com/research/fast-vision-language-models)日期2025-07-23，更新2025-09-22，不是已查实的首个权重上传日。85倍TTFT属于作者比较实验，不等于每token速度、GUI一步1秒或完整任务时间；本批不将该家族摘要结果归到stage3实测。

### 3. Gemma 3n：保留来源差异，不猜总量

[Google官方HF卡作者正文](https://huggingface.co/google/gemma-3n-E2B-it)launch说明明确写raw6B；[2025-06-26开发者正文](https://developers.googleblog.com/en/introducing-gemma-3n-developer-guide/)写raw5B，并解释PLE将部分矩阵放在CPU、加速器有效驻留约2B。不是HF自动tensor面板与正文的混比；但本批未能确认两者是否包含相同模态编码器／同一版本，因此标记**scope_or_version_unknown**，并列5B与6B，不宣称同口径已确证矛盾。effective也不能直接改名active。

官方卡支持Transformers≥4.53.0；开发者文列AI Edge Gallery/LiteRT-LLM与MLX等入口，并不证明每个后端全模态功能一致。精确量化件、最小硬件、独立内存/速度未核实。ai.google.dev模型卡入口工具不可访问，未重试或绕过；HF公开正文可读，但权重门禁未通过，也未替用户同意Gemma条款。专属论文首投日未知，不用Gemma3或架构论文代替。

### 4. Phi-4：模型、量化转换与训练硬件分别记录

[官方模型卡](https://huggingface.co/microsoft/Phi-4-multimodal-instruct)给出5.6B完整模型、MIT、Python3.10和Transformers4.48.2示例栈；自定义代码应在未来执行前单独审核。Mixture-of-LoRAs不是可直接套MoE active参数统计。[官方ONNX卡](https://huggingface.co/microsoft/Phi-4-multimodal-instruct-onnx)列INT4、CUDA和DirectML，CPU部分仅说后续或自行转换，因此不承诺现成CPU包，更不承诺手机。

[公告](https://azure.microsoft.com/en-us/blog/empowering-innovation-the-next-generation-of-the-phi-family/)2025-02-26称HF可用；模型卡只给2025-02月精度；[技术报告](https://arxiv.org/abs/2503.01743)首投2025-03-03、修订2025-03-07。均与首个权重上传事件分开。训练GPU数量以及附录微调A100/H100建议不是普通推理最低要求。

## 去重、交付和后续边界

canonical实际git HEAD核验：`11c74bc780688f4c489e710404e52789fe4a10b4`。246 nodes、77目录条目；四个精确候选无命中，已存在Gemma4不是Gemma3n重复项。最初git命令指向外层github-migration-r1而报非仓库，已纠正到public/modelatlas，不能把该初始报错当环境限制。

本包包含 research.json（完整原始候选）、source-checks.json（18条来源记录：17条可读、1条历史失败）、date-evidence.json（24个日期事件槽位：15条已知、9条unknown）、dedup.json、canonical-baseline-sha256.json、VALIDATION.json和SHA256SUMS。来源为只读滚动页面，未锁权重commit；不声称可重复部署锁定。

后续UI仅建议“简卡筛选 → 单项学习”，不把这份研究报告直接追加成网页长页。本轮不做任何UI或canonical集成。所有GUI行动能力均未建立，所有独立速度、内存和benchmark实测均unknown。未复制受限数据、模型权重或完整第三方文章。AgentWork教材许可确认与本研究无关。
