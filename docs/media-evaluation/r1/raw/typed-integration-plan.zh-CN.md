# 媒体评测：类型化集成计划（未实施）

状态：等待 root 提供 office211 已提交后的最新 SHA。不得以当前工作树或早期 SHA 构建候选；本文件不是集成完成声明。

## 数据结构决策

- 保留既有 `dataset_benchmark_registry` 33 条，逐项原样保留，不追加本包11条。
- 新增独立 `media_evaluation_registry`，容纳全部11个类型化知识实体；字段 `entity_kind` 为 benchmark / metric / harness / dataset。
- 计数为6 benchmark、3 metric、1 harness、1 dataset；“11”仅称媒体评测知识实体，不称11数据集或11基准。
- 每条仍映射独立 first-class node，使用既有稳定 node_id。metric/harness 不能退化为某个数据集的文字脚注，也不能伪装模型。
- Registry 提供原始结构化元数据，node 提供导航与概览；相同实体不可因两处存储被双计数。

## 必须可见的详情

中文原创描述、entity_kind、family/version/split、模态、指标口径、比较限制、执行状态、官方来源与核验日期、访问语义、代码/数据/原始媒体权利边界，以及独立论文首发/修订/基准发布/仓库更新字段。

- null 统一显示“未核验”，不可当作不存在。
- `never-run` 显示“未运行评测”；空结果不渲染排名或零分。
- 文本介绍公开不意味着文件可匿名下载、标签可得或本地评分可运行。
- 官方leaderboard/evaluation service仅是外链，不据其存在把对应实体分类为leaderboard。
- MMAU-mini 的提示明确：保留答案指另外的9000条 test，不能套到mini；两个split不能互换成绩。

## 集成前置和验收

1. 接收并验证 root 的最新基线 SHA；确认office211基线已纳入。
2. 只在独立候选目录实施；先保存基线文件哈希与节点、关系、原registry计数。
3. 新registry恰11条，类型计数6/3/1/1，ID唯一且与既有节点检查冲突。
4. 原33条registry深度相等；无替换、丢字段或统一强制类型。
5. 所有新实体可搜索、可导航、详情类型正确；来源链接及unknown字段可见。
6. 图节点、详情、导出、搜索和统计使用同一类型语义；不把metric计入模型/数据集数量。
7. 验证无试题、答案、音视频、权重及成绩快照；无下载、API调用或评测执行入口。
8. 对照最新基线进行差异审查、静态校验和已授权的UI验证后，交 root 独立QA；不自行写canonical或发布。

本计划不包含候选实现，不授权运行benchmark或调用任何模型。
