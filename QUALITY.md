# 质量与验证边界

内容核验日期：2026-10-28。

- 核心知识图谱、事件与厂商目录分别计数；实际规模以同源 `data.json`（发布于 `docs/data.json`）及 `VALIDATION.json` 为准。厂商目录记录不等于新增模型数量，别名、家族、服务、权重与报告不自动合并。
- 保留创作专题、AgentWork 实践交叉链接与历史自报成绩快照；覆盖是代表性的，非全球或任一厂商全量历史，不提供全球排行或完整覆盖承诺。
- 包含原创 MCP 离线课程与自编模拟验证；离线练习不是真实 MCP SDK、外部服务或模型实测。
- 原研究输入完整保留；日期覆盖层只更新已存在事件，核对原值后再合并。
- BLOOM API首发未知；截至2022-07-12可用的观察单列，不放入已知首发时间轴。
- GPT-3 private beta和Gemini Vertex AI Preview不等同GA。未知时区不补造。

## 可重复检查

```sh
python scripts/build.py
python -m unittest discover -s tests -v
find web tests -name '*.js' -print0 | xargs -0 -n 1 node --check
node --test tests/*.test.js
python scripts/check_pages.py
```

实际运行结果与文件哈希见 `VALIDATION.json`。历史 `VALIDATION.r1.json` 仅描述原始版本，不代表当前版本验证。

## 验证边界

自动化校验不替代真实浏览器视觉、移动端、键盘、屏幕阅读器与真实存储行为验收。没有执行模型、外部教程命令、付费API或独立复现实验；未验证所有外链当前HTTP状态，未做完整法律或安全审计。

浏览器检查应覆盖组合筛选/重置/空结果、事件类型与未知事件、节点反复切换、进度刷新/损坏导入/重复导入/导出回读/localStorage禁用、项目子路径资源与CSP。
