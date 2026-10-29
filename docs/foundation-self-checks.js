/* Original synthetic teaching checks. No model or external task execution, persistence or progress writes. */
(function(root){'use strict';
 function evaluate(selected, correct, allowed, explanation){
  if(selected===null || selected===undefined || selected==='')return {status:'unanswered',message:'请先选择一项，再核对。尚未提供答案。'};
  if(!Array.isArray(allowed) || !allowed.includes(selected) || !allowed.includes(correct))return {status:'invalid',message:'无法核对这个选择，请清除后重新选择。'};
  const ok=selected===correct;
  return {status:ok?'correct':'incorrect',message:(ok?'这次选择符合本题条件。':'这次选择不符合本题条件。')+'理由：'+explanation};
 }
 function init(doc){
  for(const box of doc.querySelectorAll('.self-check-interactive')){
   const inputs=Array.from(box.querySelectorAll('input[type="radio"]')),feedback=box.querySelector('.self-check-feedback');
   box.querySelector('[data-check]').addEventListener('click',()=>{
    const selected=inputs.find(input=>input.checked);
    const result=evaluate(selected?selected.value:null,box.dataset.correct,inputs.map(input=>input.value),box.dataset.explanation);
    feedback.textContent=result.message;feedback.dataset.result=result.status;
    feedback.scrollIntoView({block:'nearest',behavior:'auto'});
   });
   box.querySelector('[data-clear]').addEventListener('click',()=>{
    for(const input of inputs)input.checked=false;
    feedback.textContent='已清除选择，可以重新尝试。';delete feedback.dataset.result;
   });
   for(const input of inputs)input.addEventListener('change',()=>{feedback.textContent='选择已变更，请点击“核对我的选择”。';delete feedback.dataset.result;});
   box.hidden=false;
  }
 }
 if(typeof module==='object' && module.exports)module.exports={evaluate,init};
 if(root.document)init(root.document);
})(typeof window==='object'?window:globalThis);
