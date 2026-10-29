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
const n1='transformer',n2=data.nodes[0].id,c1=data.vendor_catalog.records[0].id,c2=data.vendor_catalog.records[1].id;
const title=(h,kind)=>h.ids.get(kind==='node'?'detail':'catalog-detail').children[0]?.textContent;
const nodeTitle=id=>data.nodes.find(n=>n.id===id).title,catTitle=id=>data.vendor_catalog.records.find(n=>n.id===id).title;
test('discovery starts with 12 cards, no implicit detail, and no history/progress writes',async()=>{
 const h=await boot();assert.equal(h.entries.length,1);assert.deepEqual(h.writes,[]);assert.equal(h.ids.get('detail-screen').hidden,true);assert.equal(h.ids.get('explore').hidden,false);assert.equal(h.ids.get('results').children.length,12);assert.equal(h.stored.size,0);
 h.click('node',n2);h.click('node',n2);assert.equal(h.entries.length,2);const before=h.writes.length;h.back();assert.equal(h.ids.get('detail-screen').hidden,true);h.forward();assert.equal(title(h,'node'),nodeTitle(n2));assert.equal(h.writes.length,before);assert.equal(h.url().pathname,'/modelatlas/');
});
test('node and legacy hash deep links preserve entity without extra entries',async()=>{
 for(const suffix of ['?node='+n1,'#node='+n1]){const h=await boot('https://example.test/modelatlas/'+suffix);assert.equal(title(h,'node'),nodeTitle(n1));assert.equal(h.entries.length,1);h.click('node',n2);h.back();assert.equal(title(h,'node'),nodeTitle(n1));}
});
test('catalog deep link and cross-panel repeated clicks remain reversible',async()=>{
 const h=await boot('https://example.test/modelatlas/?catalog='+c1);assert.deepEqual(h.writes,[]);h.click('catalog',c1);assert.equal(h.writes.length,0);h.click('catalog',c2);h.click('node',n2);h.click('catalog',c1);const count=h.writes.length;
 h.back();assert.equal(title(h,'node'),nodeTitle(n2));h.back();assert.equal(title(h,'catalog'),catTitle(c2));h.back();assert.equal(title(h,'catalog'),catTitle(c1));h.forward();h.forward();h.forward();assert.equal(h.url().searchParams.get('catalog'),c1);assert.equal(h.writes.length,count);
});
test('unknown IDs are explicit, malformed hash is inert, and neither fabricates entity identity',async()=>{
 const node=await boot('https://example.test/modelatlas/?node=missing');assert.match(title(node,'node'),/未知知识 ID/);const h=await boot('https://example.test/modelatlas/?catalog=missing');assert.match(title(h,'catalog'),/未知目录 ID/);h.click('catalog',c1);h.back();assert.match(title(h,'catalog'),/未知目录 ID/);assert.equal(h.ids.get('catalog-graph').children.length,0);assert.equal(h.ids.get('catalog-relations').children.length,0);assert.ok(h.ids.get('catalog-results').querySelectorAll('button').every(b=>b.attrs['aria-current']==='false'));const bad=await boot('https://example.test/modelatlas/#node=%E0%A4%A');assert.equal(bad.ids.get('detail-screen').hidden,true);
});
test('legacy hash normalizes only that entry; Back returns discovery and Forward restores detail',async()=>{
 const h=await boot();h.hash(n1);assert.equal(title(h,'node'),nodeTitle(n1));assert.equal(h.entries.length,2);assert.equal(h.url().searchParams.get('node'),n1);assert.equal(h.url().hash,'');const count=h.writes.length;h.back();assert.equal(h.ids.get('detail-screen').hidden,true);h.forward();assert.equal(title(h,'node'),nodeTitle(n1));assert.equal(h.writes.length,count);
});
test('explicit read, path, import and clear retain original storage schema and never write navigation',async()=>{
 const h=await boot('https://example.test/modelatlas/?node='+n1);const read=()=>h.ids.get('detail').querySelectorAll('button').find(b=>/标记为已读|已读 · 点击撤销/.test(b.textContent));const count=h.writes.length;read().events.click();assert.equal(h.writes.length,count);assert.ok(JSON.parse(h.stored.get('modelatlas.progress')).completed.includes(n1));
 h.click('catalog',c1);const after=h.writes.length;const check=h.ids.get('paths').querySelectorAll('input').find(e=>e.attrs['aria-label']===nodeTitle(n1)+' 已读');assert.ok(check);check.checked=false;check.events.change();assert.equal(h.url().searchParams.get('catalog'),c1);
 await h.ids.get('import').events.change({target:{files:[{size:100,text:async()=>JSON.stringify({schema:'modelatlas.progress.v1',completed:[n1]})}],value:'file'}});h.ids.get('clear').events.click();assert.equal(h.writes.length,after);assert.equal(h.url().searchParams.get('catalog'),c1);assert.deepEqual(JSON.parse(h.stored.get('modelatlas.progress')).completed,[]);
});
test('filter state is URL-addressable; Back/Forward restores it and new actions truncate Forward history',async()=>{
 const h=await boot();h.ids.get('query').value='no-such-node';h.ids.get('filters').events.input();assert.equal(h.url().searchParams.get('query'),'no-such-node');assert.equal(h.ids.get('results').querySelectorAll('button').length,0);h.back();assert.equal(h.ids.get('query').value,'');assert.equal(h.ids.get('results').children.length,12);h.forward();assert.equal(h.ids.get('query').value,'no-such-node');h.back();h.click('catalog',c1);assert.equal(h.entries.length,2);assert.equal(h.url().searchParams.get('catalog'),c1);
});
test('knowledge history and list pagination survive an unavailable catalog module',async()=>{const h=await boot(undefined,true);h.click('node',n2);h.back();assert.equal(h.ids.get('detail-screen').hidden,true);assert.equal(h.ids.get('catalog-load-status').dataset.state,'module-unavailable');h.ids.get('node-pagination').children.at(-1).events.click();assert.equal(h.url().searchParams.get('page'),'2');assert.equal(h.ids.get('results').children.length,12);});
test('actual relation and backlink buttons use the same history without writing reading progress',async()=>{
 const record=data.vendor_catalog.records.find(r=>r.links.some(e=>data.nodes.some(n=>n.id===e.target))),node=record.links.find(e=>data.nodes.some(n=>n.id===e.target)).target;
 const h=await boot('https://example.test/modelatlas/?catalog='+record.id);h.ids.get('catalog-relations').querySelectorAll('button').find(b=>b.textContent===nodeTitle(node)).events.click();assert.equal(h.url().searchParams.get('node'),node);h.ids.get('detail').querySelectorAll('button').find(b=>b.textContent===record.title).events.click();assert.equal(h.url().searchParams.get('catalog'),record.id);h.back();assert.equal(h.url().searchParams.get('node'),node);h.back();assert.equal(h.url().searchParams.get('catalog'),record.id);assert.equal(h.stored.size,0);
});
test('detail dismissal preserves page and filters; reopening and repeat view clicks do not duplicate entries',async()=>{
 const h=await boot('https://example.test/modelatlas/?view=explore&page=2');const id=h.ids.get('results').querySelectorAll('button')[0].dataset.id;h.click('node',id);h.ids.get('close-detail').events.click();assert.equal(h.ids.get('detail-screen').hidden,true);assert.equal(h.url().searchParams.get('page'),'2');assert.equal(h.ids.get('results').querySelectorAll('button')[0].dataset.id,id);const before=h.entries.length;h.ids.get('nav-explore').events.click({preventDefault(){}});assert.equal(h.entries.length,before);
});
test('every old section anchor reveals exactly one view, including the new evaluation destination',async()=>{
 for(const view of ['explore','vendor-catalog','timeline','evaluation','learn','coverage']){const h=await boot('https://example.test/modelatlas/#'+view);for(const id of ['explore','vendor-catalog','timeline','evaluation','learn','coverage'])assert.equal(h.ids.get(id).hidden,id!==view);assert.equal(h.stored.size,0);}
});
test('all 44 evaluation entities are accessible through finite pages and compatible node links',async()=>{
 const h=await boot('https://example.test/modelatlas/?view=evaluation');const rows=[];for(let i=0;i<4;i++){rows.push(...h.ids.get('evaluation-results').children);const next=h.ids.get('evaluation-pagination').children.at(-1);if(!next.disabled)next.events.click();}assert.equal(rows.length,44);rows.at(-1).querySelectorAll('button')[0].events.click();assert.ok(h.url().searchParams.get('node'));assert.equal(h.ids.get('detail-screen').hidden,false);assert.equal(h.stored.size,0);
});
test('conflicting query details select catalog only, including empty catalog, without stale node leakage',async()=>{
 for(const catalog of [c1,'','missing']){const h=await boot('https://example.test/modelatlas/?node='+n1+'&catalog='+catalog);assert.equal(h.ids.get('node-reading').hidden,true);assert.equal(h.ids.get('catalog-reading').hidden,false);assert.equal(h.url().searchParams.has('node'),false);assert.equal(h.entries.length,1);assert.equal(h.stored.size,0);if(catalog===c1)assert.equal(title(h,'catalog'),catTitle(c1));else assert.match(title(h,'catalog'),/未知目录 ID/);}
});
test('legacy section hashes override query details, and node hash overrides catalog identity',async()=>{
 for(const kind of ['node='+n1,'catalog='+c1]){const h=await boot('https://example.test/modelatlas/?'+kind+'#timeline');assert.equal(h.ids.get('timeline').hidden,false);assert.equal(h.ids.get('detail-screen').hidden,true);assert.equal(h.url().searchParams.has('node'),false);assert.equal(h.url().searchParams.has('catalog'),false);assert.equal(h.url().searchParams.get('view'),'timeline');assert.equal(h.entries.length,1);assert.equal(h.stored.size,0);}
 const h=await boot('https://example.test/modelatlas/?catalog='+c1+'#node='+n1);assert.equal(h.ids.get('node-reading').hidden,false);assert.equal(h.ids.get('catalog-reading').hidden,true);assert.equal(title(h,'node'),nodeTitle(n1));assert.equal(h.url().searchParams.has('catalog'),false);
});
test('unknown views fall back with a visible notice and do not invent selection or progress',async()=>{
 const h=await boot('https://example.test/modelatlas/?view=missing');assert.equal(h.ids.get('explore').hidden,false);assert.equal(h.ids.get('detail-screen').hidden,true);assert.match(h.ids.get('view-status').textContent,/未知视图/);assert.equal(h.url().searchParams.get('view'),'explore');assert.equal(h.entries.length,1);assert.equal(h.stored.size,0);
});
test('timeline and learning empty states have one-click reset restoring their URL filter and page state',async()=>{
 const h=await boot('https://example.test/modelatlas/?view=timeline&event-query=not-a-real-title&event-type=paper_revision&event-page=3&unknown-page=5');assert.match(h.ids.get('events').children[0].textContent,/无匹配事件/);h.ids.get('event-reset').events.click();assert.equal(h.ids.get('event-query').value,'');assert.equal(h.ids.get('event-type').value,'');for(const key of ['event-query','event-type','event-page','unknown-page'])assert.equal(h.url().searchParams.has(key),false);assert.equal(h.ids.get('events').children.length,12);h.back();assert.equal(h.ids.get('event-query').value,'not-a-real-title');h.forward();assert.equal(h.ids.get('event-query').value,'');assert.equal(h.stored.size,0);
 const p=await boot('https://example.test/modelatlas/?view=learn&path-query=not-a-real-path&path-page=5');assert.match(p.ids.get('paths').children[0].textContent,/无匹配路线/);p.ids.get('path-reset').events.click();assert.equal(p.ids.get('path-query').value,'');assert.equal(p.url().searchParams.has('path-query'),false);assert.equal(p.url().searchParams.has('path-page'),false);assert.ok(p.ids.get('paths').children.length>1);assert.equal(p.stored.size,0);
});
test('unknown node clears the previous graph and relations and cannot redraw stale identity on import',async()=>{
 const h=await boot('https://example.test/modelatlas/?node='+n1);assert.ok(h.ids.get('relations').children.length);h.hash('missing');assert.match(title(h,'node'),/未知知识 ID/);assert.equal(h.ids.get('graph').children.length,0);assert.equal(h.ids.get('relations').children.length,0);assert.ok(h.ids.get('results').querySelectorAll('button').every(b=>b.attrs['aria-current']==='false'));
 await h.ids.get('import').events.change({target:{files:[{size:100,text:async()=>JSON.stringify({schema:'modelatlas.progress.v1',completed:[n1]})}],value:'file'}});assert.match(title(h,'node'),/未知知识 ID/);assert.equal(h.url().searchParams.get('node'),'missing');assert.equal(h.ids.get('relations').children.length,0);
});
test('unrecognized or malformed anchors produce a notice but skip-to-main remains a valid no-op',async()=>{
 for(const hash of ['unknown-anchor','node=%E0%A4%A']){const h=await boot('https://example.test/modelatlas/#'+hash);assert.match(h.ids.get('view-status').textContent,/未知或无法解析的页面锚点/);assert.equal(h.ids.get('detail-screen').hidden,true);assert.equal(h.stored.size,0);}
 const h=await boot('https://example.test/modelatlas/#main');assert.doesNotMatch(h.ids.get('view-status').textContent,/未知/);assert.equal(h.ids.get('explore').hidden,false);assert.equal(h.writes.length,0);
});
