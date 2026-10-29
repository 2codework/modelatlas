const {findNode,collectPages}=require('./paged-ui.js');
// Self-written offline DOM test of production coverage rendering; no network, browser or model runs.
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.join(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'dist/data.json'),'utf8'));
const legacyData=require('./audio-contract.js').validate(data);
class E{constructor(tag){this.tag=tag;this.children=[];this.events={};this.dataset={};this.attrs={};this.value='';this.textContent='';}append(...xs){this.children.push(...xs);}replaceChildren(...xs){this.children=xs;this.textContent='';}setAttribute(k,v){this.attrs[k]=v;}addEventListener(k,f){this.events[k]=f;}scrollIntoView(){}querySelectorAll(tag){return this.children.flatMap(x=>[...(x.tag===tag?[x]:[]),...(x.querySelectorAll?.(tag)||[])]);}}
const text=e=>(e.textContent||'')+' '+(e.children||[]).map(text).join(' ');
async function boot(){const html=fs.readFileSync(path.join(root,'web/index.html'),'utf8'),ids=new Map([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new E('div')]));const document={getElementById:id=>ids.get(id),createElement:t=>new E(t),createTextNode:t=>({textContent:t}),createElementNS:(_,t)=>new E(t),querySelectorAll:()=>ids.get('results').querySelectorAll('button')},navigation=[];let requests=0;const ctx={document,URL,URLSearchParams,Blob,location:{search:'',hash:''},history:{replaceState(...args){navigation.push(['replace',...args]);},pushState(...args){navigation.push(['push',...args]);}},localStorage:{getItem(){return null;}},addEventListener(){},fetch:async()=>{requests++;return{ok:true,json:async()=>structuredClone(data)};},setTimeout};ctx.window=ctx;vm.createContext(ctx);for(const name of ['core','reader','catalog'])vm.runInContext(fs.readFileSync(path.join(root,'web',name+'.js'),'utf8'),ctx);await vm.runInContext(fs.readFileSync(path.join(root,'web/app.js'),'utf8'),ctx);assert.equal(ids.get('catalog-load-status').dataset.state,'ready');return{ids,navigation,get requests(){return requests;},filter(kind){ids.get('event-type').value=kind;ids.get('event-type').events.change();}};}

const C=require('../web/core.js');
const coverageRows=ui=>ui.ids.get('coverage-table').querySelectorAll('tr').slice(1).map(row=>row.children.map(x=>x.textContent));
test('production coverage labels unknown markers and explains non-certification',async()=>{
 const ui=await boot(),body=text(ui.ids.get('coverage-table'));
 assert.ok(body.includes('明确待核验标记'));
 assert.ok(body.includes('只统计明确未知标签，未计入不代表已验证，具体账户/地区/权限条件见详情。'));
 assert.ok(!body.includes('可获得性待核验'));
 assert.equal(ui.requests,1);
});
test('production regional count is seven, legacy unknown subtotal preserved and all categories agree',async()=>{
 const ui=await boot(),rows=coverageRows(ui),views=new Map(data.view_nodes.map(v=>[v.id,v]));
 const regional=rows.find(r=>r[0]==='regional-office-platforms');
 assert.deepEqual(regional,['regional-office-platforms','7','0','7','代表性条目；不保证完整']);
 // Preserve the fixed f104740 baseline subtotal; new creative nodes are counted independently.
 const baselineIds=new Set(Object.keys(JSON.parse(fs.readFileSync(path.join(root,'learning/creative-gaps/baseline-object-hashes.json'),'utf8')).nodes));
 assert.equal(baselineIds.size,237);
 const oldViews=data.view_nodes.filter(v=>baselineIds.has(v.id));
 const legacy=oldViews.filter(v=>v.availability==='未核验').length;
 const regionalIds=new Set(data.nodes.filter(n=>n.category==='regional-office-platforms').map(n=>n.id));
 const explicitOther=oldViews.filter(v=>!regionalIds.has(v.id)&&C.hasExplicitUnknownAvailability(v.availability)).length;
 assert.equal(legacy,133);assert.equal(explicitOther,legacy);
 const legacyNewViews=legacyData.view_nodes.filter(v=>!baselineIds.has(v.id));assert.equal(legacyNewViews.length,5);
 const audioIds=['speech-moshi','speech-csm-1b','speech-voxtral-realtime-2602','speech-gpt-realtime-family'];const audioViews=data.view_nodes.filter(v=>audioIds.includes(v.id));assert.deepEqual(audioViews.map(v=>v.id),audioIds);
 const newViews=data.view_nodes.filter(v=>!baselineIds.has(v.id));assert.equal(newViews.length,13);
 const addedUnknowns=newViews.filter(v=>C.hasExplicitUnknownAvailability(v.availability)).length;
 assert.equal(rows.reduce((sum,r)=>sum+Number(r[3]),0),legacy+7+addedUnknowns);
 for(const row of rows){const expected=data.nodes.filter(n=>n.category===row[0]&&C.hasExplicitUnknownAvailability(views.get(n.id).availability)).length;assert.equal(Number(row[3]),expected,row[0]);}
});
test('production detail preserves every regional availability/license/tenant string and data bytes',async()=>{
 const p=path.join(root,'dist/data.json'),before=fs.readFileSync(p),snapshot=JSON.stringify(data),ui=await boot();
 for(const node of data.nodes.filter(n=>n.category==='regional-office-platforms')){
  const target=findNode(ui.ids,node.id);
  assert.ok(target,node.id);target.events.click();
  const detail=text(ui.ids.get('detail'));
  for(const field of [node.availability,node.license,node.regional_office.tenant_requirements,'never-run'])assert.ok(detail.includes(field),node.id+': '+field);
 }
 assert.equal(JSON.stringify(data),snapshot);
 assert.deepEqual(fs.readFileSync(p),before);
});
