'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),{guidanceDOM}=require('../web/reader.js');
class E{constructor(tag,text){this.tag=tag;this.children=[];this.textContent=text||'';}append(...xs){this.children.push(...xs);}}
const doc={createElement:t=>new E(t)},all=e=>[e,...e.children.flatMap(all)],text=e=>[e.textContent,...e.children.map(text)].join(' '),D=JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'../dist/data.json')));
test('all 49 admitted best-practice records preserve ordered steps and acceptance as prose',()=>{
 const rows=D.nodes.filter(n=>n.best_practice_path);assert.equal(rows.length,49);
 for(const n of rows){const original=JSON.stringify(n),tree=guidanceDOM(n.best_practice_path,'best_practice',doc),nodes=all(tree);assert.equal(nodes.filter(x=>x.tag==='pre').length,0,n.id);assert.match(text(tree),/编辑学习建议 · 未执行/);assert.deepEqual(nodes.find(x=>x.tag==='ol').children.map(x=>x.textContent),n.best_practice_path.steps);assert.ok(nodes.some(x=>x.tag==='h5'&&x.textContent==='验收标准'));assert.ok(nodes.some(x=>x.tag==='p'&&x.textContent===n.best_practice_path.acceptance_zh));assert.equal(JSON.stringify(n),original);}
});
test('unknown keys and malformed known fields stay explicit in unchanged raw fallback',()=>{
 for(const row of [{status:'future_state',steps:['a','b'],acceptance_zh:'limit',future:{nested:'keep'}},{steps:[{instruction:'do not silently omit'}],acceptance_zh:42},['not the schema'],null]){
  const before=JSON.stringify(row),tree=guidanceDOM(row,'best_practice',doc),nodes=all(tree);assert.ok(nodes.some(x=>x.tag==='summary'&&x.textContent.includes('未适配')));assert.ok(nodes.some(x=>x.tag==='pre'&&x.textContent===JSON.stringify(row,null,2)));assert.equal(JSON.stringify(row),before);assert.doesNotMatch(text(tree),/已实测|已认证|运行成功/);
 }
});
test('known voice and parameter schemas expose conditions without JSON as ordinary prose',()=>{
 for(const n of D.nodes){for(const [key,kind] of [['streaming','streaming'],['reviewed_variants','variants'],['version_records','versions']])if(n.realtime_audio&&Object.hasOwn(n.realtime_audio,key)){const v=n.realtime_audio[key],before=JSON.stringify(v),tree=guidanceDOM(v,kind,doc);assert.equal(all(tree).filter(x=>x.tag==='pre').length,0,n.id+': '+key);assert.equal(JSON.stringify(v),before);}
 if(n.world_model_learning){const tree=guidanceDOM(n.world_model_learning.parameters,'parameters',doc);assert.equal(all(tree).filter(x=>x.tag==='pre').length,0,n.id);}}
 const v=D.nodes.find(n=>n.id==='speech-gpt-realtime-family').realtime_audio.version_records;const body=text(guidanceDOM(v,'versions',doc));assert.match(body,/计划停用日期（非已发生）/);assert.match(body,/非当前报价/);assert.match(body,/2027-01-20/);assert.match(body,/未知 \/ 未注明/);
});
test('text is inert, arrays are not coerced and false/null are distinct',()=>{
 const v={input:false,output:null,full_duplex:true,condition_zh:'<img src=x onerror=evil>'},tree=guidanceDOM(v,'streaming',doc),body=text(tree);assert.match(body,/否（仅来源记录）/);assert.match(body,/未知 \/ 未注明/);assert.match(body,/是（仅来源记录）/);assert.ok(body.includes(v.condition_zh));assert.equal(all(tree).some(x=>x.tag==='img'||x.tag==='script'),false);
});

test('unknown modality identifiers remain exact text, including prototype-like names',()=>{const tree=guidanceDOM([{exact_id:'sample',inputs:['__proto__','constructor','future-modality']}],'versions',doc);const items=all(tree).filter(x=>x.tag==='li').map(x=>x.textContent);for(const id of ['__proto__','constructor','future-modality'])assert.ok(items.includes(id));});
