'use strict';
(function(root){
 const expected={id:'seed-coder-8b-instruct-arxiv-v1-bigcodebench-completion-full',model:'Seed-Coder-8B-Instruct',benchmark:'BigCodeBench-Completion',split:'Full',report_version:'arXiv:2506.03524v1',report_date:'2025-06-04',checked_at:'2026-10-31',href:'evaluation-evidence.html'};
 const keys=[...Object.keys(expected),'title'].sort();
 function validate(index){
  if(!index||index.schema_version!=='modelatlas.evaluation_evidence_index.v1'||index.scope!=='one_existing_checkpoint_one_vendor_reported_score'||index.not_executed!==true||!Array.isArray(index.records)||index.records.length!==1)return false;
  const r=index.records[0];
  return !!r&&Object.keys(r).sort().join('|')===keys.join('|')&&Object.entries(expected).every(([k,v])=>r[k]===v)&&typeof r.title==='string'&&r.title.trim().length>0;
 }
 // Normalize punctuation only for this separate supplement, not the canonical registry.
 const normalize=value=>String(value).normalize('NFKC').toLocaleLowerCase().replace(/[\s_\-‐‑‒–—]+/gu,'');
 function search(index,query='',kind=''){
  if(!validate(index))return {status:'unavailable',rows:[]};
  if(kind)return {status:'excluded',rows:[]};
  const q=normalize(query);
  return {status:'ready',rows:index.records.filter(r=>normalize([r.title,r.model,r.benchmark,r.split,r.report_version,r.report_date,r.checked_at,'论文自报 历史证据 未独立复现'].join(' ')).includes(q))};
 }
 function render(document,index,query,kind){
  const status=document.getElementById('evaluation-supplement-count'),list=document.getElementById('evaluation-supplement-results');
  if(!status||!list)return;
  const result=search(index,query,kind);list.replaceChildren();
  status.textContent=result.status==='unavailable'?'补充证据索引未载入或版本不匹配；不能据此判断没有资料。可用上方直达链接阅读。':result.status==='excluded'?'当前资料类型不含独立论文证据；选择“全部索引”后按关键词查找补充。':`${result.rows.length} / 1 条补充证据匹配 · 单独计数，不计入上方 33 + 11 条索引`;
  for(const r of result.rows){
   const li=document.createElement('li'),a=document.createElement('a'),p=document.createElement('p');
   a.href=r.href;a.textContent=r.title+' →';
   p.textContent=`${r.benchmark} · ${r.split} · ${r.report_version}（提交于 ${r.report_date}，不是权重发布日期）；来源核验 ${r.checked_at}。厂商论文自报，未独立复现，不作排名。`;
   li.append(a,p);list.append(li);
  }
 }
 const api={validate,search,render};if(typeof module==='object'&&module.exports)module.exports=api;root.ModelAtlasEvaluationEvidenceSearch=api;
})(globalThis);
