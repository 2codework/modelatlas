/* Pure helpers shared by UI and Node's built-in tests. No dependencies. */
(function(root){
'use strict';
function safeURL(value){try {const u=new URL(value);return ['https:','http:'].includes(u.protocol)&&!u.username&&!u.password&&!/\s/.test(value)?u.href:null;}catch{return null;}}
function parseProgress(text, ids){
 if(typeof text!=='string'||text.length>1000000)throw new Error('文件过大或格式不正确');
 const p=JSON.parse(text);
 if(!p||p.schema!=='modelatlas.progress.v1'||!Array.isArray(p.completed)||p.completed.length>10000)throw new Error('不是兼容的进度文件');
 if(!p.completed.every(x=>typeof x==='string'))throw new Error('进度 ID 必须是字符串');
 return new Set(p.completed.filter(id=>ids.has(id)));
}
function search(nodes, views, filters){return nodes.filter(n=>{
 const v=views.get(n.id)||{};const text=[n.title,n.description_zh,n.summary_zh,n.id,n.category,...(n.tags||[])].join(' ').toLocaleLowerCase();
 return (!filters.query||text.includes(filters.query.trim().toLocaleLowerCase()))&&['type','category'].every(k=>!filters[k]||n[k]===filters[k])&&['availability','vendor'].every(k=>!filters[k]||v[k]===filters[k]);
});}
function deepLinkID(search,hash,ids){let id=new URLSearchParams(search).get('node');if(!id&&hash.startsWith('#node=')){try{id=decodeURIComponent(hash.slice(6));}catch{}}return ids.has(id)?id:null;}
// Legacy display-text compatibility only, not a complete availability-status schema.
// A false result never means a service/account/region has been verified available.
function hasExplicitUnknownAvailability(value){
 if(value===null||value===undefined)return true;
 if(typeof value!=='string')return false;
 const label=value.trim();
 return label===''||label==='未核验'||/^unknown\b/i.test(label);
}
// Exact metadata vocabulary only. Editorial classification takes precedence over
// source review: a citation does not turn a teaching comparison into integration.
function relationDisplay(edge){
 const e=edge&&typeof edge==='object'?edge:{};
 const editorialTypes=['editorial_learning_relation','editorial_learning_order','learning_path','learning_prerequisite','prerequisite_for','prerequisite_of'];
 const editorialEvidence=['editorial_learning_order','editorial_learning_relation','editorial_learning_relation_not_vendor_integration_claim','editorial_cross_module'];
 const editorialStatus=['editorial_learning_relation'];
 if(editorialTypes.includes(e.type)||editorialEvidence.includes(e.evidence_type)||editorialStatus.includes(e.verification_status))return {kind:'editorial',label:'编辑学习对照，非厂商集成'};
 if(e.type==='documented_migration_target'&&e.evidence_type==='official_documented_product_migration')return {kind:'documented',label:'官方文档关系，非运行核验'};
 const officialStatus=['primary_source_checked','primary_metadata_reviewed_not_executed','primary_sources_reviewed_not_executed'];
 if(officialStatus.includes(e.verification_status))return {kind:'documented',label:'来源文档关系，本库未运行核验'};
 return {kind:'unknown',label:'关系性质待核验，非运行证明'};
}
// Display-only vocabulary. Raw enums, option values, URL filters and source records stay exact.
const displayLabels={
 category:{agent_tools:'智能体工具',agents:'智能体',alignment:'对齐与安全','assistant-workspaces':'助手与工作空间',coding_agents:'编程智能体','creative-design':'设计与创作','creative-music':'音乐与音频创作','creative-video':'视频与动画创作',data:'数据',deployment:'部署',evaluation:'评测',foundations:'基础知识',frontiers:'前沿研究',inference:'推理与生成','media-evaluation':'媒体评测',memory:'记忆机制','model-families':'模型家族',multimodal:'多模态','office-agent-systems':'办公智能体系统',organizations:'机构',quantization:'量化','realtime-audio':'实时音频',reasoning:'推理能力','regional-office-platforms':'区域办公平台',retrieval:'检索','text-models':'语言模型',training:'训练','video-production':'视频制作','world-models-embodied':'世界模型与具身研究'},
 type:{agent_framework:'智能体框架',agent_system:'智能体系统',application_feature:'应用功能',architecture:'模型架构',artifact_creation_feature:'成果创建功能',benchmark:'评测基准',concept:'概念',database:'数据库',database_extension:'数据库扩展',dataset:'数据集',enterprise_workflow_agent_service:'企业工作流智能体服务',evaluation_tool:'评测工具',executable_agent_product_surface:'可执行智能体产品界面',field:'研究领域',format:'格式',framework:'框架',harness:'评测工具套件',historical_executable_agent_surface:'历史可执行智能体界面',historical_tool:'历史工具','hosted-agent-application-platform':'托管智能体应用平台','hosted-agent-development-platform':'托管智能体开发平台','hosted-agent-platform':'托管智能体平台','hosted-enterprise-agent-feature':'托管企业智能体功能','hosted-low-code-office-assistant-feature':'托管低代码办公助手功能',hosted_agent_service:'托管智能体服务',hosted_personal_team_agent_service:'托管个人与团队智能体服务',hosted_workflow_agent_platform:'托管工作流智能体平台',instruction_package:'指令包',learning_path:'学习路线',library:'程序库',low_code_agent_platform:'低代码智能体平台',low_no_code_agent_platform:'低代码／无代码智能体平台',method:'方法',metric:'评测指标',model:'模型',model_family:'模型家族',model_release:'模型发布版本',model_service:'模型服务',ordinary_tool:'普通工具',organization:'机构',pipeline:'处理流程',practice:'实践条目',protocol:'协议',research_concept:'研究概念',research_feature:'研究功能',research_system:'研究系统',research_workspace:'研究工作空间',runtime:'运行环境','self-hostable-agent-application-platform':'可自托管智能体应用平台','self-hostable-agent-development-platform':'可自托管智能体开发平台',specification:'规范',standard:'标准',standard_or_format:'标准或格式',system:'系统',theoretical_framework:'理论框架',tool:'工具',tool_interface:'工具接口',tool_service:'工具服务',tutorial:'教程',unresolved_term:'待消歧术语',workflow_agent_component:'工作流智能体组件',workflow_orchestration_component:'工作流编排组件',workspace_agent_assistant:'工作空间智能体助手',workspace_agent_client_surface:'工作空间智能体客户端界面',workspace_agent_service:'工作空间智能体服务'},
 evidence:{ambiguous:'身份或含义待消歧',offline_contract_only:'仅离线教学契约验证',primary_metadata_reviewed_not_executed:'一手元数据已核对 · 未运行',primary_source_checked:'一手来源已核对 · 非运行证明',primary_sources_reviewed_not_executed:'一手资料已核对 · 未运行',research_claim_scoped:'研究论述 · 以注明范围为准',source_reviewed_not_replicated:'资料已审阅 · 未独立复现','never-run':'未运行'},
 availability:{gated:'门控访问 · 具体条件见来源',gated_open_weights:'门控开放权重',hosted_api_only:'仅托管 API',open_weights:'开放权重',private_described:'仅有非公开访问的描述',public_download:'公开下载入口',unknown:'未知／未核验'},
 vendor:{airtable:'Airtable','atlassian-rovo':'Atlassian Rovo',glean:'Glean',lindy:'Lindy',make:'Make','microsoft-copilot-studio':'Microsoft Copilot Studio',n8n:'n8n',notion:'Notion','relevance-ai':'Relevance AI',zapier:'Zapier'}
};
function displayLabel(value,kind){
 if(value===null||value===undefined||value==='')return '未核验';
 // Reject non-scalar values without invoking user-defined coercion methods.
 if(!['string','number','boolean','bigint'].includes(typeof value))return '未核验（标签格式不受支持）';
 const text=String(value),knownKind=typeof kind==='string'&&Object.prototype.hasOwnProperty.call(displayLabels,kind);
 const labels=knownKind?displayLabels[kind]:Object.create(null);
 if(Object.prototype.hasOwnProperty.call(labels,text)&&typeof labels[text]==='string')return labels[text];
 if(kind==='availability'){
  const prefix='unknown unless explicitly qualified below; no sign-in or account eligibility check';
  if(text.startsWith(prefix))return '除下文明确说明外均未知；未登录或核验账户资格'+text.slice(prefix.length);
  const split=text.indexOf('；');if(split>0&&Object.prototype.hasOwnProperty.call(labels,text.slice(0,split)))return labels[text.slice(0,split)]+text.slice(split);
 }
 // Never infer a classification or evidence strength for a future/unrecognized enum.
 if(!knownKind||['category','type','evidence'].includes(kind)||/^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$/.test(text))return '未收录中文标签 · '+text.replace(/[_-]+/g,' ');
 return text;
}
// Stable topological order is an editorial display only; source paths stay untouched.
function learningOrder(path,nodeMap){
 const original=[...path.node_ids],inside=new Set(original),done=new Set(),ordered=[],external=new Set();
 for(const id of original)for(const pre of nodeMap.get(id)?.prerequisites||[])if(!inside.has(pre)&&nodeMap.has(pre))external.add(pre);
 while(ordered.length<original.length){const next=original.find(id=>!done.has(id)&&(nodeMap.get(id)?.prerequisites||[]).every(pre=>!inside.has(pre)||done.has(pre)));if(next===undefined)return {node_ids:original,external:[...external],cyclic:true};done.add(next);ordered.push(next);}
 return {node_ids:ordered,external:[...external],cyclic:false};
}
// Read-only edge record projection. Original leaf values remain available; no inference or URLs.
function projectEdgeRecord(node){
 const m=node?.edge_multimodal;if(!m||typeof m!=='object'||Array.isArray(m))return null;
 const translations={"unknown": "未知／未核验", "text": "文本", "image": "图像", "multiple_images": "多张图像", "video_frames": "视频帧", "video": "视频", "audio": "音频", "not separately claimed": "未单独声明", "scope_or_version_unknown": "适用范围或版本未明", "official model size label, not independently counted": "官方标称模型大小，未经独立计数", "0.5B names language backbone, not full vision-language system": "0.5B 仅指语言主干，不是完整视觉语言系统", "apple/FastVLM-0.5B HF metadata approximately0.8B; stage3 equality not verified": "apple/FastVLM-0.5B 的 HF 元数据约为 0.8B；未核验与 stage3 是否相同", "E2B effective accelerator-memory footprint; not total and not generic MoE active count": "E2B 指有效加速器内存占用口径；不是总参数，也不是通用 MoE 激活参数量", "full multimodal transformer including backbone/encoders/adapters; mixture-of-LoRAs not interchangeable with MoE active count": "完整多模态 Transformer，含主干、编码器与适配器；mixture-of-LoRAs 不等同 MoE 激活参数口径", "public Apache-2.0 per card": "模型卡声明以 Apache-2.0 公开", "Transformers/MLX examples publicly linked; full code-license audit unknown": "公开链接 Transformers／MLX 示例；完整代码许可审计未知", "Apache-2.0 model; downstream inputs and code separate": "模型采用 Apache-2.0；下游输入与代码需分别核对", "public download links, restricted research license": "公开下载链接，但采用受限科研许可", "public Apple custom software license plus third-party notices": "公开的 Apple 自定义软件许可，另有第三方声明", "Apple Machine Learning Research Model License: non-commercial scientific research and academic development only; excludes commercial exploitation, product development, and use in any commercial product or service.": "Apple 机器学习研究模型许可：仅限非商业科学研究与学术开发；排除商业利用、产品开发及任何商业产品或服务中的使用。", "open-weight designation under Gemma custom terms; HF file gate requires account and agreement": "Gemma 自定义条款下的开放权重；HF 文件访问需账号并同意条款", "Transformers implementation referenced; independent full code-license audit unknown": "引用了 Transformers 实现；独立完整代码许可审计未知", "Gemma custom license; license acceptance not performed; complete terms not reviewed": "Gemma 自定义许可；未执行许可接受，未审阅全部条款", "public MIT per model card": "模型卡声明以 MIT 公开", "public custom_code inference examples; MIT model repo metadata, dependencies separate": "公开 custom_code 推理示例；模型仓库元数据为 MIT，依赖项另行核对", "MIT; downstream media rights and dependencies require own review": "MIT；下游媒体权利与依赖项需自行审阅", "Transformers CUDA BF16 with flash_attention_2": "Transformers CUDA BF16，使用 flash_attention_2", "decord video preprocessing": "decord 视频预处理", "MLX Python/Swift on Apple Silicon, historical launch examples": "Apple Silicon 上的 MLX Python／Swift；历史发布示例", "official launch links unquantized MLX conversion; exact official quantized artifact unknown": "官方发布链接为未量化的 MLX 转换；精确的官方量化制品未知", "unknown; iPhone demo does not establish all iPhones support": "未知；iPhone 演示不证明所有 iPhone 均支持", "CoreML vision encoder plus patched mlx-vlm LLM": "CoreML 视觉编码器配合补丁版 mlx-vlm 语言模型", "iOS18.2+ / macOS15.2+ visual-QA demo built in Xcode": "在 Xcode 中构建的视觉问答演示，要求 iOS 18.2+／macOS 15.2+", "LLM-only export supports8-bit/4-bit; full-model precision not inferred": "仅语言模型导出支持 8-bit／4-bit；不据此推断全模型精度", "Apple Silicon path; exact minimum model/total RAM unknown": "Apple Silicon 路径；最低机型与总内存要求未知", "official blog links Google AI Edge Gallery/LiteRT-LLM and MLX": "官方博客链接 Google AI Edge Gallery／LiteRT-LLM 与 MLX", "exact official quantization artifact and precision unknown in this bounded pass": "本轮有限审阅中，精确官方量化制品与精度未知", "unknown; runtime-specific modality support and memory must be verified separately": "未知；各运行时的模态支持与内存需分别核验", "Python3.10, Transformers4.48.2 example stack with trust_remote_code": "示例栈为 Python 3.10、Transformers 4.48.2，使用 trust_remote_code", "official ONNX INT4 CUDA / DirectML": "官方 ONNX INT4，面向 CUDA／DirectML", "microsoft/Phi-4-multimodal-instruct-onnx gpu-int4-rtn-block-32; conversion treated separately, not bit-identical base": "microsoft/Phi-4-multimodal-instruct-onnx 的 gpu-int4-rtn-block-32；转换版本单列，不视为与基础权重逐位相同", "unknown; CUDA/DML targets not phone guarantee; training A100 counts excluded from inference requirements": "未知；CUDA／DML 目标不保证手机支持；训练所用 A100 数量不作为推理要求", "official ONNX card says stay tuned or convert; no ready CPU compatibility claimed": "官方 ONNX 卡表示敬请期待或自行转换；未声明现成的 CPU 兼容版本", "GPU RAM for video inference": "视频推理 GPU 显存", "official_self_report": "官方自报（非独立实测）", "not a universal minimum or independent test": "不是通用最低要求，也不是独立实测", "relative TTFT": "相对首 token 时间（TTFT）", "LLaVA-OneVision with0.5B LLM at1152x1152": "LLaVA-OneVision，0.5B 语言模型，1152×1152 输入", "not established in abstract reviewed": "所审阅摘要未确立硬件条件（未知）", "not tokens/sec, not per-action/GUI end-to-end timing; not assumed stage3-specific": "不是 tokens/sec，不是单次动作或 GUI 端到端计时；不假定特指 stage3", "primary_sources_reviewed_not_executed": "已审阅一手来源，未执行", "unknown_not_established; not a phone controller": "未知、未确立；不是手机控制器"},labels={"id": "记录 ID", "organization": "机构", "exact_id": "精确身份", "inputs": "输入", "outputs": "输出", "total_nominal": "标称总参数", "total_exact": "精确总参数", "total": "总参数", "llm_nominal": "语言主干标称参数", "active": "激活参数（active）", "effective": "有效参数（effective）", "scope": "分母与适用范围", "related_not_identity_proof": "相关记录（不证明同一身份）", "official_claims": "官方原始参数声明", "source": "来源 ID", "raw": "原始数值", "reconciliation_note_zh": "口径核对说明", "weights": "权重开放范围", "code": "代码开放范围", "terms": "许可条款与限制", "documented": "文档运行条件", "quantization": "量化适用范围", "hardware_minimum": "最低硬件条件", "cpu": "CPU 支持边界", "metric": "测量指标", "value": "官方自报值", "status": "证据状态", "hardware": "硬件条件", "frames_context_batch": "帧数／上下文／批量", "warning": "不可外推的边界", "baseline": "对照基线", "latency": "延迟", "peak_memory": "峰值内存", "benchmark": "基准结果", "commit": "制品提交版本", "weight_sha256": "权重 SHA-256", "downloaded": "是否下载权重", "verification_status": "核验状态", "gui_action_capability": "GUI 动作能力", "source_ids": "原始来源 ID（不等于支持来源）", "learning_source_ids": "原始学习来源 ID", "learning_path_zh": "学习步骤"};
 const groups=[['身份与输入输出',['id','organization','exact_id','inputs','outputs']],['参数与分母',['parameters']],['许可与开放边界',['openness']],['文档运行条件与量化',['runtime']],['官方自报测量 · 不是排行榜',['reported_measurements']],['独立实测与制品状态',['independent_measurements','artifact_pin','verification_status','gui_action_capability']],['学习步骤与来源范围',['learning_path_zh','source_ids','learning_source_ids']]];
 const groupLabels={parameters:'参数',openness:'开放边界',runtime:'运行条件',reported_measurements:'测量',independent_measurements:'独立实测',artifact_pin:'制品状态'};
 function fieldLabel(key){return Object.hasOwn(labels,key)?labels[key]:Object.hasOwn(groupLabels,key)?groupLabels[key]:'未收录字段 · '+key;}
 const known=new Set(groups.flatMap(g=>g[1]));const extra=Object.keys(m).filter(k=>!known.has(k));if(extra.length)groups.push(['其他原记录字段（未解释）',extra]);
 function rows(value,path,label){
  if(Array.isArray(value)){if(!value.length)return [{path,label,original:[],text:'本记录未登记条目（不表示不存在）'}];return value.flatMap((v,i)=>rows(v,path+'.'+i,label+' · '+(i+1)));}
  if(value!==null&&typeof value==='object')return Object.entries(value).flatMap(([k,v])=>rows(v,path+'.'+k,(Object.hasOwn(labels,k)?labels[k]:'未收录字段 · '+k)+(label?' / '+label:'')));
  const original=value===undefined?null:value;const text=value===null||value===undefined?'未知／未登记':value===false?'否（false）':value===true?'是（true）':(Object.hasOwn(translations,value)?translations[value]:String(value));
  return [{path,label,original,text}];
 }
 return {groups:groups.map(([title,keys])=>({title,rows:keys.flatMap(k=>rows(m[k],k,fieldLabel(k)))})),source_ids:[...(node.source_ids||[])].filter(id=>!(node.source_attempt_ids||[]).includes(id)),source_attempt_ids:[...(node.source_attempt_ids||[])],learning_url:node.learning_url};
}

const api={projectEdgeRecord,learningOrder,displayLabel,displayLabels,relationDisplay,safeURL,parseProgress,search,deepLinkID,hasExplicitUnknownAvailability};root.ModelAtlasCore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
