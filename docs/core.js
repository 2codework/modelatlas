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
const api={relationDisplay,safeURL,parseProgress,search,deepLinkID,hasExplicitUnknownAvailability};root.ModelAtlasCore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
