/* Home-only preferences/search stay in the learning portal; legacy routes remain explicit. */
(function(){
 'use strict';
 const homeHashes=new Set(['','#main','#start-here','#academy-content','#home','#academy-paths','#academy-practice','#academy-discover','#academy-evidence']);
 function isHome(){
  const params=new URLSearchParams(location.search);
  return Array.from(params.keys()).every(key=>['region','lang','q'].includes(key))&&homeHashes.has(location.hash||'');
 }
 function refresh(){
  const home=isHome();
  document.body.classList.toggle('beginner-home',home);
  document.body.classList.toggle('portal-home',home);
  const portal=document.getElementById('academy-home');if(portal)portal.hidden=!home;
  const entry=document.getElementById('start-here');if(entry)entry.hidden=!home;
  const start=document.getElementById('nav-start');if(start)start.setAttribute('aria-current',home?'page':'false');
  if(home){
   document.title='理解 AI，开发 Agent · ModelAtlas';
   for(const id of ['explore','vendor-catalog','timeline','evaluation','learn','coverage'])document.getElementById('nav-'+id)?.setAttribute('aria-current','false');
  }
 }
 globalThis.ModelAtlasEntry={refresh,isHome};refresh();
 window.addEventListener('popstate',refresh);window.addEventListener('hashchange',refresh);
})();
