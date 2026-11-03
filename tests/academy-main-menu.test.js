'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const {fixture,Element}=require('./academy-progress-fixture.cjs');
const code=fs.readFileSync(__dirname+'/../web/academy.js','utf8');
for(const language of ['zh','en'])test(`native menu local Escape and existing URL propagation: ${language}`,()=>{
 const menu=new Element,summary=new Element;let focused=0,prevented=0;summary.focus=()=>focused++;
 menu.querySelector=s=>s==='summary'?summary:null;menu.open=false;
 const suffix=language==='en'?'-en':'';
 const make=()=>['foundations','project','timeline','multimodal','resources','evaluation'].map(id=>{const a=new Element;a.href=`academy${suffix}.html#${id}`;return a});
 menu.children=make();const desktop=new Element;desktop.children=make();
 const s=fixture(code,{language,search:'?region=CN&q=attention',elements:{'.academy-main-menu':menu,'.academy-desktop-nav':desktop}});
 assert.equal(menu.open,false);assert.deepEqual(menu.children.map(a=>a.href),desktop.children.map(a=>a.href));
 assert.ok(menu.children.every(a=>a.href.includes('region=CN&q=attention')));
 for(const key of ['Enter',' ','Tab']){menu.fire('keydown',{key,preventDefault(){prevented++}});assert.equal(menu.open,false)}
 menu.open=true;menu.fire('keydown',{key:'Escape',preventDefault(){prevented++}});
 assert.equal(menu.open,false);assert.equal(focused,1);assert.equal(prevented,1);
 menu.fire('keydown',{key:'Escape',preventDefault(){prevented++}});assert.equal(focused,1);assert.equal(prevented,1);
 assert.equal(s.win.handlers.keydown,undefined);assert.equal(s.win.handlers.resize,undefined);
 assert.equal(menu.handlers.click,undefined);assert.equal(summary.handlers.keydown,undefined);
 s.region.value='US';s.region.fire('change');assert.deepEqual(menu.children.map(a=>a.href),desktop.children.map(a=>a.href));assert.ok(menu.children.every(a=>a.href.includes('region=US&q=attention')));
 assert.equal(s.calls.filter(([op])=>op==='set').length,0);
});
