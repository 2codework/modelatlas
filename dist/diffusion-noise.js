/* Original finite-vector algebra; not a model, predictor or reverse sampler. */
(function(root){'use strict';
function number(v,lo,hi,field){if(typeof v!=='number'||!Number.isFinite(v)||v<lo||v>hi)throw new Error(field);return v;}
function vector(v,field){if(!Array.isArray(v)||v.length!==2)throw new Error(field);return Array.from(v,x=>number(x,-10,10,field));}
function calculate(alpha_bar,x0,epsilon,estimate){const a=number(alpha_bar,.01,1,'alpha_bar');x0=vector(x0,'x0');epsilon=vector(epsilon,'epsilon');estimate=vector(estimate,'estimate');
const signal_coefficient=Math.sqrt(a),noise_coefficient=Math.sqrt(1-a),signal=x0.map(v=>signal_coefficient*v),noise=epsilon.map(v=>noise_coefficient*v),xt=signal.map((v,i)=>v+noise[i]);
const reconstruct=e=>xt.map((v,i)=>(v-noise_coefficient*e[i])/signal_coefficient),oracle=reconstruct(epsilon),predicted=reconstruct(estimate),error=predicted.map((v,i)=>v-x0[i]),mse=error.reduce((s,v)=>s+v*v,0)/2,estimate_mse=estimate.reduce((s,v,i)=>s+(v-epsilon[i])**2,0)/2;
return{alpha_bar:a,x0,epsilon,estimate,signal_coefficient,noise_coefficient,signal,noise,xt,oracle,predicted,error,mse,estimate_mse,amplification:Math.sqrt((1-a)/a),expected_mse:(1-a)/a*estimate_mse};}
const api={calculate};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.ModelAtlasDiffusionNoise=api;
})(globalThis);
