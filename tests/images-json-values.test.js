const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const data=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/data.json'),'utf8'));
const {validate,jsonValue}=require('./images-contract.js'),chain=require('./runtime-contract.js').validate;
const paths=[['nodes',0,'publication_date'],['nodes',258,'exact_backend_model'],['nodes',258,'architecture'],['nodes',258,'first_feature_release_date'],['nodes',258,'weights_release_date'],['sources',421,'unknown_boundary'],['chatgpt_images_feature_registry','runtime_verified']];
function set(d,p,v){let n=d;for(const k of p.slice(0,-1))n=n[k];n[p.at(-1)]=v;}
function wire(p,token,combo=false){const d=structuredClone(data);set(d,p,'__WIRE_NUMBER_SENTINEL__');if(combo)d.nodes[0].title='unauthorized';const text=JSON.stringify(d).replace('"__WIRE_NUMBER_SENTINEL__"',token);assert.ok(!text.includes('__WIRE_NUMBER_SENTINEL__'));return JSON.parse(text);}
test('complete legitimate JSON wire overflows are rejected before hash: standalone and chain',()=>{
 for(const p of paths)for(const token of ['1e400','-1e400'])for(const combo of [false,true]){const d=wire(p,token,combo);assert.throws(()=>validate(d),/non-finite/);assert.throws(()=>chain(d),/non-finite/);}
});
test('non-JSON values cannot disappear or become null during stringify',()=>{
 for(const value of [undefined,NaN,Infinity,-Infinity,()=>{},Symbol('x'),1n]){
  const d=structuredClone(data);Object.defineProperty(d,'unregistered',{value,enumerable:true});assert.throws(()=>validate(d));assert.throws(()=>chain(d));
  const a=structuredClone(data);a.nodes[0].publication_date=value;assert.throws(()=>validate(a));assert.throws(()=>chain(a));
 }
 for(const mutate of [d=>delete d.nodes[0],d=>d.nodes.extra=true,d=>d[Symbol('x')]=1,d=>Object.defineProperty(d,'extra',{value:1,enumerable:false}),d=>d.extra=d,d=>d.extra=new Date(),d=>Object.defineProperty(d,'extra',{enumerable:true,get(){throw Error('must not execute getter');}})]){const d=structuredClone(data);mutate(d);assert.throws(()=>validate(d));}
});
test('finite values and cross-realm parsed JSON remain legitimate, with unchanged full-stage verification',()=>{
 for(const value of [0,-0,1,0.1,1e300,Number.MIN_VALUE,null,true,'text',[],{}])assert.doesNotThrow(()=>jsonValue(value));
 const foreign=vm.runInNewContext('JSON.parse(raw)',{raw:JSON.stringify(data)});assert.doesNotThrow(()=>validate(foreign));assert.doesNotThrow(()=>chain(foreign));
 const before=JSON.stringify(data);validate(data);chain(data);assert.equal(JSON.stringify(data),before);
});
