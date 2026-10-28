# ModelAtlas · 大模型知识地图

> v0.2.2 · 代表性知识地图；不是全厂商、全版本目录。最后核验：2026-10-28。来源核验不是独立复现实验。

## 阅读路径

### 从语言到模型
编辑建议的学习顺序，不是历史因果关系。
nlp → tokenization → embeddings → language-modeling → seq2seq → attention → transformer → pretraining → bert → gpt-3

### 从对齐到智能体
编辑建议的学习顺序，不是历史因果关系。
instruction-tuning → rlhf → dpo → cot → reasoning-models → rag → agents → react

### 研究边界与阅读素养
编辑建议的学习顺序，不是历史因果关系。
multimodal → clip → llava → latent-diffusion → rsi → godel-machine → stop → jev

### 从模型卡到本地推理验收
记录精确模型revision、格式、模板、质量样例、延迟与硬件；不要混报运行时结果。
sys-modelpath → sys-gguf → sys-llamacpp → sys-mlx

### 从语料到可追溯RAG
以自有/获授权小语料完成权限过滤、检索召回、引用忠实和删除测试；不要求下载FineWeb。
sys-fineweb → sys-vectorsearch → sys-pgvector → sys-rag → sys-memory

### 从提示契约到受控coding agent
任务、权限、工具日志、补丁、测试和预算齐全；未经批准不执行外部副作用。
sys-promptcontracts → sys-skills → sys-mcp → sys-miniagent → sys-swebench

## Figma MCP设计上下文与写画布

供外部agent读取设计结构并执行受控写入的接口，不是独立模型。

