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
async function boot(start='https://example.test/modelatlas/?view=explore',omitCatalog=false,includeEntry=false){
 const ids=new Map([...fs.readFileSync(path.join(root,'web/index.html'),'utf8').matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new E('div')]));
 const entries=[start],writes=[],listeners={},stored=new Map();let index=0,url=new URL(start);
 const location={get search(){return url.search;},get hash(){return url.hash;}};
 function write(mode,next){url=new URL(next,url);if(mode==='push'){entries.splice(++index);entries.push(url.href);}else entries[index]=url.href;writes.push(mode);}
 const ctx={document:{body:{classList:{toggle(){}}},getElementById:id=>ids.get(id),createElement:t=>new E(t),createTextNode:t=>({textContent:t}),createElementNS:(_,t)=>new E(t),querySelectorAll:()=>ids.get('results').querySelectorAll('button')},URL,URLSearchParams,Blob,location,history:{pushState:(_,__,s)=>write('push',s),replaceState:(_,__,s)=>write('replace',s)},localStorage:{getItem:k=>stored.get(k)||null,setItem:(k,v)=>stored.set(k,v)},addEventListener:(k,f)=>(listeners[k]??=[]).push(f),fetch:async()=>({ok:true,json:async()=>structuredClone(data)}),setTimeout:fn=>fn(),confirm:()=>true};ctx.window=ctx;vm.createContext(ctx);
 for(const name of [...(includeEntry?['entry']:[]),'core','reader','catalog','app'])if(!(omitCatalog&&name==='catalog'))await vm.runInContext(fs.readFileSync(path.join(root,'web',name+'.js'),'utf8'),ctx);
 assert.notEqual(ids.get('catalog-load-status').dataset.state,'initialization-error');
 const fire=k=>(listeners[k]||[]).forEach(f=>f());
 const click=(kind,id)=>{const b=ids.get(kind==='node'?'results':'catalog-results').querySelectorAll('button').find(b=>b.dataset.id===id);assert.ok(b,id);b.events.click();};
 return {ids,ctx,writes,entries,stored,click,url:()=>url,back(){assert.ok(index>0);url=new URL(entries[--index]);fire('popstate');},forward(){assert.ok(index<entries.length-1);url=new URL(entries[++index]);fire('popstate');},hash(id){write('push','#node='+id);fire('hashchange');}};
}

function destination(h,id){return new URL(h.ids.get(id).href,h.url());}
test('both search forms provide a separate monthly collection, with a usable static fallback',()=>{
 const html=fs.readFileSync(path.join(root,'web/index.html'),'utf8');
 for(const id of ['knowledge-monthly-link','catalog-monthly-link'])assert.match(html,new RegExp('id="'+id+'" href="monthly.html\\?kind=all"'));
 assert.equal((html.match(/每月模型发布另有补充收录，未合并到本页结果/g)||[]).length,2);
});
test('knowledge keyword is safely carried to all monthly event kinds without other filters',async()=>{
 const query='GLM & <script> # 中文 + / ? kind=paper';
 const h=await boot('https://example.test/modelatlas/?view=explore&query='+encodeURIComponent(query)+'&type=model');
 const u=destination(h,'knowledge-monthly-link');
 assert.equal(u.pathname,'/modelatlas/monthly.html');assert.equal(u.searchParams.get('q'),query);
 assert.equal(u.searchParams.get('kind'),'all');assert.equal(u.hash,'');assert.deepEqual([...u.searchParams.keys()].sort(),['kind','q']);
 assert.match(h.ids.get('knowledge-monthly-link').textContent,/同一关键词/);
 assert.deepEqual(h.writes,[]);assert.equal(h.stored.size,0);
 // Native anchors are not intercepted: the browser retains the current results entry on departure.
 assert.equal(h.ids.get('knowledge-monthly-link').events.click,undefined);
});
test('catalog input, scope change, reset and Back/Forward keep each monthly link in sync',async()=>{
 const h=await boot();const input=h.ids.get('query');
 input.value='GLM';h.ids.get('filters').events.input();
 h.ids.get('search-scope').value='vendor-catalog';h.ids.get('search-scope').events.change();
 assert.equal(destination(h,'catalog-monthly-link').searchParams.get('q'),'GLM');
 h.ids.get('catalog-query').value='DeepSeek';h.ids.get('catalog-filters').events.input();
 assert.equal(destination(h,'catalog-monthly-link').searchParams.get('q'),'DeepSeek');
 assert.equal(destination(h,'knowledge-monthly-link').searchParams.get('q'),'GLM');
 const writes=h.writes.length;h.back();assert.equal(destination(h,'catalog-monthly-link').searchParams.get('q'),'GLM');
 h.forward();assert.equal(destination(h,'catalog-monthly-link').searchParams.get('q'),'DeepSeek');assert.equal(h.writes.length,writes);
 h.ids.get('catalog-filters').events.reset({preventDefault(){}});
 assert.equal(destination(h,'catalog-monthly-link').searchParams.has('q'),false);
 assert.equal(destination(h,'catalog-monthly-link').searchParams.get('kind'),'all');
 assert.equal(h.ids.get('catalog-monthly-link').textContent,'查看每月模型发布 →');
 assert.equal(h.stored.size,0);
});
test('zero results still offer the monthly query and a missing catalog module does not break the link',async()=>{
 const h=await boot('https://example.test/modelatlas/?view=vendor-catalog&catalog-query=not-a-real-model-123',true);
 assert.equal(destination(h,'catalog-monthly-link').searchParams.get('q'),'not-a-real-model-123');
 assert.equal(h.ids.get('vendor-catalog').hidden,false);
 const k=await boot('https://example.test/modelatlas/?view=explore&query=not-a-real-model-123');
 assert.match(k.ids.get('results').children[0].textContent,/无匹配节点/);
 assert.equal(destination(k,'knowledge-monthly-link').searchParams.get('q'),'not-a-real-model-123');
});
