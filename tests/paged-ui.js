// Original offline fixture helpers: exercise real filter + pagination handlers.
function findNode(ids,id){ids.get('query').value=id;ids.get('filters').events.input();return ids.get('results').querySelectorAll('button').find(b=>b.dataset.id===id);}
function collectPages(ids,list,pager){const rows=[...ids.get(list).children];let next=ids.get(pager).children.at(-1),guard=0;while(!next.disabled&&guard++<100){next.events.click();rows.push(...ids.get(list).children);next=ids.get(pager).children.at(-1);}if(guard>=100)throw Error('pagination did not terminate');return rows;}
module.exports={findNode,collectPages};
