# 端侧多模态 · 来源范围与精确身份

本批4模型/4组织是有限代表性样本，不是全球全集、性能排行或手机控制能力验证。只读来源研究；never-run。
18来源记录=17可读+1历史失败；24日期槽=15已知+9 unknown。Gemma公开卡可读不等于权重访问获批；历史失败来源保留 not_accessible，不标已核验。
节点250、厂商目录77、关系151；本批只新增4节点、18来源、24日期槽（9未知保留null），目录身份和节点分开、零新关系。
旧knowledge_graph_links及realtime_audio图统计均属于固定历史阶段，不是新增后的全图。原包逐字节封存于 raw/，精确准入见 admission.json。
精确权重commit与hash未核验；未下载权重、执行模型、SDK、外部教程、账号/密钥、设备或付费调用。参数口径、许可及日期冲突保留，不推导最低硬件、不用官方自报代替实测。

## HuggingFaceTB/SmolVLM2-500M-Video-Instruct
```json
{
  "id": "edge-smolvlm2-500m-video-instruct",
  "organization": "Hugging Face",
  "exact_id": "HuggingFaceTB/SmolVLM2-500M-Video-Instruct",
  "inputs": [
    "text",
    "image",
    "multiple_images",
    "video_frames"
  ],
  "outputs": [
    "text"
  ],
  "parameters": {
    "total_nominal": 500000000,
    "total_exact": "unknown",
    "active": "unknown",
    "effective": "not separately claimed",
    "scope": "official model size label, not independently counted"
  },
  "openness": {
    "weights": "public Apache-2.0 per card",
    "code": "Transformers/MLX examples publicly linked; full code-license audit unknown",
    "terms": "Apache-2.0 model; downstream inputs and code separate"
  },
  "runtime": {
    "documented": [
      "Transformers CUDA BF16 with flash_attention_2",
      "decord video preprocessing",
      "MLX Python/Swift on Apple Silicon, historical launch examples"
    ],
    "quantization": "official launch links unquantized MLX conversion; exact official quantized artifact unknown",
    "hardware_minimum": "unknown; iPhone demo does not establish all iPhones support"
  },
  "reported_measurements": [
    {
      "metric": "GPU RAM for video inference",
      "value": "1.8GB",
      "status": "official_self_report",
      "source": "smol-card",
      "hardware": "unknown",
      "frames_context_batch": "unknown",
      "warning": "not a universal minimum or independent test"
    }
  ],
  "source_ids": [
    "smol-card",
    "smol-launch",
    "smol-paper"
  ],
  "verification_status": "primary_sources_reviewed_not_executed",
  "gui_action_capability": "unknown_not_established; not a phone controller",
  "independent_measurements": {
    "latency": "unknown",
    "peak_memory": "unknown",
    "benchmark": "unknown"
  },
  "artifact_pin": {
    "commit": "unknown",
    "weight_sha256": "unknown",
    "downloaded": false
  },
  "learning_path_zh": [
    "先读模型卡核输入输出和限制",
    "区分参数总量、effective/active及运行时精度",
    "读许可及官方运行示例（本轮只读）",
    "将实际环境/内存/延迟保持unknown，获授权后另设小样本验证"
  ],
  "learning_source_ids": [
    "smol-card",
    "smol-launch",
    "smol-paper"
  ]
}
```

