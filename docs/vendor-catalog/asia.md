# 亚洲模型目录研究候选

核验日期：2026-10-28。共 37 条，其中 33 条模型/具名版本，4 条 API 调用名（不计为独立模型）。只读官网、官方repo、作者模型卡和论文；未运行模型。

## 重要结论
- QA更正：Qwen2.5-Omni-3B权重许可为[qwen-research（官方模型卡）](https://huggingface.co/Qwen/Qwen2.5-Omni-3B)，不能套用仓库代码Apache-2.0；[权重条文](https://huggingface.co/Qwen/Qwen2.5-Omni-3B/blob/main/LICENSE)§1.i/2.a限定非商用研究或评估，§2.b商用须申请许可；不推断授权已获批。许可模板日期不是模型发布日期。
- DeepSeek 当前API名与快照分开，旧Flash名仍接受但底层已退役。
- GLM 4.5权重MIT与repo代码Apache不可混同。EXAONE 3.5非商用许可，不应标无条件开放。
- ERNIEKit/FastDeploy、MNN等是工具，不计模型；Seed-Coder旧称Doubao-Coder不重复计。
- 这是中国、印度、韩国、日本的代表补充，不是全球齐全或各厂商全历史。

## 记录
|精确标识|厂商|类型|模态|官方证据|
|---|---|---|---|---|
|Qwen/Qwen3-0.6B|Alibaba/Qwen|model_checkpoint|llm|[官方来源](https://github.com/QwenLM/Qwen3)|
|Qwen/Qwen3-8B|Alibaba/Qwen|model_checkpoint|llm|[官方来源](https://github.com/QwenLM/Qwen3)|
|Qwen/Qwen3-235B-A22B-Instruct-2507|Alibaba/Qwen|model_checkpoint|llm|[官方来源](https://github.com/QwenLM/Qwen3)|
|deepseek-ai/DeepSeek-R1|DeepSeek|model_checkpoint|llm|[官方来源](https://github.com/deepseek-ai/DeepSeek-R1)|
|deepseek-ai/DeepSeek-R1-Zero|DeepSeek|model_checkpoint|llm|[官方来源](https://github.com/deepseek-ai/DeepSeek-R1)|
|deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B|DeepSeek|model_checkpoint|llm|[官方来源](https://github.com/deepseek-ai/DeepSeek-R1)|
|zai-org/GLM-4.5|Z.ai / 智谱|model_checkpoint|llm|[官方来源](https://github.com/zai-org/GLM-4.5)|
|zai-org/GLM-4.5-Air|Z.ai / 智谱|model_checkpoint|llm|[官方来源](https://github.com/zai-org/GLM-4.5)|
|Kimi-K2-Base|Moonshot AI|model_checkpoint|llm|[官方来源](https://github.com/MoonshotAI/Kimi-K2)|
|Kimi-K2-Instruct|Moonshot AI|model_checkpoint|llm|[官方来源](https://github.com/MoonshotAI/Kimi-K2)|
|MiniMaxAI/MiniMax-M1-40k|MiniMax|model_checkpoint|llm|[官方来源](https://github.com/MiniMax-AI/MiniMax-M1)|
|MiniMaxAI/MiniMax-M1-80k|MiniMax|model_checkpoint|llm|[官方来源](https://github.com/MiniMax-AI/MiniMax-M1)|
|ERNIE-4.5-300B-A47B-Base|Baidu|named_model_variant|llm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-300B-A47B|Baidu|named_model_variant|llm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-21B-A3B-Base|Baidu|named_model_variant|llm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-21B-A3B|Baidu|named_model_variant|llm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-VL-424B-A47B-Base|Baidu|named_model_variant|vlm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-VL-424B-A47B|Baidu|named_model_variant|vlm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-VL-28B-A3B-Base|Baidu|named_model_variant|vlm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-VL-28B-A3B|Baidu|named_model_variant|vlm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-0.3B-Base|Baidu|named_model_variant|llm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ERNIE-4.5-0.3B|Baidu|named_model_variant|llm|[官方来源](https://github.com/PaddlePaddle/ERNIE)|
|ByteDance-Seed/Seed-Coder-8B-Base|ByteDance Seed|model_checkpoint|llm|[官方来源](https://github.com/ByteDance-Seed/Seed-Coder)|
|ByteDance-Seed/Seed-Coder-8B-Instruct|ByteDance Seed|model_checkpoint|llm|[官方来源](https://github.com/ByteDance-Seed/Seed-Coder)|
|ByteDance-Seed/Seed-Coder-8B-Reasoning|ByteDance Seed|model_checkpoint|llm|[官方来源](https://github.com/ByteDance-Seed/Seed-Coder)|
|HunyuanVideo|Tencent Hunyuan|named_model_variant|video_generation|[官方来源](https://github.com/Tencent-Hunyuan/HunyuanVideo)|
|Qwen/Qwen2.5-Omni-3B|Alibaba/Qwen|model_checkpoint|llm,vlm,audio_understanding,speech_generation|[官方来源](https://github.com/QwenLM/Qwen2.5-Omni)|
|Qwen/Qwen-Image|Alibaba/Qwen|model_checkpoint|image_generation|[官方来源](https://github.com/QwenLM/Qwen-Image)|
|Qwen/Qwen-Image-2512|Alibaba/Qwen|model_checkpoint|image_generation|[官方来源](https://github.com/QwenLM/Qwen-Image)|
|BAAI/bge-m3|BAAI|model_checkpoint|text_embedding|[官方来源](https://huggingface.co/BAAI/bge-m3)|
|sarvamai/sarvam-m|Sarvam AI|model_checkpoint|llm|[官方来源](https://huggingface.co/sarvamai/sarvam-m)|
|LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct|LG AI Research|model_checkpoint|llm|[官方来源](https://huggingface.co/LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct)|
|llm-jp/llm-jp-3-3.7b-instruct|NII / LLM-jp|model_checkpoint|llm|[官方来源](https://huggingface.co/llm-jp/llm-jp-3-3.7b-instruct)|
|deepseek-flash|DeepSeek|api_alias|vlm|[官方来源](https://api-docs.deepseek.com/quick_start/pricing/)|
|deepseek-v4-pro|DeepSeek|api_alias|llm|[官方来源](https://api-docs.deepseek.com/quick_start/pricing/)|
|deepseek-v4-flash|DeepSeek|legacy_api_alias|vlm|[官方来源](https://api-docs.deepseek.com/quick_start/pricing/)|
|deepseek-v4-flash-vision-exp|DeepSeek|legacy_api_alias|vlm|[官方来源](https://api-docs.deepseek.com/quick_start/pricing/)|

## 去重与证据
读取 github-migration-r1/public/modelatlas/dist/data.json（0.2.2）。qwen/org-qwen、deepseek/org-deepseek为家族或组织；不能被checkpoint覆盖。deepseek-r1-2025是原paper-v1报告锚点；DeepSeek-R1 checkpoint与报告是不同实体，只建立关联，不自动合并或覆盖旧节点。Sarvam-M与现有sarvam-1不同；接到sarvam家族。所有existingIDs已验证存在。

## 缺口
- 未穷举各家所有历史、私有API、量化及派生权重；不能宣称齐全。
- 多数发布日期无明确证据而为null，不从版本号、论文号或git日期猜。
- Kimi初次HF访问失败仅保留为历史观察，独立QA后续已读到官方卡；EXAONE许可链接404，完整条文unknown；百度AIStudio页面无有效正文，以官方repo替代。
- PaperURL为null即本批未核实；licenseURL可为官方许可声明而非完整合同。
- current_documented仅文档存在，非当前托管API仍支持保证；旧公开权重不因较老而标弃用。
- 印度/韩国/日本仅代表公开模型；亚洲其他国家未覆盖。
- 模型权重未下载；代码、API及教程均未执行；无性能排名。

## 字段解释
JSON中的exactid是官方精确字符串；named_model_variant暂未绑定分发仓库。release_dates四种日期独立；null表示未核实。API alias不是独立训练模型，resolved_snapshot只是核验日映射，不承诺永远固定。所有性能宣传均未采用为独立实测结论。

## 独立QA元数据更正
Kimi初次访问失败保留为一次历史工具观察；独立QA于2026-10-28 19:46 UTC成功读取[Base官方卡](https://huggingface.co/moonshotai/Kimi-K2-Base)与[Instruct官方卡](https://huggingface.co/moonshotai/Kimi-K2-Instruct)，确认发布者、模型身份及modified-mit声明。EXAONE 404与完整许可条文unknown维持。37条记录的身份、模态、日期及access均未改；只修5条相关元数据，等待最终独立复核。
