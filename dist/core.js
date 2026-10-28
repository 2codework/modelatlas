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
const api={safeURL,parseProgress,search};root.ModelAtlasCore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
