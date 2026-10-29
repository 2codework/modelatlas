"""Read-only structural/provenance validator; never runs runtime or source examples."""
import json, pathlib, hashlib
P=pathlib.Path(__file__).resolve().parent
def read(n): return json.loads((P/n).read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
b=read('runtime-learning.json'); errors=[]
def check(c,m):
 if not c: errors.append(m)
ids={s['id'] for s in b['sources']}; nodes={n['id']:n for n in b['nodes']}
check(len(ids)==len(b['sources'])==16,'16 unique sources')
check(len(nodes)==len(b['nodes'])==4,'4 unique families')
for n in b['nodes']:
 check(n['type']=='runtime' and n['is_model'] is False,'non-model identity')
 check(n['runtime_verified'] is False and n['execution_status']=='never-run','no runtime claims')
 check(set(n['source_ids'])<=ids,'node source references')
 check(n['first_release_date'] is None and n['representative_release']['date_iso'] is None,'unknown dates')
 check(n['representative_release']['source_id'] in ids,'release source')
 check(set(n['independent_measurements'].values())=={'unknown'},'unknown measurements')
 check(set(['code','dependencies','models'])<=set(n['license']),'license layers')
 check(len(n['steps_zh'])>=4 and len(n['learning_links'])>=2,'reading coverage')
 check(all(x['source_id'] in ids for x in n['learning_links']),'learning sources')
t=nodes['irt-trt-llm'];o=nodes['irt-ort-core']
check(t['license']['scope']['exception_path']=='tensorrt_llm/_torch/visual_gen/models/ltx2/','exact exception path')
check(t['license']['scope']['branch']=='main','main branch scope')
check(t['platform_hardware']['historical_release']['version']=='v0.18.0','historical platform scope')
check(o['platform_hardware']['rolling_lifecycle']['directml']=='sustained engineering','DirectML lifecycle')
check('not v1.22.0' in o['platform_hardware']['rolling_lifecycle']['scope'],'no lifecycle backport')
ledger=read('reading-ledger.json');check({e['node_id'] for e in ledger['entries']}==set(nodes),'ledger coverage')
for e in ledger['entries']:
 check(set(e['read_in_r2'])|set(e['inherited_r1'])==set(e['source_ids']),'ledger source accounting')
check(sum(len(e['read_in_r2']) for e in ledger['entries'])==3,'three rechecks')
checks=read('source-checks.json');check({s['source_id'] for s in checks['checks']}==ids,'source checks coverage')
for event in read('date-evidence.json')['events']:
 check(event['date_iso'] is None and event['first_release_date'] is None,'date evidence unknown')
check(read('dedup.json')['id_collisions']==[],'historical dedup collision')
try:
 import jsonschema
 jsonschema.validate(b,read('schema.json')); schema='passed using preinstalled jsonschema'
except ImportError: schema='not run: jsonschema unavailable; stdlib invariants checked'
except Exception as e: errors.append(str(e));schema='failed'
manifest=P/'SHA256SUMS'
if manifest.exists():
 entries={line.split('  ',1)[1]:line.split('  ',1)[0] for line in manifest.read_text().splitlines()}
 check(set(entries)=={p.name for p in P.iterdir() if p.is_file() and p.name!='SHA256SUMS'},'manifest complete')
 for n,h in entries.items():check(digest(P/n)==h,'hash '+n)
else: errors.append('SHA256SUMS missing')
# Input recheck is supplementary, not required to use this standalone package elsewhere.
inputs=read('input-integrity.json')['files'];present=[p for p in inputs if (P.parent/p).is_file()]
for p in present:check(digest(P.parent/p)==inputs[p],'input changed '+p)
result={'status':'passed' if not errors else 'failed','errors':errors,'node_count':len(nodes),'source_count':len(ids),'reverified_pages_r2':3,'inherited_pages_r1':13,'unknown_first_release_dates':4,'unknown_full_release_dates':4,'unknown_metric_fields':16,'schema_validation':schema,'input_files_present_and_unchanged':len(present),'structural_check_not_runtime_test':True,'inference_runs':0}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
