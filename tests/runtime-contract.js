// Self-authored exact finite stage check, not independent research review.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
function fixture(n,h){const b=fs.readFileSync(path.join(__dirname,'fixtures',n));assert.equal(crypto.createHash('sha256').update(b).digest('hex'),h);return JSON.parse(b);}
function validate(data){
 if(Object.hasOwn(data,"chatgpt_images_feature_registry"))data=require("./images-contract.js").validate(data);
 const b=fixture('runtime-baseline.json','08bfa349e52cdb40d382765db007559bf8b48218c38258168ebdc656155e6d21'),o=fixture('runtime-golden.json','2c41d29f1313c3c5afc66062fbab01fab82a5f6d713ddd3c5543a77a9a15a89a'),r=fixture('runtime-registry.json','fbe74aefff276896a454e1d8ee4ff01706d1886e9e5cd726e78f83aeac2ff768');
 const expected=structuredClone(b);for(const k of Object.keys(o))expected[k].push(...o[k]);expected.inference_runtime_registry=r;assert.deepEqual(data,expected,'complete admitted runtime stage');return b;
}
module.exports={validate};
