// Test-only finite admission. Self-written structural checks, not independent content QA.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
function fixture(name,hash){const b=fs.readFileSync(path.join(__dirname,'fixtures',name));assert.equal(crypto.createHash('sha256').update(b).digest('hex'),hash);return JSON.parse(b);}
function validate(data){
 if(Object.hasOwn(data,"inference_runtime_registry"))data=require("./runtime-contract.js").validate(data);
 const old=fixture('early-nlp-baseline.json','ada2b8832d334eecd6122e152f95af84a2c1eb9e9c61cdfc7dc3b6e81e55b6e6');
 const delta=fixture('early-nlp-golden.json','1946fd50c9c186efa8b8628ed731cf1c05d98ed5f6efbf6bf7e4e7f614c4a7ab');
 const registry=fixture('early-nlp-registry.json','9f1ff5208b4b2683cb77d7532edb71a265b01264737f2d72e17795e4a5de1c06');
 assert.deepEqual(Object.keys(data).sort(),[...Object.keys(old),'early_nlp_registry'].sort());
 for(const key of Object.keys(old)){
  if(Object.hasOwn(delta,key)){
   const ids=data[key].map(x=>x.id);assert.equal(new Set(ids).size,ids.length,'unique '+key);
   assert.deepEqual(data[key],[...old[key],...delta[key]],'complete closed '+key);
  }else assert.deepEqual(data[key],old[key],'unchanged '+key);
 }
 assert.deepEqual(data.early_nlp_registry,registry);
 assert.deepEqual([data.nodes.length,data.sources.length,data.events.length,data.edges.length],[254,405,211,151]);
 assert.equal(data.vendor_catalog.records.length,77);assert.equal(data.events.filter(e=>e.date).length,127);
 return old;
}
module.exports={validate};
