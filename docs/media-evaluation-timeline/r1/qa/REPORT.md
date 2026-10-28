# 媒体评测时间轴提案独立 QA r1

**Accept：17条提案证据通过；提案事实无需修复。集成仍须显式扩展类型，尚未合并。**

- 10篇不同论文首发、5个末次已核验修订、DPG-Bench发布及MMAU test迁移公告各1条。全部日期与本轮较早直接读取的一手arXiv/作者README证据及已审核媒体包一致；无重新联网，无重访已阻断页面。
- MMAU论文合并为单条事件，关联test-mini与test两节点；2024论文日期只表示学术来源，不代表v05.15.25数据版本发布。平台迁移公告只关联test。
- 论文首发、论文修订、基准发布及平台迁移公告含义明确。DPG-Bench 2024-03-11来自作者changelog，而非论文或ELLA权重日期；MMAU 2026-01-30是公告日期，不是独立观测切换时刻。
- 所有日期精度day，时区保持null。原包没有保留时区，本次不提升精度；不从版本字符串、核验日期或仓库当前内容推断日期。
- 五个修订仅截至已审核快照的末次修订，不是完整历史；revision version保持未知。首发/末次字段同日的5组不另造事件，也不据此断言没有同日修订。
- 21个未知发布日期/仓库更新时间字段保留。MusicCaps未冒充精确数据发布日。

## 冲突检查

独立检查149条既有事件：ID、规范化来源+日期+类型、共享来源（任意日期/类型）、同节点+日期+类型均无冲突。arXiv规范化覆盖abs/pdf、版本后缀、.pdf、主机及query差异。提案内部17组来源/日期/类型键唯一。所有node_ids有效、source_check_refs指针有效、raw_date_fields与输入逐项匹配。该检查不是对所有措辞的全局语义去重承诺。

## Fix／集成门槛

提案无必须修改项。当前canonical `scripts/build.py:EVENT_TYPES` 与 `web/app.js:eventLabels` 尚不包含 **paper_revision**、**platform_migration**。合并前必须显式扩展schema、中文标签、筛选及回归测试；不可假装成paper_submission或benchmark_release。提案已正确注明此要求。

149→166仅为在当前无冲突基线上接受全部提案后的算术预测，不是当前已发布事件数。合并前应复查最新基线。

## 哈希与权限

`audit.json`包含17条逐事件accept/unknown、精确输入SHA-256及冲突结果。审查前后提案、媒体包、canonical、集成候选输入哈希均一致。未执行提案extract.py，未改提案或canonical，未进行评测或模型/SDK执行。
