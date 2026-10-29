# r2差异复核补记

**ACCEPT：三项修正全部通过。**

- 18来源记录＝17可读＋1历史失败，REPORT和JSON计数一致。
- 24日期槽位＝15已知＋9unknown，原24条事件逐项未改。
- FastVLM许可已把产品开发列为独立排除项，正文、候选及来源摘要一致。

18条来源ID、URL、状态未改；除上述许可摘要和新增计数外research.json内容完全一致。r1所有文件hash保持；r2清单9/9通过。canonical HEAD仍为`11c74bc780688f4c489e710404e52789fe4a10b4`。未重新联网、未改候选/canonical，待UI冻结后另行决定集成。

r2最终绑定：
- research.json SHA256：`0d42b558e49640d5b0aa6f142e08956b820edcb698baafb154332f2da9a1c0a5`
- REPORT.zh.md SHA256：`036b1533aad3f97b860e01c980d63bb8dbec839bec0134e9ba010c16cb9d359e`
- SHA256SUMS SHA256：`ff1492eed42dbc9a32ce341d49c0ef05e83a208607027514f7725550f48b3426`

全文件hash及检查详情见R2-ADDENDUM.json。此补记不更改原QA SHA256SUMS，另附R2-ADDENDUM.SHA256SUMS。
