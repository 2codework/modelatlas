// Original offline DOM/history model. This is not real-browser visual/mobile certification.
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{mount}=require('../web/topic.js');
class E{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.attrs={};this.value='';}
 append(...items){this.children.push(...items);}replaceChildren(...items){this.children=items;}after(...items){this.afterItems=items;}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return k==='href'?this.href:this.attrs[k];}addEventListener(k,f){this.events[k]=f;}focus(){this.focused=true;}
 querySelector(t){return this.children.find(x=>x.tag===t);}querySelectorAll(t){return this.children.flatMap(x=>[...(x.tag===t?[x]:[]),...(x.querySelectorAll?.(t)||[])]);}
}
function boot(file,hash=''){
 const source=fs.readFileSync(path.join(__dirname,'../dist',file),'utf8'),panels=[...source.matchAll(/<(article|section) id="([^"]+)"[^>]*>\s*<h2[^>]*>([^<]+)<\/h2>/g)].map(m=>{const p=new E(m[1]);p.id=m[2];p.append(new E('h2',m[3]),new E('p','inert source text <img>'));return p;}),directory=new E('nav');
 for(const p of panels.filter(p=>p.id!=='audio-learning-diagram')){const a=new E('a',p.children[0].textContent);a.href='#'+p.id;directory.append(a);}
 const entries=['https://example.test/modelatlas/'+file+hash],listeners={},writes=[];let index=0,url=new URL(entries[0]);const location={get hash(){return url.hash;},get search(){return url.search;},get pathname(){return url.pathname;}};
 const win={location,history:{pushState(_,__,next){url=new URL(next,url);entries.splice(++index);entries.push(url.href);writes.push(next);}},addEventListener:(k,f)=>(listeners[k]??=[]).push(f),scrollTo(){}};
 const doc={querySelectorAll:()=>panels,querySelector:()=>directory,createElement:t=>new E(t)};const ui=mount(doc,win),fire=k=>(listeners[k]||[]).forEach(f=>f());return{ui,panels,directory,entries,writes,url:()=>url,back(){url=new URL(entries[--index]);fire('popstate');},forward(){url=new URL(entries[++index]);fire('popstate');},hash(value){url=new URL('#'+value,url);fire('hashchange');}};
}
for(const [file,count] of [['realtime-audio.html',5],['creative-learning.html',6]]){
 test(file+': finite directory, all original panels retained, no initial history or implicit selection',()=>{const h=boot(file);assert.equal(h.panels.length,count);assert.equal(h.ui.links.length,count);assert.ok(h.panels.every(p=>p.hidden));assert.equal(h.directory.hidden,false);assert.equal(h.writes.length,0);assert.ok(h.panels.every(p=>p.children[1].textContent==='inert source text <img>'));});
 test(file+': old deep links, repeat clicks, return and Back/Forward restore exactly one panel',()=>{const h=boot(file),id=h.panels[0].id;h.ui.navigate(id);h.ui.navigate(id);assert.equal(h.writes.length,1);assert.equal(h.panels.filter(p=>!p.hidden).length,1);assert.equal(h.directory.hidden,true);h.ui.back.events.click();assert.equal(h.panels.filter(p=>!p.hidden).length,0);h.back();assert.equal(h.panels.find(p=>p.id===id).hidden,false);h.forward();assert.equal(h.directory.hidden,false);const deep=boot(file,'#'+id);assert.equal(deep.panels.find(p=>p.id===id).hidden,false);assert.equal(deep.writes.length,0);});
 test(file+': invalid/malformed IDs do not display another entity and hashchange restores valid ID',()=>{const h=boot(file,'#missing');assert.ok(h.panels.every(p=>p.hidden));h.hash('%E0%A4%A');assert.ok(h.panels.every(p=>p.hidden));h.hash(h.panels.at(-1).id);assert.equal(h.panels.at(-1).hidden,false);assert.equal(h.writes.length,0);});
}
