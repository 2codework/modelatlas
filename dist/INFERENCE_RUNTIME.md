# 推理运行时学习补缺 r2

这是 **4 个非模型运行时家族的有限代表批次**，不是全集、最新版清单、性能榜或部署推荐。全部仅官方来源阅读，安装、SDK/模型执行、权重下载均为零。来源支持不等于独立运行效果。

## 先把三层分开

1. **模型制品**：权重、模型结构、tokenizer、配置及原模型许可。
2. **运行时/后端**：负责执行算子或生成循环；支持必须精确到版本、模型架构、精度和设备。
3. **入口**：本地API、HTTP服务或导出工具；请求长得像OpenAI接口不代表用的是OpenAI模型。

已有的 vLLM、llama.cpp、MLX LM 不重建。新增的 ORT/OpenVINO 以核心为主节点，将 GenAI、导出层纳入辨析，不把分层重复计为额外模型。

## 四条入门路线（原创阅读任务，不是执行教程）

### SGLang

从[安装页](https://docs.sglang.ai/get_started/install.html)读出版本与设备约束，再到[量化页](https://docs.sglang.ai/advanced_features/quantization.html)找一个离线量化路径。阅读目标：把权重加载、分词、prefill/decode和返回文本画成一条线，指出量化作用的位置。安装页默认Linux/NVIDIA，不应推成通用Windows/macOS教程。量化页导航的 Basic Usage / Sending a request 是后续官方调用阅读入口，**本批没有打开这些下级页**。本批不提供未经阅读校验的具体请求参数。

### TensorRT-LLM

先读[v0.18.0 release](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.18.0)的Windows弃用，再读[支持矩阵](https://nvidia.github.io/TensorRT-LLM/reference/support-matrix.html)和[Quick Start](https://nvidia.github.io/TensorRT-LLM/quick-start-guide.html)。阅读TinyLlama例子的对象、采样配置、输出字段，区分PyTorch backend与TensorRT engine。矩阵页尾是2025-09-15；不可把它当2026全部兼容保证，也不能拿滚动Quick Start反证旧release支持所有新功能。

### ONNX Runtime

先从[安装矩阵入口](https://onnxruntime.ai/docs/install/)选择目标平台与EP，再读[量化文档](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)理解QDQ/QOperator。输出张量不是完整聊天响应；需要分词、采样、KV管理才读[GenAI层](https://onnxruntime.ai/docs/genai/)。阅读目标：用纸面输入name/dtype/shape追踪一遍图调用，再画出生成循环多次调用。INT4支持部分算子，不是任意ONNX图自动四位执行。

### OpenVINO

读[核心README](https://github.com/openvinotoolkit/openvino)的转换—设备编译—张量调用，再读[GenAI README](https://github.com/openvinotoolkit/openvino.genai)的Optimum导出和LLMPipeline。阅读目标：区分IR制品、Runtime设备插件、GenAI管线与Optimum Intel导出职责。官方示例出现的远程模型加载和trust_remote_code本批均不执行。核心支持Intel NPU不证明每条GenAI管线都支持每款NPU。

## 未来真正运行时，如何判定成功（本批未执行）

- 先记录运行时版本、模型revision、制品hash、真实device/provider，不允许“默认应该在GPU”代替证据。
- 单条短输入，固定最大输出长度；张量检查shape/dtype/有限值，生成检查可解码文本/停止条件/错误日志。
- 量化与浮点基线采用相同输入与模板；校验质量而非仅能加载。
- 最低内存、速度、成本、精度损失全部unknown；训练用卡数量不是推理最低要求。
- 软件LICENSE、第三方依赖条款和模型许可分开；许可证摘要仅为项目声明，不是完整法律审核。

## 日期与证据边界

四个历史release版本已读；页面正文仅显示月日时分，未可靠显示年份/时区，因此ISO发布日期与first-release都为null。观察日期2026-10-29不是发布日期。滚动文档的版本要求不移植到历史release。

16 个入包来源实体全部保留。r2 针对 QA 重读 3 页：main LICENSE、v0.18.0 release、ORT 安装页；其余 13 页沿用 r1 阅读及独立 QA，不声称再次打开。r2 共 3 次 web 调用、8 个操作（4 open、4 find），3 页正文可读；网络请求数与 HTTP 状态未知。r1 的 17 页/9 次调用/39 个操作只作为历史记录保留。

### r2 精确修订

- [TensorRT-LLM 当前 main LICENSE](https://github.com/NVIDIA/TensorRT-LLM/blob/main/LICENSE)：LTX-2 Community License Agreement 仅用于 `tensorrt_llm/_torch/visual_gen/models/ltx2/` 目录代码；不是全仓库许可，也没有回填为 v0.18.0 的许可。Windows 弃用仍只由历史 v0.18.0 release 支持，不代表当前所有平台结论。
- [ORT 当前安装页](https://onnxruntime.ai/docs/install/)：DirectML 为 sustained engineering。新 Windows 项目在 Python 段为“考虑 WinML”，C#/C/C++ 段为“使用 WinML”；仅转述该页建议，不声称 DirectML 已删除，也不回填到 v1.22.0。
- r2 为独立完整数据包，r1 未修改。未知日期与性能指标不补猜；无安装、下载、SDK/推理执行、Mac 操作、canonical 写入或 push。

## 文件

- `runtime-learning.json`：4节点及16来源、许可/兼容/输入输出/学习路线。
- `source-checks.json`、`source-checks-r1-history.json`、`reading-ledger.json`、`date-evidence.json`、`dedup.json`：来源、日期和去重边界。
- `schema.json`、`validate.py`、`validation.json`：本地结构校验，**不是模型测试**。
- `SHA256SUMS`：文件完整性；不代表远端源码或权重固定hash。

仍缺：完整跨版本平台矩阵、所有模型架构、首次发布日期、依赖许可清单、独立执行验证。因此不称“全面完成”。

`dedup.json` 是 r1 canonical 快照检查，不是 r2 对当前 canonical 的重扫。`input-integrity.json` 固定全部输入文件摘要；`remediation.json` 记录修订。`validate.py` 只读校验，运行不改包。包发布后不原位编辑；后续变更用 r3。
