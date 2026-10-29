// Display vocabulary only: no changes to source records, search, route or classification.
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const C=require('../web/core.js'),catalog=require('../web/catalog.js'),D=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/data.json'),'utf8'));
test('every admitted category, type and evidence enum has an explicit non-machine Chinese label',()=>{
 for(const [field,kind] of [['category','category'],['type','type'],['verification_status','evidence']]){
  const values=new Set(D.nodes.map(n=>n[field]));for(const value of values){assert.ok(Object.hasOwn(C.displayLabels[kind],value),kind+': '+value);const label=C.displayLabel(value,kind);assert.match(label,/[\u3400-\u9fff]/);assert.doesNotMatch(label,/[a-z]+[_-][a-z]+/);assert.doesNotMatch(label,/未收录中文标签/);}
 }
 for(const n of D.nodes){const execution=(n.office_agent||n.assistant_workspace||n.regional_office)?.execution_status;if(execution){assert.ok(Object.hasOwn(C.displayLabels.evidence,execution));assert.equal(C.displayLabel(execution,'evidence'),'未运行');}}
});
test('all current availability options and existing catalog badges avoid machine-enum leakage',()=>{
 for(const row of D.view_nodes)assert.doesNotMatch(C.displayLabel(row.availability,'availability'),/[a-z]+_[a-z]+/);
 for(const r of D.vendor_catalog.records)for(const key of ['entity_type','status','access']){const label=catalog.label(r[key]);assert.notEqual(label,r[key],key+': '+r[key]);assert.doesNotMatch(label,/[a-z]+_[a-z]+/);}
});
test('evidence labels preserve distinctions and never upgrade source review to runtime certification',()=>{
 assert.equal(C.displayLabel('primary_source_checked','evidence'),'一手来源已核对 · 非运行证明');
 assert.equal(C.displayLabel('primary_metadata_reviewed_not_executed','evidence'),'一手元数据已核对 · 未运行');
 assert.equal(C.displayLabel('primary_sources_reviewed_not_executed','evidence'),'一手资料已核对 · 未运行');
 assert.equal(C.displayLabel('source_reviewed_not_replicated','evidence'),'资料已审阅 · 未独立复现');
 assert.equal(C.displayLabel('offline_contract_only','evidence'),'仅离线教学契约验证');
 assert.equal(C.displayLabel('research_claim_scoped','evidence'),'研究论述 · 以注明范围为准');
 assert.equal(C.displayLabel('ambiguous','evidence'),'身份或含义待消歧');
 for(const text of Object.values(C.displayLabels.evidence))assert.doesNotMatch(text,/已实测|已认证|运行成功|产品验证通过/);
});
test('future labels, prototype names, null and malicious-looking values have explicit safe non-inferred fallback',()=>{
 for(const value of ['future_enum','future-enum','constructor','__proto__','<img src=x onerror=alert(1)>']){const label=C.displayLabel(value,'type');assert.ok(label.startsWith('未收录中文标签 · '));assert.ok(label.length>12);assert.doesNotMatch(label,/已核对|已实测|已认证/);}
 for(const value of [null,undefined,''])assert.equal(C.displayLabel(value,'evidence'),'未核验');
 assert.equal(C.displayLabel('Specific Vendor 2.1','vendor'),'Specific Vendor 2.1');
});
test('labeling leaves every source object and exact enum unchanged',()=>{
 const before=JSON.stringify(D);for(const n of D.nodes)for(const [key,kind] of [['category','category'],['type','type'],['verification_status','evidence']])C.displayLabel(n[key],kind);for(const row of D.view_nodes)C.displayLabel(row.availability,'availability');assert.equal(JSON.stringify(D),before);
 const original='open_weights；账号/地区实际可用性未验证';assert.equal(C.displayLabel(original,'availability'),'开放权重；账号/地区实际可用性未验证');
});
test('both kind and value reject inherited-property collisions and always return strings',()=>{
 const kinds=['__proto__','constructor','prototype','toString','valueOf','hasOwnProperty','isPrototypeOf',undefined,null,{},[],()=>{},Symbol('kind')];
 const values=['__proto__','constructor','prototype','toString','valueOf','hasOwnProperty','future_enum',null,undefined,{},[],()=>{},Symbol('value'),42,true,1n];
 for(const kind of kinds)for(const value of values){const label=C.displayLabel(value,kind);assert.equal(typeof label,'string');assert.ok(label.length);assert.doesNotMatch(label,/已核对|已实测|已认证/);}
 for(const [value,kind] of [['constructor','__proto__'],['toString','__proto__'],['prototype','constructor']])assert.equal(C.displayLabel(value,kind),'未收录中文标签 · '+value);
});
test('unsupported object values and kinds do not invoke coercion hooks or execute functions',()=>{
 let calls=0;const bad={toString(){calls++;throw Error('coercion must not run');},[Symbol.toPrimitive](){calls++;throw Error('coercion must not run');}};
 assert.equal(C.displayLabel(bad,'type'),'未核验（标签格式不受支持）');assert.equal(C.displayLabel('model',bad),'未收录中文标签 · model');assert.equal(C.displayLabel(()=>{calls++;},'evidence'),'未核验（标签格式不受支持）');assert.equal(calls,0);
});
