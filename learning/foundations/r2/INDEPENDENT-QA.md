# 六课独立教学与事实QA r1

**结论：ACCEPT（接纳 ai-foundations-starter-r2 为有限基础纸面导读候选）。** 无阻断项。不等于准许发布、许可确认完成、真实新手实测、产品运行或课程全覆盖。验收日期：2026-10-29 UTC。

## 精确接纳对象

- STARTER.md：`6328a792ea280a8c5f6c2d6d6a973b1d5817500660682f6ec127c69598c49926`
- lessons.json：`8c8fe93cac66423d12bea51f03d1e110bd056a8e6f21be79d234cf1b7ada1053`
- source-checks.md：`228004df584d95bbca82a420cf0a07c027d6ac50bd5b7bc55d9fb03bac421834`

本QA独立读取六课全文，核对r1→r2差异、重新计算上述SHA，重新打开官方关键来源，并人工推演每份纸面作答。没有采用作者lint结果代替独立判断。另独立脚本验证六ID唯一、各正文段落在Markdown中保留、6个跳转节点在本地canonical数据存在、纸面范围与答案齐备；见checks.json。没有浏览器操作、模型调用、SDK执行或真实用户测试。

r2相对r1只把第3课例子“三条/三项”改为“两条/两项”，与两条合成事实及两项练习一致；diff命令退出1仅表示存在这一预期差异，不是执行失败。

## 六课逐项教学判定

| 课 | 独立作答与核验 | 判断 |
|---|---|---|
| 1 模型/Agent | 草稿=生成；翻下一页=读取；发送=外部写入，需授权与结果证据；读取亦需授权。解释没有把固定循环一概宣称自主Agent | 可纸面完成，基础定义带行业差异限定，接受 |
| 2 token/上下文 | 100−70−20=10；这不是实际token计量，编码/语言/推理token影响实际限制。材料可容纳与利用准确率不等同 | 输入足够、算术正确；教学格子不迁移为真实接口容量，接受 |
| 3 提示词 | 海报/阿禾/周五；场地建议待办/负责人未注明/日期未注明。缺失不编造；“确定场地”只能是建议而不是已决事实 | r2数量矛盾已修复；答案明确建议性质，接受 |
| 4 RAG | 周四必须基于新版确实适用且可信；否则指出冲突、核实范围，不凭“新”字自动认定权威 | 有固定两份资料且条件答案合理；检索不等于答案忠实，接受 |
| 5 工具/MCP/Skill | 方法/动作/接口分别对应，但方法未必已打包、工具未必MCP；提出调用与执行结果分开 | 概念边界正确，不把Skill和MCP绝对割裂，不迁移协议报文，接受 |
| 6 办公核验 | 椅子/12把/小夏；到场人数建议待办/未定/未注明；问人数；拒绝上传通讯录 | 原文到草稿有可检查映射；恶意内容不转移授权；纸面无副作用，接受 |

所有练习在文字层面都给足输入、行动与判断理由，不必先会Python/JSON或拥有账号。**“可以按文字完成”只是审稿判断，不是已经证明不同真实新手都能独立学会。** 不应把此结论包装成教学效果实验。

## 本轮实际重开来源记录

均于2026-10-29公开读取，无登录/运行。下面记录支持段落与限制；独立教学例子不是官方给出的事实案例。不复制完整来源。滚动页没有明确更新日则保持未知。

1. [Anthropic Building effective agents](https://www.anthropic.com/research/building-effective-agents)，正文What are agents与When (and when not) to use agents，发布2024-12-19，页首明确工具生态已变。支持作者对workflow/agent架构区别及简单起步。短证据：`Workflows are systems where LLMs and tools are orchestrated through predefined code paths.` 限制：不是统一行业定义或最新产品教程。支撑课1/6的架构与渐进学习，不验证本稿合成例子的模型效果。
2. [OpenAI Understanding and counting tokens](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens)，Overview/Distinguish input and output tokens/Stay within model limits。页面显示Updated: 9 days ago，不推算精确日期。短证据：`A token count is not the same as a word count.` 支持编码/语言计数差异和推理token；教学100格算式是原创假设，不是文档容量。
3. [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)，Prompt engineering及Message roles，滚动日未知。短证据：`the content generated from a model is non-deterministic`。支持清晰指令、角色层级与验证需要。检索untrusted未命中；本页不能单独充当完整提示注入防护证据。草稿把“资料不授予权限”作为教学安全规则而非声称已防住模型攻击，故非阻断；未来安全专题应补专门安全来源。
4. [OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)，开篇与Synthesize a response based on results，滚动日未知。短证据：`Retrieval is useful on its own`。支持检索与模型综合回答是两个环节；该服务以向量索引实现，不代表所有RAG必须向量库。通知冲突和证据不足处理是原创编辑推演，不是官方产品实测。
5. [MCP Architecture overview 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)，Scope/Participants/Tool Execution。URL固定版本，不据此推断网页最后更新日。短证据：`MCP focuses solely on the protocol for context exchange`。支持host/client/server及调用交换，不规定应用怎样运用模型。课5仅用概念，不移植其报文至旧版节点，接受。
6. [Agent Skills Overview](https://agentskills.io/home)，What are Agent Skills/How do Agent Skills work，滚动日未知。短证据：`a skill is a folder containing a SKILL.md file`。支持指令包、脚本/参考资料、按需加载；宿主适配不可由“有SKILL.md”推断。课5“通常有”是宽泛教学措辞：若严格指Agent Skills格式则SKILL.md必需；当前不是格式规范教程，非阻断。
7. [OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling)，How it works与The tool calling flow，滚动日未知。短证据：`Execute code on the application side with input from the tool call`。独立补充核验课5“模型提出、应用执行”的表述。模型调用响应与真正操作成功不同；本轮未运行示例。

## 非阻断改进与实施边界

- 课3/6的题目可在下一版增加“为推导出的待办标注建议”字段，使读者先看题就知道区分事实与建议；当前答案已给这个限制，不需要阻断r2。
- 课5“工具调用是应用按约定执行一次操作”是流程层简化；严格API语义下tool call是请求、execution是执行。后句已明确模型提出不等于成功，故不是事实错误；未来可改成“模型提出工具调用请求，由应用决定并执行”。
- 课6明确无真实模型/Agent实测，UI必须保留。纸面六课不能被改名“Agent部署完成”或与MCP规则测试混报。
- 相对根链接 `/modelatlas/?node=...` 只证明目标ID存在于本地数据，尚未验证独立预览部署基路径；实现方须改成正确本地路由或保留明确外链并实测。不能据本QA称链接已浏览器可用。
- Markdown仍写“等待独立QA”，这是被冻结作者快照的历史状态；实施时追加接纳记录指向本报告，不覆盖原始快照来伪造作者当时状态。
- 许可、作者署名、发布与最终UI可访问性仍由相应负责人核验。本QA不重新许可第三方网页。

**冻结信号：上述三文件字节可作为已通过本轮独立内容QA的输入；任何内容改变须重新记录SHA及相应差异复核。**