## fastvlm_0.5b_stage3
```json
{
  "id": "edge-fastvlm-05b-stage3",
  "organization": "Apple",
  "exact_id": "fastvlm_0.5b_stage3",
  "inputs": [
    "text",
    "image"
  ],
  "outputs": [
    "text"
  ],
  "parameters": {
    "total": "unknown",
    "llm_nominal": 500000000,
    "active": "unknown",
    "effective": "unknown",
    "scope": "0.5B names language backbone, not full vision-language system",
    "related_not_identity_proof": "apple/FastVLM-0.5B HF metadata approximately0.8B; stage3 equality not verified"
  },
  "openness": {
    "weights": "public download links, restricted research license",
    "code": "public Apple custom software license plus third-party notices",
    "terms": "Apple Machine Learning Research Model License: non-commercial scientific research and academic development only; excludes commercial exploitation, product development, and use in any commercial product or service."
  },
  "runtime": {
    "documented": [
      "PyTorch Python3.10",
      "CoreML vision encoder plus patched mlx-vlm LLM",
      "iOS18.2+ / macOS15.2+ visual-QA demo built in Xcode"
    ],
    "quantization": "LLM-only export supports8-bit/4-bit; full-model precision not inferred",
    "hardware_minimum": "Apple Silicon path; exact minimum model/total RAM unknown"
  },
  "reported_measurements": [
    {
      "metric": "relative TTFT",
      "value": "85x",
      "status": "official_self_report",
      "source": "fast-paper",
      "baseline": "LLaVA-OneVision with0.5B LLM at1152x1152",
      "hardware": "not established in abstract reviewed",
      "warning": "not tokens/sec, not per-action/GUI end-to-end timing; not assumed stage3-specific"
    }
  ],
  "source_ids": [
    "fast-repo",
    "fast-paper",
    "fast-license-code",
    "fast-license-model",
    "fast-export",
    "fast-app",
    "fast-highlight",
    "fast-hf"
  ],
  "verification_status": "primary_sources_reviewed_not_executed",
  "gui_action_capability": "unknown_not_established; not a phone controller",
  "independent_measurements": {
    "latency": "unknown",
    "peak_memory": "unknown",
    "benchmark": "unknown"
  },
  "artifact_pin": {
    "commit": "unknown",
    "weight_sha256": "unknown",
    "downloaded": false
  },
  "learning_path_zh": [
    "先读模型卡核输入输出和限制",
    "区分参数总量、effective/active及运行时精度",
    "读许可及官方运行示例（本轮只读）",
    "将实际环境/内存/延迟保持unknown，获授权后另设小样本验证"
  ],
  "learning_source_ids": [
    "fast-repo",
    "fast-paper",
    "fast-license-code",
    "fast-license-model",
    "fast-export",
    "fast-app",
    "fast-highlight",
    "fast-hf"
  ]
}
```

## google/gemma-3n-E2B-it (launch, not preview)
```json
{
  "id": "edge-gemma3n-e2b-it",
  "organization": "Google DeepMind",
  "exact_id": "google/gemma-3n-E2B-it (launch, not preview)",
  "inputs": [
    "text",
    "image",
    "video",
    "audio"
  ],
  "outputs": [
    "text"
  ],
  "parameters": {
    "total": "scope_or_version_unknown",
    "official_claims": [
      {
        "source": "gemma-card",
        "raw": 6000000000
      },
      {
        "source": "gemma-launch",
        "raw": 5000000000
      }
    ],
    "effective": 2000000000,
    "active": "unknown",
    "scope": "E2B effective accelerator-memory footprint; not total and not generic MoE active count",
    "reconciliation_note_zh": "两数均来自官方作者正文，非HF自动tensor-size面板；未确认是否包含同样模态encoder及同版本，暂不定性同口径冲突。"
  },
  "openness": {
    "weights": "open-weight designation under Gemma custom terms; HF file gate requires account and agreement",
    "code": "Transformers implementation referenced; independent full code-license audit unknown",
    "terms": "Gemma custom license; license acceptance not performed; complete terms not reviewed"
  },
  "runtime": {
    "documented": [
      "Transformers≥4.53.0",
      "official blog links Google AI Edge Gallery/LiteRT-LLM and MLX"
    ],
    "quantization": "exact official quantization artifact and precision unknown in this bounded pass",
    "hardware_minimum": "unknown; runtime-specific modality support and memory must be verified separately"
  },
  "reported_measurements": [],
  "source_ids": [
    "gemma-card",
    "gemma-launch",
    "gemma-failed"
  ],
  "verification_status": "primary_sources_reviewed_not_executed",
  "gui_action_capability": "unknown_not_established; not a phone controller",
  "independent_measurements": {
    "latency": "unknown",
    "peak_memory": "unknown",
    "benchmark": "unknown"
  },
  "artifact_pin": {
    "commit": "unknown",
    "weight_sha256": "unknown",
    "downloaded": false
  },
  "learning_path_zh": [
    "先读模型卡核输入输出和限制",
    "区分参数总量、effective/active及运行时精度",
    "读许可及官方运行示例（本轮只读）",
    "将实际环境/内存/延迟保持unknown，获授权后另设小样本验证"
  ],
  "learning_source_ids": [
    "gemma-card",
    "gemma-launch",
    "gemma-failed"
  ]
}
```

