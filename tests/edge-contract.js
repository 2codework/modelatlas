// Finite test-only edge admission. Exact full objects, not a superset escape hatch.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
function fixture(name,hash){const b=fs.readFileSync(path.join(__dirname,'fixtures',name));assert.equal(crypto.createHash('sha256').update(b).digest('hex'),hash);return JSON.parse(b);}
function validate(data){
 const old=fixture('edge-multimodal-baseline.json','2d55feb50ce42852031a03a1992d41a1cf37b237008bf4bdcc1b70582e856cc2');
 const delta=fixture('edge-multimodal-reviewed-golden.json','e0f8edca9cdc4a4057e6cc19cd97830bfc1f37647f33ad6296b1dc354f9f0e02');
 const registry=fixture('edge-multimodal-registry.json','c7fe6a0b5b29f7f21cdfa64183da5f53f7369b7c1b6d45b889c4f73981a5a898');
 assert.deepEqual(Object.keys(data).sort(),[...Object.keys(old),'edge_multimodal_registry'].sort());
 for(const key of Object.keys(old)){
  if(Object.hasOwn(delta,key)){
   const ids=data[key].map(x=>x.id);assert.equal(new Set(ids).size,ids.length,'unique '+key);
   assert.deepEqual(data[key],[...old[key],...delta[key]],'complete closed '+key);
  }else assert.deepEqual(data[key],old[key],'unchanged '+key);
 }
 assert.deepEqual(data.edge_multimodal_registry,registry);
 assert.deepEqual([data.nodes.length,data.sources.length,data.events.length,data.edges.length],[250,391,206,151]);
 return old;
}
module.exports={validate};
