'use strict';
const vm=require('node:vm');
const IDS=['foundations','tokens','tools','project','timeline','multimodal','resources','evaluation'];
class Element {
 constructor(dataset={}) {this.dataset=dataset;this.handlers={};this.children=[];this.attrs={};this.value='';this.textContent='';this.checked=false;this.hidden=false;this.classList={toggle(){},add(){},remove(){}};}
 addEventListener(name,fn){(this.handlers[name]??=[]).push(fn)}
 fire(name,event={}){for(const fn of this.handlers[name]||[]) fn({target:this,preventDefault(){},...event})}
 setAttribute(name,value){this.attrs[name]=String(value);if(name==='href')this.href=String(value)}
 getAttribute(name){return name==='href'?this.href||'':this.attrs[name]||''}
 removeAttribute(name){delete this.attrs[name]}
 append(...els){this.children.push(...els)}
 appendChild(el){this.children.push(el);return el}
 replaceChildren(...els){this.children=[...els]}
 querySelector(){return null}
 querySelectorAll(){return []}
}
function fixture(code,opts={}) {
 const store=opts.store||new Map(Object.entries(opts.initial||{}));const calls=[];
 const fault={read:opts.readFault||false,write:opts.writeFault||false};
 const region=new Element,remember=new Element,notice=new Element,input=new Element,list=new Element;
 const zh=new Element({language:'zh'}),en=new Element({language:'en'});zh.href='academy.html';en.href='academy-en.html';
 const buttons=IDS.map(id=>{let b=new Element({read:id,readLabel:'Read (not mastery)',unreadLabel:'Mark as read'});b.note=new Element;b.note.textContent='Original browser-only notice';b.parentElement={querySelector:()=>b.note};return b});
 const map={'.academy-region':region,'.academy-remember-region':remember,'.academy-storage-status':notice,'#academy-search':input,'#academy-search-results':list};
 const extra=opts.elements||{};Object.assign(map,extra);
 function flatten(els){return els.flatMap(x=>[x,...flatten(x.children||[])])}
 const root={dataset:{language:opts.language||'en'},querySelector:s=>map[s]||null,querySelectorAll:s=>s==='[data-read]'?buttons:s==='[data-progress-id]'?(opts.progressSpans||[]):s==='a[data-language]'?[zh,en]:s==='a[href]'?[zh,en,...flatten([list,...Object.values(extra)]).filter(x=>x.href)]:[]};
 const win=new Element;const ctx={window:win,URLSearchParams,Set,document:{querySelector:()=>root,getElementById:id=>id==='academy-home'&&opts.home?root:null,createElement:()=>new Element},location:{search:opts.search||'',pathname:opts.home?'/index.html':'/academy-en.html',hash:opts.hash||'#tools'},localStorage:{getItem(k){calls.push(['get',k]);if(fault.read===true||fault.read===k)throw Error('synthetic read failure');return store.get(k)??null},setItem(k,v){calls.push(['set',k,v]);if(fault.write===true||fault.write===k)throw Error('synthetic write failure');store.set(k,v)},removeItem(k){calls.push(['remove',k]);store.delete(k)}}};
 vm.runInNewContext(code,ctx);
 return {win,store,calls,fault,region,remember,notice,input,list,zh,en,buttons,map,root,storage:ctx.localStorage};
}
module.exports={fixture,Element,IDS};
