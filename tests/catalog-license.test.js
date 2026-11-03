'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),C=require('../web/core.js');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/data.json'))),P=JSON.parse(fs.readFileSync(path.join(__dirname,'../learning/catalog-license/2026-10-31/evidence.json')));
const records=D.vendor_catalog.records,reviewed=records.filter(r=>C.catalogLicenseOverlay(r));
class E{constructor(tag){this.tag=tag;this.children=[];this.attrs={};this.textContent='';}append(...xs){this.children.push(...xs);}setAttribute(k,v){this.attrs[k]=v;}}
const doc={createElement:t=>new E(t)},all=e=>[e,...e.children.flatMap(all)],text=e=>[e.textContent,...e.children.map(text)].join(' ');
test('exactly five catalog overlays match structured official-source provenance',()=>{
 assert.equal(reviewed.length,5);assert.equal(P.rows.length,5);
 assert.deepEqual(reviewed.map(r=>C.catalogLicenseOverlay(r)),P.rows);
 for(const row of P.rows){assert.equal(row.checked_at,'2026-10-31');assert.ok(P.evidence.some(e=>e.catalog_id===row.guard.id&&e.applicability==='applicable'));}
});
test('every exact identity field and original source URL is guarded, including stale versions and checked dates',()=>{
 for(const r of reviewed){for(const key of Object.keys(C.catalogLicenseOverlay(r).guard)){assert.equal(C.catalogLicenseOverlay({...r,[key]:'changed'}),null,key);}
 assert.equal(C.catalogLicenseOverlay({...r,sources:[]}),null);
 assert.equal(C.catalogLicenseOverlay({...r,sources:[...r.sources,{url:'https://example.test/new'}]}),null);
 assert.equal(C.catalogLicenseOverlay({...r,sources:r.sources.map(s=>({...s,url:s.url+'?changed'}))}),null);
 assert.ok(C.catalogLicenseOverlay({...r,sources:[...r.sources].reverse()}));}
});
test('explicit existing license and license URL take precedence; unknown records receive no inferred license',()=>{
 for(const r of reviewed){for(const value of ['MIT','unknown',{},0])assert.equal(C.catalogLicenseOverlay({...r,weights_license:value}),null);
 assert.equal(C.catalogLicenseOverlay({...r,urls:{...r.urls,weights_license:'https://example.test/terms'}}),null);}
 for(const x of [null,undefined,{},...records.filter(r=>!reviewed.includes(r))])assert.equal(C.catalogLicenseOverlay(x),null);
 assert.equal(C.catalogLicenseEvidenceDOM({},doc),null);
});
test('projection and rendering preserve original dates, license fields, source data, and raw canonical records',()=>{
 const before=JSON.stringify(D);for(const r of reviewed){const overlay=C.catalogLicenseOverlay(r);overlay.checkpoint='changed';overlay.links[0].url='javascript:evil';const tree=C.catalogLicenseEvidenceDOM(r,doc);assert.ok(tree);assert.doesNotMatch(text(tree),/javascript:evil/);assert.notEqual(C.catalogLicenseOverlay(r).checkpoint,'changed');}
 assert.equal(JSON.stringify(D),before);for(const r of reviewed){assert.equal(r.checked_at,'2026-10-28');assert.equal(r.weights_license,null);assert.equal(r.dates.release_date,null);}
});
test('DOM presents declared versus full-text evidence, checkpoint and separately dated caveats without legal clearance',()=>{
 for(const r of reviewed){const tree=C.catalogLicenseEvidenceDOM(r,doc),s=text(tree);assert.match(s,/权重许可补充核验/);assert.match(s,/许可声明/);assert.match(s,/适用检查点/);assert.match(s,/2026-10-31/);assert.match(s,/不替换原记录核验日/);assert.match(s,/未下载或运行/);assert.match(s,/main 可更新/);assert.match(s,/不构成具体用途的法律许可/);assert.equal(tree.attrs['aria-label'],'权重许可补充核验');}
 const mistral=text(C.catalogLicenseEvidenceDOM(reviewed[0],doc));assert.match(mistral,/目录本身为 26.10 家族记录/);assert.match(mistral,/不将本结论外推至所有变体/);assert.match(mistral,/MaaS/);
 for(const r of reviewed.filter(r=>r.provider==='Ai2')){const s=text(C.catalogLicenseEvidenceDOM(r,doc));assert.match(s,/未列单独 LICENSE/);assert.match(s,/标准文本/);assert.match(s,/适用关系未作法律判断/);}
});
test('links are exact reviewed HTTPS sources, safe external links and text-only labels',()=>{
 for(const r of reviewed){const row=C.catalogLicenseOverlay(r),tree=C.catalogLicenseEvidenceDOM(r,doc),links=all(tree).filter(e=>e.tag==='a');assert.deepEqual(links.map(a=>a.href),row.links.map(l=>C.safeURL(l.url)));for(const a of links){assert.ok(a.href.startsWith('https://'));assert.equal(a.target,'_blank');assert.equal(a.rel,'noopener noreferrer');}assert.ok(all(tree).every(e=>!['script','img','iframe'].includes(e.tag)));}
 const r=reviewed[0];assert.equal(C.catalogLicenseOverlay({...r,sources:[{url:'javascript:alert(1)'}]}),null);
});
test('catalog detail mounts evidence separately from retained original technical fields',()=>{
 const source=fs.readFileSync(path.join(__dirname,'../web/catalog.js'),'utf8');assert.match(source,/catalogLicenseEvidenceDOM\(r,document\)/);assert.match(source,/'权重许可（原登记）':registrationValue\(r.weights_license,Boolean\(licenseEvidence\)\)/);assert.match(source,/'来源核验日（不是构建日）':r.checked_at/);
});

test('audited empty legacy fields are historical registration gaps, not contradictory current unknowns',()=>{
 const catalog=require('../web/catalog.js');
 for(const value of [null,undefined,'']){assert.equal(catalog.registrationValue(value,true),'原登记为空；补充核验另列');assert.equal(catalog.registrationValue(value,false),'未知 / 本轮未核验');}
 assert.equal(catalog.registrationValue('MIT',true),'MIT');
 const source=fs.readFileSync(path.join(__dirname,'../web/catalog.js'),'utf8');assert.ok(source.includes("Boolean(licenseEvidence)&&['model_card','weights_license'].includes(kind)"));
});

test('overlay-active detail summary remains explicitly historical, without changing unreviewed summaries',()=>{
 const catalog=require('../web/catalog.js'),r=reviewed.find(r=>r.provider==='AI21');
 assert.equal(catalog.detailIntroduction(r,true),'原登记摘要（补充核验见下方）：'+r.summary);
 assert.equal(catalog.detailIntroduction(r,false),r.summary);
 const source=fs.readFileSync(path.join(__dirname,'../web/catalog.js'),'utf8');assert.ok(source.includes('detailIntroduction(r,Boolean(ModelAtlasCore.catalogLicenseOverlay(r)||ModelAtlasCore.catalogDateOverlay(r)||ModelAtlasCore.catalogLifecycleNotice(r)))'));
});