## microsoft/Phi-4-multimodal-instruct
```json
{
  "id": "edge-phi4-multimodal-instruct",
  "organization": "Microsoft",
  "exact_id": "microsoft/Phi-4-multimodal-instruct",
  "inputs": [
    "text",
    "image",
    "audio"
  ],
  "outputs": [
    "text"
  ],
  "parameters": {
    "total_nominal": 5600000000,
    "total_exact": "unknown",
    "active": "unknown",
    "effective": "unknown",
    "scope": "full multimodal transformer including backbone/encoders/adapters; mixture-of-LoRAs not interchangeable with MoE active count"
  },
  "openness": {
    "weights": "public MIT per model card",
    "code": "public custom_code inference examples; MIT model repo metadata, dependencies separate",
    "terms": "MIT; downstream media rights and dependencies require own review"
  },
  "runtime": {
    "documented": [
      "Python3.10, Transformers4.48.2 example stack with trust_remote_code",
      "official ONNX INT4 CUDA / DirectML"
    ],
    "quantization": "microsoft/Phi-4-multimodal-instruct-onnx gpu-int4-rtn-block-32; conversion treated separately, not bit-identical base",
    "hardware_minimum": "unknown; CUDA/DML targets not phone guarantee; training A100 counts excluded from inference requirements",
    "cpu": "official ONNX card says stay tuned or convert; no ready CPU compatibility claimed"
  },
  "reported_measurements": [],
  "source_ids": [
    "phi-card",
    "phi-launch",
    "phi-paper",
    "phi-onnx"
  ],
  "verification_status": "primary_sources_reviewed_not_executed",
  "gui_action_capability": "unknown_not_established; not a phone controller",
  "independent_measurements": {
    "latency": "unknown",
    "peak_memory": "unknown",
    "benchmark": "unknown"
  },
  "artifact_pin": {
    "commit": "unknown",
    "weight_sha256": "unknown",
    "downloaded": false
  },
  "learning_path_zh": [
    "先读模型卡核输入输出和限制",
    "区分参数总量、effective/active及运行时精度",
    "读许可及官方运行示例（本轮只读）",
    "将实际环境/内存/延迟保持unknown，获授权后另设小样本验证"
  ],
  "learning_source_ids": [
    "phi-card",
    "phi-launch",
    "phi-paper",
    "phi-onnx"
  ]
}
```

