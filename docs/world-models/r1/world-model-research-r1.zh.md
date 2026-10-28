# 世界模型 / JEPA / 具身：研究补包 r1

核验日：2026-10-28。12 个代表节点，非全球完整覆盖；未修改 canonical 182 节点。JEV 仍待用户确认。

## 先看关键校正
- PlaNet 首投为 2018-11-12；Dreamer 首投为 2019-12-03，不可直接用会议年份替换。
- I-JEPA 首投 2023-01-19，代码/权重公告为 2023-06-13。
- V-JEPA 2 公告/首投 2025-06-11；当前 README release 标签为 2025-06-25，分开保留。
- OpenVLA 是具身动作策略，不因具身身份自动变成预测世界模型。

## 节点与可操作阅读练习

### World Models · research_system
压缩视觉/时间表征并在模型内学习策略。
- 首次投稿：2018-03-27；未知日期不补午夜，不猜时区。
- 前置：VAE、RNN、强化学习
 - 纯离线练习：画出视觉编码器、记忆模型、控制器三块及数据流。
- 来源：[paper-world](https://arxiv.org/abs/1803.10122)

### PlaNet · research_system
由像素学习潜在动态并在线规划动作。
- 首次投稿：2018-11-12；未知日期不补午夜，不猜时区。
- 前置：状态空间、变分推断、模型预测控制
 - 纯离线练习：用三步状态表比较两条候选动作的预测回报。
- 来源：[paper-planet](https://arxiv.org/abs/1811.04551)

### Dreamer · research_system
在潜在想象轨迹上学习行为，不等同每一步在线搜索。
- 首次投稿：2019-12-03；未知日期不补午夜，不猜时区。
- 前置：PlaNet、actor-critic、梯度
 - 纯离线练习：手绘模型学习、想象轨迹、策略更新三个循环。
- 来源：[paper-dreamer](https://arxiv.org/abs/1912.01603)

### DreamerV2 · research_system
采用离散潜在表征的世界模型与行为学习。
- 首次投稿：2020-10-05；未知日期不补午夜，不猜时区。
- 前置：Dreamer、类别分布
 - 纯离线练习：把连续隐状态和 one-hot 类别示意对照；不拟造跑分。
- 来源：[paper-dreamerv2](https://arxiv.org/abs/2010.02193)

### JEPA（架构概念） · concept
预测目标表征而非必须重建像素；不是一款统一权重模型。
- 首次投稿：未核验/不适用；未知日期不补午夜，不猜时区。
- 前置：自监督学习、编码器、表征空间
 - 纯离线练习：写下同一目标的像素误差与表征误差各关注什么。
- 来源：[vjepa-blog](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)；[paper-ijepa](https://arxiv.org/abs/2301.08243)

### DreamerV3 · research_system
强调跨领域学习稳定性与统一配置的算法研究。
- 首次投稿：2023-01-10；未知日期不补午夜，不猜时区。
- 前置：DreamerV2、归一化、奖励尺度
 - 纯离线练习：给奖励乘常数，讨论归一化前后学习目标的可比性。
- 来源：[paper-dreamerv3](https://arxiv.org/abs/2301.04104)

### I-JEPA · model_release
图像区域之间的潜在表征预测；静态空间任务不等于动作条件动态模型。
- 首次投稿：2023-01-19；未知日期不补午夜，不猜时区。
- 前置：JEPA、Vision Transformer、masking
 - 纯离线练习：手绘 4×4 图块，指定 context 与 target；列出泄漏风险。
- 来源：[paper-ijepa](https://arxiv.org/abs/2301.08243)；[ijepa-blog](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)；[ijepa-repo](https://github.com/facebookresearch/ijepa)；[ijepa-license](https://github.com/facebookresearch/ijepa/blob/main/LICENSE)

### V-JEPA · model_release
视频时空区域的特征预测，无动作条件预训练。
- 首次投稿：2024-02-15；未知日期不补午夜，不猜时区。
- 前置：I-JEPA、视频时空 patch
 - 纯离线练习：用自己画的四帧运动图标出时间遮挡，区分识别与动作反事实。
- 来源：[paper-vjepa](https://arxiv.org/abs/2404.08471)；[vjepa-blog](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)；[vjepa-repo](https://github.com/facebookresearch/jepa)

### Genie（2024 研究系统） · research_system
从无动作标注视频学习潜在动作与可交互环境。
- 首次投稿：2024-02-23；未知日期不补午夜，不猜时区。
- 前置：视频 tokenizer、动态模型、潜在动作
 - 纯离线练习：给四帧方块移动序列列出两个可能潜在动作编码；说明不可辨识性。
- 来源：[paper-genie](https://arxiv.org/abs/2402.15391)

### OpenVLA 7B（具身策略对照） · model_release
视觉语言动作策略；输出动作不等于预测下一世界状态。
- 首次投稿：2024-06-13；未知日期不补午夜，不猜时区。
- 前置：VLM、行为克隆、动作单位与坐标系
 - 纯离线练习：纸上检查七维动作字段、单位和归一化元数据；绝不连接执行器。
- 来源：[paper-openvla](https://arxiv.org/abs/2406.09246)；[openvla-repo](https://github.com/openvla/openvla)；[openvla-card](https://huggingface.co/openvla/openvla-7b)

### Cosmos（2025 初始平台） · model_release
含世界基础模型、视频 tokenizer 与数据处理的发布平台，不是单一 checkpoint。
- 首次投稿：2025-01-07；未知日期不补午夜，不猜时区。
- 前置：视频生成、条件建模、合成数据评估
 - 纯离线练习：设计合成/真实测试集隔离表；列出物理不一致检查项。
- 来源：[paper-cosmos](https://arxiv.org/abs/2501.03575)；[cosmos-news](https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-world-foundation-model-platform-to-accelerate-physical-ai-development)；[cosmos-publication](https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai)

### V-JEPA 2 / 2-AC · model_release
区分无动作视频表征模型与经动作条件后训练的 2-AC。
- 首次投稿：2025-06-11；未知日期不补午夜，不猜时区。
- 前置：V-JEPA、动作条件预测、MPC
 - 纯离线练习：纸上对两条动作序列的预测目标距离评分；注明仅教学假值。
- 来源：[paper-vjepa2](https://arxiv.org/abs/2506.09985)；[vjepa2-blog](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)；[vjepa2-repo](https://github.com/facebookresearch/vjepa2)

## 三条阅读路径
- 从压缩环境表征到在线规划与想象策略学习。 → World Models → PlaNet → Dreamer → DreamerV2 → DreamerV3
- 比较表征预测、动作条件世界模型、动作策略三类对象。 → JEPA（架构概念） → I-JEPA → V-JEPA → V-JEPA 2 / 2-AC → OpenVLA 7B（具身策略对照）
- 认识可交互环境与视频基础模型平台的异同。 → Genie（2024 研究系统） → Cosmos（2025 初始平台）

## 实践边界与方法
- 固定模型版本、数据划分、评估协议和随机种子；不把演示当通用性能证明。
- 分离表征质量、预测误差、规划回报与真实安全性；每项各自需要验证。
- 防止相邻视频帧泄漏到训练/测试两侧；保留来源与授权。
- 潜在滚动预测误差可能累积；在纸上加入误差项检查长时规划脆弱性。
- 动作策略离线检查需区分坐标、尺度与归一化；本包不执行实际机器人。
- 先审许可、第三方依赖与数据权利，再决定是否下载或运行；本轮无权重/数据下载。

## 缺口与不确定性
- 不是全球全模态全历史完成版：本包只补 12 个代表节点。
- JEV 继续保持用户术语未确认；未建立 JEV=JEPA 别名或同义边。
- 更早的 Dyna / 神经世界模型历史，MuZero、RT 系列、Octo、后续 Genie 与 Cosmos 各版本未覆盖。
- 官方 README 已出现 V-JEPA 2.1（2026-03-16），本轮未单独研究其论文/变体/许可。
- 多数研究系统的首次代码开放、checkpoint 历史、同行评议出版日期尚未验证；null 不代表从未发布。
- V-JEPA 2 的 6月11日公告与 6月25日 README release 标签保留并列；不猜测时区或原因。
- OpenVLA 7B/8B、V-JEPA 2 encoder/system 参数口径必须保留。
- OpenReview 原概念论文访问遇验证页面；未登录、未绕过，概念年份只使用官方 Meta 回顾证据。
- 配图仅提供原创示意方案，未制作或复制论文图片；外部图权利尚未核查。

## 配图计划
仅制作原创编码器→预测器→目标表征示意、像素/潜在预测对照、世界模型/策略输出对照。图形尚未生成；无复制论文图，无模型实测或机器人演示。

## 验证范围
JSON 结构、唯一 ID、来源引用与 canonical 去重会本地检查；未运行任何模型。所有 performance 结论均未由本任务复现，正文不宣称通用 agent 能力。
