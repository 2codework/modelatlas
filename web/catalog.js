'use strict';
(function(global){
 const text=value=>value===null||value===undefined||value===''?'未知 / 本轮未核验':typeof value==='object'?JSON.stringify(value,null,2):String(value);
 // Display vocabulary only: identifiers, versions, licenses and source quotations stay exact.
 const labels={
  read_primary_page:'已阅读一手页面',search_excerpt_only:'仅核对搜索摘要',primary_content_read_by_independent_auditor:'独立审阅者已阅读一手内容',official_link_discovered_not_executed:'已找到官方教程链接；未执行',read_not_executed:'已阅读；未执行',not_executed:'未执行',unknown_license_file_404:'许可条款未知；许可文件返回 404', '404_not_found':'链接返回 404（未找到）',fixed_snapshot:'固定快照',model_variant:'模型变体',legacy_api_alias:'旧版 API 别名',api_model_id:'API 模型标识',api_alias:'API 别名',fixed_api_version:'固定 API 版本',technical_report:'技术报告',open_weight_checkpoint:'开放权重检查点',named_model_variant:'具名模型变体',api_service:'API 服务',model_checkpoint:'模型检查点',model_family:'模型家族',
  GA:'正式发布（资料状态）',public_preview:'公开预览',live:'资料标记为上线',stable:'稳定版（资料状态）',retired:'已退役',catalog_listed:'官方目录列出',static_release:'静态发布',current_documented:'官方资料已公开',open_weights_documented:'开放权重已有文档',published:'已发表',active:'资料标记为活跃',deprecated:'已弃用（不等于已退役）',unknown:'未知 / 本轮未核验',
  open_weight:'开放权重',open_weights:'开放权重',api_redirect_alias:'API 重定向别名',paper:'论文',api_documented_weights_unknown:'API 已有文档；权重情况未知',gated_open_weights:'需通过访问门槛的开放权重',api_and_open_weights:'API 与开放权重',hosted_api:'托管 API',
  approve_with_limits:'附限制接纳',accept_with_caveats:'附注意事项接纳',text:'文本',image:'图像',audio:'音频',video:'视频',code:'代码',audio_variant_dependent:'音频（依变体而定）',text_transcription:'转写文本',embedding:'嵌入向量',sparse_weights:'稀疏权重',multi_vector:'多向量',llm:'语言模型',
  linked_primary_reference_not_full_paper_reviewed:'已链接一手文献；未完整审阅论文',official_reference_not_executed:'官方教程参考；未执行',primary_content_read:'已阅读一手来源内容',editorial_related:'编辑关联',editorial_learning_relation:'编辑学习关联（非技术继承证明）'
 };
 const fieldLabels={accepted:'已接纳来源包',held:'暂缓来源包',file:'文件',sha256:'SHA-256',disposition:'接纳结论',limits:'限制',decision_file:'结论文件',decision_sha256:'结论文件 SHA-256',status:'资料状态',scope:'适用范围',as_of:'截至日期',deprecation_date:'弃用日期',retirement_date:'退役日期',access_status:'资料访问状态',service_status:'服务可用状态',note_zh:'说明',notes_zh:'补充说明',original_backing_model_status:'原背后模型状态',announced:'公告日期',weights_released:'权重发布日期',api_launched:'API 上线日期',paper_first_submitted:'论文首次提交日期',paper_status:'论文核验范围',tutorial_status:'教程执行状态',input:'输入',output:'输出',id:'来源标识',url:'来源网址',locator:'证据位置',sourceproof_zh:'来源支持的说明',sourcecheckdate:'来源核验日期',checked_at:'核验日期',model_card:'模型卡',report:'报告',tutorial:'教程',weights_license:'权重许可',repository:'代码仓库',correction_history:'修订历史',field:'字段',old_value:'修订前',new_value:'修订后',reason_zh:'修订原因',date:'日期',note:'说明',outcome:'观察结果',observer:'观察者',source_id:'来源标识',resolved_snapshot:'解析到的快照',target_exact_id:'目标精确标识',time_precision:'时间精度',type:'类型',field_evidence:'字段证据',paper_scope:'论文范围',legal_terms_status:'法律条款核验状态',license_url_status:'许可链接核验状态',release_date:'发布日期',observed_web_lines:'观察到的网页行',word_limit:'字数限制'};
 const label=value=>typeof value==='string'&&Object.prototype.hasOwnProperty.call(labels,value)?labels[value]:text(value);
 const readable=(value,key='')=>{
  if(Array.isArray(value))return value.length?value.map(v=>readable(v,key)).join('；'):'未记录条目（不代表不存在）';
  if(value&&typeof value==='object')return Object.entries(value).map(([k,v])=>(fieldLabels[k]||k)+'：'+readable(v,k)).join('\n');
  return ['status','scope','access_status','service_status','original_backing_model_status','paper_status','tutorial_status','entity_type','access','qa_disposition','inputs','outputs','modality','input','output','verification_status','legal_terms_status','license_url_status','disposition'].includes(key)?label(value):text(value);
 };
 function introduction(r){
  if(typeof r.summary==='string'&&r.summary.trim())return r.summary;
  return text(r.provider)+' 的'+label(r.entity_type)+'，属于 '+text(r.family)+' 家族。输入：'+readable(r.inputs,'inputs')+'；输出：'+readable(r.outputs,'outputs')+'。访问形式：'+label(r.access)+'。以上是已记录的资料，不表示服务当前可用；具体限制与核验范围见下文。';
 }
 const search=(records,filters)=>records.filter(r=>(!filters.query||JSON.stringify(r).toLocaleLowerCase().includes(filters.query.toLocaleLowerCase()))&&['provider','entity_type','status'].every(k=>!filters[k]||r[k]===filters[k])&&(!filters.modality||[...(r.inputs||[]),...(r.outputs||[])].includes(filters.modality)));
 function validate(D){
 const c=D&&D.vendor_catalog;
 if(!c||c.schema_version!=='modelatlas.vendor-catalog.v1'||!Array.isArray(c.records)||!Array.isArray(c.bundles)||!Array.isArray(D.nodes))return false;
 const ids=new Set();
 for(const r of c.records){
  if(!r||typeof r.id!=='string'||!r.id||ids.has(r.id)||typeof r.title!=='string'||!['provider','entity_type','status'].every(k=>typeof r[k]==='string')||!['links','sources','unresolved_links'].every(k=>Array.isArray(r[k]))||!['inputs','outputs'].every(k=>r[k]===null||Array.isArray(r[k]))||!r.urls||typeof r.urls!=='object'||Array.isArray(r.urls))return false;
  ids.add(r.id);
 }
 const targets=new Set([...ids,...D.nodes.filter(n=>n&&typeof n.id==='string').map(n=>n.id)]);
 return c.records.every(r=>r.links.every(e=>e&&targets.has(e.target))&&r.sources.every(s=>s&&typeof s.url==='string'))&&c.bundles.every(b=>b&&typeof b.file==='string');
 }
 function initialize(D,chooseNode,report,writeNavigation,discovery){
  if(!validate(D)){report('unsupported-data','目录数据缺失或格式不受支持；知识图谱可独立使用。请核对同一发布版本的数据与脚本。');return null;}
  try{const controller=mount(D,chooseNode,writeNavigation,discovery);report(D.vendor_catalog.records.length?'ready':'empty',D.vendor_catalog.records.length?'目录已载入 '+D.vendor_catalog.records.length+' 条记录；不代表新增模型数。':'目录数据已载入，当前为 0 条记录。');return controller;}
  catch(error){report('mount-error','目录初始化失败；可能已有部分内容显示，请勿视为完整结果。知识图谱可独立使用。');return null;}
 }
 function mount(D,chooseNode,writeNavigation,discovery){
 const $=id=>document.getElementById(id),catalog=D.vendor_catalog;if(!catalog)return;
 const el=(tag,value)=>{const e=document.createElement(tag);if(value!==undefined)e.textContent=text(value);return e;};
 const button=(label,fn)=>{const b=el('button',label);b.type='button';b.addEventListener('click',fn);return b;};
 const link=(url,label)=>{const a=el('a',label||url),safe=ModelAtlasCore.safeURL(url);if(safe&&safe.startsWith('https:')){a.href=safe;a.target='_blank';a.rel='noopener noreferrer';}return a;};
 const records=catalog.records,map=new Map(records.map(r=>[r.id,r])),nodes=new Map(D.nodes.map(n=>[n.id,n]));let selected=null;
 for(const key of ['provider','entity_type','status','modality']){const values=key==='modality'?records.flatMap(r=>[...(r.inputs||[]),...(r.outputs||[])]):records.map(r=>r[key]);for(const v of [...new Set(values)].sort()){const option=el('option',key==='provider'?v:label(v));option.value=v;$('catalog-'+key).append(option);}}
 function navigate(id){if(map.has(id))select(id);else if(nodes.has(id))chooseNode(id,true);}
 function select(id,scroll=false,historyMode='push'){if(!map.has(id)){if(historyMode==='none'){selected=null;$('catalog-detail').replaceChildren(el('p','未知目录 ID，未自动替换为其他实体。'));$('catalog-graph').replaceChildren();$('catalog-relations').replaceChildren();for(const b of $('catalog-results').querySelectorAll('button'))b.setAttribute('aria-current','false');}return;}selected=id;const r=map.get(id),root=$('catalog-detail');root.replaceChildren(el('h3',r.title),el('p',introduction(r)));const dl=el('dl');
 for(const [heading,value] of Object.entries({'最终 QA 接纳状态':label(r.qa_disposition),'目录 ID':r.id,'精确标识':r.exact_id,'实体类型（不合并别名、报告、权重与服务）':label(r.entity_type),'厂商':r.provider,'家族':r.family,'版本':r.version,'输入':readable(r.inputs,'inputs'),'输出':readable(r.outputs,'outputs'),'原始模态定义':readable(r.modality,'modality'),'生命周期与适用范围':readable(r.lifecycle,'lifecycle'),'访问条件':readable(r.access,'access'),'权重许可':r.weights_license,'代码许可':r.code_license,'日期（不从型号推断）':readable(r.dates,'dates'),'来源核验日（不是构建日）':r.checked_at,'来源包':r.source_bundle}))dl.append(el('dt',heading),el('dd',value));const metadata=el('details');metadata.append(el('summary','精确版本、标识、许可与完整技术字段'),dl);root.append(metadata,el('p',r.license_scope_note),el('h4','限制、修订与访问观察'),el('p',readable(r.limitations)),el('p',readable(r.access_observations)));
 for(const [kind,url] of Object.entries(r.urls)){const p=el('p',(fieldLabels[kind]||kind)+'：');p.append(url?link(url):el('span','未知 / 本轮未核验'));root.append(p);}
 const evidence=el('details');evidence.append(el('summary','官方来源与逐字段证据'));root.append(evidence);for(const s of r.sources){const p=el('p');p.append(link(s.url),el('p',readable(s)));evidence.append(p);}
 root.append(el('p','官方教程仅链接；未执行 SDK、下载模型或验证服务可用性。'));if(r.unresolved_links.length)root.append(el('h4','未接入图谱的原始关联（目标不存在或身份未消歧）'),el('p',readable(r.unresolved_links)));
 const raw=el('details');raw.append(el('summary','完整目录与历史原始记录（无字段丢弃；旧 pending 不代表最终接纳，原 19:46:00Z 实为分钟精度）'),el('pre',r));root.append(raw);
 const ul=$('catalog-relations');ul.replaceChildren();for(const edge of r.links){const target=map.get(edge.target)||nodes.get(edge.target),li=el('li');li.append(button(target.title,()=>navigate(edge.target)),el('span',' · '+label(edge.type)+' · '+label(edge.verification_status)),el('p',edge.note));ul.append(li);}if(!r.links.length)ul.append(el('li','暂无已接入关联；原始建议保留，不创建虚构目标。'));
 const svg=$('catalog-graph');svg.replaceChildren();const make=(tag,attrs)=>{const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,String(v));return e;};
 const ids=[id,...new Set(r.links.map(e=>e.target))].slice(0,9);ids.forEach((nid,i)=>{const x=i?500+340*Math.cos(2*Math.PI*(i-1)/(ids.length-1)):500,y=i?230+175*Math.sin(2*Math.PI*(i-1)/(ids.length-1)):230;if(i)svg.append(make('line',{x1:500,y1:230,x2:x,y2:y,class:'edge editorial'}));const g=make('g',{class:'graph-node'+(!i?' center':''),role:'button',tabindex:0,'aria-label':(map.get(nid)||nodes.get(nid)).title});g.append(make('rect',{x:x-110,y:y-23,width:220,height:46,rx:20}));const t=make('text',{x,y:y+4,'text-anchor':'middle'});t.textContent=(map.get(nid)||nodes.get(nid)).title;g.append(t);g.addEventListener('click',()=>navigate(nid));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();navigate(nid);}});svg.append(g);});
 for(const b of $('catalog-results').querySelectorAll('button'))b.setAttribute('aria-current',String(b.dataset.id===id));if(writeNavigation)writeNavigation('catalog',id,historyMode);else if(historyMode!=='none'){const same=new URLSearchParams(location.search).get('catalog')===id&&!new URLSearchParams(location.search).has('node')&&!location.hash;if(historyMode==='replace'||!same)history[historyMode==='replace'?'replaceState':'pushState'](null,'','?catalog='+encodeURIComponent(id));}if(scroll&&!discovery)$('vendor-catalog').scrollIntoView({behavior:'auto'});
 }
 function render(){const filters={};for(const k of ['query','provider','entity_type','status','modality'])filters[k]=$('catalog-'+k).value;const found=search(records,filters);$('catalog-count').textContent=found.length+' / '+records.length+' 目录记录；不是新增模型数。';const ul=$('catalog-results');ul.replaceChildren();for(const r of (discovery?discovery.pageRows(found,'catalog-page','catalog-pagination'):found)){const li=el('li'),b=button(r.title,()=>select(r.id));b.dataset.id=r.id;b.setAttribute('aria-current',String(r.id===selected));b.append(el('small',r.provider+' / '+label(r.entity_type)),el('small',label(r.status)+' · 访问：'+label(r.access)),el('p',introduction(r))); li.append(b);ul.append(li);}if(!found.length)ul.append(el('li','无匹配记录。重置筛选后重试。'));}
 $('catalog-filters').addEventListener('submit',e=>e.preventDefault());$('catalog-filters').addEventListener('input',()=>discovery?discovery.changeFilters('vendor-catalog','catalog-page'):render());$('catalog-filters').addEventListener('reset',e=>{if(discovery){e.preventDefault();discovery.resetFilters(['catalog-query','catalog-provider','catalog-entity_type','catalog-modality','catalog-status'],'vendor-catalog','catalog-page');}else setTimeout(render,0);});
 const evidence=$('catalog-evidence');for(const bundle of catalog.bundles){const details=el('details');details.append(el('summary',bundle.file+' · 覆盖/未知/冲突/修订与完整来源包'),el('pre',bundle));evidence.append(details);const a=el('a','下载原字节 '+bundle.file);a.href='vendor-catalog/'+bundle.file;a.download=bundle.file;evidence.append(a);}evidence.append(el('p',readable(catalog.admission)));
 render();if(!writeNavigation){const initial=new URLSearchParams(location.search).get('catalog');if(initial!==null)select(initial,true,'none');
 global.addEventListener('popstate',()=>{const id=new URLSearchParams(location.search).get('catalog');if(id!==null)select(id,false,'none');});}
 return {select,search,render};
 }
 global.ModelAtlasCatalog={search,mount,validate,initialize};if(typeof module!=='undefined')module.exports={search,validate,initialize,label,readable,introduction};
})(typeof window==='undefined'?globalThis:window);