## 日期证据
```json
{
  "events": [
    {
      "model_id": "edge-smolvlm2-500m-video-instruct",
      "event": "announced",
      "date": "2025-02-20",
      "precision": "day",
      "source_id": "smol-launch",
      "note_zh": ""
    },
    {
      "model_id": "edge-smolvlm2-500m-video-instruct",
      "event": "weights_available_by",
      "date": "2025-02-20",
      "precision": "day",
      "source_id": "smol-launch",
      "note_zh": "当天文明确称模型开放；不是独立仓库首个权重commit证明"
    },
    {
      "model_id": "edge-smolvlm2-500m-video-instruct",
      "event": "paper_first_submitted",
      "date": "2025-04-07",
      "precision": "day",
      "source_id": "smol-paper",
      "note_zh": "家族论文，非权重首发"
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "paper_first_submitted",
      "date": "2024-12-17",
      "precision": "day",
      "source_id": "fast-paper",
      "note_zh": ""
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "paper_v2",
      "date": "2025-05-15",
      "precision": "day",
      "source_id": "fast-paper",
      "note_zh": ""
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "official_highlight",
      "date": "2025-07-23",
      "precision": "day",
      "source_id": "fast-highlight",
      "note_zh": ""
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "weights_available_by",
      "date": "2025-07-23",
      "precision": "day",
      "source_id": "fast-highlight",
      "note_zh": "介绍文称权重可用，不证明首次上传日期"
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "hf_availability_update",
      "date": "2025-09-22",
      "precision": "day",
      "source_id": "fast-highlight",
      "note_zh": "更新日期，非首发"
    },
    {
      "model_id": "edge-gemma3n-e2b-it",
      "event": "full_launch",
      "date": "2025-06-26",
      "precision": "day",
      "source_id": "gemma-launch",
      "note_zh": "launch而非早期preview"
    },
    {
      "model_id": "edge-gemma3n-e2b-it",
      "event": "weights_available_by",
      "date": "2025-06-26",
      "precision": "day",
      "source_id": "gemma-launch",
      "note_zh": "官方文提供权重入口；本轮未过门禁"
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "announced",
      "date": "2025-02-26",
      "precision": "day",
      "source_id": "phi-launch",
      "note_zh": ""
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "release_month",
      "date": "2025-02",
      "precision": "month",
      "source_id": "phi-card",
      "note_zh": ""
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "weights_available_by",
      "date": "2025-02-26",
      "precision": "day",
      "source_id": "phi-launch",
      "note_zh": "公告称HF可用，精确首次权重commit未核验"
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "paper_first_submitted",
      "date": "2025-03-03",
      "precision": "day",
      "source_id": "phi-paper",
      "note_zh": ""
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "paper_v2",
      "date": "2025-03-07",
      "precision": "day",
      "source_id": "phi-paper",
      "note_zh": ""
    },
    {
      "model_id": "edge-smolvlm2-500m-video-instruct",
      "event": "weights_first_uploaded",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": "未查实首个权重上传，不能用论文/公告/更新替代"
    },
    {
      "model_id": "edge-smolvlm2-500m-video-instruct",
      "event": "repo_first_public",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": ""
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "weights_first_uploaded",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": "未查实首个权重上传，不能用论文/公告/更新替代"
    },
    {
      "model_id": "edge-fastvlm-05b-stage3",
      "event": "repo_first_public",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": ""
    },
    {
      "model_id": "edge-gemma3n-e2b-it",
      "event": "weights_first_uploaded",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": "未查实首个权重上传，不能用论文/公告/更新替代"
    },
    {
      "model_id": "edge-gemma3n-e2b-it",
      "event": "repo_first_public",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": ""
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "weights_first_uploaded",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": "未查实首个权重上传，不能用论文/公告/更新替代"
    },
    {
      "model_id": "edge-phi4-multimodal-instruct",
      "event": "repo_first_public",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": ""
    },
    {
      "model_id": "edge-gemma3n-e2b-it",
      "event": "paper_first_submitted",
      "date": null,
      "precision": "unknown",
      "source_id": null,
      "note_zh": "本批未确认专属技术报告，不误用Gemma3或架构论文日期"
    }
  ],
  "rule_zh": "公告、论文、权重可用上界、首个上传分列；null就是unknown，无补造日期。",
  "summary_counts": {
    "date_event_slot_count": 24,
    "known_date_count": 15,
    "unknown_date_count": 9
  }
}

```
## 来源状态
```json
[
  {
    "id": "smol-card",
    "url": "https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "图像/多图/视频/文本入、文本出；500M标签；Apache-2.0权重；BF16 CUDA例程、decord视频预处理；官方称视频推理1.8GB GPU RAM，未列完整测量配置。",
    "locator": "Model Summary; Uses; License; How to get started",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "smol-launch",
    "url": "https://huggingface.co/blog/smolvlm2",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "2025-02-20发布三种规模，声明模型已开放；500M视频模型；提供MLX Python/Swift路径，引用未量化社区转换件；iPhone应用为演示，不是通用控制。",
    "locator": "Published; Technical Details; MLX",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "smol-paper",
    "url": "https://arxiv.org/abs/2504.05299",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "关联SmolVLM家族论文首次提交2025-04-07；不是该权重首次发布日期。",
    "locator": "Submission history v1",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-repo",
    "url": "https://github.com/apple-aiml-research/ml-fastvlm",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "Model Zoo明确0.5B stage2与stage3；另有stage3 Apple Silicon格式；PyTorch、导出、demo入口。代码与模型分开授权。",
    "locator": "Model Zoo; Inference; License",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-paper",
    "url": "https://arxiv.org/abs/2412.13303",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "v1 2024-12-17，v2 2025-05-15。摘要0.5B是LLM大小；85倍TTFT为相对LLaVA-OneVision、1152×1152设定的官方自报，不是GUI完成时间。",
    "locator": "v2 abstract; Submission history",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-license-code",
    "url": "https://github.com/apple-aiml-research/ml-fastvlm/blob/main/LICENSE",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "Apple自定义软件许可，允许受条款约束的使用/修改/再分发，另有第三方声明；不能当作模型许可。",
    "locator": "LICENSE",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-license-model",
    "url": "https://github.com/apple-aiml-research/ml-fastvlm/blob/main/LICENSE_MODEL",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "Apple Machine Learning Research Model License：限非商业科研及学术开发；排除商业利用、产品开发、商业产品/服务用途，衍生模型亦受限制。",
    "locator": "License Scope",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-export",
    "url": "https://github.com/apple-aiml-research/ml-fastvlm/blob/main/model_export/README.md",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "研究探索而非正式推荐；视觉编码器CoreML导出；补丁mlx-vlm；LLM支持8/4-bit量化，不等于整VLM全量同精度。",
    "locator": "Export Vision Encoder; Export VLM",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-app",
    "url": "https://github.com/apple-aiml-research/ml-fastvlm/blob/main/app/README.md",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "视觉问答demo声明iOS18.2+、macOS15.2+；Xcode构建，设备本地推理。未给全机型最低RAM。",
    "locator": "Features",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-highlight",
    "url": "https://machinelearning.apple.com/research/fast-vision-language-models",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "2025-07-23研究介绍称代码/权重/demo可用；2025-09-22更新称HF MLX/CoreML件可用；二者不能当首发权重日。UI导航只是VLM潜在应用语境。",
    "locator": "Published; Update",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "fast-hf",
    "url": "https://huggingface.co/apple/FastVLM-0.5B",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "官方仓库面板约0.8B params，BF16；未在本轮证实与repo stage3字节相同，不据此填stage3精确总量。",
    "locator": "Safetensors metadata",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "gemma-card",
    "url": "https://huggingface.co/google/gemma-3n-E2B-it",
    "checked_at": "2026-10-29",
    "status": "public_card_read_weights_gated_not_accessed",
    "primary": true,
    "evidence_summary_zh": "launch版E2B IT，文本/图像/视频/音频入、文本出；raw6B，effective2B；Transformers≥4.53.0。公开模型卡可读，文件需登录同意Gemma许可，本轮未同意/访问文件。",
    "locator": "Launch note; Access; Usage",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "gemma-launch",
    "url": "https://developers.googleblog.com/en/introducing-gemma-3n-developer-guide/",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "2025-06-26完整发布入口与权重链接；正文E2B raw5B，HF作者正文6B；两者范围/版本是否相同待确认。effective2B指加速器驻留口径，不是MoE active。列AI Edge Gallery/LiteRT-LLM、MLX入口，不保证各端全模态等价。",
    "locator": "Date; PLE; Get started",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "gemma-failed",
    "url": "https://ai.google.dev/gemma/docs/core/model_card_3n",
    "checked_at": "2026-10-29",
    "status": "failed_tool_access",
    "primary": true,
    "evidence_summary_zh": "web工具报URL不可访问；未重试、未绕过。其他公开官方页独立读取，不访问受限权重。",
    "locator": "open result",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "phi-card",
    "url": "https://huggingface.co/microsoft/Phi-4-multimodal-instruct",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "5.6B含主干/视觉/语音编码器和适配器；文本图像音频入、文本出；MIT；Python3.10、Transformers4.48.2例程及自定义代码；发布时间仅月精度2025-02。",
    "locator": "Model; Requirements; License",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "phi-launch",
    "url": "https://azure.microsoft.com/en-us/blog/empowering-innovation-the-next-generation-of-the-phi-family/",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "2025-02-26公告称Phi-4-multimodal已在HF等入口可用；5.6B官方自报；不以该日期证明权重首次上传时间。",
    "locator": "Date; Now available",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "phi-paper",
    "url": "https://arxiv.org/abs/2503.01743",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "Phi-4-Mini Technical Report包含multimodal与Mixture-of-LoRAs；v1 2025-03-03，v2 2025-03-07。",
    "locator": "Title; Submission history",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  },
  {
    "id": "phi-onnx",
    "url": "https://huggingface.co/microsoft/Phi-4-multimodal-instruct-onnx",
    "checked_at": "2026-10-29",
    "status": "reviewed_public_text",
    "primary": true,
    "evidence_summary_zh": "官方INT4 ONNX转换，CUDA及DirectML例程；CPU现成包未承诺，页称待续或自行转换；不能泛化成手机支持。",
    "locator": "Introduction; Model Run",
    "revision": "rolling page unless arXiv version stated",
    "executed": false
  }
]
```
