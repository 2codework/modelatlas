'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {SCORES, VALUES, calculate, checkAnswer} = require('../web/attention-math.js');
const close = (a,b) => assert.ok(Math.abs(a-b) < 1e-12, `${a} != ${b}`);
const run = (q=0, mask=false) => calculate(SCORES[q], VALUES, 4, q, mask);
test('known hand calculation: scaling, weights, output', () => {
 const r=run(); [0,Math.log(2),Math.log(3)].forEach((x,i)=>close(r.scaled[i],x));
 [1/6,2/6,3/6].forEach((x,i)=>close(r.weights[i],x)); close(r.output,22/3);
 [1/3,2/3,1].forEach((x,i)=>close(r.exponentials[i],x));
});
for (let q=0;q<3;q++) for(const mask of [false,true]) test(`normalization and boundaries query=${q} mask=${mask}`,()=>{
 const r=run(q,mask); close(r.weights.reduce((a,b)=>a+b,0),1);
 assert.ok(r.weights.every(x=>x>=0&&x<=1)); assert.ok(r.output>=2&&r.output<=10);
 r.allowed.forEach((v,j)=>{assert.equal(v,!mask||j<=q);if(!v){assert.equal(r.weights[j],0);assert.equal(r.contributions[j],0);}});
});
test('causal first position is identity',()=>{assert.deepEqual(run(0,true).weights,[1,0,0]);close(run(0,true).output,2);});
test('query two has independently expected causal weights',()=>{
 const r=run(1,true); close(r.weights[0],Math.E/(Math.E+1));close(r.weights[1],1/(Math.E+1));close(r.output,(2*Math.E+6)/(Math.E+1));
});
test('uniform scores average and final causal mask has no effect',()=>{close(run(2).output,6);assert.deepEqual(run(2),run(2,true));});
test('stable softmax handles very large scores without overflow',()=>{
 const r=calculate([10000,9999,-10000],VALUES,1,2,false); assert.ok(r.weights.every(Number.isFinite));close(r.weights[0],Math.E/(Math.E+1));
});
test('constant shift preserves normalized weights',()=>{
 const a=calculate([1,2,3],VALUES,4,2,false), b=calculate([1001,1002,1003],VALUES,4,2,false);assert.deepEqual(a.weights,b.weights);
});
test('negative extreme equal scores normalize',()=>{close(calculate([-10000,-10000,-10000],VALUES,1,2,false).output,6);});
for(const bad of [[],[0,1],[0,1,2,3],[NaN,0,0],[Infinity,0,0],[-Infinity,0,0],[10001,0,0],['0',0,0],null]) test(`reject invalid vector ${JSON.stringify(bad)}`,()=>{
 assert.throws(()=>calculate(bad,VALUES,4,0,false));assert.throws(()=>calculate(SCORES[0],bad,4,0,false));
});
test('reject invalid configuration',()=>{
 for(const d of [0,-1,1.5,1025,NaN,Infinity,'4']) assert.throws(()=>calculate(SCORES[0],VALUES,d,0,false));
 for(const q of [-1,3,0.5,NaN,'0']) assert.throws(()=>calculate(SCORES[0],VALUES,4,q,false));
 for(const c of [null,0,'false']) assert.throws(()=>calculate(SCORES[0],VALUES,4,0,c));
});
test('answer parsing rejects empty, nonfinite, exponent, oversized and non-string inputs',()=>{
 for(const x of ['', ' ', 'NaN','Infinity','1e999','10001','-10001','2junk','0x2',2,null]) assert.equal(checkAnswer(x),'invalid');
});
test('incorrect answer allows retry, correct decimal passes',()=>{assert.equal(checkAnswer('7.333333'),'retry');assert.equal(checkAnswer('2'),'correct');assert.equal(checkAnswer(' 2.0 '),'correct');});
test('calculation does not mutate fixtures',()=>{const before=JSON.stringify([SCORES,VALUES]);run(0,true);run(1);assert.equal(JSON.stringify([SCORES,VALUES]),before);assert.ok(Object.isFrozen(SCORES[0]));});
