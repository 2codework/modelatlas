'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync(__dirname+'/../web/academy.js','utf8');
const core=source.slice(source.indexOf('const coreLessons='),source.indexOf('// Reading and region feedback'));
const search=source.slice(source.indexOf('const entries='),source.indexOf("const input=root.querySelector('#academy-search')"));
const {entries,searchTokens,matchesSearch}=vm.runInNewContext(core+search+';({entries,searchTokens,matchesSearch})');
const matches=(q)=>Array.from(entries.filter(item=>matchesSearch(item,searchTokens(q))));
const original=[...['foundations','tokens','tools','project','timeline','multimodal','resources','evaluation'].map(id=>'academy.html#'+id),'retrieval-lab.html','tiny-training.html','benchmark-practice.html','release-reading.html','attention-lab.html','video-sampling-lab.html','tokenization-lab.html','diffusion-noise-lab.html'];
test('all 16 entries retain exact original order, paired links and searchable titles',()=>{
 assert.deepEqual(Array.from(entries,x=>x.destinations[0]),original);
 for(const item of entries){assert.equal(item.destinations[1],item.destinations[0].replace('.html','-en.html'));for(const title of [item.zh,item.en])assert.ok(matches(title).includes(item),title);}
 assert.deepEqual(matches('attention').map(x=>x.destinations[0]),['academy.html#tokens','attention-lab.html']);
 assert.deepEqual(matches('video').map(x=>x.destinations[0]),['academy.html#multimodal','video-sampling-lab.html']);
 assert.deepEqual(matches('training').map(x=>x.destinations[0]),['academy.html#foundations','tiny-training.html']);
});
test('AND spans explicit title, keyword and destination fields, never property names',()=>{
 assert.deepEqual(matches('mask attention-lab').map(x=>x.destinations[0]),['attention-lab.html']);
 for(const q of ['keywords','destinations','kind','zh','modify','tention','trieval','qwen30','qwen3 80b'])assert.equal(matches(q).length,0,q);
 assert.deepEqual(matches('掩 mask atten').map(x=>x.destinations[0]),['attention-lab.html']);
});
test('numeric components have boundaries, word prefixes remain usable, dots retain versions',()=>{
 const item={zh:'',en:'Dify Qwen3-8B GPT-4.1 v1.20 alpha2.5',keywords:'',destinations:[]};
 const check=q=>matchesSearch(item,searchTokens(q));
 for(const q of ['dify','dif','qwen','qwen3','qwen3 8b','GPT 4','GPT 4.1','v1','v1.20','alpha2','alpha2.5','４．１'])assert.equal(check(q),true,q);
 for(const q of ['ify','wen','qwen30','8','4.10','4.2','1.2','v1.2','v1.200','alpha2.50','5','2.5'])assert.equal(check(q),false,q);
 assert.equal(matchesSearch({...item,en:'modify'},searchTokens('Dify')),false);
});
test('punctuation-only queries never return everything; Unicode normalization is search-only',()=>{
 for(const q of ['!!!','／－','😀',''])assert.equal(matches(q).length,0,q);
 assert.deepEqual(Array.from(searchTokens('ＡＴＴＥＮＴＩＯＮ掩码　ｍａｓｋ')),['attention','掩码','mask']);
 assert.deepEqual(matches('ＭＡＳＫ　attention').map(x=>x.destinations[0]),['attention-lab.html']);
});
