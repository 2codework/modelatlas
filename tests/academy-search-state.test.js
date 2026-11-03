'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/academy.js','utf8');
class Element{constructor(dataset={}){this.dataset=dataset;this.handlers={};this.children=[];this.attrs={};this.value='';this.textContent='';this.checked=false;this.hidden=false;}addEventListener(k,fn){this.handlers[k]=fn;}fire(k){this.handlers[k]?.();}focus(){this.focused=true;}setAttribute(k,v){this.attrs[k]=v;if(k==='href')this.href=v;}getAttribute(k){return k==='href'?(this.href||''):(this.attrs[k]||'');}append(x){this.children.push(x);}replaceChildren(){this.children=[];}}
function setup(initial={},blocked=false,language='en',search='',path='/academy-en.html',historyBlocked=false){const values=new Map(Object.entries(initial)),writes=[];const clear=new Element(),feedback=new Element(),events={},replacements=[];let failHistory=historyBlocked;const region=new Element(),remember=new Element(),notice=new Element(),input=new Element(),list=new Element(),note=new Element(),button=new Element({read:'tools',readLabel:'Read',unreadLabel:'Mark'}),zh=new Element({language:'zh'}),en=new Element({language:'en'});button.parentElement={querySelector:()=>note};const elements={'.academy-region':region,'.academy-remember-region':remember,'.academy-storage-status':notice,'#academy-search':input,'#academy-search-results':list,'#academy-search-clear':clear,'#academy-search-status':feedback};const root={dataset:{language},querySelector:s=>elements[s],querySelectorAll:s=>s==='[data-read]'?[button]:s==='a[href]'?[zh,en,external,lab,...list.children.flatMap(li=>li.children)]:[zh,en]};const external=new Element(),lab=new Element();external.href='https://example.org/source?q=original';lab.href='retrieval-lab-en.html';const ctx={URLSearchParams,window:{addEventListener:(k,fn)=>{(events[k]??=[]).push(fn);}},history:{state:{keep:true},replaceState:(state,unused,url)=>{if(failHistory)throw Error('blocked');replacements.push({state,url});const u=new URL(url,'https://example.test');ctx.location.search=u.search;ctx.location.hash=u.hash;}},document:{querySelector:()=>root,getElementById:()=>null,createElement:()=>new Element()},location:{search,pathname:path,hash:'#tools'},localStorage:{getItem:k=>{if(blocked)throw Error();return values.get(k)??null;},setItem:(k,v)=>{if(blocked)throw Error();writes.push(k);values.set(k,v);},removeItem:k=>{if(blocked)throw Error();values.delete(k);}}};vm.runInNewContext(code,ctx);return {clear,feedback,events,replacements,location:ctx.location,external,lab,denyHistory:v=>{failHistory=v;},fireWindow:(k,event={})=>events[k]?.forEach(fn=>fn(event)),values,writes,region,remember,notice,input,list,button,note,zh,en};}

for(const language of ['zh','en'])for(const path of ['/index.html','/academy.html','/academy-en.html'])test(`${language} ${path} restores and switches language without changing region`,()=>{
 const s=setup({},false,language,'?region=US&q=retrieval&keep=yes',path);assert.equal(s.input.value,'retrieval');assert.equal(s.list.children.length,1);assert.equal(s.replacements.length,0);s.zh.fire('click');const u=new URL(s.zh.href,'https://local/');assert.equal(u.searchParams.get('q'),'retrieval');assert.equal(u.searchParams.get('region'),'US');assert.equal(u.hash,path.endsWith('index.html')?'#home':'#tools');assert.equal(s.writes.length,0);
 s.region.value='CN';s.region.fire('change');assert.equal(new URLSearchParams(s.location.search).get('q'),'retrieval');assert.equal(new URLSearchParams(s.location.search).get('keep'),'yes');assert.equal(s.external.href,'https://example.org/source?q=original');assert.equal(s.lab.href,'retrieval-lab-en.html?region=CN');
});
test('history replacement, clear and restore preserve legacy records and avoid query leakage',()=>{
 const initial={'modelatlas.progress':'original','modelatlas.academy.read.v1':'["tools"]'};const s=setup(initial);
 for(const q of ['r','re','retrieval']){s.input.value=q;s.input.fire('input');}assert.equal(s.replacements.length,3);assert.ok(s.replacements.every(x=>x.state.keep));assert.equal(s.lab.href,'retrieval-lab-en.html?region=unknown');
 s.clear.fire('click');assert.equal(s.input.value,'');assert.equal(s.list.children.length,0);assert.equal(s.clear.hidden,true);assert.equal(s.input.focused,true);assert.equal(new URLSearchParams(s.location.search).has('q'),false);s.clear.fire('click');
 for(const k of ['popstate','pageshow']){s.location.search='?region=SG&q=retrieval';s.fireWindow(k,{persisted:true});assert.equal(s.input.value,'retrieval');assert.equal(s.list.children.length,1);assert.equal(s.region.value,'SG');s.location.search='?region=US&q=softmax';s.fireWindow(k);assert.equal(s.input.value,'softmax');assert.equal(s.list.children.length,1);}
 assert.equal(s.values.get('modelatlas.progress'),'original');assert.equal(s.values.get('modelatlas.academy.read.v1'),'["tools"]');assert.equal(s.writes.length,0);
});
test('URL reserved characters, malicious text, empty and bounded unicode are data',()=>{
 const s=setup();for(const q of ['a & ? # + % / 中文','<img src=x onerror=alert(1)>','   ','']){s.input.value=q;s.input.fire('input');const p=new URLSearchParams(s.location.search);assert.equal(p.get('q'),q.trim()?q:null);assert.equal(s.list.children.flatMap(x=>x.children).length,0);}
 s.input.value='😀'.repeat(250);s.input.fire('input');assert.equal(Array.from(s.input.value).length,200);assert.equal(new URLSearchParams(s.location.search).get('q'),s.input.value);assert.equal(s.writes.length,0);
});
test('storage and history denial remain usable and later recovery clears distinct feedback',()=>{
 const s=setup({},true,'en','', '/academy-en.html',true);s.input.value='retrieval';s.input.fire('input');assert.equal(s.list.children.length,1);assert.match(s.feedback.textContent,/URL could not/);s.fireWindow('pageshow',{persisted:true});assert.equal(s.input.value,'retrieval');s.denyHistory(false);s.input.fire('input');assert.equal(s.feedback.textContent,'');assert.equal(new URLSearchParams(s.location.search).get('q'),'retrieval');assert.equal(s.writes.length,0);
});

