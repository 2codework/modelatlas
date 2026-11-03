'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),api=require('../web/video-sampling.js');
for(const name of ['worked','exercise']){
 test(`${name}: original reference timestamps, identities and positions`,()=>{
  assert.equal(api.sequences[name].length,9);
  api.sequences[name].forEach((f,i)=>assert.deepEqual(f,{index:i,ms:i*250,x:10+i*10,identity:i===(name==='worked'?3:5)?(name==='worked'?'B':'C'):'A'}));
  assert.throws(()=>{api.sequences[name][0].identity='X';},TypeError);
 });
 for(let s=1;s<=4;s++)for(let o=0;o<s;o++)test(`${name} independently enumerated s=${s} o=${o}`,()=>{
  const expected=[];for(let i=o;i<9;i+=s)expected.push(i);
  assert.deepEqual(api.sample(name,s,o).map(f=>f.index),expected);
 });
}
test('sparse samples miss both anomalies, alternate offsets expose different events',()=>{
 assert.deepEqual(api.sample('worked',4,0),api.sample('exercise',4,0));
 assert.equal(api.sample('worked',4,3)[0].identity,'B');assert.equal(api.sample('exercise',4,1)[1].identity,'C');
});
test('reject malformed configuration without coercion',()=>{
 for(const args of [['bad',1,0],['toString',1,0],['worked',0,0],['worked',5,0],['worked',2,2],['worked',2,-1],['worked','2',0],['worked',2,NaN],['worked',1.5,0]])assert.throws(()=>api.sample(...args));
});
test('exercise is evidence-gated, not merely a guessed answer',()=>{
 assert.equal(api.check(4,0,'5','limited'),'missing');
 assert.equal(api.check(4,1,'5','limited'),'correct');assert.equal(api.check(1,0,'5','limited'),'correct');
 assert.equal(api.check(4,1,'3','limited'),'retry');assert.equal(api.check(4,1,'5','continuous'),'retry');
 for(const answer of ['',null,'05','9','<script>'])assert.equal(api.check(4,1,answer,'limited'),'invalid');
 assert.equal(api.check(4,1,'5',''),'invalid');
});
