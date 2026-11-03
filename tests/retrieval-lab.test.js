'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/retrieval-lab.js','utf8');
function setup(query,hash){
 const links=['academy.html#tokens','retrieval-lab-en.html','#transfer','retrieval-lab.zip'].map((href,i)=>({href,getAttribute(){return this.href;},hasAttribute(k){return i===1&&k==='data-retrieval-language';},setAttribute(k,v){this.href=v;}}));
 const events={},location={search:query,hash};vm.runInNewContext(code,{URLSearchParams,location,document:{querySelectorAll:()=>links},window:{addEventListener:(n,f)=>events[n]=f}});return {links,events,location};
}
for(const region of ['unknown','CN','US','GB','SG','international'])test('retrieval navigation preserves region '+region,()=>{
const {links}=setup('?region='+region,'#transfer');assert.equal(links[0].href,'academy.html?region='+region+'#tokens');assert.equal(links[1].href,'retrieval-lab-en.html?region='+region+'#transfer');assert.equal(links[2].href,'#transfer');assert.equal(links[3].href,'retrieval-lab.zip');});
for(const query of ['', '?region=bad','?region=CN&region=US'])test('retrieval invalid region '+query,()=>{const {links}=setup(query,'#bad');assert.equal(links[1].href,'retrieval-lab-en.html?region=unknown');});
test('retrieval history recomputes query and fragment',()=>{const {links,events,location}=setup('?region=CN','#run');location.search='?region=US';location.hash='#finish';events.popstate();assert.equal(links[1].href,'retrieval-lab-en.html?region=US#finish');location.hash='#transfer';events.hashchange();assert.equal(links[1].href,'retrieval-lab-en.html?region=US#transfer');});
test('retrieval navigation has no storage or network calls',()=>{assert.doesNotMatch(code,/localStorage|sessionStorage|fetch\(|XMLHttpRequest|eval\(/);});
