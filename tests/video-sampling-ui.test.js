'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),api=require('../web/video-sampling.js');
function setup(lang='en',url='?region=SG'){
 const e={},element=()=>({value:'',textContent:'',hidden:false,children:[],events:{},options:[],replaceChildren(){this.children=[];},append(...x){this.children.push(...x);},setAttribute(k,v){this[k]=v;},addEventListener(k,fn){this.events[k]=fn;}});
 for(const id of ['sequence','stride','offset','answer','claim','reset','check','samples','summary','omitted','result','error','feedback','report','report-facts','report-limits'])e[id]=element();
 e.offset.options=Array.from({length:4},(_,i)=>({value:String(i),disabled:false}));
 const links=['academy.html#multimodal','video-sampling-lab-en.html','academy-en.html#evaluation','https://arxiv.org/html/2311.17982v1'].map(href=>({href,getAttribute(){return this.href;},setAttribute(_,v){this.href=v;}}));e.links=links;
 vm.runInNewContext(fs.readFileSync(require.resolve('../web/video-sampling-lab.js'),'utf8'),{URLSearchParams,location:{search:url.split('#')[0],hash:url.includes('#')?'#'+url.split('#')[1]:''},window:{VideoSampling:api},document:{documentElement:{lang},getElementById:id=>e[id],createElement:element,createElementNS:element,querySelectorAll:()=>links}});
 return e;
}
function change(e,id,value){e[id].value=value;e[id].events.change();}
for(const lang of ['en','zh-CN']){
 test(`${lang}: sampling, stride offset constraints and repeat reset`,()=>{
  const e=setup(lang);assert.equal(e.samples.children.length,3);assert.match(e.samples.children[1].children[1].textContent,/F4/);
  change(e,'offset','3');assert.match(e.samples.children[0].children[1].textContent,/F3.*B/);
  change(e,'stride','1');assert.equal(e.offset.value,'0');assert.equal(e.samples.children.length,9);assert.equal(e.offset.options[1].disabled,true);
  e.reset.events.click();e.reset.events.click();assert.equal(e.samples.children.length,3);assert.equal(e.report.hidden,true);
 });
 test(`${lang}: wrong sequence, blank, missing evidence, wrong claim and success recovery`,()=>{
  const e=setup(lang);e.check.events.click();assert.ok(e.feedback.textContent);assert.equal(e.report.hidden,true);
  change(e,'sequence','exercise');e.check.events.click();assert.ok(e.feedback.textContent);assert.equal(e.report.hidden,true);
  change(e,'answer','5');change(e,'claim','limited');e.check.events.click();assert.equal(e.report.hidden,true);
  change(e,'offset','1');change(e,'claim','continuous');e.check.events.click();assert.equal(e.report.hidden,true);
  change(e,'claim','limited');e.check.events.click();assert.equal(e.report.hidden,false);assert.match(e['report-facts'].textContent,/F5 · 1250 ms · ID C · x=60/);assert.ok(e['report-limits'].textContent);
  change(e,'answer','4');assert.equal(e.report.hidden,true);assert.equal(e['report-facts'].textContent,'');
  change(e,'answer','5');e.check.events.click();assert.equal(e.report.hidden,false);change(e,'stride','1');assert.equal(e.report.hidden,true);
 });
 test(`${lang}: invalid config clears stale results; reset recovers`,()=>{
  const e=setup(lang);change(e,'sequence','unknown');assert.equal(e.result.hidden,true);assert.equal(e.samples.children.length,0);assert.equal(e.summary.textContent,'');assert.ok(e.error.textContent);e.reset.events.click();assert.equal(e.result.hidden,false);assert.equal(e.error.textContent,'');
 });
 test(`${lang}: locale preserves valid attempt but not passed result`,()=>{
  const e=setup(lang);change(e,'sequence','exercise');change(e,'offset','1');change(e,'answer','5');change(e,'claim','limited');e.check.events.click();assert.equal(e.report.hidden,false);
  const href=e.links[1].href;assert.match(href,/\?region=SG#sequence=exercise&stride=4&offset=1&answer=5&claim=limited/);
  const second=setup(lang==='en'?'zh-CN':'en',href.slice(href.indexOf('?')));assert.equal(second.answer.value,'5');assert.equal(second.offset.value,'1');assert.equal(second.report.hidden,true);assert.ok(second.feedback.textContent);second.check.events.click();assert.equal(second.report.hidden,false);
 });
}
test('allowlist, duplicates, query-only state, unsupported region and external links',()=>{
 for(const url of ['?region=bad#sequence=bad&stride=99&offset=9&answer=x&claim=passed','?region=CN&region=US#stride=2&stride=4&answer=5&answer=3','?sequence=exercise&stride=1&answer=5&claim=limited']){
  const e=setup('en',url);assert.equal(e.sequence.value,'worked');assert.equal(e.stride.value,'4');assert.equal(e.answer.value,'');assert.equal(e.report.hidden,true);assert.equal(e.links[0].href,'academy.html?region=unknown#multimodal');assert.equal(e.links[3].href,'https://arxiv.org/html/2311.17982v1');
 }
 const e=setup('en','?region=CN#sequence=exercise&stride=2&offset=3&answer=5&claim=limited&passed=1');assert.equal(e.offset.value,'0');assert.equal(e.report.hidden,true);assert.ok(!e.links[1].href.includes('passed'));assert.equal(e.links[2].href,'academy-en.html?region=CN#evaluation');
});
test('static bilingual content and assets contain reference, limits and no active network/storage',()=>{
 for(const suffix of ['', '-en']){
  const html=fs.readFileSync(require.resolve('../web/video-sampling-lab'+suffix+'.html'),'utf8');
  for(const expected of ['F3 · 750 ms · ID B · x=40','F5 · 1250 ms · ID C · x=60','<noscript>','<details>','connect-src \'none\'','video-sampling.js','id="report" hidden'])assert.ok(html.includes(expected),expected);
 }
 for(const name of ['video-sampling.js','video-sampling-lab.js'])assert.doesNotMatch(fs.readFileSync(require.resolve('../web/'+name),'utf8'),/fetch\(|XMLHttpRequest|localStorage|sessionStorage|innerHTML/);
});
test('academy propagates independent region to new bilingual lab links',()=>{
 const region={value:'',addEventListener(k,fn){this[k]=fn;}},remember={checked:false,addEventListener(){}},status={textContent:''};
 const links=['video-sampling-lab.html','video-sampling-lab-en.html','https://example.org/video-sampling-lab.html'].map(href=>({href,getAttribute(){return this.href;},setAttribute(_,v){this.href=v;}}));
 const root={dataset:{language:'en'},querySelector:s=>s==='.academy-region'?region:s==='.academy-remember-region'?remember:s==='.academy-storage-status'?status:null,querySelectorAll:s=>s==='a[href]'?links:[]};
 vm.runInNewContext(fs.readFileSync(require.resolve('../web/academy.js'),'utf8'),{URLSearchParams,document:{querySelector:()=>root,getElementById:()=>null},location:{search:'?region=GB'},localStorage:{getItem:()=>null,removeItem(){}}});
 assert.equal(links[0].href,'video-sampling-lab.html?region=GB');assert.equal(links[1].href,'video-sampling-lab-en.html?region=GB');
 region.value='CN';region.change();assert.equal(links[1].href,'video-sampling-lab-en.html?region=CN');assert.equal(links[2].href,'https://example.org/video-sampling-lab.html');
});
