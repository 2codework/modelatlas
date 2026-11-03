/* Navigation only. No storage, fetching, scoring, or model execution. */
(function(){'use strict';
 const params=new URLSearchParams(location.search||'');
 const candidate=params.getAll('region').length===1?params.get('region'):null;
 const region=['unknown','CN','US','GB','SG','international'].includes(candidate)?candidate:'unknown';
 const sections=['benchmark-main','prepare','materials','source-a','source-b','worksheet','questions','transfer','t-a','t-b','t-c','finish'];
 function update(){document.querySelectorAll('a[href]').forEach(link=>{
  const href=link.getAttribute('href')||'';
  if(/^(?:academy|benchmark-practice)(?:-en)?\.html(?:[?#]|$)/.test(href)){
   const [path,hash]=href.split('#');
   const current=(location.hash||'').slice(1);
   const fragment=link.hasAttribute('data-benchmark-language')?(sections.includes(current)?current:''):hash;
   link.setAttribute('href',path.split('?')[0]+'?region='+region+(fragment?'#'+fragment:''));
  }
 });}
 update();window.addEventListener('hashchange',update);
})();
