/* Navigation only: no storage, fetch, submitted code execution or model API. */
(function(){'use strict';
function selectedRegion(){const params=new URLSearchParams(location.search||'');
const candidate=params.getAll('region').length===1?params.get('region'):null;
return ['unknown','CN','US','GB','SG','international'].includes(candidate)?candidate:'unknown';}
const sections=['training-main','prepare','worked','run','inference','transfer','reference','finish','downloads'];
function update(){const region=selectedRegion();document.querySelectorAll('a[href]').forEach(link=>{
const href=link.getAttribute('href')||'';
if(/^(?:academy|tiny-training)(?:-en)?\.html(?:[?#]|$)/.test(href)){
const [path,hash]=href.split('#');const current=(location.hash||'').slice(1);
const fragment=link.hasAttribute('data-training-language')?(sections.includes(current)?current:''):hash;
link.setAttribute('href',path.split('?')[0]+'?region='+region+(fragment?'#'+fragment:''));
}});}
update();window.addEventListener('hashchange',update);window.addEventListener('popstate',update);
})();
