// Original synthetic DOM + session-history model; executes full production scripts offline.
// Does not replace real browser Back/Forward, focus, scroll, or accessibility QA.
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.join(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'dist/data.json')));
class E{
 constructor(tag){this.tag=tag;this.children=[];this.events={};this.dataset={};this.attrs={};this.value='';this.textContent='';}
 append(...xs){this.children.push(...xs);}replaceChildren(...xs){this.children=xs;this.textContent='';}
 setAttribute(k,v){this.attrs[k]=v;}removeAttribute(k){delete this.attrs[k];}addEventListener(k,f){this.events[k]=f;}
 scrollIntoView(){this.scrolled=true;}querySelectorAll(tag){return this.children.flatMap(x=>[...(x.tag===tag?[x]:[]),...(x.querySelectorAll?.(tag)||[])]);}
}
async function boot(start='https://example.test/modelatlas/',omitCatalog=false){
 const ids=new Map([...fs.readFileSync(path.join(root,'web/index.html'),'utf8').matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new E('div')]));
 const entries=[start],writes=[],listeners={},stored=new Map();let index=0,url=new URL(start);
 const location={get search(){return url.search;},get hash(){return url.hash;}};
 function write(mode,next){url=new URL(next,url);if(mode==='push'){entries.splice(++index);entries.push(url.href);}else entries[index]=url.href;writes.push(mode);}
 const ctx={document:{getElementById:id=>ids.get(id),createElement:t=>new E(t),createTextNode:t=>({textContent:t}),createElementNS:(_,t)=>new E(t),querySelectorAll:()=>ids.get('results').querySelectorAll('button')},URL,URLSearchParams,Blob,location,history:{pushState:(_,__,s)=>write('push',s),replaceState:(_,__,s)=>write('replace',s)},localStorage:{getItem:k=>stored.get(k)||null,setItem:(k,v)=>stored.set(k,v)},addEventListener:(k,f)=>(listeners[k]??=[]).push(f),fetch:async()=>({ok:true,json:async()=>structuredClone(data)}),setTimeout:fn=>fn(),confirm:()=>true};ctx.window=ctx;vm.createContext(ctx);
 for(const name of ['core','reader','catalog','app'])if(!(omitCatalog&&name==='catalog'))await vm.runInContext(fs.readFileSync(path.join(root,'web',name+'.js'),'utf8'),ctx);
 assert.notEqual(ids.get('catalog-load-status').dataset.state,'initialization-error');
 const fire=k=>(listeners[k]||[]).forEach(f=>f());
 const click=(kind,id)=>{const b=ids.get(kind==='node'?'results':'catalog-results').querySelectorAll('button').find(b=>b.dataset.id===id);assert.ok(b,id);b.events.click();};
 return {ids,ctx,writes,entries,stored,click,url:()=>url,back(){assert.ok(index>0);url=new URL(entries[--index]);fire('popstate');},forward(){assert.ok(index<entries.length-1);url=new URL(entries[++index]);fire('popstate');},hash(id){write('push','#node='+id);fire('hashchange');}};
}
const n1='transformer',n2=data.nodes.find(n=>n.id!==n1&&!n.tutorial_markdown).id,c1=data.vendor_catalog.records[0].id,c2=data.vendor_catalog.records[1].id;
const title=(h,kind)=>h.ids.get(kind==='node'?'detail':'catalog-detail').children[0]?.textContent;
const nodeTitle=id=>data.nodes.find(n=>n.id===id).title,catTitle=id=>data.vendor_catalog.records.find(n=>n.id===id).title;
test('initial default replaces once; distinct node clicks push, repeated click does not; Back/Forward restores without writes',async()=>{
 const h=await boot();assert.equal(h.entries.length,1);assert.deepEqual(h.writes,['replace']);h.click('node',n2);h.click('node',n2);assert.equal(h.entries.length,2);const before=h.writes.length;h.back();assert.equal(title(h,'node'),nodeTitle(n1));assert.equal(h.url().search,'?node='+n1);h.forward();assert.equal(title(h,'node'),nodeTitle(n2));assert.equal(h.writes.length,before);assert.equal(h.url().pathname,'/modelatlas/');
});
test('initial node and legacy hash deep links preserve entity without extra entries',async()=>{
 for(const suffix of ['?node='+n2,'#node='+n2]){const h=await boot('https://example.test/modelatlas/'+suffix);assert.equal(title(h,'node'),nodeTitle(n2));assert.equal(h.entries.length,1);h.click('node',n1);h.back();assert.equal(title(h,'node'),nodeTitle(n2));}
});
test('initial catalog deep link never pushes; catalog duplicates and cross-panel round trips are consistent',async()=>{
 const h=await boot('https://example.test/modelatlas/?catalog='+c1);assert.deepEqual(h.writes,[]);assert.equal(title(h,'catalog'),catTitle(c1));h.click('catalog',c1);assert.equal(h.writes.length,0);h.click('catalog',c2);h.click('node',n1);h.click('catalog',c1);const count=h.writes.length;
 h.back();assert.equal(title(h,'node'),nodeTitle(n1));h.back();assert.equal(title(h,'catalog'),catTitle(c2));h.back();assert.equal(title(h,'catalog'),catTitle(c1));h.forward();h.forward();h.forward();assert.equal(h.url().search,'?catalog='+c1);assert.equal(h.writes.length,count);
});
test('invalid node falls back safely; invalid catalog remains explicit through Back; malformed hash is inert',async()=>{
 const node=await boot('https://example.test/modelatlas/?node=missing');assert.equal(title(node,'node'),nodeTitle(n1));const h=await boot('https://example.test/modelatlas/?catalog=missing');assert.match(title(h,'catalog'),/未知目录 ID/);h.click('catalog',c1);h.back();assert.match(title(h,'catalog'),/未知目录 ID/);assert.equal(h.url().search,'?catalog=missing');assert.equal(h.ids.get('catalog-graph').children.length,0);assert.equal(h.ids.get('catalog-relations').children.length,0);assert.ok(h.ids.get('catalog-results').querySelectorAll('button').every(b=>b.attrs['aria-current']==='false'));const bad=await boot('https://example.test/modelatlas/#node=%E0%A4%A');assert.equal(title(bad,'node'),nodeTitle(n1));
});
test('legacy hash navigation normalizes existing hash entry and remains reversible',async()=>{
 const h=await boot();h.hash(n2);assert.equal(title(h,'node'),nodeTitle(n2));assert.equal(h.entries.length,2);assert.equal(h.url().search,'?node='+n2);assert.equal(h.url().hash,'');const count=h.writes.length;h.back();assert.equal(title(h,'node'),nodeTitle(n1));h.forward();assert.equal(title(h,'node'),nodeTitle(n2));assert.equal(h.writes.length,count);
});
test('read toggle, path checkbox, import and clear redraw without URL writes, including while catalog is active',async()=>{
 const h=await boot();const read=()=>h.ids.get('detail').querySelectorAll('button').find(b=>/标记为已读|已读 · 点击撤销/.test(b.textContent));const count=h.writes.length;read().events.click();assert.equal(h.writes.length,count);assert.ok(JSON.parse(h.stored.get('modelatlas.progress')).completed.includes(n1));
 h.click('catalog',c1);const after=h.writes.length;const check=h.ids.get('paths').querySelectorAll('input').find(e=>e.attrs['aria-label']===nodeTitle(n1)+' 已读');assert.ok(check);check.checked=false;check.events.change();assert.equal(h.url().search,'?catalog='+c1);
 await h.ids.get('import').events.change({target:{files:[{size:100,text:async()=>JSON.stringify({schema:'modelatlas.progress.v1',completed:[n1]})}],value:'file'}});h.ids.get('clear').events.click();assert.equal(h.writes.length,after);assert.equal(h.url().search,'?catalog='+c1);assert.deepEqual(JSON.parse(h.stored.get('modelatlas.progress')).completed,[]);
});
test('restoration does not reset either panel filters and newer navigation truncates forward history',async()=>{
 const h=await boot();h.click('node',n2);h.ids.get('query').value='no-such-node';h.ids.get('filters').events.input();h.ids.get('catalog-query').value='no-such-record';h.ids.get('catalog-filters').events.input();h.back();assert.equal(h.ids.get('query').value,'no-such-node');assert.equal(h.ids.get('catalog-query').value,'no-such-record');assert.equal(title(h,'node'),nodeTitle(n1));h.ids.get('catalog-query').value='';h.ids.get('catalog-filters').events.input();h.click('catalog',c1);assert.equal(h.entries.length,2);assert.equal(h.entries.at(-1).split('?')[1],'catalog='+c1);
});
test('knowledge history still works when catalog module is unavailable',async()=>{const h=await boot(undefined,true);h.click('node',n2);h.back();assert.equal(title(h,'node'),nodeTitle(n1));assert.equal(h.ids.get('catalog-load-status').dataset.state,'module-unavailable');});
test('actual catalog relation buttons and node backlinks use the same reversible history',async()=>{
 const record=data.vendor_catalog.records.find(r=>r.links.some(e=>data.nodes.some(n=>n.id===e.target)));assert.ok(record);const node=record.links.find(e=>data.nodes.some(n=>n.id===e.target)).target;
 const h=await boot('https://example.test/modelatlas/?catalog='+record.id);h.ids.get('catalog-relations').querySelectorAll('button').find(b=>b.textContent===nodeTitle(node)).events.click();assert.equal(h.url().search,'?node='+node);h.ids.get('detail').querySelectorAll('button').find(b=>b.textContent===record.title).events.click();assert.equal(h.url().search,'?catalog='+record.id);h.back();assert.equal(h.url().search,'?node='+node);h.back();assert.equal(h.url().search,'?catalog='+record.id);
});
