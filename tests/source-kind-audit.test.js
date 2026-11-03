'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),C=require('../web/core.js');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/data.json')));
const provenance=JSON.parse(fs.readFileSync(path.join(__dirname,'../learning/source-kind/2026-10-31/classification.json')));
const group=source=>C.referenceAccess({source_ids:[source.id]},[source]).groups;
const source=id=>{const s=D.sources.find(s=>s.id===id);assert.ok(s,id);return s;};
test('exactly ten reviewed source genres refine presentation without mutating evidence or dates',()=>{
 const before=JSON.stringify(D);assert.equal(provenance.records.length,10);
 assert.equal(new Set(provenance.records.map(r=>r.source_id)).size,10);
 assert.deepEqual(D.sources.filter(s=>C.sourceKindReview(s)).map(s=>s.id).sort(),provenance.records.map(r=>r.source_id).sort());
 for(const r of provenance.records){const s=source(r.source_id),review=C.sourceKindReview(s);assert.equal(s.url,r.url);assert.equal(review.kind,r.kind);assert.equal(review.classification_reviewed_at,r.classification_reviewed_at);assert.equal(review.scope,'source_genre_only_not_content_revalidation');assert.ok(r.reason);assert.ok(r.source_observation_date);assert.equal(r.classification_reviewed_at,'2026-10-31');const g=group(s);assert.equal(g.official.length,1);assert.equal(g.papers.length,0);assert.equal(g.other.length,0);assert.equal(g.official[0].checked_at,s.checked_at);assert.equal(g.official[0].url,s.url);assert.equal(g.official[0].source_id,s.id);}
 assert.equal(JSON.stringify(D),before);assert.match(provenance.scope,/not full content revalidation/);
});
test('exact ID and exact URL are both required, including for reused official URLs',()=>{
 for(const r of provenance.records){const s=source(r.source_id);for(const altered of [{...s,id:'unreviewed-source'},{...s,url:s.url+'#changed'},{...s,url:s.url+'/'},{...s,url:'https://example.test/paper'},{...s,url:'javascript:alert(1)'}]){assert.equal(C.sourceKindReview(altered),null);assert.equal(group(altered).official.length,0);}}
 assert.equal(C.sourceKindReview(null),null);assert.equal(C.sourceKindReview({}),null);
 assert.equal(C.sourceKindReview({id:'new-paper',url:'https://arxiv.org/abs/1234',title:'official model card paper'}),null);
});
test('existing explicit kinds and source_type always take precedence, including unknown vocabulary',()=>{
 for(const r of provenance.records){const s=source(r.source_id);for(const field of ['kind','source_type']){const paper={...s,[field]:'original_paper'},other={...s,[field]:'new_unrecognized_kind'},official={...s,[field]:'official_docs'};assert.equal(C.sourceKindReview(paper),null);assert.equal(group(paper).papers.length,1);assert.equal(C.sourceKindReview(other),null);assert.equal(group(other).other.length,1);assert.equal(C.sourceKindReview(official),null);assert.equal(group(official).official.length,1);}}
});
test('three already classified sources are unchanged; seven unresolved sources remain other',()=>{
 for(const id of ['found-src-012','found-src-026']){const s=source(id);assert.equal(C.sourceKindReview(s),null);assert.equal(group(s).papers.length,1);}
 const release=source('timeline-r1-src-001');assert.equal(C.sourceKindReview(release),null);assert.equal(group(release).official.length,1);
 for(const id of ['audio-src-moshi-intro','creative-gap-src-kden-broken','early-nlp-src-crf-lafferty-list','media-src-42f01042f3e137f7','media-src-ce716e17eaedbd59','vid-src-comfy','vid-src-whisperx']){const s=source(id);assert.equal(C.sourceKindReview(s),null);assert.equal(group(s).other.length,1);assert.equal(group(s).papers.length,0);assert.equal(group(s).official.length,0);}
});
test('model cards and specification preserve specific genre rather than becoming papers',()=>{
 assert.equal(C.sourceKindReview(source('course-skills')).kind,'specification');
 for(const id of ['edge-src-smol-card','music-src-musicgen'])assert.equal(C.sourceKindReview(source(id)).kind,'official_model_card');
});
test('reviewed shorthand titles become readable without replacing future explicit titles',()=>{
 for(const id of ['cgw-src-inputs','edge-src-fast-export','edge-src-smol-card']){const s=source(id);assert.ok(C.sourceDisplayTitle(s));assert.notEqual(C.sourceDisplayTitle(s),s.title);assert.equal(C.sourceDisplayTitle({...s,title:'New reviewed title'}),null);assert.equal(C.sourceDisplayTitle({...s,url:s.url+'?changed'}),null);assert.equal(C.sourceDisplayTitle({...s,kind:'official_docs'}),null);assert.equal(group(s).official[0].title,C.sourceDisplayTitle(s));}
});
