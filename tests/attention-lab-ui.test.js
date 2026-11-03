'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const math = require('../web/attention-math.js');
function setup(lang, search='?region=SG') {
 const elements = {};
 const element = () => ({value:'', checked:false, textContent:'', hidden:false, children:[], events:{}, replaceChildren(){this.children=[];},append(x){this.children.push(x);},addEventListener(name, fn){this.events[name]=fn;}});
 for(const id of ['query','causal','rows','result','error','summary','normalizer','reset','answer','feedback','check']) elements[id]=element();
 elements.query.value='0';
 const links=['academy.html#tokens','attention-lab-en.html','academy-en.html#tools','https://arxiv.org/html/1706.03762v7'].map(href=>({href,getAttribute(){return this.href;},setAttribute(_,v){this.href=v;}}));
 elements.links=links;
 vm.runInNewContext(fs.readFileSync(require.resolve('../web/attention-lab.js'),'utf8'), {URLSearchParams,location:{search:search.split('#')[0],hash:search.includes('#')?'#'+search.split('#')[1]:''},window:{AttentionMath:math},document:{querySelectorAll:()=>links,documentElement:{lang},getElementById:id=>elements[id],createElement:element}});
 return elements;
}
for (const lang of ['en','zh-CN']) {
 test(`${lang}: query and mask update complete table`,()=>{
  const e=setup(lang);assert.match(e.summary.textContent,/7\.333333/);assert.equal(e.rows.children.length,3);
  e.causal.checked=true;e.causal.events.change();assert.match(e.summary.textContent,/2\.000000/);
  assert.equal(e.rows.children[1].children[5].textContent,'0.000000');
  e.query.value='2';e.query.events.change();assert.match(e.summary.textContent,/6\.000000/);
 });
 test(`${lang}: malformed state clears result and reset recovers`,()=>{
  const e=setup(lang);e.query.value='99';e.query.events.change();
  assert.equal(e.result.hidden,true);assert.equal(e.rows.children.length,0);assert.equal(e.summary.textContent,'');assert.ok(e.error.textContent.length>10);
  e.reset.events.click();assert.equal(e.result.hidden,false);assert.equal(e.error.textContent,'');assert.match(e.summary.textContent,/7\.333333/);
 });
 test(`${lang}: answer rejection, retry, success and repeat reset`,()=>{
  const e=setup(lang);e.check.events.click();assert.ok(e.feedback.textContent.length>0);
  const blank=e.feedback.textContent;e.answer.value='5';e.check.events.click();assert.notEqual(e.feedback.textContent,blank);
  e.answer.value='2';e.check.events.click();assert.match(e.feedback.textContent,/\[1, 0, 0\]/);
  e.reset.events.click();e.reset.events.click();assert.equal(e.feedback.textContent,'');assert.equal(e.answer.value,'');assert.equal(e.query.value,'0');assert.equal(e.causal.checked,false);
 });
}

test('navigation preserves valid region and chapter without changing external links',()=>{
 const e=setup('en');assert.equal(e.links[0].href,'academy.html?region=SG#tokens');assert.equal(e.links[1].href,'attention-lab-en.html?region=SG#query=0&mask=0');assert.equal(e.links[2].href,'academy-en.html?region=SG#tools');assert.equal(e.links[3].href,'https://arxiv.org/html/1706.03762v7');
});
test('invalid or missing region falls back to unknown',()=>{
 for(const q of ['', '?region=bad']) assert.equal(setup('en',q).links[0].href,'academy.html?region=unknown#tokens');
});

for (const lang of ['en','zh-CN']) test(`${lang}: locale navigation preserves query mask and answer without confirming it`,()=>{
 const first=setup(lang,'?region=CN'); first.query.value='2';first.query.events.change();first.causal.checked=true;first.causal.events.change();first.answer.value='2';first.answer.events.input();first.check.events.click();
 const href=first.links[1].href;
 assert.equal(href,'attention-lab-en.html?region=CN#query=2&mask=1&answer=2');
 const second=setup(lang==='en'?'zh-CN':'en',href.slice(href.indexOf('?')));
 assert.equal(second.query.value,'2');assert.equal(second.causal.checked,true);assert.equal(second.answer.value,'2');assert.match(second.summary.textContent,/6\.000000/);
 assert.ok(!second.feedback.textContent.includes('[1, 0, 0]'));assert.ok(second.feedback.textContent.length>10);
 second.answer.value='';second.answer.events.input();assert.ok(!second.links[1].href.includes('answer='));assert.equal(second.feedback.textContent,'');
 second.reset.events.click();assert.equal(second.links[1].href,'attention-lab-en.html?region=CN#query=0&mask=0');
});
test('invalid and repeated locale parameters use safe defaults',()=>{
 for(const search of ['#query=99&mask=yes&answer=NaN','#query=2&query=1&mask=1&mask=0&answer=2&answer=3','#query=1.5&mask=-1&answer=1e999']) {
  const e=setup('en',search);assert.equal(e.query.value,'0');assert.equal(e.causal.checked,false);assert.equal(e.answer.value,'');assert.equal(e.feedback.textContent,'');
 }
});
test('locale links carry valid wrong answers but omit invalid or oversized answers',()=>{
 const e=setup('en');e.answer.value='7.333333';e.answer.events.input();assert.match(e.links[1].href,/answer=7.333333/);
 for(const value of ['NaN','1e999','10001','2'.repeat(65)]) {e.answer.value=value;e.answer.events.input();assert.ok(!e.links[1].href.includes('answer='));}
});

test('answer travels in fragment only and query-only experiment state is ignored',()=>{
 const e=setup('en','?region=CN&query=2&mask=1&answer=2');assert.equal(e.query.value,'0');assert.equal(e.causal.checked,false);assert.equal(e.answer.value,'');
 e.answer.value='2';e.answer.events.input();const [request,fragment]=e.links[1].href.split('#');assert.equal(request,'attention-lab-en.html?region=CN');assert.match(fragment,/answer=2/);
});
