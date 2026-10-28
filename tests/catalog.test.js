const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {search}=require('../web/catalog.js'),data=JSON.parse(fs.readFileSync(__dirname+'/../dist/data.json'));
test('catalog search preserves case-sensitive originals while matching case-insensitively',()=>{const found=search(data.vendor_catalog.records,{query:'QWEN-RESEARCH'});assert.ok(found.length);assert.equal(found[0].raw.official_license,'qwen-research');});
test('catalog filters compose across provider/type/modality/status',()=>{const r=data.vendor_catalog.records[0];assert.ok(search(data.vendor_catalog.records,{provider:r.provider,entity_type:r.entity_type,status:r.status,modality:r.inputs[0]}).includes(r));assert.equal(search(data.vendor_catalog.records,{provider:'missing'}).length,0);});
class N{constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.value='';this.events={};this.dataset={};this.attrs={};}append(...xs){this.children.push(...xs);}replaceChildren(...xs){this.children=xs;}setAttribute(k,v){this.attrs[k]=v;}addEventListener(k,f){this.events[k]=f;}querySelectorAll(tag){return this.children.flatMap(x=>[...(x.tag===tag?[x]:[]),...x.querySelectorAll(tag)]);}scrollIntoView(){this.scrolled=true;}}
function setup(query,fixture=data){const ids=new Map();const get=id=>{if(!ids.has(id))ids.set(id,new N('div'));return ids.get(id);};const ctx={URLSearchParams,ModelAtlasCore:require('../web/core.js'),document:{getElementById:get,createElement:t=>new N(t),createElementNS:(_,t)=>new N(t)},location:{search:query},history:{replaceState:(_,__,url)=>{ctx.location.search=url;},pushState:(_,__,url)=>{ctx.location.search=url;}},addEventListener(){},setTimeout:fn=>fn()};ctx.window=ctx;vm.runInNewContext(fs.readFileSync(__dirname+'/../web/catalog.js','utf8'),ctx);const chosen=[];const api=ctx.ModelAtlasCatalog.mount(fixture,id=>chosen.push(id));return{ctx,get,api,chosen};}
test('catalog deep link renders full record, graph and equivalent list with safe text',()=>{const id=data.vendor_catalog.records[0].id,{get,ctx}=setup('?catalog='+id);assert.equal(ctx.location.search,'?catalog='+id);assert.equal(get('catalog-results').children.length,77);assert.ok(get('catalog-detail').children.length>10);assert.ok(get('catalog-graph').children.length);assert.ok(get('catalog-relations').children.length);assert.equal(get('vendor-catalog').scrolled,true);});
test('unknown catalog deep link remains explicit and never selects another entity',()=>{const {ctx,get}=setup('?catalog=missing');assert.equal(ctx.location.search,'?catalog=missing');assert.ok(get('catalog-detail').children[0].textContent.includes('未知目录 ID'));});
test('render path does not interpret HTML and repeats/reset without duplicate rows',()=>{const {get,api}=setup('');const id=data.vendor_catalog.records[0].id;api.select(id);api.select(id);get('catalog-query').value='<script>';get('catalog-filters').events.input();assert.equal(get('catalog-results').children.length,1);get('catalog-query').value='';get('catalog-filters').events.reset();assert.equal(get('catalog-results').children.length,77);assert.ok(!fs.readFileSync(__dirname+'/../web/catalog.js','utf8').includes('innerHTML'));});

const {label,readable,introduction}=require('../web/catalog.js');
const content=n=>[n.textContent,...n.children.map(content)].join('\n');
test('reader introduces missing summaries from exact recorded fields only',()=>{
 const r=data.vendor_catalog.records.find(r=>r.exact_id==='Qwen/Qwen3-0.6B');
 const intro=introduction(r);assert.match(intro,/Alibaba\/Qwen 的模型检查点/);assert.match(intro,/输入：文本；输出：文本/);assert.match(intro,/不表示服务当前可用/);
 const {get}=setup('?catalog='+r.id);const detail=get('catalog-detail');assert.equal(detail.children[1].textContent,intro);
 assert.match(content(detail),/Apache-2.0/);assert.match(content(detail),/官方教程参考；未执行/);assert.match(content(detail),/未完整审阅论文/);assert.match(content(detail),/open weights 不等于 open source/);
 assert.equal(detail.querySelectorAll('details')[0].attrs.open,undefined);
 assert.deepEqual(JSON.parse(detail.querySelectorAll('pre')[0].textContent),r);
});
test('known labels translate; new values and exact quotations never disappear',()=>{
 assert.equal(label('deprecated'),'已弃用（不等于已退役）');assert.equal(label('future_status'),'future_status');assert.equal(label('__proto__'),'__proto__');
 assert.equal(readable(null),'未知 / 本轮未核验');assert.match(readable([]),/不代表不存在/);
 assert.equal(readable({note:'active',exact_id:'text',status:'future_status'}),'说明：active\nexact_id：text\n资料状态：future_status');
 assert.equal(introduction({summary:'source conflict: A ≠ B'}),'source conflict: A ≠ B');
});
test('reader uses text-only rendering and rejects unsafe source links',()=>{
 const fixture=JSON.parse(JSON.stringify(data)),r=fixture.vendor_catalog.records[0];
 r.summary='<img src=x onerror=alert(1)>';r.sources=[{url:'javascript:alert(1)',sourceproof_zh:'<script>bad()</script>',status:'primary_content_read'}];r.urls={report:'data:text/html,bad',repository:'https://example.com/model'};
 const {get}=setup('?catalog='+r.id,fixture);assert.equal(get('catalog-detail').children[1].textContent,r.summary);
 const links=get('catalog-detail').querySelectorAll('a');assert.equal(links.filter(a=>a.href).length,1);assert.equal(links.find(a=>a.href).href,'https://example.com/model');
 assert.match(content(get('catalog-detail')),/<script>bad\(\)<\/script>/);
});
test('every record renders without mutating any data or hiding full conditions',()=>{
 const before=JSON.stringify(data),{api,get}=setup('');
 for(const r of data.vendor_catalog.records){api.select(r.id);const detail=get('catalog-detail');assert.deepEqual(JSON.parse(detail.querySelectorAll('pre')[0].textContent),r);assert.match(content(detail),/未执行 SDK/);assert.equal(detail.children[1].textContent,introduction(r));}
 assert.equal(JSON.stringify(data),before);
});
