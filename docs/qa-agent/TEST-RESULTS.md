# 本地执行记录 / Local execution record

- 日期 / Date: 2026-11-01 UTC.
- 环境 / Environment: cloud Linux, Python 3.12.14, Python standard library only.
- 命令（ModelAtlas 根目录） / Command (ModelAtlas root):

```sh
python -m unittest discover -s tests -p test_qa_agent_lab.py -v
```

**结果 / Result: 33 tests passed.**

覆盖 / Coverage: normal cited answer; Chinese question; no evidence; conflicting sources; bounded timeout; bounded rate limit; transient recovery; invalid arguments; strict schema; untrusted document injection ignored; human denial before read; strict Boolean approval; no automatic human-review retry; human waiting excluded from execution deadline; step budget; cooperative deadline; invalid budget; fabricated citation; unsupported answer; redacted trace; unauthorized tool; final-release denial; required release callback; strict Boolean release approval; no automatic release-review retry; release-review waiting excluded from execution deadline.

命令行额外检查 / Additional CLI checks:

```sh
printf 'yes\nyes\n' | python learning/qa-agent/demo.py
printf 'yes\nno\n' | python learning/qa-agent/demo.py
printf 'no\n' | python learning/qa-agent/demo.py
printf 'yes\n' | python learning/qa-agent/demo.py --question 'What is the budget?'
```

分别得到 / Results respectively: `answered / supported_exact_fact`, `refused / human_release_denied`, `refused / human_denied`, `refused / no_evidence`. The piped inputs simulate confirmation in a test; they are not evidence of authorization for any real service.

这些是确定性离线控制逻辑测试。没有调用模型/API/网络、下载权重、执行真实 RAG、跑基准或验证生产安全；不是全站测试、浏览器测试或上线验收。 / These are deterministic offline controller tests. No model/API/network call, weights download, real RAG, benchmark, or production security verification occurred; this is not a full-site test, browser test, or deployment acceptance.

## 追加合同回归 / Added contract regressions

2026-11-01：冻结 compose 前证据，隔离每次尝试的列表与 Claim 对象，拒绝嵌套可变字段，隔离发布审核与适配器输出；校验 deadline 类型、有限性与范围。新增 7 项回归通过（包括多个表驱动非法值）。这是模拟合同修复，不是生产安全认证。 / Evidence is frozen before compose; each attempt receives isolated list and Claim objects; mutable nested fields are rejected; release review and adapter output are detached. Deadline type, finiteness and range are validated. Seven additional regression tests passed, including table-driven invalid values. This is a simulation-contract fix, not production security certification.
