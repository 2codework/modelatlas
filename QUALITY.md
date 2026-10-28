# v0.2.2 质量与验证边界

内容核验日期：2026-10-28。

- 148 节点、98 关联、138 来源、87 事件（50 有日期，37 日期未知）。
- 保留创作专题与 AgentWork 实践交叉链接，以及3条历史自报成绩快照；不提供全球排行或完整覆盖承诺。
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
