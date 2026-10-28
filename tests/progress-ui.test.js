// Synthetic offline event harness executing production save/import/clear handlers.
// No browser, dependency installation, network, or downloaded code execution.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync(require('node:path').join(__dirname,'../web/app.js'),'utf8');
function harness(failSave=false){
 const elements=new Map(),handlers={},writes=[];
 const $=id=>{if(!elements.has(id))elements.set(id,{textContent:'',addEventListener:(event,fn)=>handlers[id]=fn});return elements.get(id);};
 const context=vm.createContext({$,C:require('../web/core.js'),Set,JSON,Error,allIds:new Set(['a','b']),window:{confirm:()=>true},localStorage:{setItem:(key,value)=>{if(failSave)throw Error('QuotaExceededError');writes.push(JSON.parse(value));}},renderPaths(){},choose(){}});
 vm.runInContext(source.match(/let completed=.*?\n/)[0],context);
 vm.runInContext(source.split('\n').find(x=>x.trim().startsWith('function save()')),context);
 const start=source.indexOf(" $('import').addEventListener"),end=source.indexOf(" for(const snap",start);
 vm.runInContext(source.slice(start,end),context);
 vm.runInContext('completed=new Set(["a"])',context);
 return {context,handlers,writes,$,state:()=>Array.from(vm.runInContext('[...completed]',context))};
}
const data=ids=>JSON.stringify({schema:'modelatlas.progress.v1',completed:ids});
function pending(h){let resolve,reject;const target={files:[{size:100,text:()=>new Promise((a,b)=>{resolve=a;reject=b})}],value:'file'};const done=h.handlers.import({target});return {resolve,reject,done,target};}
test('successful import persists and clears input for repeated selection',async()=>{const h=harness(),p=pending(h);p.resolve(data(['b']));await p.done;assert.deepEqual(h.state(),['b']);assert.deepEqual(h.writes.at(-1).completed,['b']);assert.equal(p.target.value,'');assert.match(h.$('progress-status').textContent,/导入成功/);});
test('failed persistence remains visible after import',async()=>{const h=harness(true),p=pending(h);p.resolve(data(['b']));await p.done;assert.deepEqual(h.state(),['b']);assert.equal(h.writes.length,0);assert.match(h.$('progress-status').textContent,/无法持久保存/);assert.match(h.$('progress-status').textContent,/导出备份/);});
test('confirmed clear invalidates pending import',async()=>{const h=harness(),p=pending(h);h.handlers.clear();p.resolve(data(['b']));await p.done;assert.deepEqual(h.state(),[]);assert.equal(h.writes.length,1);assert.deepEqual(h.writes[0].completed,[]);});
test('latest selected import wins even if older read completes later',async()=>{const h=harness(),a=pending(h),b=pending(h);b.resolve(data(['b']));await b.done;a.resolve(data(['a']));await a.done;assert.deepEqual(h.state(),['b']);assert.equal(h.writes.length,1);});
test('superseded import cannot clear newer input or overwrite status',async()=>{const h=harness(),a=pending(h),b=pending(h);a.reject(Error('old read failure'));await a.done;assert.equal(a.target.value,'file');assert.equal(h.$('progress-status').textContent,'');b.resolve(data(['b']));await b.done;assert.equal(b.target.value,'');});
test('manual progress edit invalidates pending import',async()=>{const h=harness(),p=pending(h);vm.runInContext('completed.add("b");save()',h.context);p.resolve(data([]));await p.done;assert.deepEqual(h.state(),['a','b']);assert.equal(h.writes.length,1);});
test('malformed latest import preserves existing state and can be retried',async()=>{const h=harness(),p=pending(h);p.resolve('{');await p.done;assert.deepEqual(h.state(),['a']);assert.equal(h.writes.length,0);assert.equal(p.target.value,'');assert.match(h.$('progress-status').textContent,/导入失败/);const retry=pending(h);retry.resolve(data(['b']));await retry.done;assert.deepEqual(h.state(),['b']);});
test('canceled clear does not discard pending import',async()=>{const h=harness(),p=pending(h);h.context.window.confirm=()=>false;h.handlers.clear();p.resolve(data(['b']));await p.done;assert.deepEqual(h.state(),['b']);});
