/* Progressive, local-only topic navigation. Without JavaScript all original text remains readable. */
(function(global){
'use strict';
function mount(doc,win){
 const panels=Array.from(doc.querySelectorAll('main > article[id], main > section[id]'));
 const directory=doc.querySelector('main > nav');if(!directory||!panels.length)return null;
 const map=new Map(panels.map(p=>[p.id,p])),make=(tag,text)=>{const e=doc.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
 const links=Array.from(directory.querySelectorAll('a'));
 for(const p of panels)if(!links.some(a=>a.getAttribute('href')==='#'+p.id)){const a=make('a',p.querySelector('h2')?.textContent||p.id);a.href='#'+p.id;links.push(a);}
 directory.replaceChildren(...links);directory.className='topic-directory';
 const toolbar=make('div');toolbar.className='topic-toolbar';const back=make('button','← 返回专题目录');back.type='button';
 const label=make('label','切换阅读主题'),select=make('select');select.setAttribute('aria-label','切换阅读主题');const empty=make('option','选择主题');empty.value='';select.append(empty);
 for(const p of panels){const o=make('option',p.querySelector('h2')?.textContent||p.id);o.value=p.id;select.append(o);}label.append(select);toolbar.append(back,label);directory.after(toolbar);
 const message=make('p');message.setAttribute('role','status');message.className='muted';toolbar.after(message);
 function readHash(){try{return decodeURIComponent(win.location.hash.slice(1));}catch{return '';}}
 function render(focus=false){const id=readHash(),valid=map.has(id);for(const p of panels)p.hidden=p.id!==id;directory.hidden=valid;toolbar.hidden=!valid;select.value=valid?id:'';message.textContent=valid?'单项阅读 · 原始事实、限制与来源完整保留':id?'没有对应主题，请从目录重新选择。':'选择一个主题开始阅读；不会自动执行模型或练习。';for(const a of links)a.setAttribute('aria-current',String(a.getAttribute('href')==='#'+id));if(focus&&valid){const h=map.get(id).querySelector('h2');h?.setAttribute('tabindex','-1');h?.focus?.();}return id;}
 function navigate(id){if(readHash()===id)return;win.history.pushState(null,'',win.location.pathname+win.location.search+(id?'#'+encodeURIComponent(id):''));render(true);win.scrollTo?.(0,0);if(!id)links[0]?.focus?.();}
 links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();navigate(a.getAttribute('href').slice(1));}));back.addEventListener('click',()=>navigate(''));select.addEventListener('change',()=>navigate(select.value));win.addEventListener('popstate',()=>render());win.addEventListener('hashchange',()=>render());win.addEventListener('keydown',e=>{if(e.key==='Escape'&&map.has(readHash()))navigate('');});render();return {render,navigate,panels,links,toolbar,back,select};
}
if(typeof module!=='undefined')module.exports={mount};else if(global.document)mount(global.document,global);
})(typeof window==='undefined'?globalThis:window);
