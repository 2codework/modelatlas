// Exact finite new stage; no blind slicing of historical assertions.
// Baseline raw bytes: c97ae6a9c72f085eb936c1a0d56b79033a313e6927f1fc9b9b775ec6cf4b8955.
// JS JSON serialization normalizes numeric lexemes; the full-value hash below
// was computed directly from that original baseline, not the candidate.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const hash=v=>crypto.createHash('sha256').update(v).digest('hex');
// JSON-value contract, not a sandbox for arbitrary executable JavaScript objects.
// Do not use realm-specific prototype identity: parsed records may cross VM realms.
function jsonValue(value,ancestors=new Set()){
 if(value===null||typeof value==='string'||typeof value==='boolean')return;
 if(typeof value==='number'){assert.ok(Number.isFinite(value),'non-finite JSON number');return;}
 assert.equal(typeof value,'object','unsupported JSON value');
 assert.ok(!ancestors.has(value),'cyclic JSON value');ancestors.add(value);
 assert.ok(Array.isArray(value)||Object.prototype.toString.call(value)==='[object Object]','not a JSON record/array');
 const keys=Reflect.ownKeys(value);assert.ok(keys.every(k=>typeof k==='string'),'symbol JSON key');
 if(Array.isArray(value)){
  assert.equal(keys.length,value.length+1,'sparse/extra array properties');
  for(let i=0;i<value.length;i++)assert.ok(Object.hasOwn(value,String(i)),'sparse JSON array');
 }
 for(const key of keys){
  if(Array.isArray(value)&&key==='length')continue;
  const descriptor=Object.getOwnPropertyDescriptor(value,key);
  assert.ok(descriptor.enumerable&&Object.hasOwn(descriptor,'value'),'non-data/non-enumerable JSON property');
  jsonValue(descriptor.value,ancestors);
 }
 ancestors.delete(value);
}
function validate(data){
 jsonValue(data);
 const root=path.join(__dirname,'..','learning/chatgpt-images-feature/r1');
 assert.equal(hash(fs.readFileSync(path.join(root,'admission.json'))),'31aa079b1e7d49a599af219e0a4d60a206a48796405b5333bcd382225a7e6401');
 const admission=JSON.parse(fs.readFileSync(path.join(root,'admission.json')));
 const overlay=JSON.parse(fs.readFileSync(path.join(root,'overlay.json')));
 assert.equal(hash(fs.readFileSync(path.join(root,'overlay.json'))),admission.files_sha256['overlay.json']);
 const old=structuredClone(data);
 for(const k of ['nodes','sources','view_nodes']){assert.deepEqual(old[k].slice(-overlay[k].length),overlay[k]);old[k]=old[k].slice(0,-overlay[k].length);}
 assert.equal(hash(fs.readFileSync(path.join(root,'registry.json'))),admission.files_sha256['registry.json']);
 assert.deepEqual(old.chatgpt_images_feature_registry,JSON.parse(fs.readFileSync(path.join(root,'registry.json'))));
 delete old.chatgpt_images_feature_registry;
 assert.equal(hash(JSON.stringify(old)+'\n'),'05300dfbdc3b319aa9d1ef1d56a7ad80bf594044141b295434a4942c864a22d2','complete original graph preserved');
 return old;
}
module.exports={validate,jsonValue};
