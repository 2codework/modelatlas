/* Lesson navigation only; no storage, requests, grading or host execution. */
(function(){'use strict';
 const sections=['evidence','evidence-A','evidence-B','evidence-C','evidence-D','evidence-E','worked','practice','reference','template'];
 function update(){
 const params=new URLSearchParams(location.search||'');
 const candidate=params.getAll('region').length===1?params.get('region'):null;
 const region=['unknown','CN','US','GB','SG','international'].includes(candidate)?candidate:'unknown';
 document.querySelectorAll('a[href]').forEach(link=>{
  const href=link.getAttribute('href')||'';
  if(/^(?:academy|release-reading)(?:-en)?\.html(?:[?#]|$)/.test(href)){
   const [path,hash]=href.split('#');
   const current=(location.hash||'').slice(1);
   const fragment=link.hasAttribute('data-release-language')?(sections.includes(current)?current:''):hash;
   link.setAttribute('href',path.split('?')[0]+'?region='+region+(fragment?'#'+fragment:''));
  }
 });
 }
 update();window.addEventListener('hashchange',update);window.addEventListener('popstate',update);
})();
