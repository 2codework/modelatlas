import json, pathlib, hashlib
from collections import Counter
P=pathlib.Path('benchmark-research-r1'); p=P/'records.json'; b=json.loads(p.read_text()); R={r['node_id']:r for r in b['records']}
R['bench-mbpp']['dataset_sizes']=[]
R['bench-osworld-original']['dataset_sizes']=[{'value':369,'split':'original paper benchmark; arXiv v2 2024-05-30','unit':'tasks','as_of':'2026-10-28','source_url':'https://arxiv.org/abs/2404.07972'}]
for k in ['bench-osworld-original','bench-androidworld','bench-webarena','bench-visualwebarena','bench-workarena-l1','bench-workarena-plusplus','bench-weblinx-1-0','bench-weblinx-1-1']:
 u=R[k]['official_links']['paper']; R[k]['sources'].append({'url':u,'publisher_type':'benchmark_author','checked_at':'2026-10-28','checked_via':'web','evidence_scope':'论文任务定义与评测设计；未导入成绩'})
for k in ['bench-ocrbench','bench-ocrbench-v2']: R[k]['license_evidence']['code']['source_url']='https://github.com/Yuliang-Liu/MultimodalOCR'
R['bench-longbench']['license_evidence']['code']['source_url']='https://github.com/THUDM/LongBench'
R['bench-osworld-verified']['license_evidence']['code']['source_url']='https://github.com/xlang-ai/OSWorld'
b['coverage_gaps'].append('ChartQA官方ACL论文PDF抓取timeout；未重试，精确评分容差保留未核验；论文landing与官方repo已读取。')
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
# Strict schema: every field required, all known object keys declared. Null is allowed only where observed.
def merge(s,t):
 if s==t:return s
 if s.get('type')=='object' and t.get('type')=='object':
  return {'type':'object','properties':{k:merge(s['properties'][k],t['properties'][k]) if k in s['properties'] and k in t['properties'] else (s['properties'].get(k) or t['properties'][k]) for k in s['properties'].keys()|t['properties'].keys()},'required':sorted(set(s['required'])&set(t['required'])),'additionalProperties':False}
 if s.get('type')=='array' and t.get('type')=='array':return {'type':'array','items': merge(s['items'],t['items'])}
 if not s:return t
 if not t:return s
 opts=[]
 for x in [s,t]:opts.extend(x.get('anyOf',[x]))
 out=[]
 for x in opts:
  if x not in out:out.append(x)
 return {'anyOf':out}
def schema(v):
 if v is None:return {'type':'null'}
 if isinstance(v,bool):return {'type':'boolean'}
 if isinstance(v,str):return {'type':'string'}
 if isinstance(v,int):return {'type':'integer'}
 if isinstance(v,list):
  a={}
  for x in v:a=merge(a,schema(x))
  return {'type':'array','items':a}
 if isinstance(v,dict):return {'type':'object','properties':{k:schema(x) for k,x in v.items()},'required':list(v),'additionalProperties':False}
s=schema(b);s['$schema']='https://json-schema.org/draft/2020-12/schema';s['title']='ModelAtlas benchmark metadata research candidate r1'
rs=s['properties']['records']['items'];rs['properties']['availability']={'enum':['public','gated','private_described','results_only']};rs['properties']['results_preview']['properties']['scores']={'type':'array','maxItems':0};rs['properties']['checked_at']={'type':'string','format':'date'}
(P/'records.schema.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
import jsonschema
jsonschema.Draft202012Validator(s).validate(b)
assert len(b['records'])==22
assert all(not r['results_preview']['scores'] for r in b['records'])
assert not set(b['baseline']['preserved_node_ids'])&set(R)
assert all(r['sources'] and r['checked_at']=='2026-10-28' for r in b['records'])
# Narrative evidence per source group; intentionally no extracted questions, answers, or raw dataset pages.
evidence=[
 {'source':'https://github.com/MMMU-Benchmark/MMMU','observations':['README Evaluation lists dev150/val900/test10500','MMMU-Pro uses filtered questions/options/vision-only design','test answers now released; data card dates release 2026-02-12']},
 {'source':'https://github.com/lupantech/MathVista','observations':['Data Downloading lists testmini1000/test5141','README says test answer labels not public','third-party EvalScope warns no score parity report']},
 {'source':'https://www.docvqa.org/challenges/2020','observations':['Task1 ANLS, case insensitive, space sensitive','Task2 retrieval MAP is distinct; not included in Task1 record']},
 {'source':'https://github.com/Yuliang-Liu/MultimodalOCR/tree/main/OCRBench_v2','observations':['10000 QA pairs; English/Chinese','eval.py followed by get_score.py','Copyright Statement: research only, not commercial']},
 {'source':'https://github.com/NVIDIA/RULER','observations':['main README marks old requirements/evaluation deprecated','points to rulerv1-ns and rulerv2-ns; those branches not reviewed']},
 {'source':'https://github.com/xlang-ai/OSWorld','observations':['2025-07-28 Verified update','README explicitly tells readers to compare new-version results with new benchmark results']},
 {'source':'https://github.com/ServiceNow/WorkArena','observations':['Getting Started requires gated WorkArena-Instances application and approval','L1 current README: 33 atomic tasks,19912 instances; ++682 templates','current README counts may differ from original paper; record snapshot date retained']},
 {'source':'https://github.com/McGill-NLP/weblinx','observations':['1.1 removes some demonstrations, adds no demonstrations','evaluated steps substantially change including tab actions','authors request WebLINX-1.1/BG reporting']},
 {'source':'https://huggingface.co/datasets/gaia-benchmark/GAIA','observations':['gated access and no crawlable resharing','test answers and metadata private','October2025 format update to Parquet does not create a new benchmark score cohort']}
]
(P/'evidence-notes.json').write_text(json.dumps({'checked_at':'2026-10-28','kind':'original_metadata_paraphrases_only','evidence':evidence},ensure_ascii=False,indent=2)+'\n')
audit={'status':'PASS_LOCAL_STRUCTURE_NOT_INDEPENDENT_REVIEW','record_count':len(R),'baseline_preserved_count':11,'availability_counts':dict(Counter(r['availability'] for r in R.values())),'families_count':len(set(r['family'] for r in R.values())),'schema_validation':'pass; jsonschema Draft202012Validator','production_mutated':False,'scores_imported':0,'questions_answers_saved':0,'known_fetch_gaps':['ScreenSpot candidate URL cache miss; excluded','ChartQA paper PDF timeout; metric detail unverified; not retried'],'ready_for_parent_QA':True}
(P/'SELF-CHECK.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(P/'manifest.json').write_text(json.dumps({x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in P.iterdir() if x.is_file() and x.name!='manifest.json'},indent=2)+'\n')
print(json.dumps(audit,ensure_ascii=False))
