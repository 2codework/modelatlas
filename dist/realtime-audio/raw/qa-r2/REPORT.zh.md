# 实时音频研究 r2 最终独立复核

**结论：accept_scoped_research。F01–F06及Moshi日期范围全部闭环，无待修阻断项。** 仅接受四家四模型/家族的有限文档研究；不代表全球模型、历史版本、配图全部齐全，也不授权合入或执行模型。

## 完整性与保全
- r2共18文件，SHA256SUMS覆盖其余17文件且全部通过；清单自身SHA256：`58aa85c48a794e3aa68beab4566f424897381cf1861ee0f27f879f81cc897627`。
- r1全部7文件与before-qa逐字节一致，R1-SHA256记录正确。
- 原20条source-checks全部原样保留（包括1失败、2部分解析）；新增论文HTML及rechecks没有覆写原结果。
- canonical SHA仍为`08b1dc2ab60f1eda3e64a65aee0034487506af8108cf44bfeec98aa8b97ef578`。原研究r1/r2、QA r1与canonical均未修改。

## 修正闭环
| 项目 | 复核结果 |
|---|---|
| F01 | Voxtral论文v2补2026-02-21 00:06:15 UTC；日期证据表与模型字段一致，未当成权重发布。 |
| F02 | BF16/vLLM单GPU>=16GB明确为官方部署条件；绝对最低显存null，未称实测。 |
| F03 | 论文target delay、HF摘要/功能/推荐配置、公告、实际端到端分别登记；无数值不同即矛盾的结论。 |
| F04 | 旧快照+别名的2026-07-20弃用及2027-01-20计划停用不外推2.1；文本输出$16/$24按精确ID分开，单位每百万token。 |
| F05 | GPT-Realtime-2前代列coverage gap，未猜日期；2.1首发null。 |
| F06 | Voxtral协议双向流式true、语音到语音对话false分开，删除泛化full_duplex:false。 |
| Moshi | 家族公告/论文日期与Moshiko BF16变体分开，checkpoint首次上传null。 |

## 逐模型
- Moshi：accept；开放权重许可与代码许可分开，未补猜variant历史。
- CSM 1B：accept；r1字段未改，门控、依赖权限、产品区别及streaming/full-duplex未知继续保留。
- Voxtral Realtime2602：accept；不合并已有Transcribe3，且旧2602接口限制不外推新版。
- GPT-Realtime：accept；按version_records使用生命周期与价格，不可由family日期给2.1推定发布日。

## 官方证据
延用QA r1当日独立核验的官方材料：[论文版本史](https://arxiv.org/abs/2602.11298)、[论文v3 §3.2/4/4.2/4.3/A.2](https://arxiv.org/html/2602.11298v3)、[旧模型卡](https://developers.openai.com/api/docs/models/gpt-realtime)、[2.1模型卡](https://developers.openai.com/api/docs/models/gpt-realtime-2.1)、[弃用公告](https://developers.openai.com/api/docs/deprecations)。

r2新增480ms推荐配置一项已再次独立打开[HF Recommended Settings](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)：480ms推荐、可配置80至1200的80ms倍数与2400单值，符合r2记录；不能自动用论文训练target范围替换此配置范围。

## 保留未知与执行边界
权重实际首次上传、revision锁定、CSM实时双工、完整GPT前代史、最低硬件、端到端测速、账号/地区/权限、配图核验均未被本次验收补齐。没有运行SDK、下载权重、登录、调用模型API、付费或访问设备。公开评测仅元数据/链接，未提取题目。

可重现本地文档断言见verify.py；18项检查全部通过，VALIDATION.json包含r2所有文件hash。网页引用hash沿用QA r1的审计记录（不是远端完整页面/权重hash）。
