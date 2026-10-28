const test=require('node:test'),assert=require('node:assert/strict'),C=require('../web/core.js');
test('explicit unknown display labels only; compatibility not availability certification',()=>{
 for(const value of [null,undefined,'','  ','未核验',' 未核验 ','unknown','UNKNOWN','unknown unless explicitly qualified below; no sign-in or account eligibility check；需租户','unknown — scope not checked'])assert.equal(C.hasExplicitUnknownAvailability(value),true,String(value));
 for(const value of ['not unknown','known unknown','unknownish','unknown_status','public_download','gated','需账号','未核验之外的其他文本',false,0,{},[]])assert.equal(C.hasExplicitUnknownAvailability(value),false,String(value));
});
