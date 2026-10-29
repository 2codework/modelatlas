"""Independent read-only delta QA; stdlib only, no source scripts executed."""
import pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent; W=P.parent
A=W/'inference-runtime-research-r1'; B=W/'inference-runtime-research-r2'; Q=W/'inference-runtime-independent-qa-r1'
def j(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(d): return {p.name:sha(p) for p in d.iterdir() if p.is_file()}
before={d.name:snap(d) for d in (A,B,Q)}
a=j(A/'runtime-learning.json');b=j(B/'runtime-learning.json'); errors=[]; checks=[]
def ck(c,s):
 checks.append({'check':s,'passed':bool(c)})
 if not c:errors.append(s)
ck(len(b['nodes'])==4 and [n['id'] for n in a['nodes']]==[n['id'] for n in b['nodes']],'4 original family identities retained')
ck(len(b['sources'])==16 and {(s['id'],s['url']) for s in a['sources']}=={(s['id'],s['url']) for s in b['sources']},'16 original source identities and URLs retained')
allowed={'irt-trt-llm':{'platform_hardware','license'},'irt-ort-core':{'platform_hardware'}}
for x,y in zip(a['nodes'],b['nodes']):
 delta={k for k in set(x)|set(y) if x.get(k)!=y.get(k)}
 ck(delta<=allowed.get(x['id'],set()),'only permitted field changes '+x['id'])
 ck(y['first_release_date'] is None and y['representative_release']['date_iso'] is None,'unknown dates '+y['id'])
 ck(len(y['independent_measurements'])==4 and set(y['independent_measurements'].values())=={'unknown'},'four unknown metrics '+y['id'])
 ck(y['execution_status']=='never-run' and y['runtime_verified'] is False,'no runtime verification '+y['id'])
for name in ('date-evidence.json','dedup.json'):
 ck((A/name).read_bytes()==(B/name).read_bytes(),'preserved '+name)
ck((A/'source-checks.json').read_bytes()==(B/'source-checks-r1-history.json').read_bytes(),'r1 source ledger exactly preserved')
ids={s['id'] for s in b['sources']}; target={'irt-src-trt-license','irt-src-trt-release','irt-src-ort-install'}
ck({s['id'] for s in b['sources'] if s['reading_revision']=='r2_reverified'}==target,'three reread source labels')
ck(sum(s['reading_revision']=='inherited_r1_not_reopened_r2' for s in b['sources'])==13,'13 inherited source labels')
ledger=j(B/'reading-ledger.json')['entries']; read=[]; inherited=[]
for e in ledger:
 read+=e['read_in_r2'];inherited+=e['inherited_r1']
 ck(not set(e['read_in_r2'])&set(e['inherited_r1']) and set(e['source_ids'])==set(e['read_in_r2'])|set(e['inherited_r1']),'disjoint complete ledger '+e['node_id'])
ck(set(read)==target and len(read)==3 and len(inherited)==13 and set(read+inherited)==ids,'ledger full unique coverage')
s=j(B/'source-checks.json')
ck(s['r2_unique_pages_opened']==3 and s['r2_open_operations']+s['r2_find_operations']==s['r2_web_operations']==8 and s['blocked_api_retries']==0,'author ledger arithmetic; not independent transcript recount')
t=b['nodes'][1];o=b['nodes'][2]
ck(t['license']['scope']['exception_path']=='tensorrt_llm/_torch/visual_gen/models/ltx2/' and t['license']['scope']['branch']=='main','exact exception path and branch')
ck(t['platform_hardware']['historical_release']['version']=='v0.18.0' and 'not reviewed' in t['license']['scope']['historical_v0_18_0_license'],'separate historical release/license scope')
ck(o['platform_hardware']['rolling_lifecycle']['directml']=='sustained engineering' and 'not v1.22.0' in o['platform_hardware']['rolling_lifecycle']['scope'],'rolling DirectML lifecycle only')
for d in (A,B,Q):
 manifest={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (d/'SHA256SUMS').read_text().splitlines()}
 ck(set(manifest)==set(before[d.name])-{'SHA256SUMS'},'complete manifest '+d.name)
 ck(all(sha(d/n)==h for n,h in manifest.items()),'all listed hashes '+d.name)
ck(all(sha(W/n)==h for n,h in j(B/'input-integrity.json')['files'].items()),'all 16 r2 input snapshot hashes')
ck(before=={d.name:snap(d) for d in (A,B,Q)},'all inputs unchanged during QA')
print(json.dumps({'status':'passed' if not errors else 'failed','errors':errors,'checks':checks,'counts':{'families':4,'sources':16,'unknown_first_dates':4,'unknown_full_dates':4,'unknown_metrics':16,'reread':3,'inherited':13},'input_hashes':before,'scope':'data delta and hashes, not execution or full new 16-page review'},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
