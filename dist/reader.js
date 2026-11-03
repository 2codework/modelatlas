'use strict';
// Deliberately small Markdown reader: no HTML parsing, images, scripts or embedded content.
function markdownDOM(text,doc=document){
 const make=(tag,t)=>{const e=doc.createElement(tag);if(t!==undefined)e.textContent=t;return e;};
 function inline(parent,s){const re=/`([^`\n]+)`|\*\*([^*\n]+)\*\*|\[([^\]]+)\]\(([^\s)]+)\)/g;let end=0,m;while((m=re.exec(s))){parent.append(doc.createTextNode(s.slice(end,m.index)));if(m[1]!==undefined)parent.append(make('code',m[1]));else if(m[2]!==undefined)parent.append(make('strong',m[2]));else{let u;try{u=new URL(m[4]);}catch{}if(u&&u.protocol==='https:'&&!u.username&&!u.password){const a=make('a',m[3]+'（来源）');a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';parent.append(a);}else parent.append(doc.createTextNode(m[0]));}end=re.lastIndex;}parent.append(doc.createTextNode(s.slice(end)));return parent;}

 const root=make('div'),lines=String(text).split('\n');let i=0;
 while(i<lines.length){const line=lines[i];if(!line.trim()){i++;continue;}const fence=/^\s*(`{3,}|~{3,})([a-zA-Z0-9_-]*)\s*$/.exec(line);if(fence){const body=[];i++;while(i<lines.length&&!new RegExp('^\\s*'+fence[1][0]+'{'+fence[1].length+',}\\s*$').test(lines[i]))body.push(lines[i++]);if(i<lines.length)i++;const pre=make('pre'),code=make('code',body.join('\n'));pre.append(code);root.append(pre);continue;}const h=/^(#{1,6})\s+(.+)$/.exec(line);if(h){root.append(inline(make('h'+Math.min(6,h[1].length+2)),h[2]));i++;continue;}
 if(line.includes('|')&&i+1<lines.length&&/^\s*\|?\s*:?-{3,}/.test(lines[i+1])){const table=make('table'),wrap=make('div');wrap.className='table-scroll';const cells=s=>s.trim().replace(/^\||\|$/g,'').split('|').map(x=>x.trim());const head=make('thead'),tr=make('tr');cells(line).forEach(c=>tr.append(inline(make('th'),c)));head.append(tr);table.append(head);i+=2;const body=make('tbody');while(i<lines.length&&lines[i].includes('|')&&lines[i].trim()){const row=make('tr');cells(lines[i++]).forEach(c=>row.append(inline(make('td'),c)));body.append(row);}table.append(body);wrap.append(table);root.append(wrap);continue;}
 const item=/^\s*(?:[-*]|\d+\.)\s+(.+)$/.exec(line);if(item){const list=make(/^\s*\d/.test(line)?'ol':'ul');while(i<lines.length){const m=/^\s*(?:[-*]|\d+\.)\s+(.+)$/.exec(lines[i]);if(!m)break;list.append(inline(make('li'),m[1]));i++;}root.append(list);continue;}
 root.append(inline(make('p'),line));i++;
 }return root;
}
function deepLinkID(search,key,ids){const id=new URLSearchParams(search).get(key);return ids.has(id)?id:null;}


