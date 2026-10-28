// Test-only closed append contract. No production adapter import.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
function fixture(name,hash){const bytes=fs.readFileSync(path.join(__dirname,'fixtures',name));assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),hash);return JSON.parse(bytes);}
function validate(data){
 const old=fixture('realtime-audio-baseline.json','08b1dc2ab60f1eda3e64a65aee0034487506af8108cf44bfeec98aa8b97ef578');
 const delta=fixture('realtime-audio-reviewed-golden.json','246db58481bd5179dbd52d7e22aca3f5458b5d7f66b758616ead34e893b72246');
 assert.deepEqual(Object.keys(data).sort(),[...Object.keys(old),'realtime_audio_registry'].sort());
 for(const key of Object.keys(old)){
  if(Object.hasOwn(delta,key)){
   const ids=data[key].map(x=>x.id);assert.equal(new Set(ids).size,ids.length,'unique '+key);
   assert.deepEqual(data[key],[...old[key],...delta[key]],'complete closed '+key);
  }else assert.deepEqual(data[key],old[key],'unchanged '+key);
 }
 return old;
}
module.exports={validate};
