'use strict';
(function(global){
 const text=value=>value===null||value===undefined||value===''?'未知 / 本轮未核验':typeof value==='object'?JSON.stringify(value,null,2):String(value);
 const search=(records,filters)=>records.filter(r=>(!filters.query||JSON.stringify(r).toLocaleLowerCase().includes(filters.query.toLocaleLowerCase()))&&['provider','entity_type','status'].every(k=>!filters[k]||r[k]===filters[k])&&(!filters.modality||[...(r.inputs||[]),...(r.outputs||[])].includes(filters.modality)));
 function mount(D,chooseNode){
 const $=id=>document.getElementById(id),catalog=D.vendor_catalog;if(!catalog)return;
 const el=(tag,value)=>{const e=document.createElement(tag);if(value!==undefined)e.textContent=text(value);return e;};
 const button=(label,fn)=>{const b=el('button',label);b.type='button';b.addEventListener('click',fn);return b;};
 const link=(url,label)=>{const a=el('a',label||url),safe=ModelAtlasCore.safeURL(url);if(safe&&safe.startsWith('https:')){a.href=safe;a.target='_blank';a.rel='noopener noreferrer';}return a;};
 const records=catalog.records,map=new Map(records.map(r=>[r.id,r])),nodes=new Map(D.nodes.map(n=>[n.id,n]));let selected=null;
 for(const key of ['provider','entity_type','status','modality']){const values=key==='modality'?records.flatMap(r=>[...(r.inputs||[]),...(r.outputs||[])]):records.map(r=>r[key]);for(const v of [...new Set(values)].sort()){const option=el('option',v);option.value=v;$('catalog-'+key).append(option);}}
 function navigate(id){if(map.has(id))select(id);else if(nodes.has(id))chooseNode(id,true);}
 function select(id,scroll=false){if(!map.has(id))return;selected=id;const r=map.get(id),root=$('catalog-detail');root.replaceChildren(el('h3',r.title),el('p',r.summary));const dl=el('dl');
 for(const [label,value] of Object.entries({'最终 QA 接纳状态':r.qa_disposition,'目录 ID':r.id,'精确标识':r.exact_id,'实体类型（不合并别名、报告、权重与服务）':r.entity_type,'厂商':r.provider,'家族':r.family,'版本':r.version,'输入':r.inputs,'输出':r.outputs,'原始模态定义':r.modality,'生命周期与适用范围':r.lifecycle,'访问条件':r.access,'权重许可':r.weights_license,'代码许可':r.code_license,'日期（不从型号推断）':r.dates,'来源核验日（不是构建日）':r.checked_at,'来源包':r.source_bundle}))dl.append(el('dt',label),el('dd',value));root.append(dl,el('p',r.license_scope_note),el('h4','限制、修订与访问观察'),el('pre',r.limitations),el('pre',r.access_observations));
 for(const [kind,url] of Object.entries(r.urls)){const p=el('p',kind+'：');p.append(url?link(url):el('span','未知 / 本轮未核验'));root.append(p);}
 root.append(el('h4','官方来源与证据'));for(const s of r.sources){const p=el('p');p.append(link(s.url),el('pre',s));root.append(p);}
 root.append(el('p','官方教程仅链接；未执行 SDK、下载模型或验证服务可用性。'));if(r.unresolved_links.length)root.append(el('h4','未接入图谱的原始关联（目标不存在或身份未消歧）'),el('pre',r.unresolved_links));
 const raw=el('details');raw.append(el('summary','完整历史原始记录（无字段丢弃；旧 pending 不代表最终接纳，原 19:46:00Z 实为分钟精度）'),el('pre',r.raw));root.append(raw);
 const ul=$('catalog-relations');ul.replaceChildren();for(const edge of r.links){const target=map.get(edge.target)||nodes.get(edge.target),li=el('li');li.append(button(target.title,()=>navigate(edge.target)),el('span',' · '+edge.type+' · '+edge.verification_status),el('pre',edge.note));ul.append(li);}if(!r.links.length)ul.append(el('li','暂无已接入关联；原始建议保留，不创建虚构目标。'));
 const svg=$('catalog-graph');svg.replaceChildren();const make=(tag,attrs)=>{const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,String(v));return e;};
 const ids=[id,...new Set(r.links.map(e=>e.target))].slice(0,9);ids.forEach((nid,i)=>{const x=i?500+340*Math.cos(2*Math.PI*(i-1)/(ids.length-1)):500,y=i?230+175*Math.sin(2*Math.PI*(i-1)/(ids.length-1)):230;if(i)svg.append(make('line',{x1:500,y1:230,x2:x,y2:y,class:'edge editorial'}));const g=make('g',{class:'graph-node'+(!i?' center':''),role:'button',tabindex:0,'aria-label':(map.get(nid)||nodes.get(nid)).title});g.append(make('rect',{x:x-110,y:y-23,width:220,height:46,rx:20}));const t=make('text',{x,y:y+4,'text-anchor':'middle'});t.textContent=(map.get(nid)||nodes.get(nid)).title;g.append(t);g.addEventListener('click',()=>navigate(nid));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();navigate(nid);}});svg.append(g);});
 for(const b of $('catalog-results').querySelectorAll('button'))b.setAttribute('aria-current',String(b.dataset.id===id));history.replaceState(null,'','?catalog='+encodeURIComponent(id));if(scroll)$('vendor-catalog').scrollIntoView({behavior:'auto'});
 }
 function render(){const filters={};for(const k of ['query','provider','entity_type','status','modality'])filters[k]=$('catalog-'+k).value;const found=search(records,filters);$('catalog-count').textContent=found.length+' / '+records.length+' 目录记录；不是新增模型数。';const ul=$('catalog-results');ul.replaceChildren();for(const r of found){const li=el('li'),b=button(r.title,()=>select(r.id));b.dataset.id=r.id;b.setAttribute('aria-current',String(r.id===selected));b.append(el('small',r.provider+' / '+r.entity_type));li.append(b);ul.append(li);}if(!found.length)ul.append(el('li','无匹配记录。重置筛选后重试。'));}
 $('catalog-filters').addEventListener('submit',e=>e.preventDefault());$('catalog-filters').addEventListener('input',render);$('catalog-filters').addEventListener('reset',()=>setTimeout(render,0));
 const evidence=$('catalog-evidence');for(const bundle of catalog.bundles){const details=el('details');details.append(el('summary',bundle.file+' · 覆盖/未知/冲突/修订与完整来源包'),el('pre',bundle));evidence.append(details);const a=el('a','下载原字节 '+bundle.file);a.href='vendor-catalog/'+bundle.file;a.download=bundle.file;evidence.append(a);}evidence.append(el('pre',catalog.admission));
 render();const initial=new URLSearchParams(location.search).get('catalog');if(map.has(initial))select(initial,true);else if(initial)$('catalog-detail').append(el('p','未知目录 ID，未自动替换为其他实体。'));
 global.addEventListener('popstate',()=>{const id=new URLSearchParams(location.search).get('catalog');if(map.has(id))select(id);});
 return {select,search};
 }
 global.ModelAtlasCatalog={search,mount};if(typeof module!=='undefined')module.exports={search};
})(typeof window==='undefined'?globalThis:window);