function resultLinks(s,q){s.input.value=q;s.input.fire('input');return s.list.children.flatMap(li=>li.children);}
for(const language of ['zh','en'])test(`${language}: reordered, mixed-language and fullwidth terms share an AND result`,()=>{
 const s=setup({},false,language,'?region=US'),suffix=language==='en'?'-en':'';
 for(const q of ['attention mask','mask attention','ATTEN MASK','注意力 mask','mask注意力','ＡＴＴＥＮＴＩＯＮ　ｍａｓｋ','  mask\tattention\nmask  ','attention-lab mask','attention 掩码 输出']){
  assert.deepEqual(resultLinks(s,q).map(a=>a.href),[`attention-lab${suffix}.html?region=US`],q);
  assert.equal(s.input.value,q);assert.equal(new URLSearchParams(s.location.search).get('q'),q);
 }
 for(const q of ['attention missing','mask training','tention mask','ask attention','!!!','３','Qwen30','Qwen3-80B','8']){
  assert.equal(resultLinks(s,q).length,0,q);assert.match(s.list.children[0].textContent,language==='en'?/No lesson or lab/:/未找到课程或实验/);
 }
 for(const q of ['qwen3 8b','８Ｂ ＱＷＥＮ３','release yarn','Qwen/Qwen3-8B'])assert.deepEqual(resultLinks(s,q).map(a=>a.href),[`release-reading${suffix}.html?region=US`],q);
 assert.equal(s.writes.length,0);
});
test('raw multi-term URL, language, history, BFCache, clear and concurrent marks stay isolated',()=>{
 const key='modelatlas.academy.read.v1',s=setup({[key]:'["tools"]','modelatlas.progress':'legacy'},false,'en','?region=US&keep=yes');
 const q='  ＡＴＴＥＮＴＩＯＮ　mask  ';resultLinks(s,q);s.zh.fire('click');
 let u=new URL(s.zh.href,'https://local/');assert.equal(u.searchParams.get('q'),q);assert.equal(u.searchParams.get('region'),'US');assert.equal(u.hash,'#tools');
 s.region.value='CN';s.region.fire('change');assert.equal(new URLSearchParams(s.location.search).get('q'),q);assert.equal(new URLSearchParams(s.location.search).get('keep'),'yes');
 assert.equal(s.list.children[0].children[0].href,'attention-lab-en.html?region=CN');
 s.values.set(key,'["tools","foundations","future-id"]');
 for(const event of ['popstate','pageshow']){
  s.location.search='?region=SG&q='+encodeURIComponent('mask attention');s.fireWindow(event,{persisted:true});
  assert.equal(s.input.value,'mask attention');assert.equal(s.region.value,'SG');assert.equal(s.list.children[0].children[0].href,'attention-lab-en.html?region=SG');
 }
 assert.equal(s.writes.length,0);s.button.fire('click');assert.equal(s.values.get(key),'["foundations","future-id"]');assert.equal(s.values.get('modelatlas.progress'),'legacy');
 s.clear.fire('click');assert.equal(s.input.focused,true);assert.equal(s.list.children.length,0);assert.equal(new URLSearchParams(s.location.search).has('q'),false);
 const long='Ａ'.repeat(199)+'😀'+'mask';resultLinks(s,long);assert.equal(s.input.value,'Ａ'.repeat(199)+'😀');assert.equal(new URLSearchParams(s.location.search).get('q'),s.input.value);
});