- ID / 类型：design-figma-mcp / tool_interface
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'rolling remote MCP; write beta', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-figma', 'design-src-figma-access']}
- 版本：rolling remote MCP; write beta
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[预约界面从需求到可验收原型](https://2codework.github.io/agentwork/?case=design-ui-flow)
- 对应实践（编辑学习关系）：[组件感知的设计到代码交接](https://2codework.github.io/agentwork/?case=design-design-code)
- license：{'status': 'source_reviewed', 'details': 'proprietary service; complete contractual license unknown'}
- cost：{'status': 'partially_verified', 'details': '部分写入beta免费，正式计费将变化；草稿外写入有Full seat条件，具体额度unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：MCP工具可用不代表批准改写全部设计文件。
- 来源：https://developers.figma.com/docs/figma-mcp-server/
- 来源：https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/

## Firefly图像生成与编辑

图像能力服务；agent负责选择输入、检查约束与失败恢复。

- ID / 类型：design-firefly-image / model_service
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'Image5 / rolling API', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-firefly', 'design-src-adobe-rights']}
- 版本：Image5 / rolling API
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[虚构品牌视觉方向与权利清单](https://2codework.github.io/agentwork/?case=design-brand-kit)
- 对应实践（编辑学习关系）：[产品合成背景与保真验收](https://2codework.github.io/agentwork/?case=design-product-composite)
- 对应实践（编辑学习关系）：[局部图像修补与非目标区保护](https://2codework.github.io/agentwork/?case=design-image-repair)
- license：{'status': 'source_reviewed', 'details': 'proprietary; output rights depend on applicable terms'}
- cost：{'status': 'partially_verified', 'details': '商业API计费与合同unknown；本轮零调用', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：生成的产品外观与字样需要人工验证，不能直接当实拍。
- 来源：https://developer.adobe.com/firefly-services/docs/firefly-api/
- 来源：https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html

## Photoshop API v2确定性编辑编排

模板、图层及智能对象工作流的服务节点；不是全部操作都由生成模型完成。

- ID / 类型：design-photoshop-v2 / tool_service
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'v2 GA', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-photoshop', 'design-src-ps-migration']}
- 版本：v2 GA
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[产品合成背景与保真验收](https://2codework.github.io/agentwork/?case=design-product-composite)
- 对应实践（编辑学习关系）：[局部图像修补与非目标区保护](https://2codework.github.io/agentwork/?case=design-image-repair)
- 对应实践（编辑学习关系）：[历史PSD批处理到v2迁移练习](https://2codework.github.io/agentwork/?case=design-ps-legacy-migrate)
- license：{'status': 'source_reviewed', 'details': 'proprietary service; complete license unknown'}
- cost：{'status': 'partially_verified', 'details': '商业服务合同与单价unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：linked资源失效会破坏模板，不能只保存PSD而忽略依赖。
- 来源：https://developer.adobe.com/firefly-services/docs/photoshop/
- 来源：https://developer.adobe.com/firefly-services/docs/photoshop/guides/

## Photoshop API v1历史工作流

保留旧模板和接口迁移知识，不作为新接入首选。

- ID / 类型：design-photoshop-v1 / historical_tool
- 生命周期：{'status': 'deprecated', 'as_of': '2026-10-28', 'applicable_version': 'v1 deprecated; announced EOL 2026-07-31', 'replacement_node_ids': ['design-photoshop-v2'], 'note_zh': '核验日已过官方EOL日期；仅历史迁移参考，不测试服务响应。', 'source_ids': ['design-src-ps-migration', 'design-src-ps-eol']}
- 版本：v1 deprecated; announced EOL 2026-07-31
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[历史PSD批处理到v2迁移练习](https://2codework.github.io/agentwork/?case=design-ps-legacy-migrate)
- license：{'status': 'unknown', 'details': 'unknown'}
- cost：{'status': 'partially_verified', 'details': '历史合同unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：不能把旧教程原样用于v2。
- 来源：https://developer.adobe.com/firefly-services/docs/photoshop/guides/
- 来源：https://developer.adobe.com/firefly-services/docs/photoshop/getting-started/deprecation-announcement/

## Canva模板数据填充与导出

结构化模板自动化；内容规划和审校是agent层职责。

- ID / 类型：design-canva-template / tool_service
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'unified SDK / REST rolling docs', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-canva', 'design-src-canva-autofill', 'design-src-canva-rights']}
- 版本：unified SDK / REST rolling docs
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[虚构品牌视觉方向与权利清单](https://2codework.github.io/agentwork/?case=design-brand-kit)
- 对应实践（编辑学习关系）：[多语种海报变体与模板填充](https://2codework.github.io/agentwork/?case=design-poster-localize)
- 对应实践（编辑学习关系）：[资产权利与内容凭证交付](https://2codework.github.io/agentwork/?case=design-asset-provenance)
- license：{'status': 'source_reviewed', 'details': 'Canva content license by asset category; API terms unknown'}
- cost：{'status': 'partially_verified', 'details': '账号、模板资格、商业计划与单价unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：设计导出成功不代表每种素材都能再分发或用于logo。
- 来源：https://www.canva.dev/docs/apps/rest-apis/
- 来源：https://www.canva.dev/docs/apps/rest-apis/autofill-guide/
- 来源：https://www.canva.com/policies/content-license-agreement/

## DTCG设计token交换

跨设计工具与代码的语义变量交换；不是模型或agent。

- ID / 类型：design-dtcg / specification
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '2025.10 final', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-tokens', 'design-src-tokens-draft']}
- 版本：2025.10 final
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[品牌token规范化与双主题](https://2codework.github.io/agentwork/?case=design-tokens-migration)
- license：{'status': 'source_reviewed', 'details': 'W3C Community Final Specification Agreement; not W3C Standard'}
- cost：{'status': 'partially_verified', 'details': '公开阅读；工程集成成本unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：旧draft URL会漂移，不可当稳定实现契约。
- 来源：https://www.designtokens.org/TR/2025.10/format/
- 来源：https://www.designtokens.org/tr/drafts/format/

## WCAG 2.2验收标准

界面验收约束；模型可以辅助发现问题而不能认证合规。

- ID / 类型：design-wcag / standard
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'WCAG 2.2 Recommendation 2024-12-12', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-wcag']}
- 版本：WCAG 2.2 Recommendation 2024-12-12
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[预约界面从需求到可验收原型](https://2codework.github.io/agentwork/?case=design-ui-flow)
- 对应实践（编辑学习关系）：[品牌token规范化与双主题](https://2codework.github.io/agentwork/?case=design-tokens-migration)
- 对应实践（编辑学习关系）：[表单可访问性审校](https://2codework.github.io/agentwork/?case=design-a11y-audit)
- 对应实践（编辑学习关系）：[从事实表到可编辑演示](https://2codework.github.io/agentwork/?case=design-slides-story)
- license：{'status': 'source_reviewed', 'details': 'W3C document rules; not asset license'}
- cost：{'status': 'partially_verified', 'details': '公开阅读；审计人力成本unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：无自动错误不等于完整通过，仍需键盘和辅助技术检查。
- 来源：https://www.w3.org/TR/WCAG22/

## Inkscape位图描摹

经典矢量化流程，可被agent安排但本身无自主规划。

- ID / 类型：design-inkscape-trace / ordinary_tool
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'guide 1.3; installed version unknown', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-inkscape']}
- 版本：guide 1.3; installed version unknown
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[经典剪影矢量化与节点清理](https://2codework.github.io/agentwork/?case=design-vector-trace)
- license：{'status': 'unknown', 'details': 'unknown'}
- cost：{'status': 'partially_verified', 'details': '本轮未安装；发布包费用unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：描摹不是原始曲线恢复，复杂照片不适合直接转logo。
- 来源：https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html

## Google Slides结构化排版

把批准内容写入可编辑页面元素；API不是审美决策模型。

- ID / 类型：design-slides-api / tool_interface
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'API v1', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-slides']}
- 版本：API v1
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[从事实表到可编辑演示](https://2codework.github.io/agentwork/?case=design-slides-story)
- license：{'status': 'source_reviewed', 'details': 'proprietary service; asset rights separate'}
- cost：{'status': 'partially_verified', 'details': '配额、账号与收费unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：文本框写入成功不表示无溢出，必须检查渲染结果。
- 来源：https://developers.google.com/workspace/slides/api/guides/overview

## Playwright视觉回归

基线截图对比帮助检测布局变化，不负责定义哪版更好。

- ID / 类型：design-visual-regression / evaluation_tool
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'rolling docs; release unknown', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-playwright', 'design-src-pw-license']}
- 版本：rolling docs; release unknown
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[组件感知的设计到代码交接](https://2codework.github.io/agentwork/?case=design-design-code)
- 对应实践（编辑学习关系）：[响应式视觉回归与差异分流](https://2codework.github.io/agentwork/?case=design-visual-qa)
- license：{'status': 'source_reviewed', 'details': 'Apache-2.0'}
- cost：{'status': 'partially_verified', 'details': 'Apache-2.0软件；CI/浏览器运行成本unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：不得用自动更新基线掩盖缺陷。
- 来源：https://playwright.dev/docs/test-snapshots
- 来源：https://github.com/microsoft/playwright/blob/main/LICENSE

## Storybook组件可访问性检查

在组件状态中检查可访问性问题，结合手工状态覆盖。

- ID / 类型：design-storybook-a11y / evaluation_tool
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': 'docs 10.6', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-storybook', 'design-src-sb-license']}
- 版本：docs 10.6
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[表单可访问性审校](https://2codework.github.io/agentwork/?case=design-a11y-audit)
- license：{'status': 'source_reviewed', 'details': 'MIT'}
- cost：{'status': 'partially_verified', 'details': 'MIT软件；托管增值服务价格unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：默认状态通过不代表弹窗、错误态、加载态通过。
- 来源：https://storybook.js.org/docs/writing-tests/accessibility-testing
- 来源：https://github.com/storybookjs/storybook/blob/next/LICENSE

## C2PA素材来源链

记录可验证来源与编辑声明，辅助资产交付审计。

- ID / 类型：design-c2pa / specification
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '2.5 October 2026', 'replacement_node_ids': [], 'note_zh': '文档状态不等于运行验证；具体账号与版本另验。', 'source_ids': ['design-src-c2pa']}
- 版本：2.5 October 2026
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[资产权利与内容凭证交付](https://2codework.github.io/agentwork/?case=design-asset-provenance)
- license：{'status': 'source_reviewed', 'details': '规范条款与实现许可分开; exact implementation license unknown'}
- cost：{'status': 'partially_verified', 'details': '公开规范；签名证书/服务成本unknown', 'exact_price': 'unknown'}
- 学习步骤（未执行）：固定输入、权限与版本
- 学习步骤（未执行）：草稿生成后按案例rubric检查
- 学习步骤（未执行）：保留原件、差异与失败记录
- 注意：凭证缺失不自动等于伪造；签名有效不等于版权可用。
- 注意：来源凭证本身不能证明内容真实、准确或符合事实。
- 来源：https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html
- 来源：https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html

## MusicGen v1

离散音频 token 自回归音乐生成，学习文本和旋律条件。

- ID / 类型：music-musicgen / model
- 生命周期：historical
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[无歌词配乐草图](https://2codework.github.io/agentwork/?case=music-musicgen-sketch)
- license：代码 MIT / 权重 CC-BY-NC 4.0；仅按许可允许的非商业研究使用
- license_notes：代码 MIT / 权重 CC-BY-NC 4.0；仅按许可允许的非商业研究使用
- historical_context：固定旧版用于理解方法；不因过时删除
- 来源：https://github.com/facebookresearch/audiocraft/blob/main/model_cards/MUSICGEN_MODEL_CARD.md

## JASCO v1

Flow Matching 加入时间局部和弦、鼓与旋律控制。

- ID / 类型：music-jasco / model
- 生命周期：historical
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[和弦与节奏约束编曲](https://2codework.github.io/agentwork/?case=music-jasco-arrangement)
- license：代码 MIT / 权重 CC-BY-NC 4.0
- license_notes：代码 MIT / 权重 CC-BY-NC 4.0
- historical_context：固定旧版用于理解方法；不因过时删除
- 来源：https://github.com/facebookresearch/audiocraft/blob/main/docs/JASCO.md
- 来源：https://github.com/facebookresearch/audiocraft/blob/main/model_cards/JASCO_MODEL_CARD.md

## Stable Audio Open 1.0

开放权重音效与音频生成；不等同于当前云服务版本。

- ID / 类型：music-stable-audio-open / model
- 生命周期：historical
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- license：Stable Audio Open 1.0 的 LICENSE.md 标 2024-07-05 Community License；商业使用须注册，关联实体合计年收入超过 100 万美元触发另行许可要求；分发有归属声明等义务。仍需就具体部署完整审阅，不是无条件商用。
- license_notes：Stable Audio Open 1.0 的 LICENSE.md 标 2024-07-05 Community License；商业使用须注册，关联实体合计年收入超过 100 万美元触发另行许可要求；分发有归属声明等义务。仍需就具体部署完整审阅，不是无条件商用。
- historical_context：固定旧版用于理解方法；不因过时删除
- 来源：https://stability.ai/news-updates/stable-audio-open-research-paper
- 来源：https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md

## HTDemucs v4

波形/频谱混合模型分离人声、鼓、贝斯及其他。

- ID / 类型：music-demucs / model
- 生命周期：historical
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[原创混合音轨分轨诊断](https://2codework.github.io/agentwork/?case=music-stem-separation)
- license：需复核模型与依赖许可；分轨不消除原曲权利
- license_notes：需复核模型与依赖许可；分轨不消除原曲权利
- historical_context：固定旧版用于理解方法；不因过时删除
- 来源：https://github.com/facebookresearch/demucs

## Whisper

多语种 ASR、语音翻译与语言识别。

- ID / 类型：music-whisper / model
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[Whisper 离线转写与人工校对](https://2codework.github.io/agentwork/?case=music-speech-transcript)
- license：代码与权重 MIT；语料录音仍需同意
- license_notes：代码与权重 MIT；语料录音仍需同意
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://github.com/openai/whisper

## gpt-4o-transcribe-diarize

说话人标签转写的旧 API 专用模型。

- ID / 类型：music-diarize / model
- 生命周期：deprecated
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[旧说话人分离接口迁移审阅](https://2codework.github.io/agentwork/?case=music-diarization-migrate)
- license：API 计费；上传前取得录音/数据处理许可
- license_notes：API 计费；上传前取得录音/数据处理许可
- historical_context：固定旧版用于理解方法；不因过时删除
- 来源：https://developers.openai.com/api/docs/guides/speech-to-text

## Lyria 3.5 / Clip

Gemini API 音乐生成；Clip 预览与完整歌曲模型区分。

- ID / 类型：music-lyria / model
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[原创歌词到完整歌曲结构](https://2codework.github.io/agentwork/?case=music-lyria-song)
- license：云 API 额度与服务条款；输出权利不等于版权登记保证
- license_notes：云 API 额度与服务条款；输出权利不等于版权登记保证
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://ai.google.dev/gemini-api/docs/music-generation

## Suno generation service

歌曲/歌词/编曲产品入口，底层版本与下载政策需分开记。

- ID / 类型：music-suno / tool
- 生命周期：unknown
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[歌词辅助与发行资格台账](https://2codework.github.io/agentwork/?case=music-suno-lyrics)
- license：付费/免费和生成/下载日期分列，发行前确认现行条款与权益
- license_notes：付费/免费和生成/下载日期分列，发行前确认现行条款与权益
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://www.suno.com/blog/suno-updates-tos
- 来源：https://help.suno.com/en/articles/2410177

## Neutron 5 Mix Assistant

轨道混音建议与处理，供人类监听修改。

- ID / 类型：music-neutron / tool
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[混音助手的 A/B 实验](https://2codework.github.io/agentwork/?case=music-mix-assistant)
- license：商业插件；未购买/未安装；参考素材须有权
- license_notes：商业插件；未购买/未安装；参考素材须有权
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://www.izotope.com/products/neutron/

## Ozone 12 Master Assistant

母带处理建议和信号链，不替代听感判断。

- ID / 类型：music-ozone / tool
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[母带助手不等于一键发布](https://2codework.github.io/agentwork/?case=music-master-assistant)
- license：商业插件；不承诺固定价格；禁止盗版
- license_notes：商业插件；不承诺固定价格；禁止盗版
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://docs.izotope.com/ozone12/en/index-en.html

## Auphonic multitrack

语音多轨自适应后期和混音输出。

- ID / 类型：music-auphonic / tool
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[双主持播客多轨后期](https://2codework.github.io/agentwork/?case=music-podcast-post)
- license：按服务额度/时长核账；上传受隐私与合同限制
- license_notes：按服务额度/时长核账；上传受隐私与合同限制
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://us1.auphonic.com/help/algorithms/multitrack.html

## ElevenLabs SFX

文本描述生成音效，含时长与循环控制。

- ID / 类型：music-eleven-sfx / model
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[虚构游戏音效变体与循环](https://2codework.github.io/agentwork/?case=music-sfx-foley)
- license：按时长/credits 预算；素材/发行权另审
- license_notes：按时长/credits 预算；素材/发行权另审
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://elevenlabs.io/docs/overview/capabilities/sound-effects

## ElevenLabs TTS

文字到语音；仅使用有合法授权的产品内置或设计声线。

- ID / 类型：music-eleven-tts / model
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[合法合成声线的原创微播客](https://2codework.github.io/agentwork/?case=music-tts-podcast)
- license：付费额度与声线使用条件复核；不克隆、冒充真人
- license_notes：付费额度与声线使用条件复核；不克隆、冒充真人
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://elevenlabs.io/docs/overview/capabilities/text-to-speech

## Accessible captions QA

同步语音和必要非语音文字信息；自动输出需人工核对。

- ID / 类型：music-captions / standard
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[可访问性字幕从 ASR 到人工验收](https://2codework.github.io/agentwork/?case=music-accessible-captions)
- license：人工校对成本；录音和转写均需最小化访问
- license_notes：人工校对成本；录音和转写均需最小化访问
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://www.w3.org/WAI/media/av/captions/

## Magenta RealTime 2

交互式实时音乐生成；v1 为 legacy 分支。

- ID / 类型：music-mrt2 / model
- 生命周期：current
- 版本：未核验
- 核验：2026-10-28 · source_reviewed_not_replicated
- 对应实践（编辑学习关系）：[实时音乐控制的状态机演练](https://2codework.github.io/agentwork/?case=music-mrt-live)
- license：代码 Apache-2.0；权重许可未完成独立审查，商用待确认
- license_notes：代码 Apache-2.0；权重许可未完成独立审查，商用待确认
- historical_context：当前仅确认官方文档陈述，未证明账号/地区实际可用
- 来源：https://github.com/magenta/magenta-realtime

## Wan2.2 文/图/音驱动视频

生成镜头的模型家族，不负责项目权限、预算、剪辑交付或事实核验。

- ID / 类型：vid-wan22 / model_family
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-wan']}
- 版本：2.2
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[虚构产品15秒图生视频演示](https://2codework.github.io/agentwork/?case=video-product-i2v)
- 对应实践（编辑学习关系）：[原创动画角色跨镜头一致性](https://2codework.github.io/agentwork/?case=video-character-continuity)
- 对应实践（编辑学习关系）：[不克隆音色的配音与节奏](https://2codework.github.io/agentwork/?case=video-narration-sync)
- 对应实践（编辑学习关系）：[历史视频微调迁移教学](https://2codework.github.io/agentwork/?case=video-historical-edit-migration)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/Wan-Video/Wan2.2

## LTX-Video 历史入口

维护者已把主要开发入口转至LTX-2；旧版用于版本迁移教学。

- ID / 类型：vid-ltx-video / model_family
- 生命周期：{'status': 'superseded_per_maintainer', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': ['vid-ltx2'], 'source_ids': ['vid-src-ltxv']}
- 版本：LTX-Video legacy
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[历史视频微调迁移教学](https://2codework.github.io/agentwork/?case=video-historical-edit-migration)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/Lightricks/LTX-Video

## LTX-2 音视频生成

音视频生成与训练实现，后端、权重许可和资源要求需逐版本固定。

- ID / 类型：vid-ltx2 / model_family
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-ltx2']}
- 版本：LTX-2 family; revision not pinned
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[原创动画角色跨镜头一致性](https://2codework.github.io/agentwork/?case=video-character-continuity)
- 对应实践（编辑学习关系）：[不克隆音色的配音与节奏](https://2codework.github.io/agentwork/?case=video-narration-sync)
- 对应实践（编辑学习关系）：[历史视频微调迁移教学](https://2codework.github.io/agentwork/?case=video-historical-edit-migration)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/Lightricks/LTX-2

## CogVideoX

视频扩散Transformer路线；代码与不同规模权重的许可边界须分开。

- ID / 类型：vid-cogvideox / model_family
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-cog', 'vid-src-cogpaper']}
- 版本：CogVideoX-2B/5B / v3 2025-03-26
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/zai-org/CogVideo
- 来源：https://arxiv.org/abs/2408.06072

## AnimateDiff 运动模块

在图像扩散基础上引入运动模块的历史代表方法；不是退役断言。

- ID / 类型：vid-animatediff / method
- 生命周期：{'status': 'historical_pinned_specification', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-animatediff', 'vid-src-animatepaper']}
- 版本：revision unknown / v2 2024-02-08
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[无对白教育动画循环](https://2codework.github.io/agentwork/?case=video-silent-animation-loop)
- 对应实践（编辑学习关系）：[历史视频微调迁移教学](https://2codework.github.io/agentwork/?case=video-historical-edit-migration)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/guoyww/AnimateDiff
- 来源：https://arxiv.org/abs/2307.04725

## Tune-A-Video 单视频微调

历史单视频微调研究；与免训练图生视频是不同成本/控制路线。

- ID / 类型：vid-tune-a-video / method
- 生命周期：{'status': 'historical_pinned_specification', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-tune', 'vid-src-tunepaper']}
- 版本：ICCV 2023 implementation / v2 2023-03-17
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[历史视频微调迁移教学](https://2codework.github.io/agentwork/?case=video-historical-edit-migration)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/showlab/Tune-A-Video
- 来源：https://arxiv.org/abs/2212.11565

## ComfyUI 图式运行时

节点图连接模型和处理步骤；增加目标、状态、反馈及权限控制才构成本文Agent设计。

- ID / 类型：vid-comfyui / runtime
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-comfy']}
- 版本：revision not pinned
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[虚构产品15秒图生视频演示](https://2codework.github.io/agentwork/?case=video-product-i2v)
- 对应实践（编辑学习关系）：[项目归档与局部重做](https://2codework.github.io/agentwork/?case=video-archive-reproducible)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/Comfy-Org/ComfyUI

## Whisper 语音识别

用于字幕初稿，不生成声音；逐字与时间码仍需校对。

- ID / 类型：vid-whisper / model_family
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-whisper']}
- 版本：revision not pinned
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[十分钟培训课拆成可维护章节](https://2codework.github.io/agentwork/?case=video-training-chapters)
- 对应实践（编辑学习关系）：[双语字幕与无障碍版本](https://2codework.github.io/agentwork/?case=video-caption-accessibility)
- 对应实践（编辑学习关系）：[视频Agent的证据型质检](https://2codework.github.io/agentwork/?case=video-qc-evidence)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/openai/whisper

## WhisperX 对齐流程

识别与时间对齐工具；说话人编号不证明真实身份。

- ID / 类型：vid-whisperx / tool
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-whisperx']}
- 版本：revision not pinned
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[双语字幕与无障碍版本](https://2codework.github.io/agentwork/?case=video-caption-accessibility)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/m-bain/whisperX

## FFmpeg 媒体处理

按明确输入参数执行剪裁、混流、编码，不自主决定叙事。

- ID / 类型：vid-ffmpeg / tool
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-ffmpeg']}
- 版本：online documentation; local binary unknown
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[虚构产品15秒图生视频演示](https://2codework.github.io/agentwork/?case=video-product-i2v)
- 对应实践（编辑学习关系）：[无对白教育动画循环](https://2codework.github.io/agentwork/?case=video-silent-animation-loop)
- 对应实践（编辑学习关系）：[原素材重剪为30秒科普预告](https://2codework.github.io/agentwork/?case=video-edit-original-footage)
- 对应实践（编辑学习关系）：[不克隆音色的配音与节奏](https://2codework.github.io/agentwork/?case=video-narration-sync)
- 对应实践（编辑学习关系）：[视频Agent的证据型质检](https://2codework.github.io/agentwork/?case=video-qc-evidence)
- 对应实践（编辑学习关系）：[项目归档与局部重做](https://2codework.github.io/agentwork/?case=video-archive-reproducible)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://ffmpeg.org/ffmpeg.html

## OpenTimelineIO 时间线交换

序列化编辑决策与素材引用；素材归档和渲染另做。

- ID / 类型：vid-otio / standard_or_format
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-otio']}
- 版本：revision not pinned
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[从一分钟原创短故事到可拍分镜](https://2codework.github.io/agentwork/?case=video-brief-storyboard)
- 对应实践（编辑学习关系）：[十分钟培训课拆成可维护章节](https://2codework.github.io/agentwork/?case=video-training-chapters)
- 对应实践（编辑学习关系）：[原创短片的长叙事预演](https://2codework.github.io/agentwork/?case=video-long-film-previs)
- 对应实践（编辑学习关系）：[原素材重剪为30秒科普预告](https://2codework.github.io/agentwork/?case=video-edit-original-footage)
- 对应实践（编辑学习关系）：[项目归档与局部重做](https://2codework.github.io/agentwork/?case=video-archive-reproducible)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/AcademySoftwareFoundation/OpenTimelineIO

## Kdenlive 字幕与转录剪辑

依据配置的识别引擎制作字幕与选片，人工保留最终剪辑决定。

- ID / 类型：vid-kdenlive / tool
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-kdenlive']}
- 版本：26.08 manual
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[十分钟培训课拆成可维护章节](https://2codework.github.io/agentwork/?case=video-training-chapters)
- 对应实践（编辑学习关系）：[双语字幕与无障碍版本](https://2codework.github.io/agentwork/?case=video-caption-accessibility)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html

## FilmAgent 虚拟制片研究

多角色在受限3D虚拟环境协作，需与实际电影拍摄能力区分。

- ID / 类型：vid-filmagent / agent_system
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-filmagent']}
- 版本：research project page
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[从一分钟原创短故事到可拍分镜](https://2codework.github.io/agentwork/?case=video-brief-storyboard)
- 对应实践（编辑学习关系）：[原创短片的长叙事预演](https://2codework.github.io/agentwork/?case=video-long-film-previs)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://filmagent.github.io/

## ViMax 制片编排

把策划、角色、镜头和生成连接起来；API配置示例不保证本地无付费互换。

- ID / 类型：vid-vimax / agent_system
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-vimax']}
- 版本：v1.2.0 announcement; head not pinned
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[从一分钟原创短故事到可拍分镜](https://2codework.github.io/agentwork/?case=video-brief-storyboard)
- 对应实践（编辑学习关系）：[原创动画角色跨镜头一致性](https://2codework.github.io/agentwork/?case=video-character-continuity)
- 对应实践（编辑学习关系）：[原创短片的长叙事预演](https://2codework.github.io/agentwork/?case=video-long-film-previs)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/HKUDS/ViMax

## VideoAgent 编辑框架（HKUDS）

多Agent编辑研究系统，不等于同名2024长视频问答项目。

- ID / 类型：vid-videoagent-edit / agent_system
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-videoagent', 'vid-src-videoagentpaper']}
- 版本：head not pinned / v1 metadata reviewed
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[原素材重剪为30秒科普预告](https://2codework.github.io/agentwork/?case=video-edit-original-footage)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://github.com/HKUDS/VideoAgent
- 来源：https://arxiv.org/abs/2606.23327

## VideoAgent 长视频理解（2024）

检索视觉证据进行问答的研究系统，不应列作视频生成模型。

- ID / 类型：vid-videoagent-understand / agent_system
- 生命周期：{'status': 'historical_pinned_specification', 'as_of': '2026-10-28', 'applicable_version': '仅上述来源快照；部署前固定commit与权重SHA256', 'replacement_node_ids': [], 'source_ids': ['vid-src-understand']}
- 版本：paper metadata reviewed
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 对应实践（编辑学习关系）：[视频Agent的证据型质检](https://2codework.github.io/agentwork/?case=video-qc-evidence)
- license：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 学习步骤（未执行）：先阅读版本和许可，保存配置与来源。
- 学习步骤（未执行）：只用原创合成输入建立小样与人工真值。
- 学习步骤（未执行）：计量成本，逐镜头审查，保存失败，不以演示代替复现。
- 注意：公开仓库不等于免费运行、权重无条件商用、生产可靠或自主Agent。
- 来源：https://arxiv.org/abs/2403.10517

## 自然语言处理 NLP

研究计算系统如何处理、理解和生成语言；语言模型只是其中一类方法。

- ID / 类型：nlp / field
- 生命周期：unknown
- 版本：SLP3 online manuscript 2026-08-19
- 核验：2026-10-28 · primary_source_checked
- 注意：NLP不始于Transformer，也不等于聊天机器人。
- 来源：https://web.stanford.edu/~jurafsky/slp3/

## 分词与 tokenization

把文本转换为模型处理的符号序列；不同语言和分词器的token边界不同。

- ID / 类型：tokenization / concept
- 生命周期：unknown
- 版本：SLP3 2026-08-19
- 核验：2026-10-28 · primary_source_checked
- 注意：一个token不固定等于一个词或一个汉字。
- 来源：https://web.stanford.edu/~jurafsky/slp3/

## 语言建模

估计语言序列的概率；自回归生成通过条件概率逐步产生后续符号。

- ID / 类型：language-modeling / concept
- 生命周期：unknown
- 版本：SLP3 2026-08-19
- 核验：2026-10-28 · primary_source_checked
- 注意：概率高不等于事实正确。
- 来源：https://web.stanford.edu/~jurafsky/slp3/

## 向量表示 / embeddings

用连续向量表示离散符号或对象，便于学习相似性和执行神经计算。

- ID / 类型：embeddings / concept
- 生命周期：unknown
- 版本：representative paper v1; not invention date
- 核验：2026-10-28 · primary_source_checked
- 注意：静态词向量、上下文表示与句向量不是同一个对象。
- 来源：https://arxiv.org/abs/1301.3781
- 事件：paper_submission · 2013-01-16 · 向量表示 / embeddings：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1301.3781

## word2vec

以高效的预测任务学习词的连续表示，是静态词向量的重要里程碑。

- ID / 类型：word2vec / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：word2vec不是Transformer，也不是对话大模型。
- 来源：https://arxiv.org/abs/1301.3781
- 事件：paper_submission · 2013-01-16 · 向量表示 / embeddings：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1301.3781

## LSTM sequence-to-sequence

编码器把输入序列编码，解码器产生输出序列；2014论文使用多层LSTM。

- ID / 类型：seq2seq / architecture
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：seq2seq是任务/架构范式，不专指Transformer。
- 来源：https://arxiv.org/abs/1409.3215
- 事件：paper_submission · 2014-09-10 · LSTM sequence-to-sequence：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1409.3215

## 神经注意力：软对齐

解码时对输入表示分配可学习权重，减少固定长度编码的瓶颈。

- ID / 类型：attention / method
- 生命周期：unknown
- 版本：Bahdanau et al. paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：注意力权重不能直接视为完整的因果解释。
- 来源：https://arxiv.org/abs/1409.0473
- 事件：paper_submission · 2014-09-01 · 神经注意力：软对齐：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1409.0473

## Transformer

以注意力与前馈网络为核心的序列建模架构；原论文提出编码器—解码器结构。

- ID / 类型：transformer / architecture
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：Transformer原论文并非decoder-only；也不是所有模型都使用同一注意力实现。
- 来源：https://arxiv.org/abs/1706.03762
- 事件：paper_submission · 2017-06-12 · Transformer：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1706.03762

## 预训练与迁移学习

先用较广泛的数据和目标训练，再迁移到下游任务；目标和架构可以不同。

- ID / 类型：pretraining / concept
- 生命周期：unknown
- 版本：representative study v1
- 核验：2026-10-28 · primary_source_checked
- 注意：预训练模型不自动具备可靠的指令遵循。
- 来源：https://arxiv.org/abs/1910.10683
- 事件：paper_submission · 2019-10-23 · 预训练与迁移学习：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1910.10683

## BERT

双向Transformer语言表示模型家族；采用预训练后微调的使用方式。

- ID / 类型：bert / model_family
- 生命周期：unknown
- 版本：family; original paper
- 核验：2026-10-28 · primary_source_checked
- 注意：BERT不是典型的自回归聊天模型。
- 来源：https://arxiv.org/abs/1810.04805
- 事件：paper_submission · 2018-10-11 · BERT：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1810.04805

## T5

把多类NLP任务统一表示为文本到文本的预训练Transformer家族。

- ID / 类型：t5 / model_family
- 生命周期：unknown
- 版本：family; original report
- 核验：2026-10-28 · primary_source_checked
- 注意：统一任务格式不代表任务之间的难度完全相同。
- 来源：https://arxiv.org/abs/1910.10683
- 事件：paper_submission · 2019-10-23 · 预训练与迁移学习：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1910.10683

## GPT

自回归语言模型家族；本版以GPT-3原始论文为已核验历史锚点，不列当前版本。

- ID / 类型：gpt / model_family
- 生命周期：unknown
- 版本：family anchored to GPT-3 paper
- 核验：2026-10-28 · primary_source_checked
- 注意：GPT家族名称不等于某个API快照或ChatGPT产品。
- 来源：https://arxiv.org/abs/2005.14165

## GPT-3（2020论文）

研究自回归语言模型在少样本上下文设置下完成任务的能力。

- ID / 类型：gpt-3 / model_release
- 生命周期：unknown
- 版本：GPT-3 paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：few-shot上下文学习通常不意味着推理时更新模型权重。
- 来源：https://arxiv.org/abs/2005.14165
- 事件：paper_submission · 2020-05-28 · GPT-3（2020论文）：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2005.14165
- 事件：announcement · 未知 / 待核验 · GPT-3（2020论文）：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · GPT-3（2020论文）：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 2020-06-11 · GPT-3家族：OpenAI API private beta · 精度 day · 时区 未知 · 范围 private_beta_approved_users · 版本 GPT-3 family API; not a fixed checkpoint; original 2020 launch · 截至已可用（非首发） 无独立观察 · 说明 不是GA，不是论文首次提交，也不是权重开放。 · 证据 Date header; paragraphs beginning Today the API runs and But we also know · 来源 https://openai.com/index/openai-api/
- 事件：report_publication · 未知 / 待核验 · GPT-3（2020论文）：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## 上下文学习 ICL

在提示中提供示例或任务描述，让固定权重模型适应当前任务。

- ID / 类型：in-context-learning / concept
- 生命周期：unknown
- 版本：representative paper
- 核验：2026-10-28 · primary_source_checked
- 注意：上下文适应与参数微调不同。
- 来源：https://arxiv.org/abs/2005.14165
- 事件：paper_submission · 2020-05-28 · GPT-3（2020论文）：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2005.14165

## 监督指令微调 SFT

使用指令与期望回答示例调整模型行为；是InstructGPT流程的一部分。

- ID / 类型：instruction-tuning / method
- 生命周期：unknown
- 版本：representative paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：SFT不是RLHF的同义词。
- 来源：https://arxiv.org/abs/2203.02155
- 事件：paper_submission · 2022-03-04 · 监督指令微调 SFT：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2203.02155

## 人类反馈强化学习 RLHF

InstructGPT流程用人类偏好排序训练奖励模型，再用强化学习调整语言模型。

- ID / 类型：rlhf / method
- 生命周期：unknown
- 版本：InstructGPT example; not first RLHF invention
- 核验：2026-10-28 · primary_source_checked
- 注意：偏好优化不保证真实、无偏或适合所有人的价值观。
- 来源：https://arxiv.org/abs/2203.02155
- 事件：paper_submission · 2022-03-04 · 监督指令微调 SFT：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2203.02155

## Constitutional AI / RLAIF

用明确原则引导自我批评与修订，并以AI偏好反馈支持后续训练。

- ID / 类型：constitutional-ai / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：AI反馈仍依赖人类设计的原则和训练环境；不是无条件安全保证。
- 来源：https://arxiv.org/abs/2212.08073
- 事件：paper_submission · 2022-12-15 · Constitutional AI / RLAIF：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2212.08073

## Direct Preference Optimization

通过偏好样本直接优化策略的目标，避免经典RLHF中显式奖励模型和在线RL训练的组合。

- ID / 类型：dpo / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：DPO仍需要偏好数据；不是不做训练的提示技巧。
- 来源：https://arxiv.org/abs/2305.18290
- 事件：paper_submission · 2023-05-29 · Direct Preference Optimization：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2305.18290

## Chain-of-Thought prompting

用分步示例提示模型生成中间推理文本，是推理提示方法的重要研究方向。

- ID / 类型：cot / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：生成看似合理的推理链不保证答案正确，也不保证忠实反映内部计算。
- 来源：https://arxiv.org/abs/2201.11903
- 事件：paper_submission · 2022-01-28 · Chain-of-Thought prompting：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2201.11903

## 推理导向模型

通过训练和推理策略加强多步骤问题求解的模型类别；本版以DeepSeek-R1为实例。

- ID / 类型：reasoning-models / concept
- 生命周期：unknown
- 版本：representative report
- 核验：2026-10-28 · primary_source_checked
- 注意：推理模型不是已证明具有普适逻辑正确性的形式系统。
- 来源：https://arxiv.org/abs/2501.12948
- 事件：paper_submission · 2025-01-22 · 推理导向模型：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2501.12948

## DeepSeek

本版仅收录R1作为DeepSeek家族的历史推理实例，不推断所有版本结构或能力。

- ID / 类型：deepseek / model_family
- 生命周期：unknown
- 版本：family; R1 anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：DeepSeek公司、产品与单个模型权重需要分开。
- 来源：https://arxiv.org/abs/2501.12948
- 来源：https://github.com/deepseek-ai/DeepSeek-R1

## DeepSeek-R1（2025原始报告）

报告包含冷启动数据和多阶段训练；与不进行前置SFT的R1-Zero区别明确。

- ID / 类型：deepseek-r1-2025 / model_release
- 生命周期：unknown
- 版本：original paper v1; not later checkpoint
- 核验：2026-10-28 · primary_source_checked
- 注意：不能把R1-Zero的纯RL实验流程直接套用于R1。
- 来源：https://arxiv.org/abs/2501.12948
- 来源：https://github.com/deepseek-ai/DeepSeek-R1
- 事件：paper_submission · 2025-01-22 · 推理导向模型：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2501.12948
- 事件：announcement · 未知 / 待核验 · DeepSeek-R1（2025原始报告）：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · DeepSeek-R1（2025原始报告）：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 未知 / 待核验 · DeepSeek-R1（2025原始报告）：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · DeepSeek-R1（2025原始报告）：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## 检索增强生成 RAG

组合可检索外部知识与生成模型，使回答能够利用参数之外的材料。

- ID / 类型：rag / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：检索到相关内容不意味着答案必定正确或引用充分。
- 来源：https://arxiv.org/abs/2005.11401
- 事件：paper_submission · 2020-05-22 · 检索增强生成 RAG：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2005.11401

## 多模态模型

联合处理多种信息形式；必须分别注明输入和输出支持，不能仅用多模态一词推断所有能力。

- ID / 类型：multimodal / concept
- 生命周期：unknown
- 版本：concept; representative sources
- 核验：2026-10-28 · primary_source_checked
- 注意：图像理解、图像生成、语音识别、语音生成不是同一种能力。
- 来源：https://arxiv.org/abs/2103.00020
- 来源：https://arxiv.org/abs/2312.11805

## CLIP

通过图像—文本配对学习可迁移表示，支持文本描述与图像的匹配。

- ID / 类型：clip / model_family
- 生命周期：unknown
- 版本：original paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：CLIP不是自然语言对话模型，也不直接生成图像。
- 来源：https://arxiv.org/abs/2103.00020
- 事件：paper_submission · 2021-02-26 · CLIP：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2103.00020

## LLaVA

连接视觉编码器与语言模型，通过视觉指令微调支持图文问答。

- ID / 类型：llava / model_family
- 生命周期：unknown
- 版本：original paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：家族后续版本不能直接继承首版报告的全部训练描述。
- 来源：https://arxiv.org/abs/2304.08485
- 事件：paper_submission · 2023-04-17 · LLaVA：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2304.08485

## Whisper

利用大规模弱监督音频转写数据训练的语音识别模型家族。

- ID / 类型：whisper / model_family
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：语音识别不是语音合成，也不保证逐字无误。
- 来源：https://arxiv.org/abs/2212.04356
- 事件：paper_submission · 2022-12-06 · Whisper：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2212.04356

## Latent Diffusion

在压缩的潜在表示空间执行扩散过程，用于图像合成等任务。

- ID / 类型：latent-diffusion / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：图像生成模型不一定是自回归语言模型。
- 来源：https://arxiv.org/abs/2112.10752
- 事件：paper_submission · 2021-12-20 · Latent Diffusion：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2112.10752

## 语言模型驱动的 agents

以模型作为决策组件，与工具或环境循环交互的系统；ReAct是一个代表性研究范式。

- ID / 类型：agents / concept
- 生命周期：unknown
- 版本：concept; ReAct anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：agent不是单一模型名称；工具权限、环境、评估和终止条件同样关键。
- 来源：https://arxiv.org/abs/2210.03629

## ReAct

交替产生推理文本和行动，并利用环境观察继续完成任务。

- ID / 类型：react / method
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：生成行动文本不意味着工具已实际执行成功。
- 来源：https://arxiv.org/abs/2210.03629
- 事件：paper_submission · 2022-10-06 · ReAct：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2210.03629

## 递归自我改进 RSI

研究系统修改自身改进机制并循环提升的可能性；定义、闭环范围与可验证收益必须明确。

- ID / 类型：rsi / research_concept
- 生命周期：unknown
- 版本：research concept; no general realized claim
- 核验：2026-10-28 · research_claim_scoped
- 注意：有限任务的自修代码实验不是无限自我提升或AGI已经实现的证明。
- 来源：https://arxiv.org/abs/cs/0309048
- 来源：https://arxiv.org/abs/2310.02304

## Gödel machine

在形式化公理和效用设定下，以找到改进证明作为自修改条件的理论框架。

- ID / 类型：godel-machine / theoretical_framework
- 生命周期：unknown
- 版本：paper v1; scoped theoretical result
- 核验：2026-10-28 · research_claim_scoped
- 注意：理论最优性条件不等于现实系统能高效找到所需证明。
- 来源：https://arxiv.org/abs/cs/0309048
- 事件：paper_submission · 2003-09-25 · Gödel machine：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/cs/0309048

## Self-Taught Optimizer (STOP)

研究语言模型辅助的程序框架如何改进自身；论文明确底层语言模型没有被修改。

- ID / 类型：stop / research_system
- 生命周期：unknown
- 版本：paper v1; COLM 2024
- 核验：2026-10-28 · research_claim_scoped
- 注意：论文明确称其不是完整的递归自我改进。
- 来源：https://arxiv.org/abs/2310.02304
- 事件：paper_submission · 2023-10-03 · Self-Taught Optimizer (STOP)：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2310.02304

## JEV（用户术语，待确认）

含义未确定：需用户给出全称、论文或链接后再建立实体和技术关系。

- ID / 类型：jev / unresolved_term
- 生命周期：unknown
- 版本：未核验
- 核验：2026-10-28 · ambiguous
- 注意：不得未经确认等同JEPA，亦不得虚构其论文和发布日期。

## GLUE

汇集多种语言理解任务，用于比较模型在指定评测协议下的表现。

- ID / 类型：glue / benchmark
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：单一基准得分不代表所有语言能力或真实部署质量。
- 来源：https://arxiv.org/abs/1804.07461
- 事件：paper_submission · 2018-04-20 · GLUE：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/1804.07461

## MMLU

跨多个知识学科的语言理解评测；结果依赖版本、提示、采样和污染控制。

- ID / 类型：mmlu / benchmark
- 生命周期：unknown
- 版本：paper v1
- 核验：2026-10-28 · primary_source_checked
- 注意：原始论文结果不是持续有效的模型排行榜。
- 来源：https://arxiv.org/abs/2009.03300
- 事件：paper_submission · 2020-09-07 · MMLU：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2009.03300

## Meta

本图谱中与Llama原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-llama / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2307.09288

## Llama

Llama家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：llama / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2307.09288

## Llama 2

包含基础模型与对话微调版本的历史模型系列。

- ID / 类型：llama-2 / model_release
- 生命周期：unknown
- 版本：2
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2307.09288
- 事件：paper_submission · 2023-07-18 · Llama 2：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2307.09288
- 事件：announcement · 2023-07-18 · Llama 2：官方宣布 · 精度 day · 时区 未知 · 范围 public_announcement · 版本 Llama 2 original release · 截至已可用（非首发） 无独立观察 · 说明 此条仅记录宣布。 · 证据 Date header; Takeaways; paragraph beginning We’re now ready · 来源 https://ai.meta.com/blog/llama-2/
- 事件：weights_release · 2023-07-18 · Llama 2：权重开放 · 精度 day · 时区 未知 · 范围 weights_available_subject_to_llama2_license · 版本 Llama 2 pretrained and conversational fine-tuned weights · 截至已可用（非首发） 无独立观察 · 说明 开放权重不代表OSI开源；不据Azure目录可用推断API GA。 · 证据 Date header; Takeaways; paragraph beginning We’re now ready · 来源 https://ai.meta.com/blog/llama-2/
- 事件：api_launch · 未知 / 待核验 · Llama 2：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Llama 2：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Alibaba Cloud / Qwen Team

本图谱中与Qwen原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-qwen / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2309.16609

## Qwen

Qwen家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：qwen / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2309.16609

## Qwen（2023首篇报告）

报告区分基础预训练模型、聊天对齐模型及代码/数学方向。

- ID / 类型：qwen-2023 / model_release
- 生命周期：unknown
- 版本：2023 report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2309.16609
- 事件：paper_submission · 2023-09-28 · Qwen（2023首篇报告）：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2309.16609
- 事件：announcement · 未知 / 待核验 · Qwen（2023首篇报告）：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · Qwen（2023首篇报告）：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 未知 / 待核验 · Qwen（2023首篇报告）：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Qwen（2023首篇报告）：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Mistral AI

本图谱中与Mistral原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-mistral / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2310.06825

## Mistral

Mistral家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：mistral / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2310.06825

## Mistral 7B v0.1

历史7B模型，报告说明grouped-query attention与sliding-window attention。

- ID / 类型：mistral-7b-v0-1 / model_release
- 生命周期：unknown
- 版本：7B v0.1
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2310.06825
- 事件：paper_submission · 2023-10-10 · Mistral 7B v0.1：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2310.06825
- 事件：announcement · 2023-09-27 · Mistral 7B v0.1：官方宣布 · 精度 day · 时区 未知 · 范围 public_announcement · 版本 Mistral 7B original v0.1 · 截至已可用（非首发） 无独立观察 · 说明 不是10月技术报告提交日。 · 证据 Date header; Mistral 7B in short; Download it link · 来源 https://mistral.ai/news/announcing-mistral-7b/, https://huggingface.co/mistralai/Mistral-7B-v0.1
- 事件：weights_release · 2023-09-27 · Mistral 7B v0.1：权重开放 · 精度 day · 时区 未知 · 范围 public_weight_download_apache_2_0 · 版本 Mistral 7B original v0.1 · 截至已可用（非首发） 无独立观察 · 说明 原文提供下载及Hub入口，不据此填API事件。 · 证据 Date header; Mistral 7B in short; Download it link · 来源 https://mistral.ai/news/announcing-mistral-7b/, https://huggingface.co/mistralai/Mistral-7B-v0.1
- 事件：api_launch · 未知 / 待核验 · Mistral 7B v0.1：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Mistral 7B v0.1：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## BigScience Workshop

本图谱中与BLOOM原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-bloom / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2211.05100

## BLOOM

BLOOM家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：bloom / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2211.05100

## BLOOM 176B

多语言自回归语言模型，作为跨国开放科研协作实例。

- ID / 类型：bloom-176b / model_release
- 生命周期：unknown
- 版本：176B original report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2211.05100
- 事件：paper_submission · 2022-11-09 · BLOOM 176B：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2211.05100
- 事件：announcement · 2022-07-12 · BLOOM 176B：官方宣布 · 精度 day · 时区 未知 · 范围 public_announcement · 版本 BLOOM original 176B · 截至已可用（非首发） 无独立观察 · 说明 不是后来的论文提交日。 · 证据 Date header; Today we release; Researchers can now download; inference API paragraph · 来源 https://huggingface.co/blog/bloom
- 事件：weights_release · 2022-07-12 · BLOOM 176B：权重开放 · 精度 day · 时区 未知 · 范围 public_weight_download_subject_to_rail · 版本 BLOOM original 176B · 截至已可用（非首发） 无独立观察 · 说明 需同意Responsible AI License，非无限制开放。 · 证据 Date header; Today we release; Researchers can now download; inference API paragraph · 来源 https://huggingface.co/blog/bloom
- 事件：api_launch · 未知 / 待核验 · BLOOM 176B：Hub小规模推理API已可用 · 精度 unknown · 时区 未知 · 范围 hosted_inference_for_tests_prototyping_small_scale · 版本 BLOOM 176B Hugging Face hosted inference · 截至已可用（非首发） 2022-07-12 · 说明 官方2022-07-12公告证明截至当日BLOOM 176B的Hub推理API已可用于小规模测试及原型；不证明API精确首发日期，不是生产GA。首发日期仍待核验。 · 证据 Date header; Today we release; Researchers can now download; inference API paragraph · 来源 https://huggingface.co/blog/bloom
- 事件：report_publication · 未知 / 待核验 · BLOOM 176B：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Google / Gemini Team

本图谱中与Gemini原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-gemini / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2312.11805

## Gemini

Gemini家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：gemini / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2312.11805

## Gemini（首代技术报告）

原始报告描述多模态模型家族；不推断当前服务的模态或限制。

- ID / 类型：gemini-1-report / model_release
- 生命周期：unknown
- 版本：first generation report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2312.11805
- 事件：paper_submission · 2023-12-19 · Gemini（首代技术报告）：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2312.11805
- 事件：announcement · 2023-12-06 · Gemini 1.0：官方宣布 · 精度 day · 时区 未知 · 范围 public_announcement · 版本 Gemini 1.0 family (Ultra, Pro, Nano) · 截至已可用（非首发） 无独立观察 · 说明 不是所有规模当日API开放；不等同arXiv提交。 · 证据 Date header; Introducing Gemini; Availability · 来源 https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/
- 事件：weights_release · 未知 / 待核验 · Gemini（首代技术报告）：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 2023-12-13 · Gemini 1.0 Pro / Pro Vision：Vertex AI API Preview · 精度 day · 时区 未知 · 范围 public_preview_vertex_ai · 版本 Gemini 1.0 Pro and Pro Vision on Vertex AI; not Ultra/Nano · 截至已可用（非首发） 无独立观察 · 说明 收窄原家族事件到已核验API版本和平台；不是GA。 · 证据 Date header; opening paragraph; December 13, 2023 / Vertex AI Gemini models · 来源 https://cloud.google.com/blog/products/ai-machine-learning/gemini-support-on-vertex-ai, https://docs.cloud.google.com/vertex-ai/docs/core-release-notes
- 事件：report_publication · 未知 / 待核验 · Gemini（首代技术报告）：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Technology Innovation Institute

本图谱中与Falcon原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-falcon / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2311.16867

## Falcon

Falcon家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：falcon / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2311.16867

## Falcon 180B

Falcon系列中的历史因果解码器模型。

- ID / 类型：falcon-180b / model_release
- 生命周期：unknown
- 版本：180B report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2311.16867
- 事件：paper_submission · 2023-11-28 · Falcon 180B：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2311.16867
- 事件：announcement · 2023-09-06 · Falcon 180B：官方宣布 · 精度 day · 时区 未知 · 范围 public_announcement · 版本 Falcon 180B original release · 截至已可用（非首发） 无独立观察 · 说明 不采纳发布材料里的全局排名断言。 · 证据 Date header; Abu Dhabi-UAE dateline and launch paragraph · 来源 https://www.tii.ae/news/technology-innovation-institute-introduces-worlds-most-powerful-open-llm-falcon-180b
- 事件：weights_release · 2023-09-06 · Falcon 180B：权重开放 · 精度 day · 时区 未知 · 范围 gated_weight_download_license_acceptance_required · 版本 Falcon 180B base and chat · 截至已可用（非首发） 无独立观察 · 说明 公开可取得权重但须接受条款；开放不等于不受限制。 · 证据 Date header; Abu Dhabi-UAE dateline and launch paragraph; Date header; Introduction; How to use Falcon 180B / license acceptance · 来源 https://www.tii.ae/news/technology-innovation-institute-introduces-worlds-most-powerful-open-llm-falcon-180b, https://huggingface.co/blog/falcon-180b
- 事件：api_launch · 未知 / 待核验 · Falcon 180B：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Falcon 180B：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Inception / MBZUAI / Cerebras

本图谱中与Jais原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-jais / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2308.16149

## Jais

Jais家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：jais / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2308.16149

## Jais 13B

重点面向阿拉伯语与英语，报告区分基础版与聊天版。

- ID / 类型：jais-13b / model_release
- 生命周期：unknown
- 版本：13B original report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2308.16149
- 事件：paper_submission · 2023-08-30 · Jais 13B：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2308.16149
- 事件：announcement · 未知 / 待核验 · Jais 13B：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · Jais 13B：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 未知 / 待核验 · Jais 13B：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Jais 13B：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Cohere For AI

本图谱中与Aya原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-aya / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2402.07827

## Aya

Aya家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：aya / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2402.07827

## Aya 101

多语言指令微调模型，重视低资源语言覆盖。

- ID / 类型：aya-101 / model_release
- 生命周期：unknown
- 版本：Aya 101 report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2402.07827
- 事件：paper_submission · 2024-02-12 · Aya 101：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2402.07827
- 事件：announcement · 未知 / 待核验 · Aya 101：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · Aya 101：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 未知 / 待核验 · Aya 101：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Aya 101：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Baichuan

本图谱中与Baichuan原始技术报告关联的研究/开发主体；不将地点视为团队成员国籍。

- ID / 类型：org-baichuan / organization
- 生命周期：unknown
- 版本：historical report attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：公司、合作项目、模型家族和版本是不同实体。
- 来源：https://arxiv.org/abs/2309.10305

## Baichuan

Baichuan家族入口；本版仅用已核验历史报告连接具体版本。

- ID / 类型：baichuan / model_family
- 生命周期：unknown
- 版本：family; historical anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名称不等于固定权重、固定许可证或固定能力。
- 来源：https://arxiv.org/abs/2309.10305

## Baichuan 2

历史多语言模型系列；报告包含7B与13B模型。

- ID / 类型：baichuan-2 / model_release
- 生命周期：unknown
- 版本：2 original report
- 核验：2026-10-28 · primary_source_checked
- 注意：该日期是论文首发日期，不应自动当作产品发布或权重开放日。
- 来源：https://arxiv.org/abs/2309.10305
- 事件：paper_submission · 2023-09-19 · Baichuan 2：所引论文首次提交 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv submission history [v1] · 来源 https://arxiv.org/abs/2309.10305
- 事件：announcement · 未知 / 待核验 · Baichuan 2：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · Baichuan 2：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 未知 / 待核验 · Baichuan 2：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Baichuan 2：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## OpenAI

GPT-3、InstructGPT及CLIP等所引用原始研究的研发主体。

- ID / 类型：org-openai / organization
- 生命周期：unknown
- 版本：historical research attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：机构当前产品线与历史论文中的模型不可混同。
- 来源：https://arxiv.org/abs/2005.14165
- 来源：https://arxiv.org/abs/2203.02155
- 来源：https://arxiv.org/abs/2103.00020

## Anthropic

Constitutional AI研究关联机构；此节点不表示所有Claude版本都有同一训练细节。

- ID / 类型：org-anthropic / organization
- 生命周期：unknown
- 版本：historical research attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：单篇训练研究不等于完整披露所有产品实现。
- 来源：https://arxiv.org/abs/2212.08073

## DeepSeek-AI

DeepSeek-R1论文与官方仓库的发布主体。

- ID / 类型：org-deepseek / organization
- 生命周期：unknown
- 版本：R1 attribution
- 核验：2026-10-28 · primary_source_checked
- 注意：论文报告与独立复现实验是不同证据。
- 来源：https://arxiv.org/abs/2501.12948
- 来源：https://github.com/deepseek-ai/DeepSeek-R1

## Sarvam-1

官方模型卡描述面向印度语言的基础文本补全模型，不能直接当作指令聊天模型。

- ID / 类型：sarvam-1 / model_release
- 生命周期：unknown
- 版本：sarvamai/sarvam-1 model card; release date not verified
- 核验：2026-10-28 · primary_source_checked
- 注意：基础模型支持的语言不表示每种语言质量相同。
- 来源：https://huggingface.co/sarvamai/sarvam-1
- 事件：announcement · 未知 / 待核验 · Sarvam-1：announcement日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：weights_release · 未知 / 待核验 · Sarvam-1：weights_release日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：api_launch · 未知 / 待核验 · Sarvam-1：api_launch日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源
- 事件：report_publication · 未知 / 待核验 · Sarvam-1：report_publication日期待独立核验 · 精度 unknown · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明 未核验不等于未发生；不可用论文首发日期填充。 · 证据 见原始来源 · 来源

## Sarvam

Sarvam模型家族入口；本版仅核验Sarvam-1官方模型卡。

- ID / 类型：sarvam / model_family
- 生命周期：unknown
- 版本：family; Sarvam-1 anchor
- 核验：2026-10-28 · primary_source_checked
- 注意：家族名不等于特定权重或全部后续版本。
- 来源：https://huggingface.co/sarvamai/sarvam-1

## vLLM推理服务

面向语言模型推理与服务的运行时；关注吞吐、显存、并发和受支持的模型及内核，不是模型权重。

- ID / 类型：sys-vllm / runtime
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-vllm', 'sys-src-paged']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定模型与运行时版本
- 学习步骤（未执行）：核对硬件和量化支持
- 学习步骤（未执行）：以同一输入长度与并发评估首token延迟、解码速度及显存。
- 注意：不是所有量化在所有GPU上都能运行；吞吐增益不等于单请求延迟同比下降。
- 来源：https://docs.vllm.ai/en/stable/features/quantization/index.html
- 来源：https://arxiv.org/abs/2309.06180

## PagedAttention与KV缓存

把注意力KV缓存按块管理，以减少碎片并支持共享；KV缓存是推理状态，不是长期用户记忆。

- ID / 类型：sys-pagedattention / method
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-paged']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：区分prefill与decode
- 学习步骤（未执行）：画出请求到缓存块的映射
- 学习步骤（未执行）：在不同序列长度下记录缓存占用。
- 注意：论文特定负载上的加速不能外推到任意设备；缓存优化不会自动增加模型知识。
- 来源：https://arxiv.org/abs/2309.06180
- 事件：paper_submission · 2023-09-12 · sys-event-pagedattention-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2309.06180

## llama.cpp

C/C++实现的本地及云端推理项目，支持多种硬件后端；常用GGUF承载模型。

- ID / 类型：sys-llamacpp / runtime
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-llama', 'sys-src-gguf']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：核对模型架构与转换支持
- 学习步骤（未执行）：固定GGUF文件哈希
- 学习步骤（未执行）：核对上下文/模板
- 学习步骤（未执行）：在隔离环境评测CPU或GPU后端。
- 注意：支持Apple Silicon不意味着仅支持Mac；同为4位文件也可能采用不同量化布局。
- 来源：https://github.com/ggml-org/llama.cpp
- 来源：https://github.com/ggml-org/ggml/blob/master/docs/gguf.md

## MLX LM

基于MLX的语言模型生成和微调工具，主要面向Apple Silicon；与MLX数组框架本身分层。

- ID / 类型：sys-mlx / runtime
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-mlx']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：先看支持模型和内存需求
- 学习步骤（未执行）：确认模型转换方式与聊天模板
- 学习步骤（未执行）：比较原精度与量化质量；这里只作教程研究。
- 注意：不要把统一内存容量当作无限显存；trust_remote_code会扩大执行风险，不应盲目开启。
- 来源：https://github.com/ml-explore/mlx-lm

## GPTQ

利用近似二阶信息的训练后权重量化方法；需结合校准、位宽、分组及推理内核理解。

- ID / 类型：sys-gptq / method
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-gptq']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：选代表性校准数据
- 学习步骤（未执行）：固定量化配置
- 学习步骤（未执行）：比较原权重与量化权重的任务质量及运行成本。
- 注意：GPTQ不是单一通用文件格式；论文压缩效果不是所有模型的保证。
- 来源：https://arxiv.org/abs/2210.17323
- 事件：paper_submission · 2022-10-31 · sys-event-gptq-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2210.17323

## AWQ

利用激活统计识别显著通道并缩放，以降低低位权重量化误差。

- ID / 类型：sys-awq / method
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-awq']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：收集代表性激活统计
- 学习步骤（未执行）：记录位宽和分组
- 学习步骤（未执行）：验证目标内核
- 学习步骤（未执行）：运行同口径质量对比。
- 注意：activation-aware不等于把所有激活都量化；低位权重不自动加速所有设备。
- 来源：https://arxiv.org/abs/2306.00978
- 事件：paper_submission · 2023-06-01 · sys-event-awq-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2306.00978

## QLoRA与NF4

冻结低位量化基础权重并训练LoRA适配器；NF4、双重量化与分页优化器服务于节省微调内存。

- ID / 类型：sys-qlora / method
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-qlora']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：区分底座权重和可训练适配器
- 学习步骤（未执行）：记录NF4与计算精度
- 学习步骤（未执行）：保留验证集
- 学习步骤（未执行）：测试合并/部署后的结果。
- 注意：QLoRA不是单纯推理格式；4位存储不代表全部计算都是4位。
- 来源：https://arxiv.org/abs/2305.14314
- 事件：paper_submission · 2023-05-23 · sys-event-qlora-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2305.14314

## GGUF模型容器

保存张量和模型元数据的二进制格式，可包含不同张量类型；与具体量化算法不是同一层。

- ID / 类型：sys-gguf / format
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-gguf']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：检查架构/分词器/模板元数据
- 学习步骤（未执行）：核对张量类型
- 学习步骤（未执行）：记录来源和哈希
- 学习步骤（未执行）：验证目标运行时兼容。
- 注意：GGUF不等于4位量化；扩展名不能证明模型许可或质量。
- 来源：https://github.com/ggml-org/ggml/blob/master/docs/gguf.md

## Safetensors张量容器

用于安全存储张量的格式，避免pickle式任意对象反序列化；不负责定义整个模型行为。

- ID / 类型：sys-safetensors / format
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-safe']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：核对文件与索引哈希
- 学习步骤（未执行）：匹配配置和分词器
- 学习步骤（未执行）：检查加载端是否还需要额外代码。
- 注意：张量文件安全不等于仓库所有代码安全，也不代表模型已量化。
- 来源：https://huggingface.co/docs/safetensors/index

## RAG工程实践

把检索得到的外部证据加入生成流程；原论文的联合建模方法与今天广义RAG工程管线应区分。

- ID / 类型：sys-rag / pipeline
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-rag']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：整理合法语料
- 学习步骤（未执行）：分块保留来源
- 学习步骤（未执行）：检索/重排
- 学习步骤（未执行）：将证据与问题一起生成
- 学习步骤（未执行）：检查引用及拒答。
- 注意：向量库不是RAG全部；检索到相关内容不保证回答忠实或内容可信。
- 来源：https://arxiv.org/abs/2005.11401
- 事件：paper_submission · 2020-05-22 · sys-event-rag-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2005.11401

## 向量检索与ANN

用向量距离寻找邻近项；近似近邻以召回率换延迟/内存，精确搜索可作为质量基线。

- ID / 类型：sys-vectorsearch / concept
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-faiss', 'sys-src-pg']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定嵌入版本与距离
- 学习步骤（未执行）：建立精确基线
- 学习步骤（未执行）：调索引参数
- 学习步骤（未执行）：测recall@k及延迟。
- 注意：向量维度相同不表示不同嵌入模型能混用；相似度不是事实正确概率。
- 来源：https://github.com/facebookresearch/faiss
- 来源：https://github.com/pgvector/pgvector

## Faiss相似度检索库

提供稠密向量相似度检索与聚类算法，包含精确及近似索引；不是完整数据库服务。

- ID / 类型：sys-faiss / library
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-faiss']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：建立小规模精确索引
- 学习步骤（未执行）：比较压缩/近似索引
- 学习步骤（未执行）：记录召回、内存、构建和查询时间。
- 注意：持久化、权限、事务与服务运维不能仅凭使用Faiss就视为已具备。
- 来源：https://github.com/facebookresearch/faiss

## pgvector

为PostgreSQL增加向量类型与相似度查询，可选择精确搜索、HNSW或IVFFlat。

- ID / 类型：sys-pgvector / database_extension
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-pg']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：先用精确SQL建立基线
- 学习步骤（未执行）：按距离建索引
- 学习步骤（未执行）：结合过滤条件检验召回
- 学习步骤（未执行）：审查租户隔离。
- 注意：ANN后过滤可能返回少于k条；加近似索引可能改变结果而非只加速。
- 来源：https://github.com/pgvector/pgvector

## Qdrant

以collection组织向量与payload的向量数据库；向量维度、距离及过滤设计影响检索。

- ID / 类型：sys-qdrant / database
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-qdrant']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：定义collection向量配置
- 学习步骤（未执行）：保留原文ID和权限字段
- 学习步骤（未执行）：写入/查询
- 学习步骤（未执行）：测试过滤、删除及恢复。
- 注意：payload过滤不能代替应用授权；数据库存在不说明嵌入已自动生成。
- 来源：https://qdrant.tech/documentation/manage-data/collections/

## Milvus

面向向量搜索的数据库系统，组织结构化字段及多种向量数据；可部署规模与配置相关。

- ID / 类型：sys-milvus / database
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-milvus']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：设计collection schema
- 学习步骤（未执行）：选择索引和度量
- 学习步骤（未执行）：导入小样本
- 学习步骤（未执行）：测召回与资源
- 学习步骤（未执行）：规划扩容。
- 注意：不能把云服务和开源软件部署方式、成本或许可完全混同。
- 来源：https://milvus.io/docs/overview.md

## Agent记忆分层

短期记忆通常为线程状态；长期记忆跨会话保存。记忆是应用数据管理，不必改变模型权重。

- ID / 类型：sys-memory / concept
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-memory']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：定义作用域
- 学习步骤（未执行）：存储事实及来源/时间
- 学习步骤（未执行）：按需检索
- 学习步骤（未执行）：支持修正、遗忘和删除
- 学习步骤（未执行）：验证线程隔离。
- 注意：上下文窗口、KV缓存、向量库、用户画像不是同一种记忆。
- 来源：https://docs.langchain.com/oss/python/concepts/memory

## MemGPT

通过层级记忆与数据移动管理有限上下文，借鉴操作系统虚拟内存思想。

- ID / 类型：sys-memgpt / system
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-memgpt']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：画出上下文内外存储
- 学习步骤（未执行）：记录读写事件
- 学习步骤（未执行）：测试跨会话检索与失效
- 学习步骤（未执行）：测错误记忆传播。
- 注意：操作系统类比不是让LLM成为真实内核；外部存储不等于无限可靠回忆。
- 来源：https://arxiv.org/abs/2310.08560
- 事件：paper_submission · 2023-10-12 · sys-event-memgpt-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2310.08560

## FineWeb

由网页抓取加工而来的大规模文本语料；需要按数据卡指定版本/子集和处理流程理解规模。

- ID / 类型：sys-fineweb / dataset
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-fineweb']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：读数据卡许可
- 学习步骤（未执行）：选子集及快照
- 学习步骤（未执行）：抽样看质量和语言
- 学习步骤（未执行）：做去重/隐私审查
- 学习步骤（未执行）：保留文档来源。
- 评测/数据集登记：{"node_id": "sys-fineweb", "availability": "public_download", "license": "ODC-BY metadata; underlying page rights require separate review", "split": "版本/子集，train", "access_url": "https://huggingface.co/datasets/HuggingFaceFW/fineweb", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "训练语料，不设统一能力分数", "protocol": "记录抓取快照、过滤、去重、分词器", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-fineweb"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://huggingface.co/datasets/HuggingFaceFW/fineweb"}}
- 注意：数据库许可不等于每个原网页内容统一授权；token总量依赖版本与分词器。
- 来源：https://huggingface.co/datasets/HuggingFaceFW/fineweb

## Dolma

混合网页、代码、论文等来源的预训练语料及相关构建工具；版本不同，组成与统计也不同。

- ID / 类型：sys-dolma / dataset
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-dolma']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定数据版本
- 学习步骤（未执行）：记录组成比例
- 学习步骤（未执行）：审查原来源约束
- 学习步骤（未执行）：隔离测试集污染
- 学习步骤（未执行）：保存处理日志。
- 评测/数据集登记：{"node_id": "sys-dolma", "availability": "public_download", "license": "ODC-BY metadata; mixed-source terms apply", "split": "v1.6/v1.7等版本须固定", "access_url": "https://huggingface.co/datasets/allenai/dolma", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "训练语料，不设统一能力分数", "protocol": "记录混合比例与数据处理版本", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-dolma"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://huggingface.co/datasets/allenai/dolma"}}
- 注意：不能只记总token数而忽略数据版本；数据集许可与组成内容许可应分层。
- 来源：https://huggingface.co/datasets/allenai/dolma

## The Stack v2

具有来源信息的代码语料集合，包含不同原始许可证；访问条款及批量获取条件需分别核验。

- ID / 类型：sys-stack / dataset
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-stack']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：读访问条款
- 学习步骤（未执行）：记录原项目许可证与来源
- 学习步骤（未执行）：尊重移除要求
- 学习步骤（未执行）：评测前做代码去重。
- 评测/数据集登记：{"node_id": "sys-stack", "availability": "gated", "license": "varied original code licenses + dataset access conditions", "split": "版本/语言/许可证子集", "access_url": "https://huggingface.co/datasets/bigcode/the-stack-v2", "access_application_url": "https://huggingface.co/datasets/bigcode/the-stack-v2", "access_application_note": "以数据卡当日访问条款为准", "metric": "训练语料，不设统一能力分数", "protocol": "批量访问需遵循Software Heritage条件；逐文件保留来源", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-stack"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://huggingface.co/datasets/bigcode/the-stack-v2"}}
- 注意：公开数据卡不代表无条件可下载；不能用一个总许可覆盖全部代码。
- 来源：https://huggingface.co/datasets/bigcode/the-stack-v2

## C4

Common Crawl加工语料家族；此处使用Ai2托管数据卡，需区分英文、多语言及其它配置。

- ID / 类型：sys-c4 / dataset
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-c4']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：指定configuration和split
- 学习步骤（未执行）：核对清洗策略
- 学习步骤（未执行）：记录来源与快照
- 学习步骤（未执行）：检查领域和语言偏差。
- 评测/数据集登记：{"node_id": "sys-c4", "availability": "public_download", "license": "ODC-BY dataset-card metadata; underlying content review required", "split": "configuration + train/validation", "access_url": "https://huggingface.co/datasets/allenai/c4", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "训练语料；验证loss须声明模型/分词器", "protocol": "不能将不同配置的token数直接混合", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-c4"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://huggingface.co/datasets/allenai/c4"}}
- 注意：C4与mC4不是可随意合并比较的单一数据版本；公开文本仍需内容权利审查。
- 来源：https://huggingface.co/datasets/allenai/c4

## MMLU

学科多项选择题评测；结果依赖题集版本、few-shot示例、选项评分和聚合方式。

- ID / 类型：sys-mmlu / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-mmlu', 'sys-src-harness']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定任务配置
- 学习步骤（未执行）：隔离dev/validation/test
- 学习步骤（未执行）：记录prompt与评分方式
- 学习步骤（未执行）：报告学科及总体指标。
- 评测/数据集登记：{"node_id": "sys-mmlu", "availability": "public_download", "license": "未在本轮逐文件核验，禁止推定统一授权", "split": "dev/validation/test；学科分组", "access_url": "https://github.com/hendrycks/test", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "accuracy；须声明聚合", "protocol": "few-shot数、选项logprob或生成答案、模板、截断", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-mmlu", "sys-src-harness"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://github.com/hendrycks/test"}}
- 注意：MMLU不等于所有知识或真实工作能力；MMLU-Pro不能冒充同一个benchmark。
- 来源：https://github.com/hendrycks/test
- 来源：https://github.com/EleutherAI/lm-evaluation-harness

## GSM8K

面向多步骤小学数学应用题的评测；答案抽取规则和推理采样会显著影响结果。

- ID / 类型：sys-gsm8k / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-gsm']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定test split
- 学习步骤（未执行）：声明是否思维链/工具
- 学习步骤（未执行）：保存答案抽取规则
- 学习步骤（未执行）：报告一次采样与多次采样区别。
- 评测/数据集登记：{"node_id": "sys-gsm8k", "availability": "public_download", "license": "仓库许可需在再分发前逐文件复核", "split": "train/test", "access_url": "https://github.com/openai/grade-school-math", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "最终答案正确率", "protocol": "答案提取、CoT、工具、采样/投票次数", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-gsm"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://github.com/openai/grade-school-math"}}
- 注意：不能把多数投票成绩当单次成功率；训练集中见过类似题会影响解释。
- 来源：https://github.com/openai/grade-school-math

## HumanEval

通过执行测试验证代码补全的功能正确性；常用pass@k，对采样数量有要求。

- ID / 类型：sys-humaneval / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-human']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定题集/语言
- 学习步骤（未执行）：隔离沙箱运行
- 学习步骤（未执行）：记录n、k和温度
- 学习步骤（未执行）：保留超时及失败分类。
- 评测/数据集登记：{"node_id": "sys-humaneval", "availability": "public_download", "license": "仓库许可需在再分发前逐文件复核", "split": "HumanEval问题集；固定版本", "access_url": "https://github.com/openai/human-eval", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "pass@k", "protocol": "n≥k；温度、超时、测试环境、沙箱", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-human"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://github.com/openai/human-eval"}}
- 注意：通过有限测试不等于代码完全正确；不能在有敏感文件或凭据的主机直接执行生成代码。
- 来源：https://github.com/openai/human-eval

## SWE-bench家族

以真实仓库问题和测试检验补丁；Full、Lite、Verified、Multilingual和Multimodal范围不同。

- ID / 类型：sys-swebench / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-swe']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定子集和harness
- 学习步骤（未执行）：锁定仓库/容器
- 学习步骤（未执行）：记录agent、模型、预算和重试
- 学习步骤（未执行）：报告resolved比例。
- 评测/数据集登记：{"node_id": "sys-swebench", "availability": "public_download", "license": "数据与原仓库代码分层许可；再分发前复核", "split": "Full/Lite/Verified/Multilingual/Multimodal", "access_url": "https://www.swebench.com/", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "% Resolved", "protocol": "模型、agent、harness、测试容器、预算、重试", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-swe"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://www.swebench.com/"}}
- 注意：模型+工具+脚手架的整体分数不能归功为裸模型能力；不同子集不能直接排同榜。
- 来源：https://www.swebench.com/

## LiveCodeBench

滚动收集竞赛编程题并按时间切片，帮助降低旧题污染影响；包含多种代码相关任务。

- ID / 类型：sys-livecodebench / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-live', 'sys-src-livepaper']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定release和题目日期范围
- 学习步骤（未执行）：声明模型截止信息
- 学习步骤（未执行）：保留prompt和采样
- 学习步骤（未执行）：分场景报告。
- 评测/数据集登记：{"node_id": "sys-livecodebench", "availability": "public_download", "license": "代码与竞赛题来源权利分层；本轮未做完整许可审计", "split": "release + 日期窗口 + scenario", "access_url": "https://github.com/LiveCodeBench/LiveCodeBench", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "按场景pass@k/正确率", "protocol": "题目发布日期、模型截止、prompt、采样", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-live", "sys-src-livepaper"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://github.com/LiveCodeBench/LiveCodeBench"}}
- 注意：论文标题中的contamination-free不是永远零污染保证；上线后题目也可能被训练使用。
- 来源：https://github.com/LiveCodeBench/LiveCodeBench
- 来源：https://arxiv.org/abs/2403.07974
- 事件：paper_submission · 2024-03-12 · sys-event-livecodebench-paper-v1 · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 arXiv Submission history v1 · 来源 https://arxiv.org/abs/2403.07974

## GPQA

研究生层次问答评测；主集与Diamond等子集、选项顺序和是否可检索应明确标注。

- ID / 类型：sys-gpqa / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-gpqa']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：从官方入口获取
- 学习步骤（未执行）：尊重防污染提示
- 学习步骤（未执行）：固定子集与随机种子
- 学习步骤（未执行）：分开closed-book/open-book结果。
- 评测/数据集登记：{"node_id": "sys-gpqa", "availability": "public_download", "license": "官方仓库显示MIT；内容再分发仍需复核适用范围", "split": "main/diamond等必须指明", "access_url": "https://github.com/idavidrein/gpqa", "access_application_url": null, "access_application_note": "以数据卡当日访问条款为准", "metric": "多项选择accuracy", "protocol": "选项shuffle种子、few-shot、CoT、open/closed-book", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "本轮只审阅来源，未下载数据或执行评测；运行时须锁定revision、prompt、seed及环境。", "checked_at": "2026-10-28", "source_ids": ["sys-src-gpqa"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://github.com/idavidrein/gpqa"}}
- 注意：Google-proof是评测设计描述，不是对所有搜索或未来模型的绝对保证。
- 来源：https://github.com/idavidrein/gpqa

## FrontierMath Tiers 1–4

官方描述的未公开高难数学题评测；与公开研究问题分支不是同一题库。

- ID / 类型：sys-frontiermath / benchmark
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-frontier']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：阅读公开方法和结果
- 学习步骤（未执行）：向运营方询问合法评测入口
- 学习步骤（未执行）：记录tier/工具/预算
- 学习步骤（未执行）：不传播未授权题目。
- 评测/数据集登记：{"node_id": "sys-frontiermath", "availability": "private_described", "license": "未授权公开完整题库；仅公开metadata", "split": "仅本节点Tiers 1–4；不混同Open Problems", "access_url": "https://epoch.ai/frontiermath", "access_application_url": "https://epoch.ai/frontiermath", "access_application_note": "公开项目页入口，不声称已提供自助申请或已获准", "metric": "正确解决比例；需运营方口径", "protocol": "tier、工具、推理预算、判分与独立验证情况", "contamination": "须报告训练数据截止与重合检查；公开题目可能被训练使用；未检出不等于零污染。", "reproducibility": "无法独立获得完整题库；只登记公开描述，不获取秘密题或答案。", "checked_at": "2026-10-28", "source_ids": ["sys-src-frontier"], "display_policy": "只展示公开介绍、口径、来源及跳转链接；不镜像试题、答案、受限集或整套语料。", "results_preview": {"scores": [], "status": "not_imported", "reason_zh": "本轮未固化模型版本/配置一致的成绩快照，避免误导排名；跳转官方结果入口。", "official_results_url": "https://epoch.ai/frontiermath"}}
- 注意：不能因公开了样例或成绩就称完整题集开源；无法独立取得全部题目时明确复现限制。
- 来源：https://epoch.ai/frontiermath

## LM Evaluation Harness

统一组织多任务语言模型评测的框架；任务配置、模型接口和版本共同决定评分口径。

- ID / 类型：sys-harness / framework
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-harness']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：固定commit和任务YAML
- 学习步骤（未执行）：锁定数据版本
- 学习步骤（未执行）：保存完整配置
- 学习步骤（未执行）：对少量样本检查prompt及答案映射。
- 注意：工具统一不意味着不同配置的结果可比；新版任务定义可能改变旧分数。
- 来源：https://github.com/EleutherAI/lm-evaluation-harness

## 评测污染与可复现性

训练/调优数据与测试数据重合会削弱泛化结论；需要区分显式泄漏、近重复和题型学习。

- ID / 类型：sys-contamination / practice
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-livepaper', 'sys-src-harness']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：记录数据截止日期
- 学习步骤（未执行）：做精确/近重复审查
- 学习步骤（未执行）：隔离开发与测试
- 学习步骤（未执行）：保留评测代码和预算
- 学习步骤（未执行）：披露未知项。
- 注意：未检出污染不是证明没有污染；私有测试也不自动保证公平与可复现。
- 来源：https://arxiv.org/abs/2403.07974
- 来源：https://github.com/EleutherAI/lm-evaluation-harness

## Model Context Protocol

在host、client和server间连接工具、资源与提示的开放协议；本节点固定2025-06-18规范。

- ID / 类型：sys-mcp / protocol
- 生命周期：{'status': 'historical_pinned_specification', 'as_of': '2026-10-28', 'applicable_version': 'MCP specification 2025-06-18 (historical pinned version; not claimed latest)', 'replacement_node_ids': [], 'note_zh': '为保证可复查固定2025-06-18规范；不声称其为当前最新版本；替代版本本轮未核验。', 'source_ids': ['sys-src-mcp', 'sys-src-mcpnews']}
- 版本：MCP specification 2025-06-18 (historical pinned version; not claimed latest)
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：区分三种角色
- 学习步骤（未执行）：协商能力
- 学习步骤（未执行）：验证输入输出schema
- 学习步骤（未执行）：按权限调用
- 学习步骤（未执行）：记录审计并处理不可信工具内容。
- 注意：协议兼容不等于工具安全或模型更聪明；MCP本身不是权重、记忆数据库或训练方法。
- 来源：https://modelcontextprotocol.io/specification/2025-06-18
- 来源：https://www.anthropic.com/news/model-context-protocol
- 事件：announcement · 2024-11-25 · sys-event-mcp-announced · 精度 day · 时区 未知 · 范围 未核验 · 版本 未核验 · 截至已可用（非首发） 无独立观察 · 说明  · 证据 Official announcement Published Nov 25, 2024; describes open-sourcing protocol · 来源 https://www.anthropic.com/news/model-context-protocol

## Agent Skills

以SKILL.md元数据与正文组织的可发现指令包，可附脚本、参考资料和资源；加载与执行由宿主决定。

- ID / 类型：sys-skills / instruction_package
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-skills']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：写明确触发描述
- 学习步骤（未执行）：提供步骤/失败边界
- 学习步骤（未执行）：逐步加载参考资料
- 学习步骤（未执行）：审查脚本权限
- 学习步骤（未执行）：用任务测试触发与结果。
- 注意：skill不是参数微调；allowed-tools字段不是绕过宿主授权；文档可能携带不可信指令。
- 来源：https://agentskills.io/specification

## SWE-agent

将模型与软件工程环境及操作循环结合以修复问题的研究项目；官方现提示转向mini-SWE-agent。

- ID / 类型：sys-sweagent / agent_framework
- 生命周期：{'status': 'superseded_per_maintainer', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': ['sys-miniagent'], 'note_zh': '官方README明确推荐今后采用mini-SWE-agent；保留SWE-agent用于历史设计学习。', 'source_ids': ['sys-src-sweagent']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：读历史设计
- 学习步骤（未执行）：固定环境与仓库
- 学习步骤（未执行）：观察读文件/编辑/测试循环
- 学习步骤（未执行）：保存补丁和轨迹
- 学习步骤（未执行）：人工审阅。
- 注意：框架名字不是特定模型；历史SOTA和当前推荐不能混为一谈。
- 来源：https://github.com/SWE-agent/SWE-agent

## mini-SWE-agent

以简洁实现组织模型、执行环境和循环；当前仓库提示v2，历史v1需单独查看。

- ID / 类型：sys-miniagent / agent_framework
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '当前所读README标记v2；v1另分支，未锁定commit', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-mini']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：阅读agent/model/environment分层
- 学习步骤（未执行）：选择隔离环境
- 学习步骤（未执行）：限制预算
- 学习步骤（未执行）：记录每次动作
- 学习步骤（未执行）：测试并检查diff。
- 注意：短代码不代表低风险；不同模型后端与工具预算仍会改变结果。
- 来源：https://github.com/SWE-agent/mini-swe-agent

## OpenHands

面向软件开发的agent项目；执行环境与宿主挂载路径决定能读取和修改哪些资源。

- ID / 类型：sys-openhands / agent_framework
- 生命周期：{'status': 'current_documentation_reviewed', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-openhands']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：检查版本与部署模式
- 学习步骤（未执行）：仅挂载授权项目
- 学习步骤（未执行）：使用隔离环境
- 学习步骤（未执行）：保存轨迹/补丁
- 学习步骤（未执行）：测试后请求合并。
- 注意：无沙箱模式可能获得宿主文件系统访问；容器也不自动隔离全部网络和挂载目录。
- 来源：https://github.com/OpenHands/OpenHands

## 提示词与任务契约

把任务目标、输入、输出、限制、证据要求和完成标准写清；是应用层工程而非模型新增能力。

- ID / 类型：sys-promptcontracts / practice
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-skills', 'sys-src-mcp']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：明确产物
- 学习步骤（未执行）：给定可信上下文与输出schema
- 学习步骤（未执行）：列明工具边界
- 学习步骤（未执行）：提供可判定验收
- 学习步骤（未执行）：用反例测试。
- 注意：长提示不必然更好；检索文档中的指令不能替代用户授权。
- 来源：https://agentskills.io/specification
- 来源：https://modelcontextprotocol.io/specification/2025-06-18

## 不同模型的部署学习路径

模型家族教程应落到具体模型ID、revision、许可证、分词器/聊天模板及运行时支持；避免一条命令套全部模型。

- ID / 类型：sys-modelpath / learning_path
- 生命周期：{'status': 'reference_concept_or_dataset', 'as_of': '2026-10-28', 'applicable_version': '研究快照 2026-10-28；实际运行需固定revision', 'replacement_node_ids': [], 'note_zh': '收录不等于推荐生产采用；运行兼容性需按固定版本重新核验。', 'source_ids': ['sys-src-vllm', 'sys-src-llama', 'sys-src-mlx']}
- 版本：研究快照 2026-10-28；实际运行需固定revision
- 核验：2026-10-28 · primary_sources_reviewed_not_executed
- 学习步骤（未执行）：先查模型卡
- 学习步骤（未执行）：选择vLLM/llama.cpp/MLX适配路线
- 学习步骤（未执行）：记录精度和上下文
- 学习步骤（未执行）：小规模验收
- 学习步骤（未执行）：同口径对比。
- 注意：API协议兼容不代表所有模型支持相同工具调用或多模态；本研究未实测任何设备。
- 来源：https://docs.vllm.ai/en/stable/features/quantization/index.html
- 来源：https://github.com/ggml-org/llama.cpp
- 来源：https://github.com/ml-explore/mlx-lm

## 历史报告成绩快照（非排行榜，非独立复现）

### GPT-4历史报告：MMLU
- model：GPT-4 (pre-trained base model)
- model_version：未知
- model_version_note：报告正文p6明确为pre-trained base；精确checkpoint/API标识未披露，不能视作当前GPT-4服务。
- benchmark_version：未知
- benchmark_version_note：报告所用具体数据revision未在已核验表格中提供。
- split：未知
- split_note：已核验表格未给出明确split，不补猜test revision。
- metric：reported benchmark score
- unit：%
- harness：未知
- harness_note：未独立核验可复现harness版本；不推定OpenAI Evals提交。
- report_date：2024-03-04
- report_first_published_date：未知
- report_version：arXiv:2303.08774v6
- checked_at：2026-10-28
- source_url：https://arxiv.org/pdf/2303.08774v6
- reported_by：OpenAI — original report self-reported
- evidence_type：primary_report_aggregate_metadata
- verification_status：primary_report_checked_not_independently_reproduced
- limitations_zh：历史报告自报数据，仅核对公开汇总值与表格口径；本站未运行评测。并非当前API表现，不形成排名，不能与其他shot、prompt、版本或数据切分横比。
- id：gpt4-v6-mmlu
- title：GPT-4历史报告：MMLU
- benchmark：MMLU (English)
- value：86.4
- shot：5
- shot_note：Table 2 GPT-4列明确列示shot数量。
- evidence_locator：PDF p7 Table 2；模型为预训练base的说明见p6；不是译文MMLU的Figure 5。
- prompt：few-shot；多选题展示选项并要求返回答案字母（Table 2说明）。
- node_id：sys-mmlu

### GPT-4历史报告：ARC Challenge
- model：GPT-4 (pre-trained base model)
- model_version：未知
- model_version_note：报告正文p6明确为pre-trained base；精确checkpoint/API标识未披露，不能视作当前GPT-4服务。
- benchmark_version：未知
- benchmark_version_note：报告所用具体数据revision未在已核验表格中提供。
- split：未知
- split_note：已核验表格未给出明确split，不补猜test revision。
- metric：reported benchmark score
- unit：%
- harness：未知
- harness_note：未独立核验可复现harness版本；不推定OpenAI Evals提交。
- report_date：2024-03-04
- report_first_published_date：未知
- report_version：arXiv:2303.08774v6
- checked_at：2026-10-28
- source_url：https://arxiv.org/pdf/2303.08774v6
- reported_by：OpenAI — original report self-reported
- evidence_type：primary_report_aggregate_metadata
- verification_status：primary_report_checked_not_independently_reproduced
- limitations_zh：历史报告自报数据，仅核对公开汇总值与表格口径；本站未运行评测。并非当前API表现，不形成排名，不能与其他shot、prompt、版本或数据切分横比。
- id：gpt4-v6-arc
- title：GPT-4历史报告：ARC Challenge
- benchmark：AI2 Reasoning Challenge — Challenge-set
- value：96.3
- shot：25
- shot_note：Table 2 GPT-4列明确列示shot数量。
- evidence_locator：PDF p7 Table 2；模型为预训练base的说明见p6；不是译文MMLU的Figure 5。
- prompt：few-shot；多选题展示选项并要求返回答案字母（Table 2说明）。

### GPT-4历史报告：GSM-8K
- model：GPT-4 (pre-trained base model)
- model_version：未知
- model_version_note：报告正文p6明确为pre-trained base；精确checkpoint/API标识未披露，不能视作当前GPT-4服务。
- benchmark_version：未知
- benchmark_version_note：报告所用具体数据revision未在已核验表格中提供。
- split：未知
- split_note：已核验表格未给出明确split，不补猜test revision。
- metric：reported benchmark score
- unit：%
- harness：未知
- harness_note：未独立核验可复现harness版本；不推定OpenAI Evals提交。
- report_date：2024-03-04
- report_first_published_date：未知
- report_version：arXiv:2303.08774v6
- checked_at：2026-10-28
- source_url：https://arxiv.org/pdf/2303.08774v6
- reported_by：OpenAI — original report self-reported
- evidence_type：primary_report_aggregate_metadata
- verification_status：primary_report_checked_not_independently_reproduced
- limitations_zh：历史报告自报数据，仅核对公开汇总值与表格口径；本站未运行评测。并非当前API表现，不形成排名，不能与其他shot、prompt、版本或数据切分横比。 报告明确部分GSM-8K训练集加入预训练混合；该分数使用CoT，不可据此声称无训练污染。
- id：gpt4-v6-gsm8k
- title：GPT-4历史报告：GSM-8K
- benchmark：GSM-8K
- value：92.0
- shot：5
- shot_note：Table 2 GPT-4列明确列示shot数量。
- evidence_locator：PDF p7 Table 2 GSM-8K行及表下注释；p6脚注6。
- prompt：5-shot chain-of-thought（Table 2）
- node_id：sys-gsm8k

## 关系索引（教学建议不代表历史因果）
- design-dtcg → provides_design_context → design-figma-mcp · editorial_learning_relation_not_vendor_integration_claim · design-src-figma, design-src-figma-access, design-src-tokens, design-src-tokens-draft
- design-wcag → guides_evaluation → design-storybook-a11y · editorial_learning_relation_not_vendor_integration_claim · design-src-sb-license, design-src-storybook, design-src-wcag
- design-photoshop-v1 → superseded_by → design-photoshop-v2 · editorial_learning_relation_not_vendor_integration_claim · design-src-ps-migration, design-src-photoshop
- design-c2pa → audits_provenance → design-firefly-image · editorial_learning_relation_not_vendor_integration_claim · design-src-c2pa, design-src-firefly, design-src-adobe-rights
- design-visual-regression → evaluates_output → design-figma-mcp · editorial_learning_relation_not_vendor_integration_claim · design-src-pw-license, design-src-figma, design-src-playwright, design-src-figma-access
- vid-whisperx → uses → vid-whisper · primary_sources_reviewed_not_executed · vid-src-whisperx
- vid-ltx-video → superseded_by → vid-ltx2 · primary_sources_reviewed_not_executed · vid-src-ltxv
- vid-vimax → learning_path → vid-wan22 · editorial_learning_relation ·
- vid-filmagent → learning_path → vid-otio · editorial_learning_relation ·
- vid-videoagent-edit → learning_path → vid-ffmpeg · editorial_learning_relation ·
- vid-comfyui → learning_path → vid-otio · editorial_learning_relation ·
- vid-wan22 → learning_path → vid-whisper · editorial_learning_relation ·
- vid-whisper → learning_path → vid-kdenlive · editorial_learning_relation ·
- vid-kdenlive → learning_path → vid-otio · editorial_learning_relation ·
- llama-2 → version_of → llama · primary_source_checked · found-src-026
- llama → developed_by → org-llama · primary_source_checked · found-src-026
- qwen-2023 → version_of → qwen · primary_source_checked · found-src-027
- qwen → developed_by → org-qwen · primary_source_checked · found-src-027
- mistral-7b-v0-1 → version_of → mistral · primary_source_checked · found-src-028
- mistral → developed_by → org-mistral · primary_source_checked · found-src-028
- bloom-176b → version_of → bloom · primary_source_checked · found-src-029
- bloom → developed_by → org-bloom · primary_source_checked · found-src-029
- gemini-1-report → version_of → gemini · primary_source_checked · found-src-017
- gemini → developed_by → org-gemini · primary_source_checked · found-src-017
- falcon-180b → version_of → falcon · primary_source_checked · found-src-030
- falcon → developed_by → org-falcon · primary_source_checked · found-src-030
- jais-13b → version_of → jais · primary_source_checked · found-src-031
- jais → developed_by → org-jais · primary_source_checked · found-src-031
- aya-101 → version_of → aya · primary_source_checked · found-src-032
- aya → developed_by → org-aya · primary_source_checked · found-src-032
- baichuan-2 → version_of → baichuan · primary_source_checked · found-src-033
- baichuan → developed_by → org-baichuan · primary_source_checked · found-src-033
- nlp → prerequisite_of → tokenization · editorial_learning_relation · found-src-001
- tokenization → prerequisite_of → embeddings · editorial_learning_relation · found-src-002
- tokenization → prerequisite_of → language-modeling · editorial_learning_relation · found-src-001
- embeddings → prerequisite_of → word2vec · editorial_learning_relation · found-src-002
- language-modeling → prerequisite_of → seq2seq · editorial_learning_relation · found-src-003
- seq2seq → prerequisite_of → attention · editorial_learning_relation · found-src-004
- attention → prerequisite_of → transformer · editorial_learning_relation · found-src-005
- transformer → prerequisite_of → pretraining · editorial_learning_relation · found-src-006
- pretraining → prerequisite_of → instruction-tuning · editorial_learning_relation · found-src-009
- instruction-tuning → prerequisite_of → rlhf · editorial_learning_relation · found-src-009
- rlhf → prerequisite_of → dpo · editorial_learning_relation · found-src-011
- rlhf → prerequisite_of → reasoning-models · editorial_learning_relation · found-src-013
- pretraining → prerequisite_of → multimodal · editorial_learning_relation · found-src-016, found-src-017
- multimodal → prerequisite_of → clip · editorial_learning_relation · found-src-016
- multimodal → prerequisite_of → llava · editorial_learning_relation · found-src-018
- in-context-learning → prerequisite_of → agents · editorial_learning_relation · found-src-021
- agents → prerequisite_of → react · editorial_learning_relation · found-src-021
- agents → prerequisite_of → rsi · editorial_learning_relation · found-src-022, found-src-023
- bert → uses → transformer · primary_source_checked · found-src-007
- t5 → uses → transformer · primary_source_checked · found-src-006
- gpt-3 → uses → transformer · primary_source_checked · found-src-008
- llava → uses → multimodal · primary_source_checked · found-src-018
- constitutional-ai → uses → rlhf · primary_source_checked · found-src-010
- deepseek-r1-2025 → uses → reasoning-models · primary_source_checked · found-src-013, found-src-014
- bert → evaluated_by → glue · primary_source_checked · found-src-007
- baichuan-2 → evaluated_by → mmlu · primary_source_checked · found-src-033
- gpt-3 → version_of → gpt · primary_source_checked · found-src-008
- deepseek-r1-2025 → version_of → deepseek · primary_source_checked · found-src-013, found-src-014
- gpt → developed_by → org-openai · primary_source_checked · found-src-008, found-src-009, found-src-016
- clip → developed_by → org-openai · primary_source_checked · found-src-008, found-src-009, found-src-016
- whisper → developed_by → org-openai · primary_source_checked · found-src-008, found-src-009, found-src-016
- deepseek → developed_by → org-deepseek · primary_source_checked · found-src-013, found-src-014
- constitutional-ai → introduced_by → org-anthropic · primary_source_checked · found-src-010
- react → instance_of → agents · primary_source_checked · found-src-021
- stop → investigates → rsi · research_claim_scoped · found-src-023
- godel-machine → formalizes → rsi · research_claim_scoped · found-src-022
- sarvam-1 → version_of → sarvam · primary_source_checked · found-src-034
- sys-pagedattention → prerequisite_for → sys-vllm · editorial_learning_relation · sys-src-vllm, sys-src-paged
- sys-gguf → prerequisite_for → sys-llamacpp · editorial_learning_relation · sys-src-llama, sys-src-gguf
- sys-vectorsearch → prerequisite_for → sys-faiss · editorial_learning_relation · sys-src-faiss
- sys-vectorsearch → prerequisite_for → sys-pgvector · editorial_learning_relation · sys-src-pg
- sys-vectorsearch → prerequisite_for → sys-qdrant · editorial_learning_relation · sys-src-qdrant
- sys-vectorsearch → prerequisite_for → sys-milvus · editorial_learning_relation · sys-src-milvus
- sys-rag → prerequisite_for → sys-memory · editorial_learning_relation · sys-src-memory
- sys-memory → prerequisite_for → sys-memgpt · editorial_learning_relation · sys-src-memgpt
- sys-humaneval → prerequisite_for → sys-swebench · editorial_learning_relation · sys-src-swe
- sys-humaneval → prerequisite_for → sys-livecodebench · editorial_learning_relation · sys-src-live, sys-src-livepaper
- sys-livecodebench → prerequisite_for → sys-contamination · editorial_learning_relation · sys-src-livepaper, sys-src-harness
- sys-harness → prerequisite_for → sys-contamination · editorial_learning_relation · sys-src-livepaper, sys-src-harness
- sys-swebench → prerequisite_for → sys-sweagent · editorial_learning_relation · sys-src-sweagent
- sys-swebench → prerequisite_for → sys-miniagent · editorial_learning_relation · sys-src-mini
- sys-swebench → prerequisite_for → sys-openhands · editorial_learning_relation · sys-src-openhands
- sys-skills → prerequisite_for → sys-promptcontracts · editorial_learning_relation · sys-src-skills, sys-src-mcp
- sys-mcp → prerequisite_for → sys-promptcontracts · editorial_learning_relation · sys-src-skills, sys-src-mcp
- sys-vllm → prerequisite_for → sys-modelpath · editorial_learning_relation · sys-src-vllm, sys-src-llama, sys-src-mlx
- sys-llamacpp → prerequisite_for → sys-modelpath · editorial_learning_relation · sys-src-vllm, sys-src-llama, sys-src-mlx
- sys-mlx → prerequisite_for → sys-modelpath · editorial_learning_relation · sys-src-vllm, sys-src-llama, sys-src-mlx
- sys-llamacpp → loads_format → sys-gguf · source_supported_or_explicit_distinction · sys-src-llama
- sys-vllm → implements → sys-pagedattention · source_supported_or_explicit_distinction · sys-src-paged
- sys-vllm → supports_method_conditionally → sys-awq · source_supported_or_explicit_distinction · sys-src-vllm
- sys-vllm → supports_method_conditionally → sys-gptq · source_supported_or_explicit_distinction · sys-src-vllm
- sys-sweagent → evaluated_on → sys-swebench · source_supported_or_explicit_distinction · sys-src-swe
- sys-miniagent → evaluated_on → sys-swebench · source_supported_or_explicit_distinction · sys-src-swe
- sys-skills → complementary_not_equivalent → sys-mcp · source_supported_or_explicit_distinction · sys-src-skills
- sys-memory → distinct_from → sys-pagedattention · source_supported_or_explicit_distinction · sys-src-memory
- rag → extends → sys-rag · editorial_cross_module · sys-src-rag

## 来源目录
- design-src-figma · https://developers.figma.com/docs/figma-mcp-server/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-figma-access · https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-firefly · https://developer.adobe.com/firefly-services/docs/firefly-api/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-photoshop · https://developer.adobe.com/firefly-services/docs/photoshop/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-ps-migration · https://developer.adobe.com/firefly-services/docs/photoshop/guides/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-canva · https://www.canva.dev/docs/apps/rest-apis/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-canva-autofill · https://www.canva.dev/docs/apps/rest-apis/autofill-guide/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-canva-rights · https://www.canva.com/policies/content-license-agreement/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-tokens · https://www.designtokens.org/TR/2025.10/format/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-tokens-draft · https://www.designtokens.org/tr/drafts/format/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-wcag · https://www.w3.org/TR/WCAG22/ · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-inkscape · https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-slides · https://developers.google.com/workspace/slides/api/guides/overview · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-playwright · https://playwright.dev/docs/test-snapshots · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-storybook · https://storybook.js.org/docs/writing-tests/accessibility-testing · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-c2pa · https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-adobe-rights · https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-pw-license · https://github.com/microsoft/playwright/blob/main/LICENSE · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-sb-license · https://github.com/storybookjs/storybook/blob/next/LICENSE · 核验 2026-10-28 · 仅核验公开文档；未登录、调用付费API、下载模型或运行第三方软件。
- design-src-ps-eol · https://developer.adobe.com/firefly-services/docs/photoshop/getting-started/deprecation-announcement/ · 核验 2026-10-28 · 独立审查反馈后实际打开核验；未执行服务。
- design-src-c2pa-explainer · https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html · 核验 2026-10-28 · 独立审查反馈后实际打开核验；未执行服务。
- music-src-musicgen · https://github.com/facebookresearch/audiocraft/blob/main/model_cards/MUSICGEN_MODEL_CARD.md · 核验 2026-10-28 · 原始来源页面
- music-src-jasco · https://github.com/facebookresearch/audiocraft/blob/main/docs/JASCO.md · 核验 2026-10-28 · 原始来源页面
- music-src-jasco-card · https://github.com/facebookresearch/audiocraft/blob/main/model_cards/JASCO_MODEL_CARD.md · 核验 2026-10-28 · 原始来源页面
- music-src-stable · https://stability.ai/news-updates/stable-audio-open-research-paper · 核验 2026-10-28 · 原始来源页面
- music-src-stable-license · https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md · 核验 2026-10-28 · 原始来源页面
- music-src-demucs · https://github.com/facebookresearch/demucs · 核验 2026-10-28 · 原始来源页面
- music-src-whisper · https://github.com/openai/whisper · 核验 2026-10-28 · 原始来源页面
- music-src-asr · https://developers.openai.com/api/docs/guides/speech-to-text · 核验 2026-10-28 · 原始来源页面
- music-src-lyria · https://ai.google.dev/gemini-api/docs/music-generation · 核验 2026-10-28 · 原始来源页面
- music-src-suno-new · https://www.suno.com/blog/suno-updates-tos · 核验 2026-10-28 · 原始来源页面
- music-src-suno-old · https://help.suno.com/en/articles/2410177 · 核验 2026-10-28 · 原始来源页面
- music-src-neutron · https://www.izotope.com/products/neutron/ · 核验 2026-10-28 · 原始来源页面
- music-src-ozone · https://docs.izotope.com/ozone12/en/index-en.html · 核验 2026-10-28 · 原始来源页面
- music-src-auphonic · https://us1.auphonic.com/help/algorithms/multitrack.html · 核验 2026-10-28 · 原始来源页面
- music-src-sfx · https://elevenlabs.io/docs/overview/capabilities/sound-effects · 核验 2026-10-28 · 原始来源页面
- music-src-tts · https://elevenlabs.io/docs/overview/capabilities/text-to-speech · 核验 2026-10-28 · 原始来源页面
- music-src-captions · https://www.w3.org/WAI/media/av/captions/ · 核验 2026-10-28 · 原始来源页面
- music-src-mrt · https://github.com/magenta/magenta-realtime · 核验 2026-10-28 · 原始来源页面
- vid-src-wan · https://github.com/Wan-Video/Wan2.2 · 核验 2026-10-28 · 官方公开推理代码与权重；5B TI2V示例24GB显存，A14B I2V及S2V示例80GB；这是指定配置的门槛，不是所有流程的成本。
- vid-src-ltxv · https://github.com/Lightricks/LTX-Video · 核验 2026-10-28 · 维护者声明LTX-2是主要开发入口；保留旧流程用于历史比较，迁移必须重核权重和接口。
- vid-src-ltx2 · https://github.com/Lightricks/LTX-2 · 核验 2026-10-28 · 官方音视频生成与LoRA训练仓库；存在多份许可，不能从开放代码推断全部权重无条件商用。
- vid-src-cog · https://github.com/zai-org/CogVideo · 核验 2026-10-28 · 旧THUDM URL跳转此官方仓库；2B与5B权重许可不同，代码Apache-2.0并不覆盖所有权重。
- vid-src-cogpaper · https://arxiv.org/abs/2408.06072 · 核验 2026-10-28 · 视频时空VAE和扩散Transformer方法；论文版本性能不等于每个历史权重规格。
- vid-src-animatediff · https://github.com/guoyww/AnimateDiff · 核验 2026-10-28 · 运动模块框架，不是完整制片Agent；基础图像权重与LoRA许可另查。
- vid-src-animatepaper · https://arxiv.org/abs/2307.04725 · 核验 2026-10-28 · 为同一基础图像模型家族增加可迁移运动模块；历史方法教学保留，不声称官方弃用。
- vid-src-tune · https://github.com/showlab/Tune-A-Video · 核验 2026-10-28 · 单视频微调研究实现；不能默认兼容最新环境。
- vid-src-tunepaper · https://arxiv.org/abs/2212.11565 · 核验 2026-10-28 · 单视频微调与结构引导的历史路线。
- vid-src-comfy · https://github.com/Comfy-Org/ComfyUI · 核验 2026-10-28 · 图式推理编排工具；自定义节点是代码供应链边界，图本身不等于自主Agent。
- vid-src-whisper · https://github.com/openai/whisper · 核验 2026-10-28 · 自动语音识别工具/模型；不是配音或音色克隆。
- vid-src-whisperx · https://github.com/m-bain/whisperX · 核验 2026-10-28 · 支持对齐流程；重叠语音及字典外内容有局限；说话人分离路径需要额外模型协议和令牌，本任务不启用。
- vid-src-ffmpeg · https://ffmpeg.org/ffmpeg.html · 核验 2026-10-28 · 媒体处理工具；使用前核验构建参数和编码器许可。
- vid-src-otio · https://github.com/AcademySoftwareFoundation/OpenTimelineIO · 核验 2026-10-28 · 剪辑时间线交换数据与API，不是视频渲染器。
- vid-src-kdenlive · https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html · 核验 2026-10-28 · 官方文档描述转录、字幕和按转录选片；功能需先配置识别引擎与模型。
- vid-src-filmagent · https://filmagent.github.io/ · 核验 2026-10-28 · 虚拟3D空间的多角色制片研究；不能外推为任意实拍场景或免费端到端电影制作。
- vid-src-vimax · https://github.com/HKUDS/ViMax · 核验 2026-10-28 · Agent编排脚本分镜及生成；示例要求LLM/图像/视频API配置，不能等同已支持无账号本地免费替代。
- vid-src-videoagent · https://github.com/HKUDS/VideoAgent · 核验 2026-10-28 · 视频理解、编辑、重制Agent框架；仅核验文档，无独立复现。
- vid-src-videoagentpaper · https://arxiv.org/abs/2606.23327 · 核验 2026-10-28 · 编辑Agent研究；不导入作者成绩为通用质量承诺。
- vid-src-understand · https://arxiv.org/abs/2403.10517 · 核验 2026-10-28 · 长视频理解问答Agent，与HKUDS编辑框架同名但不是同一项目。
- found-src-001 · https://web.stanford.edu/~jurafsky/slp3/ · 核验 2026-10-28 · official_page
- found-src-002 · https://arxiv.org/abs/1301.3781 · 核验 2026-10-28 · metadata_and_abstract
- found-src-003 · https://arxiv.org/abs/1409.3215 · 核验 2026-10-28 · metadata_and_abstract
- found-src-004 · https://arxiv.org/abs/1409.0473 · 核验 2026-10-28 · metadata_and_abstract
- found-src-005 · https://arxiv.org/abs/1706.03762 · 核验 2026-10-28 · metadata_and_abstract
- found-src-006 · https://arxiv.org/abs/1910.10683 · 核验 2026-10-28 · metadata_and_abstract
- found-src-007 · https://arxiv.org/abs/1810.04805 · 核验 2026-10-28 · metadata_and_abstract
- found-src-008 · https://arxiv.org/abs/2005.14165 · 核验 2026-10-28 · metadata_and_abstract
- found-src-009 · https://arxiv.org/abs/2203.02155 · 核验 2026-10-28 · metadata_and_abstract
- found-src-010 · https://arxiv.org/abs/2212.08073 · 核验 2026-10-28 · metadata_and_abstract
- found-src-011 · https://arxiv.org/abs/2305.18290 · 核验 2026-10-28 · metadata_and_abstract
- found-src-012 · https://arxiv.org/abs/2201.11903 · 核验 2026-10-28 · metadata_and_abstract
- found-src-013 · https://arxiv.org/abs/2501.12948 · 核验 2026-10-28 · metadata_and_abstract
- found-src-014 · https://github.com/deepseek-ai/DeepSeek-R1 · 核验 2026-10-28 · official_page
- found-src-015 · https://arxiv.org/abs/2005.11401 · 核验 2026-10-28 · metadata_and_abstract
- found-src-016 · https://arxiv.org/abs/2103.00020 · 核验 2026-10-28 · metadata_and_abstract
- found-src-017 · https://arxiv.org/abs/2312.11805 · 核验 2026-10-28 · metadata_and_abstract
- found-src-018 · https://arxiv.org/abs/2304.08485 · 核验 2026-10-28 · metadata_and_abstract
- found-src-019 · https://arxiv.org/abs/2212.04356 · 核验 2026-10-28 · metadata_and_abstract
- found-src-020 · https://arxiv.org/abs/2112.10752 · 核验 2026-10-28 · metadata_and_abstract
- found-src-021 · https://arxiv.org/abs/2210.03629 · 核验 2026-10-28 · metadata_and_abstract
- found-src-022 · https://arxiv.org/abs/cs/0309048 · 核验 2026-10-28 · metadata_and_abstract
- found-src-023 · https://arxiv.org/abs/2310.02304 · 核验 2026-10-28 · metadata_and_abstract
- found-src-024 · https://arxiv.org/abs/1804.07461 · 核验 2026-10-28 · metadata_and_abstract
- found-src-025 · https://arxiv.org/abs/2009.03300 · 核验 2026-10-28 · metadata_and_abstract
- found-src-026 · https://arxiv.org/abs/2307.09288 · 核验 2026-10-28 · metadata_and_abstract
- found-src-027 · https://arxiv.org/abs/2309.16609 · 核验 2026-10-28 · metadata_and_abstract
- found-src-028 · https://arxiv.org/abs/2310.06825 · 核验 2026-10-28 · metadata_and_abstract
- found-src-029 · https://arxiv.org/abs/2211.05100 · 核验 2026-10-28 · metadata_and_abstract
- found-src-030 · https://arxiv.org/abs/2311.16867 · 核验 2026-10-28 · metadata_and_abstract
- found-src-031 · https://arxiv.org/abs/2308.16149 · 核验 2026-10-28 · metadata_and_abstract
- found-src-032 · https://arxiv.org/abs/2402.07827 · 核验 2026-10-28 · metadata_and_abstract
- found-src-033 · https://arxiv.org/abs/2309.10305 · 核验 2026-10-28 · metadata_and_abstract
- found-src-034 · https://huggingface.co/sarvamai/sarvam-1 · 核验 2026-10-28 · official_page
- sys-src-vllm · https://docs.vllm.ai/en/stable/features/quantization/index.html · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-paged · https://arxiv.org/abs/2309.06180 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-llama · https://github.com/ggml-org/llama.cpp · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-mlx · https://github.com/ml-explore/mlx-lm · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-gptq · https://arxiv.org/abs/2210.17323 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-awq · https://arxiv.org/abs/2306.00978 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-qlora · https://arxiv.org/abs/2305.14314 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-gguf · https://github.com/ggml-org/ggml/blob/master/docs/gguf.md · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-safe · https://huggingface.co/docs/safetensors/index · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-rag · https://arxiv.org/abs/2005.11401 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-faiss · https://github.com/facebookresearch/faiss · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-pg · https://github.com/pgvector/pgvector · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-qdrant · https://qdrant.tech/documentation/manage-data/collections/ · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-milvus · https://milvus.io/docs/overview.md · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-memgpt · https://arxiv.org/abs/2310.08560 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-memory · https://docs.langchain.com/oss/python/concepts/memory · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-fineweb · https://huggingface.co/datasets/HuggingFaceFW/fineweb · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-dolma · https://huggingface.co/datasets/allenai/dolma · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-stack · https://huggingface.co/datasets/bigcode/the-stack-v2 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-c4 · https://huggingface.co/datasets/allenai/c4 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-mmlu · https://github.com/hendrycks/test · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-gsm · https://github.com/openai/grade-school-math · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-human · https://github.com/openai/human-eval · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-swe · https://www.swebench.com/ · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-mcp · https://modelcontextprotocol.io/specification/2025-06-18 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-mcpnews · https://www.anthropic.com/news/model-context-protocol · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-skills · https://agentskills.io/specification · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-sweagent · https://github.com/SWE-agent/SWE-agent · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-openhands · https://github.com/OpenHands/OpenHands · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-harness · https://github.com/EleutherAI/lm-evaluation-harness · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-live · https://github.com/LiveCodeBench/LiveCodeBench · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-livepaper · https://arxiv.org/abs/2403.07974 · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-frontier · https://epoch.ai/frontiermath · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-gpqa · https://github.com/idavidrein/gpqa · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- sys-src-mini · https://github.com/SWE-agent/mini-swe-agent · 核验 2026-10-28 · 仅元数据与原创摘要；未下载或执行项目。
- timeline-r1-src-001 · https://openai.com/index/openai-api/ · 核验 2026-10-28 · 官方正文明确GPT-3家族驱动API，并明确当日为private beta而非GA。
- timeline-r1-src-002 · https://ai.meta.com/blog/llama-2/ · 核验 2026-10-28 · 当日宣布Llama 2可用，并明确包含预训练和对话微调模型权重及起始代码。
- timeline-r1-src-003 · https://mistral.ai/news/announcing-mistral-7b/ · 核验 2026-10-28 · 公告当日发布Mistral 7B并提供模型下载；Apache 2.0。部署到云不等于厂商API上线。
- timeline-r1-src-004 · https://huggingface.co/blog/bloom · 核验 2026-10-28 · 当日发布176B BLOOM，说明可下载权重，且已有供小规模测试及原型使用的推理API。
- timeline-r1-src-005 · https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/ · 核验 2026-10-28 · 12月6日介绍Gemini，API在该公告中仍为12月13日计划；不可据此单独认定已上线。
- timeline-r1-src-006 · https://cloud.google.com/blog/products/ai-machine-learning/gemini-support-on-vertex-ai · 核验 2026-10-28 · 12月13日正文明确Gemini Pro现已在Vertex AI公开可用。
- timeline-r1-src-007 · https://docs.cloud.google.com/vertex-ai/docs/core-release-notes · 核验 2026-10-28 · 明确Gemini Pro与Pro Vision为Preview；不能标作GA。
- timeline-r1-src-008 · https://www.tii.ae/news/technology-innovation-institute-introduces-worlds-most-powerful-open-llm-falcon-180b · 核验 2026-10-28 · 研发机构当日宣布Falcon 180B发布并开放研究与商业用途访问；不是无限制许可。
- timeline-r1-src-009 · https://huggingface.co/blog/falcon-180b · 核验 2026-10-28 · 当日欢迎Falcon 180B进入Hub并链接base/chat权重；使用需接受许可及条款。
- timeline-r1-src-010 · https://huggingface.co/mistralai/Mistral-7B-v0.1 · 核验 2026-10-28 · 核对v0.1版本身份；发布日期证据仍来自原始公告。

## 覆盖缺口
- 未比较真实生成质量、成本、速度或生产部署效果
- Inkscape官网教程与许可页面403；使用维护指南验证描摹功能，软件许可仍unknown
- Canva直接猜测autofill路径不可访问，已通过官方文档链接定位正确指南
- 未覆盖3D/CAD/工业设计/字体生成/印前色彩管理等后续专题
- 价格、区域可用性、账号权限和具体输出法律地位不由通用文档完整确定
- 未进行真实生成/试听/时延或音质评测
- 未验证账户、地区可用性、价格和购买条件
- 未覆盖全部 DAW、唱声合成、空间音频、乐谱 OCR、音频修复产品
- Stable Audio 精确商业许可证适用与 Suno 冲突条款需要发行前专项复核
- 没有镜像模型权重、训练音频或版权歌词
- 未实测任何生成、编辑、转录或Agent原生链路；未安装第三方代码或下载权重。
- 未核实全量模型具体许可证条款、价格与各操作系统兼容性；Blender官方手册抓取返回402，未引用其具体功能。
- Runway、Veo、Sora等付费/账号服务未执行；不以本轮检索暗示全行业覆盖。
- 未实测任何长片角色一致性、口型、完整版权清理或无障碍标准合规。
- 早期统计NLP、HMM/CRF、RNN/LSTM原始论文仍需单列
- 日本、韩国、东南亚、非洲、拉丁美洲以及其他欧洲研究生态覆盖不足
- 未系统枚举2025—2026最新版本；家族与具体权重/服务快照需持续补录
- 视频与音乐已初步纳入相关技术节点；更多独立系列、版本与教程仍待补充。3D、机器人和世界模型仍缺独立系列；不代表全领域覆盖。
- 许可证/商用条款、参数、训练数据与开放程度应按具体版本另行核验
- JEV待用户确认，不映射JEPA
- 不提供当前价格、排行榜、无条件性能优越声明
- 未覆盖全部公开/私有/内部benchmark；无法证明全球穷尽。
- 未核验全部数据集文件级许可证、修订历史及去重清单。
- 动态仓库多数未锁定commit；版本字段明确快照，不代表最新已实测版。
- MCP使用明确历史规范2025-06-18，未宣称2026-10-28最新协议版本。
- 尚未覆盖SGLang、TensorRT-LLM、ONNX Runtime、OpenVINO及所有硬件内核。
- 尚未系统收录多模态/语音/机器人、安全与医学等专用评测。
- 模型家族逐版本教程需与模型登记表继续关联；本轮只有运行时路线，不捏造具体模型支持。
- JEV未定义，未重复研究或臆测展开。
- 已收录 3 条历史自报成绩快照；不是独立复现或可比榜单，不生成排名。
