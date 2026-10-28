# Asia independent QA — 2026-10-28

## 修订复核结论（19:49 UTC）

候选已修订并独立复核：**37 accept_with_caveats、0 hold、0 blocking revise**。JSON SHA256 `0992a408fe836216597e00b6a1ff9bf76a67562025f385512417cd1bc6914aa7`。Omni权重许可与代码许可正确分离；Kimi新证据与历史失败分开；R1不再自动合并paper锚点；EXAONE明确条文unknown。原审结论留存如下，不代表修订后仍阻断。Kimi完整命名空间为可选规范化建议，短名+vendor已唯一；QA访问时间仅确认分钟，补零:00不应被解释为秒精度。API alias通用去重文案仍应在导入映射时按entity_type处理，不能产生额外训练模型。

## 初审结论先行
**不能原样全量并入：1 hold、3 revise、33 accept_with_caveats。** 37个唯一record、33模型/具名变体+4 API alias、12发布组织、CN/IN/KR/JP计数正确。15个source_ids全部解析，所有existingIDs实际存在。仅检查目录证据，未下载权重/运行SDK/API/教程；无远端、账号或原始文件变更。

### 必须修复
1. **Qwen2.5-Omni-3B权重许可错误（hold）**。[官方模型卡](https://huggingface.co/Qwen/Qwen2.5-Omni-3B)标qwen-research；[具体LICENSE](https://huggingface.co/Qwen/Qwen2.5-Omni-3B/blob/main/LICENSE)第2节限定非商业研究/评估，商业用途另申请。不是Apache-2.0。许可证模板日期2024-09-19不是模型发布日期。
2. **Kimi两record需更新当前证据和checkpoint规范ID（revise）**：本次实际打开[Base](https://huggingface.co/moonshotai/Kimi-K2-Base)、[Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct)，均可读，支持text-generation/modified-mit。原作者不可访问是历史观察，不能假称其当时已验证，也不能把历史故障泛化为当前故障。建议exactid加`moonshotai/`、原短名保留alias；[官方repo](https://github.com/MoonshotAI/Kimi-K2)也支持两变体及Modified MIT。
3. **DeepSeek-R1自动并入建议需改（revise）**：现图谱`deepseek-r1-2025`的version为`original paper v1; not later checkpoint`，date_kind为paper_first_submitted。它虽类型写model_release，实际证据是原始报告锚点。不能直接把checkpoint覆盖进报告节点或把2025-01-22移作weights日期。可显式关联；若整合，先做实体类型决策。

### 高风险核验通过但保留限定
- [DeepSeek当前官方API表](https://api-docs.deepseek.com/quick_start/pricing/)：Flash→V4.1-Flash-1017、Pro→V4-Pro-0813；两个legacy Flash请求名仍接受，底层原模型退役且重定向。不能用旧知识反驳新docs。通用dedup文案“新增精确版本”应改alias映射；三Flash名共享快照，非三个独立模型。未执行请求，不声称runtime实测。
- [GLM正文](https://github.com/zai-org/GLM-4.5)明确4.5/Air权重MIT，仓库代码标签Apache不能替代。
- [EXAONE模型卡](https://huggingface.co/LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct)支持NC许可名称；点击其[条文链接](https://huggingface.co/LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct/tree/main/LICENSE)本次404。完整条文仍unknown，不推断商业允许，不需删除已支持的NC名称。
- [ERNIE表](https://github.com/PaddlePaddle/ERNIE)支持十具名变体、VL text/image/video→text、其他text→text及Apache权重声明。ERNIEKit/FastDeploy是工具。named_model_variant尚不等于已核对每个分发checkpoint。
- [Seed-Coder](https://github.com/ByteDance-Seed/Seed-Coder)三变体存在，Doubao-Coder只是旧名。bf16另有artifact不代表同一语义模型另计。
- [HunyuanVideo许可](https://github.com/Tencent-Hunyuan/HunyuanVideo/blob/main/LICENSE.txt)为自定义社区协议，有限制（包括地域），不可叫无条件开源。误探无扩展名/LICENSE为404，随后按照repo实际列出的/LICENSE.txt读取成功；原record链接本身正确。

## 全部非null日期核验
日期仅day精度，无时区/时刻推断；其余null原样保留。

|record|字段/日期|实际读取证据|
|---|---|---|
|Seed-Coder Base/Instruct/Reasoning（3）|announced 2025-05-08|[News 2025/05/08 release](https://github.com/ByteDance-Seed/Seed-Coder)|
|HunyuanVideo|weights_released 2024-12-03|[News Dec 3 model weights](https://github.com/Tencent-Hunyuan/HunyuanVideo)|
|Qwen2.5-Omni-3B|weights_released 2025-04-30|[News 3B release/download](https://github.com/QwenLM/Qwen2.5-Omni)|
|Qwen-Image|weights_released 2025-08-04|[News weights](https://github.com/QwenLM/Qwen-Image)|
|Qwen-Image-2512|weights_released 2025-12-31|[News weights](https://github.com/QwenLM/Qwen-Image)|

## 其他primary实际读取与归属
[Qwen3](https://github.com/QwenLM/Qwen3)：原版0.6B/8B及235B-A22B-Instruct-2507、Apache权重声明；[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)：R1/Zero/Distill型号、MIT与Qwen蒸馏基座Apache区分。
[MiniMax repo](https://github.com/MiniMax-AI/MiniMax-M1)与[40k](https://huggingface.co/MiniMaxAI/MiniMax-M1-40k)/[80k](https://huggingface.co/MiniMaxAI/MiniMax-M1-80k)卡支持独立预算变体及Apache。
[Qwen-Image-2512卡](https://huggingface.co/Qwen/Qwen-Image-2512)也确认text-to-image/Apache，不混Edit。
[BGE-M3](https://huggingface.co/BAAI/bge-m3)为MIT文本检索模型，dense/sparse/multi-vector输出支持。
[Sarvam-M卡](https://huggingface.co/sarvamai/sarvam-m)明确Mistral-Small后训练text-only/Apache；[Sarvam about-us](https://www.sarvam.ai/about-us)支持印度组织归属，不能据此把基座发明归印度。
[LLM-jp卡](https://huggingface.co/llm-jp/llm-jp-3-3.7b-instruct)指向NII，Apache与日英文本；[NII地址](https://www.nii.ac.jp/en/about/access/)确认Tokyo。
[LG官方组织页面](https://www.lgresearch.ai/about/mission)及其官方搜索结果LOCATION支持韩国并存在美国研究中心；country仅发布组织归属，不代表所有作者国籍或训练地点。

## 图谱与范围
读取`github-migration-r1/public/modelatlas/dist/data.json` v0.2.2。qwen/deepseek/sarvam是家族，org-qwen/org-deepseek是组织，均不能被checkpoint覆盖。Sarvam-M不同于既有Sarvam-1锚点。对其他厂商型号关键词检索未发现既有版本节点；每条disposition记录source_ids解析、唯一性、existingIDs与节点类型。

源md和json数量、范围、主要警示一致；但md当前“ Kimi不可访问”须改为带时间的历史缺口。本批并非完整亚洲或全球、也非各家最新全版本。现官网可见更多GLM/Qwen/ERNIE等版本只证明覆盖不全，不构成本次已验record错误。论文链接不是全文审核；未逐一独立打开所有paper或所有低风险checkpoint卡，不将其标为全文/逐artifact通过。

## 访问结果与边界
完成全部15个primary来源打开与指定高风险claim检查，7个非null日期检查。EXAONE条文404保留unknown；最初Sarvam `/about`、LG `/about`工具不可读，使用搜索发现实际官方`/about-us`与`/about/mission`并读取。无权限拒绝或待审批操作，无绕过。Kimi本轮无访问失败。所有未支持claim维持unknown，不从ID日期推导。

逐record机器可读结果：`dispositions.json`。原输入未编辑。
