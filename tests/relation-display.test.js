// Original synthetic DOM + session-history model; executes full production scripts offline.
// Does not replace real browser Back/Forward, focus, scroll, or accessibility QA.
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.join(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'dist/data.json')));
class E{
 constructor(tag){this.tag=tag;this.children=[];this.events={};this.dataset={};this.attrs={};this.value='';this.textContent='';}
 append(...xs){this.children.push(...xs);}replaceChildren(...xs){this.children=xs;this.textContent='';}
 setAttribute(k,v){this.attrs[k]=v;}removeAttribute(k){delete this.attrs[k];}addEventListener(k,f){this.events[k]=f;}
 scrollIntoView(){this.scrolled=true;}querySelectorAll(tag){return this.children.flatMap(x=>[...(x.tag===tag?[x]:[]),...(x.querySelectorAll?.(tag)||[])]);}
}
async function boot(start='https://example.test/modelatlas/',omitCatalog=false,fixture=data){
 const ids=new Map([...fs.readFileSync(path.join(root,'web/index.html'),'utf8').matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new E('div')]));
 const entries=[start],writes=[],listeners={},stored=new Map();let index=0,url=new URL(start);
 const location={get search(){return url.search;},get hash(){return url.hash;}};
 function write(mode,next){url=new URL(next,url);if(mode==='push'){entries.splice(++index);entries.push(url.href);}else entries[index]=url.href;writes.push(mode);}
 const ctx={document:{getElementById:id=>ids.get(id),createElement:t=>new E(t),createTextNode:t=>({textContent:t}),createElementNS:(_,t)=>new E(t),querySelectorAll:()=>ids.get('results').querySelectorAll('button')},URL,URLSearchParams,Blob,location,history:{pushState:(_,__,s)=>write('push',s),replaceState:(_,__,s)=>write('replace',s)},localStorage:{getItem:k=>stored.get(k)||null,setItem:(k,v)=>stored.set(k,v)},addEventListener:(k,f)=>(listeners[k]??=[]).push(f),fetch:async()=>({ok:true,json:async()=>structuredClone(fixture)}),setTimeout:fn=>fn(),confirm:()=>true};ctx.window=ctx;vm.createContext(ctx);
 for(const name of ['core','reader','catalog','app'])if(!(omitCatalog&&name==='catalog'))await vm.runInContext(fs.readFileSync(path.join(root,'web',name+'.js'),'utf8'),ctx);
 assert.notEqual(ids.get('catalog-load-status').dataset.state,'initialization-error');
 const fire=k=>(listeners[k]||[]).forEach(f=>f());
 const click=(kind,id)=>{const b=ids.get(kind==='node'?'results':'catalog-results').querySelectorAll('button').find(b=>b.dataset.id===id);assert.ok(b,id);b.events.click();};
 return {ids,ctx,writes,entries,stored,click,url:()=>url,back(){assert.ok(index>0);url=new URL(entries[--index]);fire('popstate');},forward(){assert.ok(index<entries.length-1);url=new URL(entries[++index]);fire('popstate');},hash(id){write('push','#node='+id);fire('hashchange');}};
}

