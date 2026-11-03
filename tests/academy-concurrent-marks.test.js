'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {fixture,Element,IDS}=require('./academy-progress-fixture.cjs');
const code=fs.readFileSync(path.join(__dirname,'../web/academy.js'),'utf8'),KEY='modelatlas.academy.read.v1';
function page(store,language='en'){const summary=new Element,reading=new Element,next=new Element;const spans=IDS.map(id=>new Element({progressId:id}));return {...fixture(code,{store,language,elements:{'#academy-progress-summary':summary,'.academy-reading-status':reading,'#academy-progress-next':next},progressSpans:spans}),summary,reading,next,spans};}
function click(p,id){p.buttons[IDS.indexOf(id)].fire('click');}
function marked(p,id){return p.buttons[IDS.indexOf(id)].attrs['aria-pressed']==='true';}
function stored(store){return JSON.parse(store.get(KEY));}
function event(p,options={}){p.win.fire('storage',{key:KEY,storageArea:p.storage,...options});}
function writes(p){return p.calls.filter(([op,key])=>op==='set'&&key===KEY).length;}
for(const language of ['en','zh']){
 test(language+' two independent pages preserve unrelated marks and unknown duplicates without events',()=>{
  const store=new Map([[KEY,'["future","future","tools","tools"]']]),a=page(store,language),b=page(store);
  click(a,'foundations');click(b,'tokens');assert.deepEqual(stored(store),['future','future','tools','tools','foundations','tokens']);
  const reload=page(store,language);assert.ok(marked(reload,'foundations'));assert.ok(marked(reload,'tokens'));assert.match(reload.summary.textContent,/3 \/ 8/);
 });
 test(language+' stale same-ID set means set, not invert latest; same-ID unset means unset',()=>{
  for(const initial of ['[]','["tokens","tokens","future"]']){
   const store=new Map([[KEY,initial]]),a=page(store,language),b=page(store);click(a,'tokens');click(b,'tokens');
   assert.equal(stored(store).includes('tokens'),initial==='[]');assert.equal(marked(b,'tokens'),initial==='[]');
   if(initial!=='[]')assert.deepEqual(stored(store),['future']);
  }
 });
 test(language+' newly corrupt raw and read denial are protected on click without event',()=>{
  for(const bad of ['{bad','null','{}','[null]','["future",2]']){
   const store=new Map([[KEY,'["tools"]']]),p=page(store,language);store.set(KEY,bad);click(p,'tokens');assert.equal(store.get(KEY),bad);assert.equal(writes(p),0);assert.ok(marked(p,'tokens'));assert.match(p.reading.textContent,/temporary|临时/);
  }
  const store=new Map([[KEY,'["tools"]']]),p=page(store,language);store.set(KEY,'["future"]');p.fault.read=KEY;click(p,'tokens');assert.equal(store.get(KEY),'["future"]');assert.equal(writes(p),0);assert.ok(marked(p,'tokens'));
 });
 test(language+' storage update refreshes visible count labels next and buttons, never writes',()=>{
  const store=new Map(),a=page(store),b=page(store,language);click(a,'foundations');event(b);assert.ok(marked(b,'foundations'));assert.match(b.summary.textContent,/1 \/ 8/);assert.match(b.spans[0].textContent,/Marked read|已标记/);assert.ok(b.next.href.endsWith('#tokens'));assert.equal(writes(b),0);
  // Ignore queued event values and read the actual newest record.
  store.set(KEY,'["tokens","tools"]');event(b,{newValue:'["foundations"]'});assert.ok(!marked(b,'foundations'));assert.ok(marked(b,'tools'));
  store.delete(KEY);event(b,{newValue:null});assert.match(b.summary.textContent,/0 \/ 8/);
  store.set(KEY,'["tokens"]');event(b);store.clear();event(b,{key:null});assert.ok(!marked(b,'tokens'));assert.equal(writes(b),0);
 });
 test(language+' foreign storage area and unrelated keys do not update reading state',()=>{
  const store=new Map(),p=page(store,language);store.set(KEY,'["tokens"]');event(p,{storageArea:{}});event(p,{key:'modelatlas.academy.region'});assert.ok(!marked(p,'tokens'));event(p);assert.ok(marked(p,'tokens'));
 });
 test(language+' pending set/unset survives events, clear, BFCache and write failure; explicit retry merges',()=>{
  const store=new Map([[KEY,'["tools","future","future"]']]),a=page(store,language),b=page(store);a.fault.write=KEY;
  click(a,'foundations');click(a,'tools');assert.ok(marked(a,'foundations'));assert.ok(!marked(a,'tools'));
  click(b,'tokens');event(a);assert.ok(marked(a,'tokens'));assert.ok(marked(a,'foundations'));assert.ok(!marked(a,'tools'));assert.match(a.reading.textContent,/temporary|临时/);
  const before=writes(a);a.win.fire('pageshow',{persisted:true});assert.equal(writes(a),before);assert.ok(marked(a,'foundations'));
  a.fault.write=false;click(a,'timeline');assert.deepEqual(stored(store),['future','future','tokens','foundations','timeline']);assert.doesNotMatch(a.reading.textContent,/temporary|临时/);
  a.fault.write=KEY;click(a,'project');store.clear();event(a,{key:null});assert.ok(marked(a,'project'));assert.ok(!marked(a,'tokens'));assert.match(a.reading.textContent,/temporary|临时/);
 });
 test(language+' invalid event then repair or remove recovers safely without auto-saving pending edits',()=>{
  const store=new Map([[KEY,'["tools"]']]),p=page(store,language);store.set(KEY,'[false]');event(p);click(p,'foundations');assert.equal(writes(p),0);assert.equal(store.get(KEY),'[false]');
  store.set(KEY,'["future","tokens"]');event(p);assert.ok(marked(p,'foundations'));assert.ok(marked(p,'tokens'));assert.ok(!marked(p,'tools'));assert.match(p.reading.textContent,/temporary|临时/);assert.equal(writes(p),0);
  click(p,'timeline');assert.deepEqual(stored(store),['future','tokens','foundations','timeline']);
  store.set(KEY,'null');p.win.fire('pageshow',{persisted:true});store.delete(KEY);event(p);assert.match(p.summary.textContent,/0 \/ 8/);assert.doesNotMatch(p.reading.textContent,/temporary|临时/);
 });
 test(language+' read recovery merges pending intent and fresh navigation reads only persisted records',()=>{
  const store=new Map([[KEY,'["future","tokens"]']]),p=page(store,language);p.fault.read=KEY;click(p,'foundations');event(p);assert.equal(writes(p),0);assert.ok(marked(p,'foundations'));
  const fresh=page(store,language);assert.ok(!marked(fresh,'foundations'));assert.ok(marked(fresh,'tokens'));p.fault.read=false;p.win.fire('pageshow',{persisted:true});assert.ok(marked(p,'foundations'));assert.equal(writes(p),0);click(p,'tools');assert.deepEqual(stored(store),['future','tokens','foundations','tools']);
 });
}
