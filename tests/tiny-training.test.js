'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/tiny-training.js','utf8');
function setup(query,hash){
 const links=['academy.html#tokens','tiny-training-en.html','#transfer','tiny-training-lab.zip'].map((href,i)=>({href,getAttribute(){return this.href;},hasAttribute(k){return i===1&&k==='data-training-language';},setAttribute(k,v){this.href=v;}}));
 const events={},location={search:query,hash};vm.runInNewContext(code,{URLSearchParams,location,document:{querySelectorAll:()=>links},window:{addEventListener:(n,f)=>events[n]=f}});return {links,events,location};
}
for(const region of ['unknown','CN','US','GB','SG','international'])test('training navigation preserves region '+region,()=>{
const {links}=setup('?region='+region,'#transfer');assert.equal(links[0].href,'academy.html?region='+region+'#tokens');assert.equal(links[1].href,'tiny-training-en.html?region='+region+'#transfer');assert.equal(links[2].href,'#transfer');assert.equal(links[3].href,'tiny-training-lab.zip');});
for(const query of ['', '?region=bad','?region=CN&region=US'])test('training invalid region '+query,()=>{const {links}=setup(query,'#bad');assert.equal(links[1].href,'tiny-training-en.html?region=unknown');});
test('training history recomputes query and fragment',()=>{const {links,events,location}=setup('?region=CN','#run');location.search='?region=US';location.hash='#finish';events.popstate();assert.equal(links[1].href,'tiny-training-en.html?region=US#finish');location.hash='#transfer';events.hashchange();assert.equal(links[1].href,'tiny-training-en.html?region=US#transfer');});
test('training navigation has no storage or network calls',()=>{assert.doesNotMatch(code,/localStorage|sessionStorage|fetch\(|XMLHttpRequest|eval\(/);});
