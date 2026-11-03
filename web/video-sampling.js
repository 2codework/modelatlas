/* Original synthetic teaching sequence, not video/model output. */
(function(root){
 'use strict';
 const sequences=Object.freeze(Object.fromEntries(['worked','exercise'].map(name=>[name,Object.freeze(Array.from({length:9},(_,i)=>Object.freeze({index:i,ms:i*250,x:10+i*10,identity:i===(name==='worked'?3:5)?(name==='worked'?'B':'C'):'A'})))])));
 function sample(name,stride,offset){
  if(!Object.hasOwn(sequences,name)||!Number.isInteger(stride)||stride<1||stride>4||!Number.isInteger(offset)||offset<0||offset>=stride)throw Error('Invalid sampling configuration');
  return sequences[name].filter(f=>f.index>=offset&&(f.index-offset)%stride===0);
 }
 function check(stride,offset,answer,claim){
  const frames=sample('exercise',stride,offset);
  if(!/^[0-8]$/.test(answer)||!['limited','continuous'].includes(claim))return 'invalid';
  if(!frames.some(f=>f.index===5))return 'missing';
  return answer==='5'&&claim==='limited'?'correct':'retry';
 }
 const api=Object.freeze({sequences,sample,check});
 if(typeof module==='object'&&module.exports)module.exports=api;else root.VideoSampling=api;
})(typeof globalThis!=='undefined'?globalThis:this);
