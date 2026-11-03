const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/entry.js','utf8');
function boot(search='',hash=''){
 const location={search,hash},classes=new Map(),elements=new Map(),events={};
 const document={title:'',body:{classList:{toggle:(k,v)=>classes.set(k,v)}},getElementById(id){if(!elements.has(id))elements.set(id,{setAttribute(k,v){this[k]=v;}});return elements.get(id);}};
 const ctx={URLSearchParams,location,document,window:{addEventListener:(k,fn)=>events[k]=fn}};
 vm.runInNewContext(code,ctx);return {ctx,location,document,classes,elements,events};
}
test('only home preferences and course query preserve portal across reload',()=>{
 for(const search of ['', '?region=CN','?lang=zh&region=CN','?q=attention+mask&region=US','?q=%E7%BC%96%E7%A0%81+bpe','?region=CN&region=US']){
  const s=boot(search);assert.equal(s.ctx.ModelAtlasEntry.isHome(),true,search);assert.equal(s.elements.get('academy-home').hidden,false);assert.match(s.document.title,/理解 AI/);
 }
});
test('legacy view, detail, filter and unknown query routes never become home',()=>{
 for(const search of ['?view=explore','?view=learn&region=US','?node=agents','?catalog=missing','?query=attention','?event-query=2025','?foo=bar','?q=x&view=timeline','?view=','?node=']){
  const s=boot(search);assert.equal(s.ctx.ModelAtlasEntry.isHome(),false,search);assert.equal(s.elements.get('academy-home').hidden,true);
 }
});
test('all home jump links preserve portal on hashchange and back',()=>{
 const s=boot('?region=US&q=mask');
 for(const hash of ['#academy-paths','#academy-practice','#academy-discover','#academy-evidence','#home','#academy-content']){
  s.location.hash=hash;s.events.hashchange();assert.equal(s.classes.get('portal-home'),true,hash);
 }
 s.location.hash='#node=agents';s.events.hashchange();assert.equal(s.classes.get('portal-home'),false);
 s.location.hash='#home';s.events.popstate();assert.equal(s.classes.get('portal-home'),true);
 for(const hash of ['#timeline','#agents','#%E0%A4%A','#unknown'])assert.equal(boot('',hash).ctx.ModelAtlasEntry.isHome(),false,hash);
});
test('legacy restore does not force learning-home anchors to scroll to zero',()=>{
 const app=fs.readFileSync(__dirname+'/../web/app.js','utf8');
 assert.ok(app.includes("if(!initial&&!globalThis.ModelAtlasEntry?.isHome?.())"));
 assert.ok(app.includes("const home=globalThis.ModelAtlasEntry?.isHome?.()===true;"));
});
