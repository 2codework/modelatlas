/* Finite, local-only course reader. Native hashes preserve Back/Forward; no storage. */
(function(){'use strict';
 const lessons=Array.from(document.querySelectorAll('article[id]')),intro=document.getElementById('course-intro'),status=document.getElementById('course-status'),links=Array.from(document.querySelectorAll('aside nav a'));
 function show(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{id='invalid';}if(id==='course-main')return;const selected=lessons.find(x=>x.id===id);for(const lesson of lessons)lesson.hidden=lesson!==selected;intro.hidden=!!selected;for(const a of links){if(a.getAttribute('href')==='#'+id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}status.textContent=selected?'第 '+(lessons.indexOf(selected)+1)+' 课 / 共 '+lessons.length+' 课 · '+(selected.querySelector('h2')?.textContent||selected.id):id?'未找到这节课。请从目录选择，不自动替换成其他内容。':'从左侧目录选一课开始；手机上目录位于页面顶部。';if(selected){selected.scrollIntoView({behavior:'auto',block:'start'});selected.setAttribute('tabindex','-1');selected.focus({preventScroll:true});}}
 window.addEventListener('hashchange',show);show();
})();
