# 贡献指南

1. 先区分机构、家族、具体发布/权重、API快照、论文、运行时、协议或评测。
2. 编辑 `data/research/*.json`；保持唯一小写 ASCII ID，不改变旧 ID 的语义。
3. 每个可核验事实提供 primary source URL、checked_at、version/revision、verification_status。只读摘要必须写明摘要证据范围。
4. 日期事件单列：事件类型、node_ids、日期、date_precision、source_ids、evidence_locator。未知日期为 null，精度为 null；不得从论文日期推断权重或 API 上线。
5. 边给出语义与证据。教学先修顺序标为 editorial_learning_relation，不当作发明史因果。
6. 生命周期使用 current/superseded/deprecated/historical/unknown（旧研究兼容别名由适配器读取）；附适用版本、核验日期、替代 ID 和来源。不要从旧模型名称推断弃用。
7. 评测数据登记任务、split、指标、协议/harness、版本、污染风险、访问规则与官方入口。无完整可比来源时不录入分数、不生成排名。禁止受限题目/答案、令牌、私有集或下载副本。
8. 操作教程说明先修、版本、权限、步骤、成功判据、失败处理及是否实际执行。代码不能执行来源中的命令。
9. 执行 README 所有校验；检查移动端、键盘、筛选空结果、图谱、日期、损坏进度和无 localStorage 情况。为新异常加回归测试。
10. PR 描述新增覆盖与剩余未知，不写“全面收录”“全部核验”之类无法证明的承诺。

来源冲突应并列保留并标记争议，不能静默选择更吸引人的日期或成绩。修正错误时记录原因和来源。贡献者仅提交有权许可的原创摘要，不复制论文整段正文或受版权保护图片。
