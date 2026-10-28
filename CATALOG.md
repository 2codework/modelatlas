# 厂商目录接纳与字段契约

本批 77 **目录记录**（global 40 + Asia 37），不是 77 个新增模型，也不是全世界或任一厂商完整历史清单。厂商覆盖缺口保留在来源包 `coverage_matrix`。历史知识层保持 160 nodes / 118 edges / 153 sources / 87 events（50 有日期、37 未知）；12 MCP 课程和原跨仓库关系未改写。

## 可重现接纳

`data/vendor-catalog/admission.json` 固定输入 SHA-256、最终 disposition 及 Asia 逐条决策 hash。构建失败即停止，不以构建时间刷新核验日期。原始 JSON/Markdown、Asia QA report/dispositions 均按原字节发布到 `docs/vendor-catalog/`。原文件中的 pending、initial_summary 或旧访问失败是**历史记录**，不是最终默认接纳状态。最终 Asia 37 条均 accept_with_caveats；原报告仍保留初审提出过的问题，不抹除审计轨迹。

## 显式映射，不默默丢字段

| 派生字段 | global | Asia |
|---|---|---|
| id | 原 id | SHA-256(provider + entity_type + exactid) 前16位，附 asia- 前缀；不是模型名 |
| exact_id | exact_id（可 null） | exactid |
| entity_type / version | 原字段 | 原字段 |
| provider / family | vendor / 未声明则 null | vendor / family |
| inputs / outputs | modality.input/output | input_modalities/output_modalities |
| modality / lifecycle | 完整原字段 | 完整原字段 |
| status | lifecycle.status | lifecycle.access_status |
| weights_license | weights_license | weights_license 或 official_license |
| code_license | code_license 或 null | repository_code_license 或 null |
| dates | release_date | release_dates（不同事件不合并） |
| checked_at | source_checked_date | sourcecheckdate |
| urls | model_card_url/report_url/tutorial_url/weights_license_url | modelcardURL/paperURL/tutorialURL/official_licenseURL/repositoryURL |
| sources | 按 source_ids 解析本包来源 | 同左（不和另一包同名 source ID 混淆） |
| links | dedup_suggestions → 存在的历史 ID；relations → 唯一同厂商 exact_id | existingIDs → 存在的历史 ID（editorial_related） |
| raw / bundles.raw | **逐字段完整原记录 / 整个来源包** | 同左，含所有许可、证据、限制、大小写、覆盖与历史状态 |

未映射为快捷字段的所有字段仍可全文搜索，并在原记录和同源 BOOK 中完整显示。字段值 null 表示本轮未知/未核验，不表示不存在、闭源或免费。实体类型不归并：family、API alias、fixed API version/snapshot、checkpoint、API service、report 保留各自类型；不从 API 名称推断 pinned。无精确 ID 的 Meta 两个变体按来源标题独立保留，不把两个 null 当同实体。

## 关系与限制

目录是独立图层，不膨胀历史 nodes/edges 计数。只有真实存在的目标才生成可点击边；未解析 target_exact_id 和 dedup 建议保留文本。家族与现有节点关联是编辑导航，不代表身份等同或历史因果。原知识节点有反向目录入口。R1 checkpoint 只关联 `deepseek-r1-2025` paper-v1 锚点，不覆盖或合并。别名与目标记录保持独立。

Qwen2.5-Omni-3B 权重为 qwen-research，限非商用研究/评估；商用须另申请，不继承代码 Apache-2.0。EXAONE 条款 URL 的 404/unknown 保留，名称不是完整法律授权。Kimi 初次失败和 QA 成功分别保存；19:46 的 QA 观察仅精确到分钟，默认派生 sources/access_observations 显示 `2026-10-28T19:46Z` 与 precision；原 `:00` 字节仍留在 raw，不能解释为秒级测量。

默认详情展示最终 disposition、许可分层、限制、修订与访问观察；展开历史原始数据可复核全部字段。没有价格榜、性能排名、服务可用性承诺或模型/SDK执行。官方教程只提供链接，不把链接当执行结果。

## 离线验证

```
python scripts/build.py
python -m unittest discover -s tests
node --test tests/*.test.js
python scripts/check_pages.py
node --check web/app.js
node --check web/catalog.js
```

测试包括 duplicate ID/identity、dangling source/links、无效日期与未知日期、hash gate、URL安全、raw原字节/全字段与BOOK保留、权重/代码许可分离、Kimi分钟精度、组合筛选、大小写全文搜索、深链接、未知ID、重复选择和重置的自编 DOM 渲染模拟。无第三方安装。此 DOM harness 不是浏览器截图 QA；独立真实浏览器检查仍需父任务完成。
