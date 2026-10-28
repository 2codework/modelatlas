import json,hashlib,pathlib
r1=pathlib.Path('realtime-audio-model-research-r1');r2=pathlib.Path('realtime-audio-model-research-r2');out=pathlib.Path('realtime-audio-model-qa-r2')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((r1/'raw-models.json').read_text()); b=json.loads((r2/'raw-models.json').read_text()); m={x['id']:x for x in b['models']};v=m['speech-voxtral-realtime-2602'];g=m['speech-gpt-realtime-family'];mo=m['speech-moshi']; checks={}
checks['manifest_self_hash']=h(r2/'SHA256SUMS')=='58aa85c48a794e3aa68beab4566f424897381cf1861ee0f27f879f81cc897627'
lines=(r2/'SHA256SUMS').read_text().splitlines();checks['manifest_entries']=all(h(r2/line.split('  ',1)[1])==line.split('  ',1)[0] for line in lines);checks['all_18_files_covered']=len(list(r2.rglob('*')))==19 and len(lines)==17
checks['r1_all_7_files_byte_identical']=all(p.read_bytes()==(r2/'before-qa'/p.name).read_bytes() for p in r1.iterdir() if p.is_file())
record=json.loads((r2/'R1-SHA256.json').read_text()); checks['r1_hash_record_correct']=all(h(r1/k)==val==h(r2/'before-qa'/k) for k,val in record.items())
s1=json.loads((r1/'source-checks.json').read_text());s2=json.loads((r2/'source-checks.json').read_text());checks['original_20_source_records_unchanged']=s1['checks']==s2['checks'][:20] and a['sources']==b['sources'][:20]
checks['F01']=any(x['kind']=='paper_v2' and x['date']=='2026-02-21' and x['timestamp_utc']=='2026-02-21T00:06:15Z' for x in v['dates'])
checks['F02']=v['absolute_minimum_vram_gb'] is None and v['official_deployment_configuration']=={'precision':'BF16','runtime':'vLLM','gpu_count':1,'gpu_memory_gb_at_least':16,'source_ids':['vox-card'],'section':'Usage / vLLM / Serve','verified_by_execution':False}
checks['F03']=len(v['latency_evidence'])==6 and v['latency_evidence'][-1]['value'] is None
versions={x['exact_id']:x for x in g['version_records']};old=versions['gpt-realtime-2025-08-28'];new=versions['gpt-realtime-2.1']
checks['F04']=old['related_alias']=='gpt-realtime' and old['deprecation_announced']=='2026-07-20' and old['scheduled_shutdown']=='2027-01-20' and old['pricing_per_million_tokens_usd']['text_output']==16 and new['pricing_per_million_tokens_usd']['text_output']==24 and new['release_date'] is None and 'deprecation_announced' not in new
checks['F05']=any(x['entity']=='GPT-Realtime-2' for x in b['coverage_gaps'])
checks['F06']=v['streaming']['transport_bidirectional_streaming'] is True and v['streaming']['conversational_speech_to_speech'] is False and 'full_duplex' not in v['streaming']
checks['Moshi_scope']=mo['exact_version'] is None and mo['reviewed_variants'][0]['first_weights_upload_date'] is None and '家族' in mo['date_scope_zh']
sids={x['id'] for x in b['sources']};bad=[]
def walk(x):
 if isinstance(x,dict):
  for k,val in x.items():
   if k.endswith('source_ids'):
    bad.extend(z for z in val if z not in sids)
   walk(val)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(b);checks['source_refs_resolve']=not bad
c=pathlib.Path('github-migration-r1/public/modelatlas/docs/data.json');checks['canonical_unchanged']=h(c)=='08b1dc2ab60f1eda3e64a65aee0034487506af8108cf44bfeec98aa8b97ef578'
checks['execution_flags_false']=all(x is False for x in b['execution'].values());checks['csm_unchanged']=a['models'][1]==b['models'][1]
dates=json.loads((r2/'dedup-and-date-evidence.json').read_text())['date_evidence'];checks['date_evidence_matches_models']=all(x['events']==m[x['model_id']]['dates'] for x in dates)
result={'schema_version':'realtime-audio-final-qa.v2','as_of':'2026-10-28','verdict':'accept_scoped_research' if all(checks.values()) else 'fix','checks':checks,'open_fix_count':0,'models':[{'id':x['id'],'verdict':'accept_scoped_research','unknown_retained':True} for x in b['models']],'coverage_claim':'NOT global or complete historical coverage','remaining_unknown':['first weight upload/revision hashes','CSM real-time/full duplex','GPT2.1 release date and complete predecessor history','absolute minimum hardware and measured end-to-end latency','actual account/region/API permissions','illustration QA not performed'],'evidence_basis':'Independent official sources from QA r1, plus HF Recommended Settings independently re-opened for r2','r2_file_hashes':{str(p.relative_to(r2)):h(p) for p in sorted(r2.rglob('*')) if p.is_file()}}
(out/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(checks,indent=2));assert all(checks.values())
