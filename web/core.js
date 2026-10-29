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
const api={learningOrder,displayLabel,displayLabels,relationDisplay,safeURL,parseProgress,search,deepLinkID,hasExplicitUnknownAvailability};root.ModelAtlasCore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
