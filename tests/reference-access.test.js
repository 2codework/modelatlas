'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),C=require('../web/core.js');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/data.json')));
class E{constructor(tag){this.tag=tag;this.children=[];this.attrs={};this.events={};this.textContent='';}append(...xs){this.children.push(...xs);}setAttribute(k,v){this.attrs[k]=v;}addEventListener(k,v){this.events[k]=v;}}
const doc={createElement:t=>new E(t)},all=e=>[e,...e.children.flatMap(all)],text=e=>[e.textContent,...e.children.map(text)].join(' ');
test('existing paper classifications are explicit, not inferred from title or domain',()=>{
 const n=D.nodes.find(n=>n.id==='transformer'),p=C.referenceAccess(n,D.sources);assert.equal(p.groups.papers[0].url,'https://arxiv.org/abs/1706.03762');assert.equal(p.version,'paper v1');assert.equal(p.checked_at,n.checked_at);
 const item={source_ids:['a','b'],source_urls:['https://arxiv.org/abs/fake']},sources=[{id:'a',url:'https://example.test/1',title:'Important paper',kind:'primary'},{id:'b',url:'https://example.test/2',kind:'official_metadata'}];const projection=C.referenceAccess(item,sources);assert.equal(projection.groups.papers.length,0);assert.equal(projection.groups.official.length,0);assert.equal(projection.groups.other.length,3);assert.match(projection.version,/未登记/);
});
test('catalog explicit report/model-card entries and missing versions do not invent evidence',()=>{
 const r=D.vendor_catalog.records.find(r=>r.urls.report),p=C.referenceAccess(r,[],true);assert.equal(p.groups.papers[0].url,C.safeURL(r.urls.report));assert.equal(p.version,r.version);assert.equal(p.groups.papers[0].checked_at,null);
 const missing=C.referenceAccess({urls:{report:null,model_card:null},sources:[],version:null,checked_at:null},[],true);assert.equal(missing.groups.papers.length,0);assert.equal(missing.checked_at,'未登记');
});
test('all actual projections preserve source records and only link registered safe URLs',()=>{
 const before=JSON.stringify(D);for(const n of D.nodes){const projected=C.referenceAccess(n,D.sources),allowed=new Set([...(n.source_urls||[]),...D.sources.filter(s=>(n.source_ids||[]).includes(s.id)).map(s=>s.url)].map(C.safeURL));for(const row of Object.values(projected.groups).flat())assert.ok(allowed.has(row.url),n.id+': '+row.url);}for(const r of D.vendor_catalog.records){const allowed=new Set([...Object.values(r.urls),...Object.values(C.catalogResourceOverlay(r)?.urls||{}),...r.sources.map(s=>s.url)].map(C.safeURL));for(const row of Object.values(C.referenceAccess(r,[],true).groups).flat())assert.ok(allowed.has(row.url));}assert.equal(JSON.stringify(D),before);
});
test('unsafe URLs, duplicate URLs and hostile labels remain inert without guessed fallback links',()=>{
 const item={source_urls:['javascript:alert(1)','https://user:pass@example.test','https://example.test/ok','https://example.test/ok'],source_ids:['a']};const sources=[{id:'a',title:'<img src=x onerror=evil>',kind:'paper',url:'https://example.test/ok'}];const p=C.referenceAccess(item,sources);assert.equal(Object.values(p.groups).flat().length,1);const tree=C.referenceAccessDOM(item,sources,{},doc);assert.equal(all(tree).filter(e=>e.tag==='a').length,1);assert.ok(text(tree).includes(sources[0].title));assert.equal(all(tree).some(e=>['img','script'].includes(e.tag)),false);
});
test('source controls call only supplied local disclosure actions and preserve missing-state wording',()=>{
 let sources=0,meta=0;const tree=C.referenceAccessDOM({},[],{onAllSources:()=>sources++,onMetadata:()=>meta++},doc);const buttons=all(tree).filter(e=>e.tag==='button');assert.equal(buttons.length,2);buttons[0].events.click();buttons[0].events.click();buttons[1].events.click();assert.equal(sources,2);assert.equal(meta,1);assert.match(text(tree),/不代表该资料不存在/);assert.match(text(tree),/不是发布日期/);assert.match(text(tree),/不表示当前可访问/);assert.match(text(tree),/链接页面可能更新，请核对记录版本/);
});
test('catalog tutorial field is a registered use-resource, not a promise the URL is a tutorial',()=>{const item={urls:{tutorial:'https://example.test/pricing'},sources:[]};const tree=C.referenceAccessDOM(item,[],{catalog:true},doc);assert.match(text(tree),/使用资料（登记入口）/);assert.match(text(tree),/文档与代码入口/);assert.doesNotMatch(text(tree),/官方教程参考/);});
test('missing document titles use truthful reader labels rather than internal source IDs',()=>{const n=D.nodes.find(n=>n.id==='transformer'),p=C.referenceAccess(n,D.sources);assert.equal(p.groups.papers[0].title,'论文／报告来源（未登记标题）');assert.equal(p.groups.papers[0].source_id,'found-src-005');const tree=C.referenceAccessDOM(n,D.sources,{},doc);assert.doesNotMatch(text(tree),/found-src-005/);assert.match(text(tree),/未登记标题/);});

test('DeepSeek overlay affects exactly four reviewed identities without changing original evidence or aliases',()=>{
 const before=JSON.stringify(D),expected=['deepseek-flash','deepseek-v4-pro','deepseek-v4-flash','deepseek-v4-flash-vision-exp'];
 const records=D.vendor_catalog.records.filter(r=>C.catalogResourceOverlay(r));assert.deepEqual(records.map(r=>r.exact_id),expected);
 for(const r of records){const overlay=C.catalogResourceOverlay(r),p=C.referenceAccess(r,[],true),tree=C.referenceAccessDOM(r,[],{catalog:true},doc);
  assert.equal(overlay.urls.pricing_reference,r.urls.tutorial);assert.ok(r.sources.some(s=>s.url===overlay.urls.pricing_reference));assert.equal(overlay.checked_at,'2026-10-31');assert.equal(overlay.status,'read_not_executed');
  assert.deepEqual(p.groups.official.map(s=>s.url),Object.values(overlay.urls));assert.match(text(tree),/官方首个 API 请求指南/);assert.match(text(tree),/价格与模型映射参考（非教程）/);assert.match(text(tree),/未执行/);assert.match(text(tree),/价格及别名路由/);assert.doesNotMatch(text(tree),/\$[0-9]/);
  assert.equal(C.catalogResourceOverlay({...r,exact_id:'unrelated'}),null);assert.equal(C.catalogResourceOverlay({...r,id:'unrelated'}),null);assert.equal(C.catalogResourceOverlay({...r,urls:{tutorial:'https://example.test/pricing'}}),null);
 }
 assert.equal(records[2].entity_type,'legacy_api_alias');assert.equal(records[3].entity_type,'legacy_api_alias');assert.equal(JSON.stringify(D),before);
});