// Explicit reader projection. Never recursively render source-bundle machine metadata.
function researchChapterDOM(chapter,cases,doc=document){
 const make=(tag,t)=>{const e=doc.createElement(tag);if(t!==undefined)e.textContent=t;return e;};
 const copy=(parent,label,value)=>{if(typeof value==='string'&&value.trim()){if(label)parent.append(make('h4',label));parent.append(markdownDOM(value,doc));}};
 const d=chapter.data,root=make('div');
 const topics={roles:['岗位地图','按岗位理解任务拆解、人工验收与授权边界。'],industries:['行业地图','用合成行业任务学习输入、步骤、验收和风险判断。'],learning:['学习方法','学习、写作、研究检索、知识管理、无障碍与多语言练习。'],'creative-design':['设计专题','界面、设计系统、图像、演示与资产溯源的合成教学流程。'],'creative-music':['音乐与音频专题','配乐、编曲、混音、转录和音频后期的合成教学流程。'],'creative-video':['视频与动画专题','视频生成、剪辑、字幕、动画与交付的合成教学流程。']};
 const topic=topics[chapter.id]||['研究资料','代表性教学资料，并非完整市场目录。'];
 root.append(make('h3',topic[0]));copy(root,'',topic[1]);
 root.append(make('p',`收录 ${(d.cases||[]).length} 个教学流程、${(d.sources||[]).length} 条登记来源；来源核查日期：${d.checked_at||'未提供'}。不是全部岗位、行业或产品目录。`));
 copy(root,'证据与使用边界','以下是原创合成教学方案，未实测完整工作流，也不代表真实部署、质量保证或效率收益。来源只支持其明确描述的能力与限制。许可、费用、版本、账号权限和素材权利必须在实际使用前复核；上传、付费、外部写入和发布仍需批准。');
 if(Array.isArray(d.coverage_gaps)){root.append(make('h4','尚未覆盖与待核验'));const ul=make('ul');for(const gap of d.coverage_gaps)if(typeof gap==='string'){const li=make('li');li.append(markdownDOM(gap,doc));ul.append(li);}root.append(ul);}
 if(chapter.id==='industries'){copy(root,'行业教学正文（稿件版本说明属于采集记录）',d.content_markdown);copy(root,'行业覆盖与边界',d.coverage_markdown);}
 const list=make('div');root.append(make('h4','实践与适用边界'),list);
 for(const raw of d.cases||[]){const id=chapter.id.startsWith('creative-')?raw.id:chapter.id+'-'+String(raw.id).toLowerCase();const c=cases.find(c=>c.id===id);if(!c)continue;const item=make('details');item.append(make('summary',c.title));copy(item,'',c.summary);const a=make('a','打开完整实践与验收');a.href='?case='+encodeURIComponent(c.id);item.append(a);
 for(const [key,label] of [['evidence_note','证据说明'],['license','许可'],['risks','风险与授权'],['cost','费用'],['compute_cost','计算费用'],['permission_boundary','权限'],['applicable_versions','适用版本'],['lifecycle','生命周期'],['historical_context','历史边界'],['practice_status','实践证据状态'],['failure_recovery','失败恢复']])copy(item,label,c[key]);list.append(item);}
 root.append(make('h4','来源与证据范围'));
 for(const source of d.sources||[]){const row=make('div');copy(row,'',source.title||source.publisher_title||'来源');for(const url of source.urls||[source.url])if(typeof url==='string'){const a=make('a','阅读原始来源');try{const u=new URL(url);if(u.protocol==='https:'&&!u.username&&!u.password){a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';row.append(a);}}catch{}}
 copy(row,'','核查日期：'+(source.checked_at||d.checked_at||'未提供'));
 for(const key of ['verified_claim','supports','notes','notes_zh','claim_scope','evidence_scope','license_status'])copy(row,'',source[key]);root.append(row);}
 const raw=make('details');raw.open=false;raw.append(make('summary','原始资料 · 历史采集快照，不代表当前整合状态'),make('p','以下保留采集时的全部原字段。适配、整合与发布状态可能已经变化；请勿将内部元数据视为当前产品状态。'),make('pre',JSON.stringify(d,null,2)));root.append(raw);return root;
}
if(typeof module!=='undefined')module.exports={markdownDOM,deepLinkID,researchChapterDOM};

// Bounded teaching projections: prose for known schemas, explicit original fallback
// for unknown keys/shapes. This never changes the research object or executes HTML.
function guidanceDOM(value,kind,doc=document){
 const make=(tag,text)=>{const e=doc.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
 const root=make('div');root.className='guidance-reading';
 const statuses={editorial_guidance_not_executed:'编辑学习建议 · 未执行',unknown_or_configuration_dependent:'未知，或取决于具体配置',paper_reported:'论文自报 · 非独立复测',counting_scope_unresolved:'参数统计口径尚未消歧',different_scopes_do_not_merge:'统计范围不同，不合并数值',deprecated_not_yet_scheduled_shutdown:'已弃用；计划停用日期尚未到达',current_guide_example_not_marked_deprecated_in_reviewed_sources:'已核资料中的当前指南示例；该资料未标为弃用'};
 const schemas={
  best_practice:{status:['实践状态','status'],steps:['建议步骤','steps'],acceptance_zh:['验收标准','text']},
  streaming:{input:['流式输入','bool'],output:['流式输出','bool'],full_duplex:['全双工','bool'],condition_zh:['适用条件与限制','text'],transport_bidirectional_streaming:['双向流式传输','bool'],conversational_speech_to_speech:['语音到语音对话','bool'],source_ids:['来源记录 ID','list']},
  parameters:{value:['参数记录','scalar'],status:['统计口径','status'],source_ids:['来源记录 ID','list']},
  variants:{exact_id:['精确标识','text'],parent_family:['所属家族','text'],revision_sha:['固定修订 SHA','scalar'],first_weights_upload_date:['权重首次上传日期','scalar'],source_ids:['来源记录 ID','list']},
  versions:{exact_id:['精确版本','text'],related_alias:['相关别名','text'],immutable_dated_snapshot:['固定日期快照','scalar'],announcement_date:['公告日期','scalar'],release_date:['发布日期','scalar'],deprecation_announced:['弃用公告日期','scalar'],scheduled_shutdown:['计划停用日期（非已发生）','scalar'],lifecycle_as_of:['生命周期资料截至','scalar'],status:['生命周期状态','status'],inputs:['输入类型','modalities'],outputs:['输出类型','modalities'],pricing_per_million_tokens_usd:['来源记录价格 · 美元 / 百万 token（非当前报价）','pricing'],free_tier:['免费层记录','free'],source_ids:['来源记录 ID','list']},
  pricing:{text_input:['文本输入','scalar'],text_output:['文本输出','scalar'],audio_input:['音频输入','scalar'],audio_output:['音频输出','scalar']}
 };
 const modalityLabels={text:'文本',audio:'音频',image:'图像',aligned_text:'对齐文本'};
 const scalar=x=>x===null||typeof x==='string'||typeof x==='number'||typeof x==='boolean';
 const words=x=>x===null?'未知 / 未注明':typeof x==='boolean'?(x?'是（仅来源记录）':'否（仅来源记录）'):String(x);
 function fallback(parent,raw){const d=make('details');d.className='guidance-original';d.append(make('summary','未适配的字段或格式 · 展开原始记录'),make('p','以下字段尚未转换为阅读形式，不据此补充含义或验证状态。完整内容仍保留。'),make('pre',JSON.stringify(raw,null,2)));parent.append(d);}
 function render(parent,item,type){
  if(!item||typeof item!=='object'||Array.isArray(item)||!Object.hasOwn(schemas,type)){fallback(parent,item);return;}
  const schema=schemas[type];let unknown=false;const definitions=type==='best_practice'?null:make('dl');if(definitions)parent.append(definitions);
  for(const [key,[label,format]] of Object.entries(schema)){
   if(!Object.hasOwn(item,key))continue;const v=item[key];let node;
   if(format==='text'&&typeof v==='string')node=make('p',v);
   else if(format==='scalar'&&scalar(v))node=make('p',words(v));
   else if(format==='bool'&&(v===null||typeof v==='boolean'))node=make('p',words(v));
   else if(format==='status'&&typeof v==='string')node=make('p',Object.hasOwn(statuses,v)?statuses[v]:'尚无中文状态说明：'+v);
   else if(format==='free'&&typeof v==='string')node=make('p',v==='not supported'?'来源记录为不支持；以所列版本及核验范围为限':v);
   else if(['steps','list','modalities'].includes(format)&&Array.isArray(v)&&v.every(x=>typeof x==='string')){node=make(format==='steps'?'ol':'ul');for(const text of v)node.append(make('li',format==='modalities'&&Object.hasOwn(modalityLabels,text)?modalityLabels[text]:text));}
   else if(format==='pricing'&&v&&typeof v==='object'&&!Array.isArray(v)){node=make('div');render(node,v,'pricing');}
   else{unknown=true;continue;}
   if(definitions){const description=make('dd');description.append(node);definitions.append(make('dt',label),description);}else parent.append(make('h5',label),node);
  }
  if(Object.keys(item).some(k=>!Object.hasOwn(schema,k)))unknown=true;
  if(unknown)fallback(parent,item);
 }
 if(['variants','versions'].includes(kind)&&Array.isArray(value)){const list=make('ol');for(const item of value){const li=make('li');render(li,item,kind);list.append(li);}root.append(list);}
 else render(root,value,kind);
 return root;
}
if(typeof module!=='undefined')module.exports.guidanceDOM=guidanceDOM;
