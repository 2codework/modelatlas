/* Navigation only: no model, storage, network or submitted code execution. */
(function(){'use strict';
function region(){const p=new URLSearchParams(location.search||'');const r=p.getAll('region').length===1?p.get('region'):null;return ['unknown','CN','US','GB','SG','international'].includes(r)?r:'unknown';}
const ids=['retrieval-main','prepare','materials','worked','run','safety','evaluate','transfer','finish','reference','downloads'];
function update(){document.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href')||'';if(/^(?:academy|retrieval-lab)(?:-en)?\.html(?:[?#]|$)/.test(h)){const [path,hash]=h.split('#');const current=(location.hash||'').slice(1);const fragment=a.hasAttribute('data-retrieval-language')?(ids.includes(current)?current:''):hash;a.setAttribute('href',path.split('?')[0]+'?region='+region()+(fragment?'#'+fragment:''));}});}
update();window.addEventListener('hashchange',update);window.addEventListener('popstate',update);
})();
