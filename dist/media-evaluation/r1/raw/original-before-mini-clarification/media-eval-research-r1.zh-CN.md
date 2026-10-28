# 媒体评测 metadata 补包 r1

核验：2026-10-28 UTC。11 条；canonical 33 条中无 ID 重复。未改 canonical。评测 execution = never-run。

## 选入实体

| 实体 | 类别 | 口径/边界 | 官方来源 |
|---|---|---|---|
| GenEval | benchmark_metadata | 文生图对象组合对齐：共现、数量、位置与颜色。 可重新采样prompts，不能将自定义集合成绩当原版；不测量全部美学或人类偏好。 | [论文](https://arxiv.org/abs/2310.11513) · [入口](https://github.com/djghosh13/geneval) |
| DPG-Bench | benchmark_metadata | 检验图像生成对复杂密集文本描述的遵循。 不能把ELLA模型发布日期当基准发布日期；不可与GenEval整体分数直接换算。 | [论文](https://arxiv.org/abs/2403.05135) · [入口](https://github.com/TencentQQGYLab/ELLA) |
| Fréchet Inception Distance (FID) | metric_metadata | 比较真实与生成图像特征分布的距离；不是独立数据集。 代码仓库警告旧unbatched实现有bug；不是逐样本准确率，也不直接评估文本对齐。不同参考集和实现不横比。 | [论文](https://arxiv.org/abs/1706.08500) · [入口](https://github.com/bioinf-jku/TTUR) |
| VBench（原版T2V） | benchmark_metadata | 视频生成的16个细分维度，覆盖时序质量与条件一致性。 原版、I2V、Trustworthiness、VBench++与2.0不可混同；pip包版本不是基准代际。 | [论文](https://arxiv.org/abs/2311.17982) · [入口](https://github.com/Vchitect/VBench) |
| VBench-2.0 | benchmark_metadata | 视频生成内在可信性：人体保真、可控性、创造力、物理与常识。 框架结合通用VLM/LLM和专用检测器；本轮不下载、不运行、不调用裁判模型。 | [论文](https://arxiv.org/abs/2503.21755) · [入口](https://github.com/Vchitect/VBench/tree/master/VBench-2.0) |
| Fréchet Video Distance (FVD) | metric_metadata | 用于视频生成分布比较的距离指标；不是SCV数据集本身。 FVD与同论文提出的SCV基准须分实体；不能由FVD断言物理常识或文本遵循。 | [论文](https://arxiv.org/abs/1812.01717) · [入口](https://github.com/google-research/google-research/tree/master/frechet_video_distance) |
| Fréchet Audio Distance (FAD) | metric_metadata | 音频分布距离，原论文针对音乐增强质量评价。 reference-free 指无需逐样本干净配对，并非完全无需背景集合；不同embedding的FAD不可直接横比；不直接测文本语义匹配。 | [论文](https://arxiv.org/abs/1812.08466) · [入口](https://github.com/google-research/google-research/tree/master/frechet_audio_distance) |
| AudioBench（评测工具／套件） | harness_metadata | 音频语言模型的语音、声景与副语言理解评测工具。 当前README写50+数据集；论文摘要为8任务26数据集，属于不同scope。不能把当前工具链当固定26项数据集；本轮不调用任何API或裁判服务。 | [论文](https://arxiv.org/abs/2406.16020) · [入口](https://github.com/AudioLLMs/AudioBench) |
| MMAU v05.15.25 — test-mini | benchmark_metadata | 语音、环境声与音乐理解/推理；分版分切分登记。 版本标识带日期但本轮不以之替代独立核验的发布日期。test答案及解释保留，不能声称本地完整评分可用；mini不是test的可互换成绩。 | [论文](https://arxiv.org/abs/2410.19168) · [入口](https://huggingface.co/datasets/gamma-lab-umd/MMAU-test-mini) |
| MMAU v05.15.25 — test | benchmark_metadata | 语音、环境声与音乐理解/推理；分版分切分登记。 版本标识带日期但本轮不以之替代独立核验的发布日期。test答案及解释保留，不能声称本地完整评分可用；mini不是test的可互换成绩。 | [论文](https://arxiv.org/abs/2410.19168) · [入口](https://huggingface.co/datasets/gamma-lab-umd/MMAU-test) |
| MusicCaps | dataset_metadata | 专家描述的音乐—文本配对数据，支持音乐生成与理解研究。 Kaggle正文未通过本轮文本读取核验；不填未经确认的精确5521、split、license或可匿名下载结论；原始音乐权利与描述元数据必须分开。 | [论文](https://arxiv.org/abs/2301.11325) · [入口](https://www.kaggle.com/datasets/googleai/musiccaps) |

## 集成硬边界

- metric ≠ dataset ≠ harness ≠ leaderboard。FID/FVD/FAD 不得套用题库split或榜单总分语义；AudioBench 是多数据集工具套件。
- VBench原版与2.0分开；MMAU v05.15.25 test-mini/test分开；MMAU-Pro未纳入本轮。
- 日期字段分为论文首发、论文修订、基准发布、仓库更新；未核验置null。
- 结果数组均为空；只有公开元数据与官方跳转，不复制题目/答案/媒体。
- 公开介绍≠匿名下载≠标签可得≠完整本地评分；代码许可≠数据许可≠原始素材权利。

## 已确认的重要变动

- AudioBench README为50+数据集，论文摘要为26；两个scope不能覆盖。
- MMAU作者README说明新版修订，且2026-01-30把test评估迁至HF Space；test答案仍保留。
- FID作者仓库明确旧unbatched实现有bug，版本必须锁定。

## 未知／读取边界

- 所有harness commit未固定、执行环境未验证；不可称可复现实跑。
- 除明确字段外代码/数据/原始媒体授权均unknown；没有把repo许可自动延伸至数据。
- MusicCaps Kaggle正文空；精确大小、split、license、匿名下载资格未核验。
- MMAU数据卡revision与v05.15.25精确映射未固定；集成只标版本声明，不声称已下载该revision。
- 没有抓取试题/答案文件或音视频；网页附带示例未保留到产物。
- 未做任何成绩快照或跨基准排行榜。

MusicCaps正文读取失败是证据不足，不是下载授权拒绝；未尝试绕过。Google旧详情路径重定向通用目录，已排除为主证据。

## 检查

- JSON可解析；11个稳定ID唯一；与33条canonical记录无ID冲突。
- 所有记录都有官方论文、核验日期、never-run、独立许可/访问语义和比较限制。
- 源查验细节见 `source-checks.json`；未运行评测、下载权重、安装依赖或调用模型API。
