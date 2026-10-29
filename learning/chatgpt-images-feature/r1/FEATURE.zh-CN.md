# ChatGPT 网页图片创建与编辑

这是**应用中的图片功能**，不是独立基础模型或开源权重。它适合用文字描述生成图片，或附上已有图片，说明要修改什么、保留什么；提供参考图分析，不等于已经生成编辑结果。[官方网页功能说明](https://learn.chatgpt.com/docs/image-generation)；[图片输入说明](https://learn.chatgpt.com/docs/image-inputs)

## 能做什么、怎么开始

在已有可用ChatGPT账户的网页对话中，附上有权使用的图片并描述目标。对于海报局部修改，可以只请求改时间，同时列出不能变化的文字与布局；如果页面提供选区，可用它指出区域，但不能把选区当作像素锁。[图片编辑帮助](https://help.openai.com/en/articles/11084440-images-in-chatgpt)

前提是账户、套餐、工作区与地区支持该功能，且当前额度允许。图片上传与创建可能分别受限；达到上限即停，不承诺固定免费次数，不采用API价格或Codex额度倍率计算网页费用。使用前自行核对[额度说明](https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq)与[支持地区](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries)。这不是所有中文读者默认可用的路线。

## 必须知道的局限

- 选区可能不精确，修改可能扩展到区外。保留原图，逐项比较真实输出，不能只信助手说“其余不变”。
- 指定宽高、颜色值和文字，不等于得到精确尺寸、品牌色或逐像素不变的保证。需要自行测量和核验。
- 未证实这条网页路线会返回可编辑文字层、SVG/PSD原生图层，不能把一张PNG当作原生设计工程。
- 生产关键文字应逐字复核；严格印刷或品牌交付需额外检查。上述是验收边界，不是宣称产品一定失败。[编辑风险](https://help.openai.com/en/articles/11084440-images-in-chatgpt)；[官方审稿建议](https://learn.chatgpt.com/docs/image-generation)

## 不要把网页功能和API型号混为一谈

ModelAtlas已有 `GPT-Image-2.5 Sunburst` 托管API目录记录；[API型号页](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)支持其文字/图片输入与图片输出，但**没有据此确认本次ChatGPT网页使用的具体底层型号**。同一官方Learn页里的Codex/CLI型号和用量语境，也不能自动移植给网页。

本条目核验到的是2026-10-29官方文档仍描述的网页功能，不是实际账户可用性测试。精确底层型号、首次功能发布日期、架构与权重开放日期均保持未知；不以页面相对更新时间或API快照编号猜日期。

## 对应练习

AgentWork `poster-change-time`：只改海报活动时间，核对其他内容不变。它与本功能是**编辑学习关系**，不是实测成功或API兼容证明。教材使用PNG原创素材，不需API密钥、MCP或额外Skill；严格不变量仍需人工验收。

本稿是待接纳的条目提案，未加入现行数据。网页能力与API型号页为本轮直接阅读；选区风险、额度与地区依据复用同日已QA海报教材的官方帮助来源记录，未把复用记成再次实跑或新抓取。
