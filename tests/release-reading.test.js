'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/release-reading.js','utf8');
const sections=['evidence','evidence-A','evidence-B','evidence-C','evidence-D','evidence-E','worked','practice','reference','template'];
function setup(suffix='',query='?region=US',hash=''){
 const hrefs=[`academy${suffix}.html#timeline`,`academy${suffix}.html#resources`,`release-reading${suffix?'':'-en'}.html`,'#reference',`release-brief-template${suffix}.md`,'https://huggingface.co/Qwen/Qwen3-8B'];
 const links=hrefs.map((href,i)=>({href,getAttribute(){return this.href;},hasAttribute(k){return i===2&&k==='data-release-language';},setAttribute(k,v){assert.equal(k,'href');this.href=v;}}));
 const events={},location={search:query,hash};
 const context={URLSearchParams,location,document:{querySelectorAll:()=>links},window:{addEventListener:(name,fn)=>{events[name]=fn;}}};
 vm.runInNewContext(code,context);
 return {links,hrefs,events,location,context};
}
for(const suffix of ['', '-en'])for(const region of ['unknown','CN','US','GB','SG','international'])test(`release lesson keeps language and region: ${suffix} ${region}`,()=>{
 const {links,hrefs,context}=setup(suffix,'?region='+region);
 vm.runInNewContext(code,context);
 assert.equal(links[0].href,`academy${suffix}.html?region=${region}#timeline`);
 assert.equal(links[1].href,`academy${suffix}.html?region=${region}#resources`);
 assert.equal(links[2].href,`release-reading${suffix?'':'-en'}.html?region=${region}`);
 assert.deepEqual(links.slice(3).map(x=>x.href),hrefs.slice(3));
});
for(const query of ['','?region=XX','?region=CN&region=US','?region=US&region=US','?region=%3Cscript%3E'])test('invalid region stays unknown with valid lesson fragment: '+query,()=>{
 const {links}=setup('',query,'#practice');
 assert.equal(links[0].href,'academy.html?region=unknown#timeline');
 assert.equal(links[2].href,'release-reading-en.html?region=unknown#practice');
});
for(const suffix of ['', '-en'])for(const section of sections)test(`language retains real shared anchor: ${suffix} ${section}`,()=>{
 const {links}=setup(suffix,'?region=US&ignored=1','#'+section);
 assert.equal(links[2].href,`release-reading${suffix?'':'-en'}.html?region=US#${section}`);
 assert.equal(links[0].href,`academy${suffix}.html?region=US#timeline`);
});
for(const hash of ['','#unknown','#timeline','#Practice','#practice?region=CN','#practice#template','#%70ractice','#%3Cscript%3E','#<script>','#javascript:alert(1)'])test('unknown or untrusted fragment is not propagated: '+hash,()=>{
 const {links}=setup('', '?region=US',hash);
 assert.equal(links[2].href,'release-reading-en.html?region=US');
 assert.equal(links[0].href,'academy.html?region=US#timeline');
});
test('hash navigation, back and forward refresh links without leaking stale fragments',()=>{
 const {links,events,location}=setup('', '?region=US','#practice');
 for(const hash of ['#template','#practice','#template','#unknown','','#evidence-B']){
  location.hash=hash;events.hashchange();
  assert.equal(links[2].href,'release-reading-en.html?region=US'+(sections.includes(hash.slice(1))?hash:''));
  assert.equal(links[0].href,'academy.html?region=US#timeline');
 }
 // Same-document history may change query as well as hash; no stale region survives.
 location.search='?region=CN&region=US';location.hash='#worked';events.popstate();
 assert.equal(links[2].href,'release-reading-en.html?region=unknown#worked');
 location.search='?region=SG';events.popstate();events.hashchange();
 assert.equal(links[2].href,'release-reading-en.html?region=SG#worked');
});
test('allowlist matches all actual bilingual IDs and only language link is marked',()=>{
 for(const suffix of ['', '-en']){
  const html=fs.readFileSync(__dirname+`/../web/release-reading${suffix}.html`,'utf8');
  assert.deepEqual([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]).sort(),[...sections].sort());
  assert.equal((html.match(/data-release-language/g)||[]).length,1);
  assert.match(html,new RegExp(`<a data-release-language href="release-reading${suffix?'':'-en'}\\.html"`));
 }
});
