const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const {evaluate,init}=require('../web/foundation-self-checks.js');
const html=fs.readFileSync(__dirname+'/../web/foundations.html','utf8');
const checks=[...html.matchAll(/class="self-check-interactive" hidden data-correct="([012])" data-explanation="([^"]+)">([\s\S]*?)<\/fieldset>/g)];
test('all six admitted exercises exhaust every option with explanatory feedback',()=>{
 assert.equal(checks.length,6);
 for(const [,correct,explanation,body] of checks){
  const allowed=[...body.matchAll(/type="radio"[^>]* value="([012])"/g)].map(m=>m[1]);
  assert.deepEqual(allowed,['0','1','2']);assert.ok(explanation.length>40);
  for(const selected of allowed){const result=evaluate(selected,correct,allowed,explanation);assert.equal(result.status,selected===correct?'correct':'incorrect');assert.ok(result.message.includes(explanation));}
  for(const selected of [null,undefined,'']){const result=evaluate(selected,correct,allowed,explanation);assert.equal(result.status,'unanswered');assert.ok(!result.message.includes(explanation));}
  for(const selected of ['x','3',0,{},[],false])assert.equal(evaluate(selected,correct,allowed,explanation).status,'invalid');
  assert.equal(evaluate('0','9',allowed,explanation).status,'invalid');
 }
});
function makeBox(correct='1'){
 const inputs=['0','1','2'].map(value=>({value,checked:false,events:{},addEventListener(k,fn){this.events[k]=fn;}}));
 const feedback={textContent:'',dataset:{}};
 const button=()=>({events:{},addEventListener(k,fn){this.events[k]=fn;}}),check=button(),clear=button();
 return {hidden:true,dataset:{correct,explanation:'原理说明：只按授权与原文核对，不补编事实。'},inputs,feedback,check,clear,querySelectorAll(){return inputs;},querySelector(q){return q==='[data-check]'?check:q==='[data-clear]'?clear:feedback;}};
}
test('optional DOM checks require explicit choice, clear safely, never auto-check or move focus',()=>{
 const boxes=Array.from({length:6},()=>makeBox());init({querySelectorAll:()=>boxes});
 for(const box of boxes){
  assert.equal(box.hidden,false);assert.ok(box.inputs.every(i=>!i.checked));
  box.check.events.click();assert.equal(box.feedback.dataset.result,'unanswered');
  box.inputs[0].checked=true;box.check.events.click();assert.equal(box.feedback.dataset.result,'incorrect');
  box.check.events.click();assert.equal(box.feedback.dataset.result,'incorrect');
  box.inputs[0].checked=false;box.inputs[1].checked=true;box.inputs[1].events.change();assert.equal(box.feedback.dataset.result,undefined);assert.match(box.feedback.textContent,/选择已变更/);
  box.check.events.click();assert.equal(box.feedback.dataset.result,'correct');
  // Hiding an article for native hash navigation does not rebuild the check.
  box.hidden=true;box.hidden=false;assert.equal(box.inputs[1].checked,true);assert.equal(box.feedback.dataset.result,'correct');
  box.clear.events.click();assert.ok(box.inputs.every(i=>!i.checked));assert.equal(box.feedback.dataset.result,undefined);
  box.check.events.click();assert.equal(box.feedback.dataset.result,'unanswered');
 }
});
test('helper has no networking, persistence, history or progress mutation',()=>{
 const js=fs.readFileSync(__dirname+'/../web/foundation-self-checks.js','utf8');
 for(const forbidden of [/fetch\s*\(/,/XMLHttpRequest/,/localStorage/,/sessionStorage/,/sendBeacon/,/location\./,/history\./,/\.focus\(/])assert.doesNotMatch(js,forbidden);
});
