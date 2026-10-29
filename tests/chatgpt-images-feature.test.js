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
async function boot(start='https://example.test/modelatlas/?view=explore',omitCatalog=false,includeEntry=false,input=data){
 const ids=new Map([...fs.readFileSync(path.join(root,'web/index.html'),'utf8').matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new E('div')]));
 const entries=[start],writes=[],listeners={},stored=new Map();let index=0,url=new URL(start);
 const location={get search(){return url.search;},get hash(){return url.hash;}};
 function write(mode,next){url=new URL(next,url);if(mode==='push'){entries.splice(++index);entries.push(url.href);}else entries[index]=url.href;writes.push(mode);}
 const ctx={document:{body:{classList:{toggle(){}}},getElementById:id=>ids.get(id),createElement:t=>new E(t),createTextNode:t=>({textContent:t}),createElementNS:(_,t)=>new E(t),querySelectorAll:()=>ids.get('results').querySelectorAll('button')},URL,URLSearchParams,Blob,location,history:{pushState:(_,__,s)=>write('push',s),replaceState:(_,__,s)=>write('replace',s)},localStorage:{getItem:k=>stored.get(k)||null,setItem:(k,v)=>stored.set(k,v)},addEventListener:(k,f)=>(listeners[k]??=[]).push(f),fetch:async()=>({ok:true,json:async()=>structuredClone(input)}),setTimeout:fn=>fn(),confirm:()=>true};ctx.window=ctx;vm.createContext(ctx);
 for(const name of [...(includeEntry?['entry']:[]),'core','reader','catalog','app'])if(!(omitCatalog&&name==='catalog'))await vm.runInContext(fs.readFileSync(path.join(root,'web',name+'.js'),'utf8'),ctx);
 assert.notEqual(ids.get('catalog-load-status').dataset.state,'initialization-error');
 const fire=k=>(listeners[k]||[]).forEach(f=>f());
 const click=(kind,id)=>{const b=ids.get(kind==='node'?'results':'catalog-results').querySelectorAll('button').find(b=>b.dataset.id===id);assert.ok(b,id);b.events.click();};
 return {ids,ctx,writes,entries,stored,click,url:()=>url,back(){assert.ok(index>0);url=new URL(entries[--index]);fire('popstate');},forward(){assert.ok(index<entries.length-1);url=new URL(entries[++index]);fire('popstate');},hash(id){write('push','#node='+id);fire('hashchange');}};
}

const feature='creative-chatgpt-web-images',url='https://2codework.github.io/agentwork/index.html?q=%E6%B5%B7%E6%8A%A5';
const descendants=e=>[e,...(e.children||[]).flatMap(descendants)];
const content=e=>descendants(e).map(n=>n.textContent||'').join(' ');
const blocks=h=>descendants(h.ids.get('detail')).filter(n=>n.attrs?.['data-optional-practice']==='poster-change-time');
test('application feature has a readable overview before metadata and exactly one safe optional poster practice',async()=>{
 assert.equal(data.nodes.find(n=>n.id===feature)?.type,'application_feature');
 const h=await boot('https://example.test/modelatlas/?node='+feature),root=h.ids.get('detail'),all=descendants(root),overview=all.find(n=>n.attrs?.['data-feature-overview']==='chatgpt-web-images');
 assert.ok(overview);assert.ok(root.children.indexOf(overview)<root.children.findIndex(n=>n.className==='reference-metadata'));
 const text=content(overview);for(const term of ['不是独立基础模型','不是 Image API','账户','套餐','工作区','所在地区','当前额度','达到上限即停','不保证固定免费次数','选区不是像素锁','区外','尺寸','颜色','图层','底层型号','仍未知','未运行产品'])assert.ok(text.includes(term),term);
 assert.equal(blocks(h).length,1);const practice=blocks(h)[0],links=descendants(practice).filter(n=>n.tag==='a');assert.equal(links.length,1);assert.equal(links[0].href,url);assert.equal(links[0].target,'_blank');assert.equal(links[0].rel,'noopener noreferrer');
 for(const term of ['作者理想对照不是 AI 实际生成','不要把对照图上传当输入','真实输出必须另行保存与记录','人的编辑学习流程','不是 API 兼容证明','未在产品实跑','额度或重试上限就停'])assert.ok(content(practice).includes(term),term);
 assert.ok(root.children.indexOf(overview)<root.children.indexOf(practice));assert.equal(all.filter(n=>['script','iframe','input','video','audio'].includes(n.tag)).length,0);assert.equal(h.stored.size,0);
});
test('search finds the application feature and return/history preserve the original query without duplicate practice',async()=>{
 const h=await boot('https://example.test/modelatlas/?view=explore&query='+encodeURIComponent('ChatGPT 网页图片'));
 assert.ok(h.ids.get('results').querySelectorAll('button').some(b=>b.dataset.id===feature));h.click('node',feature);assert.equal(blocks(h).length,1);h.click('node',feature);assert.equal(blocks(h).length,1);h.back();assert.equal(h.ids.get('detail-screen').hidden,true);assert.equal(h.url().searchParams.get('query'),'ChatGPT 网页图片');h.forward();assert.equal(blocks(h).length,1);
 for(let i=0;i<2;i++){h.hash('transformer');assert.equal(blocks(h).length,0);h.back();assert.equal(blocks(h).length,1);}
});
test('feature scopes stay inert under hostile data and lookalike routes; sibling and beginner entry remain independent',async()=>{
 const d=structuredClone(data),n=d.nodes.find(n=>n.id===feature),payload='<img src=x onerror=evil>';
 n.capabilities_zh=[payload];n.description_zh=payload;n.source_urls=['javascript:evil()'];
 const h=await boot('https://example.test/modelatlas/?node='+feature,false,false,d),all=descendants(h.ids.get('detail'));assert.ok(content(h.ids.get('detail')).includes(payload));assert.equal(all.filter(n=>['img','script','iframe'].includes(n.tag)).length,0);assert.ok(!all.some(n=>n.tag==='a'&&/^javascript:/i.test(n.href||'')));assert.equal(blocks(h).length,1);
 for(const id of [feature+'-extra',feature+'<img src=x>', 'creative-underlord','music-lyria']){const f=await boot('https://example.test/modelatlas/?node='+encodeURIComponent(id));assert.equal(blocks(f).length,0);}
 const home=await boot('https://example.test/modelatlas/',false,true);assert.equal(home.ids.get('nav-start').attrs['aria-current'],'page');assert.equal(blocks(home).length,0);
});

test('shared exact-stage golden negatives reject all unauthorized changes without mutation',()=>{
 const legacy=require('./images-contract.js').validate,runtime=require('./runtime-contract.js').validate;
 const cases=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/images-negative-cases.json')));
 for(const c of cases){const d=structuredClone(data);let target=d;for(const key of c.path.slice(0,-1))target=target[key];const key=c.path.at(-1);
  if(c.action==='set')Object.defineProperty(target,key,{value:c.value,enumerable:true,writable:true,configurable:true});else if(c.action==='delete')delete target[key];else if(c.action==='append')target[key].push(c.value);else if(c.action==='reverse')target[key].reverse();else assert.fail(c.action);
  const before=JSON.stringify(d);assert.throws(()=>legacy(d),c.name);assert.throws(()=>runtime(d),c.name);assert.equal(JSON.stringify(d),before,c.name);
 }
 const before=JSON.stringify(data);const old=legacy(data);runtime(data);runtime(old);assert.equal(JSON.stringify(data),before);
});