const C=require('../web/core.js');
const text=e=>[e.textContent||'',...e.children?.map(text)||[]].join('');
test('exact metadata vocabulary, editorial precedence, safe unknown fallback and purity',()=>{
 for(const edge of [{type:'learning_path'},{evidence_type:'editorial_cross_module'},{evidence_type:'editorial_learning_relation_not_vendor_integration_claim'},{verification_status:'editorial_learning_relation'}]){const before=JSON.stringify(edge);assert.equal(C.relationDisplay(edge).kind,'editorial');assert.equal(JSON.stringify(edge),before);}
 assert.equal(C.relationDisplay({type:'learning_path',verification_status:'primary_source_checked'}).kind,'editorial');
 assert.equal(C.relationDisplay({type:'editorial_learning_relation',evidence_type:'editorial_learning_relation_not_vendor_integration_claim',verification_status:'documentation_review_not_runtime_verified'}).kind,'editorial');
 assert.equal(C.relationDisplay({verification_status:'primary_source_checked'}).label,'来源文档关系，本库未运行核验');
 assert.equal(C.relationDisplay({type:'documented_migration_target',evidence_type:'official_documented_product_migration'}).label,'官方文档关系，非运行核验');
 for(const edge of [null,{verification_status:'documentation_review_not_runtime_verified'},{type:'documented_migration_target'},{evidence_type:'official_documented_product_migration'},{}, {type:'not_learning_path'},{evidence_type:'not_editorial_cross_module'},{verification_status:'unverified_primary_source_checked'}])assert.equal(C.relationDisplay(edge).kind,'unknown');
});
test('all 139 real edges retain identity and receive explicit classes',()=>{
 assert.equal(data.edges.length,151);const original=data.edges.slice(0,139);const before=JSON.stringify(original),counts={};
 for(const edge of original){const d=C.relationDisplay(edge);counts[d.kind]=(counts[d.kind]||0)+1;assert.ok(['editorial','documented','unknown'].includes(d.kind));if(['editorial_learning_order','editorial_learning_relation_not_vendor_integration_claim','editorial_cross_module'].includes(edge.evidence_type))assert.equal(d.kind,'editorial');}
 assert.deepEqual(counts,{editorial:84,documented:45,unknown:10});assert.equal(JSON.stringify(original),before);console.log('139 edge classifications',counts);
});
test('synthetic edge semantics remain verbatim text; source links, SVG classes and relation navigation work',async()=>{
 const fixture=structuredClone(data),a='transformer',b=data.nodes.find(n=>n.id!==a).id;
 const payload='<img src=x onerror=alert(1)> & exact';
 fixture.edges=[{source:a,target:b,type:'learning_path',direction_semantics:payload,unknown_boundary_zh:payload,source_urls:['https://example.test/evidence']},{source:a,target:b,type:'documented_migration_target',evidence_type:'official_documented_product_migration'},{source:a,target:b,type:'unrecognized'}];
 const h=await boot('https://example.test/modelatlas/?node='+a,false,fixture),list=h.ids.get('relations');
 assert.match(text(list),/编辑学习对照，非厂商集成/);assert.match(text(list),/官方文档关系，非运行核验/);assert.match(text(list),/关系性质待核验/);
 assert.equal(list.querySelectorAll('p').filter(e=>e.textContent===payload).length,2);assert.equal(list.querySelectorAll('img').length,0);assert.equal(list.querySelectorAll('a')[0].href,'https://example.test/evidence');
 assert.deepEqual(h.ids.get('graph').querySelectorAll('line').map(e=>e.attrs.class),['edge editorial','edge documented','edge unknown']);
 assert.ok(h.ids.get('graph').querySelectorAll('line').every(e=>e.attrs['aria-label'].includes('非')));
 list.querySelectorAll('button').find(e=>e.textContent===data.nodes.find(n=>n.id===b).title).events.click();assert.equal(h.url().search,'?node='+b);h.back();assert.equal(h.url().search,'?node='+a);assert.match(text(h.ids.get('relations')),/编辑学习对照/);
});

test('12 admitted relations classified independently without upgrading source review',()=>{
 const added=data.edges.slice(139),counts={};assert.equal(added.length,12);
 for(const e of added){const d=C.relationDisplay(e);counts[d.kind]=(counts[d.kind]||0)+1;assert.equal(e.application_status,'accepted_into_derived_graph_not_product_execution');assert.equal(e.candidate_status_at_research,'candidate_only_not_applied');assert.ok(e.unknown_boundary_zh);}
 assert.deepEqual(counts,{documented:1,editorial:11});assert.equal(C.relationDisplay({verification_status:'documentation_review_not_runtime_verified'}).kind,'unknown');
});
test('actual migration and editorial nodes retain limits and sources through repeated navigation',async()=>{
 const h=await boot('https://example.test/modelatlas/?node=office-zapier-agents');
 let list=h.ids.get('relations');assert.match(text(list),/官方文档关系，非运行核验/);assert.match(text(list),/未定 Agents 停用日/);assert.match(text(list),/on-demand/);assert.ok(list.querySelectorAll('a').some(x=>x.href.includes('Migrating-from-Agents-to-AI-by-Zapier')));
 h.click('node','assistant-chatgpt-deep-research');list=h.ids.get('relations');assert.match(text(list),/编辑学习对照，非厂商集成/);assert.match(text(list),/不推定同一模型/);assert.ok(list.querySelectorAll('a').length>=2);
 h.back();assert.equal(h.url().search,'?node=office-zapier-agents');assert.match(text(h.ids.get('relations')),/工具默认不暂停/);h.forward();assert.equal(h.url().search,'?node=assistant-chatgpt-deep-research');
});
