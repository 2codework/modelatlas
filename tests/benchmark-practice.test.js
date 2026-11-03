'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/benchmark-practice.js','utf8');
function fixture(search,hash){
 const original=['academy-en.html#evaluation','benchmark-practice-en.html','#worksheet','benchmark-ledger-template.md','https://github.com/ByteDance-Seed/Bagel/blob/main/EVAL.md'];
 const links=original.map((href,i)=>({href,getAttribute(){return this.href;},setAttribute(k,v){assert.equal(k,'href');this.href=v;},hasAttribute(k){return i===1&&k==='data-benchmark-language';}}));
 const events={};const context={URLSearchParams,location:{search,hash},document:{querySelectorAll:()=>links},window:{addEventListener:(name,fn)=>events[name]=fn}};
 vm.runInNewContext(code,context);return {links,events,context,original};
}
for(const region of ['unknown','CN','US','GB','SG','international'])test('benchmark language and region independent: '+region,()=>{
 const x=fixture('?region='+region,'#transfer');
 assert.equal(x.links[0].href,'academy-en.html?region='+region+'#evaluation');
 assert.equal(x.links[1].href,'benchmark-practice-en.html?region='+region+'#transfer');
 assert.deepEqual(x.links.slice(2).map(a=>a.href),x.original.slice(2));
 x.context.location.hash='#questions';x.events.hashchange();
 assert.equal(x.links[1].href,'benchmark-practice-en.html?region='+region+'#questions');
 x.events.hashchange();assert.equal(x.links[0].href,'academy-en.html?region='+region+'#evaluation');
});
for(const query of ['','?region=XX','?region=CN&region=US','?region=%3Cscript%3E'])test('benchmark invalid region is unknown '+query,()=>{
 const x=fixture(query,'#transfer');assert.equal(x.links[0].href,'academy-en.html?region=unknown#evaluation');
});
test('language fragments are allowlisted and stale fragment cleared',()=>{
 const x=fixture('?region=US','#finish');x.context.location.hash='#evil';x.events.hashchange();
 assert.equal(x.links[1].href,'benchmark-practice-en.html?region=US');
});
