# 媒体评测时间轴只读衔接提案

仅从已审核本地研究JSON提取，不访问网页、不改候选或canonical。准备日2026-10-28不是事件日期。

## 17个建议事件

10个论文首次提交、5个末次已核验论文修订、1个DPG-Bench发布、1个MMAU test平台迁移公告。MMAU共享论文只建1事件关联2节点。所有精度为day，时区保留未知。

| 日期 | 类型 | 论文/事件 | 关联节点 | 证据 |
|---|---|---|---|---|
| 2017-06-26 | paper_submission | 1706.08500 论文首次提交 | metric-fid-original | [一手来源](https://arxiv.org/abs/1706.08500)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2018-01-12 | paper_revision | 1706.08500 论文末次已核验修订 | metric-fid-original | [一手来源](https://arxiv.org/abs/1706.08500)；arXiv abstract 页面 last revised 与 Submission history 最后一条；仅所审核快照的末次修订 |
| 2018-12-03 | paper_submission | 1812.01717 论文首次提交 | metric-fvd-original | [一手来源](https://arxiv.org/abs/1812.01717)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2018-12-20 | paper_submission | 1812.08466 论文首次提交 | metric-fad-original | [一手来源](https://arxiv.org/abs/1812.08466)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2019-01-17 | paper_revision | 1812.08466 论文末次已核验修订 | metric-fad-original | [一手来源](https://arxiv.org/abs/1812.08466)；arXiv abstract 页面 last revised 与 Submission history 最后一条；仅所审核快照的末次修订 |
| 2019-03-27 | paper_revision | 1812.01717 论文末次已核验修订 | metric-fvd-original | [一手来源](https://arxiv.org/abs/1812.01717)；arXiv abstract 页面 last revised 与 Submission history 最后一条；仅所审核快照的末次修订 |
| 2023-01-26 | paper_submission | 2301.11325 论文首次提交 | data-musiccaps-original | [一手来源](https://arxiv.org/abs/2301.11325)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2023-10-17 | paper_submission | 2310.11513 论文首次提交 | bench-geneval-original | [一手来源](https://arxiv.org/abs/2310.11513)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2023-11-29 | paper_submission | 2311.17982 论文首次提交 | bench-vbench-original | [一手来源](https://arxiv.org/abs/2311.17982)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2024-03-08 | paper_submission | 2403.05135 论文首次提交 | bench-dpg-bench-original | [一手来源](https://arxiv.org/abs/2403.05135)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2024-03-11 | benchmark_release | DPG-Bench 官方发布公告 | bench-dpg-bench-original | [一手来源](https://github.com/TencentQQGYLab/ELLA)；ELLA README → Changelog，2024.3.11 条目明确 Release DPG-Bench |
| 2024-06-23 | paper_submission | 2406.16020 论文首次提交 | harness-audiobench | [一手来源](https://arxiv.org/abs/2406.16020)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2024-10-24 | paper_submission | 2410.19168 论文首次提交 | bench-mmau-v051525-test-mini, bench-mmau-v051525-test | [一手来源](https://arxiv.org/abs/2410.19168)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2025-03-27 | paper_submission | 2503.21755 论文首次提交 | bench-vbench-2-0 | [一手来源](https://arxiv.org/abs/2503.21755)；arXiv abstract 页面标题上方 Submitted on；Submission history [v1] |
| 2025-05-06 | paper_revision | 2406.16020 论文末次已核验修订 | harness-audiobench | [一手来源](https://arxiv.org/abs/2406.16020)；arXiv abstract 页面 last revised 与 Submission history 最后一条；仅所审核快照的末次修订 |
| 2025-08-20 | paper_revision | 2503.21755 论文末次已核验修订 | bench-vbench-2-0 | [一手来源](https://arxiv.org/abs/2503.21755)；arXiv abstract 页面 last revised 与 Submission history 最后一条；仅所审核快照的末次修订 |
| 2026-01-30 | platform_migration | MMAU test 评估入口迁移公告 | bench-mmau-v051525-test | [一手来源](https://github.com/Sakshi113/MMAU)；MMAU README → Announcement，30 Jan 2026；test evaluation moved from Eval.ai to HF Space |

## 合并前边界

- Await root approval and current navigation/media acceptance; no merge performed.
- Add paper_revision and platform_migration as explicit schema/UI/filter labels if accepted; do not silently relabel as paper_submission or benchmark_release.
- Recheck latest baseline for duplicate IDs, paper-source/date/event-type collisions and existing node associations.
- Group shared-paper first submissions/revisions by canonical paper URL, date and event kind; MMAU test-mini/test share one original-paper event.
- MMAU-v05.15.25 node IDs retain current version identity but 2024 paper event is original-paper background, not that later dataset release.
- Keep platform announcement time separate from actual service cutover, and all timezone fields unknown.
- Do not add events for nulls, checked_at, paper same-day duplicate revisions, version-string dates or repository current content.
- If all 17 unique events later accepted against unchanged149 baseline, arithmetic total166 is provisional, not current count.

## 未知与不纳入

- 所有未核验benchmark_release和repository_last_update保持null，逐项见JSON unknown_dates。
- 同一论文的首发/末次修订同日时不另造修订事件，5篇论文共6条记录如此。
- paper_revision/platform_migration不是当前统一时间轴已有枚举，后续必须显式扩展、测试再合并。
- MusicCaps只挂MusicLM论文首发，不把2023-01-26冒充数据集精确发布日。
- 平台迁移是公告日期，不是实测切换时间；不使用已读取入口的Running状态作为时间证据。
- 当前149事件的论文URL未发现重合；这是源URL规范化检查，不是完整语义去重。
- 已阻断/不可提取页面未重访；没有题目、答案、媒体、下载或真实评测。

## 核验

输入研究包、canonical data和候选data的SHA-256均保持不变。17个ID唯一；所有事件指向已审核source_checks条目。proposal.json保存逐事件原始字段、证据位置、精度、未知时区与node_ids。
