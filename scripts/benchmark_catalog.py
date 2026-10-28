"""Metadata-only benchmark adapter. Raw history is immutable; access claims are explicit."""
import copy, hashlib, json, shutil

LIFECYCLE_STATUS = {'documented':'unknown', 'historical_variant':'historical', 'deprecated_pipeline':'deprecated'}
def lifecycle_status(record):
    status=record.get('lifecycle',{}).get('status')
    if status not in LIFECYCLE_STATUS: raise ValueError('unsupported benchmark lifecycle: '+str(status))
    return LIFECYCLE_STATUS[status]

def load(root):
    path=root/'data/benchmarks'
    admission=json.loads((path/'admission.json').read_text())
    for name,digest in admission['sha256'].items():
        if hashlib.sha256((path/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('benchmark hash mismatch: '+name)
    raw=json.loads((path/'raw/records.json').read_text())
    overlay=json.loads((path/'overlay.json').read_text())
    records=copy.deepcopy(raw['records'])
    ids={r['node_id'] for r in records}
    if len(records)!=22 or len(ids)!=22: raise ValueError('benchmark duplicate/count mismatch')
    bundle={'schema_version':'benchmark-adapted.v1','title':'公开评测介绍 · 22条版本/分片记录','checked_at':raw['checked_at'],'scope_zh':'公开介绍、经来源支持的聚合量与官方跳转；不是题库或排行榜。','nodes':[],'edges':[],'sources':[],'events':[],'dataset_benchmark_registry':records,'coverage_gaps':['评测新增22条记录/15个家族，不代表完整覆盖。公开入口不等于匿名下载、完整标签或商用许可；没有新增成绩。'],'raw_benchmark_metadata':raw,'access_overlay':overlay}
    for r in records:
        nid=r['node_id']
        access=copy.deepcopy(overlay['default_access'])
        access.update(overlay['records'].get(nid,{}))
        r['raw_availability']=r['availability']
        r['access_semantics']=access
        r['availability']=access['label_zh']
        r['access_application_note']=access['note_zh']+' '+r['access_application_note']
        r['harness_metadata']=r['harness']
        r['harness']='官方入口：'+r['harness']['url']+'；精确revision未固定，未执行评测。'
        r['source_urls']=list(dict.fromkeys(s['url'] for s in r['sources']))
        for url in r['official_links'].values():
            if url and url not in r['source_urls']:r['source_urls'].append(url)
        r['source_ids']=[]
        for i,url in enumerate(r['source_urls']):
            sid='bench-src-'+nid.removeprefix('bench-')+'-'+str(i+1)
            r['source_ids'].append(sid)
            bundle['sources'].append({'id':sid,'title':r['name']+' · 官方来源/入口','url':url,'checked_at':r['checked_at'],'kind':'official_metadata','primary':True,'verification_status':'primary_metadata_reviewed_downstream_not_exhaustive','evidence_scope':'公开介绍、版本与聚合元数据；不代表所有下游文件或许可逐一审计。','version':r['version']})
        sizes='；'.join(str(x['value'])+' '+x['unit']+'（'+x['split']+'；核验 '+x['as_of']+'；'+x['source_url']+'）' for x in r['dataset_sizes']) or '聚合规模未核验，不推测样本量。'
        desc=r['description_zh']+' 任务：'+r['task_zh']+'。版本：'+r['version']+'；分片：'+r['split']+'。访问：'+access['label_zh']+'。规模：'+sizes
        node={'id':nid,'title':r['name'],'type':'benchmark','category':'evaluation','description_zh':desc,'summary_zh':r['description_zh'],'version':r['version'],'checked_at':r['checked_at'],'verification_status':'primary_metadata_reviewed_not_executed','source_ids':r['source_ids'],'source_urls':r['source_urls'],'availability':r['availability'],'license':r['license'],'tags':[r['family'],r['task_zh'],r['version'],r['split'],*r['modality']],'input_modalities':r['modality'],'lifecycle':{'status':lifecycle_status(r),'note_zh':'原始状态：'+r['lifecycle']['status']+'；'+r['lifecycle']['note_zh']+' 仅按来源状态映射，不由名称推断。核验日期不是发布日期。','replacement_node_ids':[]},'misconceptions':[r['display_policy'],'公开入口不等于完整可复现或可商用。不同版本/分片不得合并成绩。',access['note_zh']],'benchmark_metadata':copy.deepcopy(r)}
        bundle['nodes'].append(node)
        for relation in r['relations']:
            if relation['target_node_id'] not in ids or relation['score_comparable'] is not False:raise ValueError('benchmark invalid relation')
            bundle['edges'].append({'source':nid,'target':relation['target_node_id'],'type':relation['type'],'source_ids':r['source_ids'],'verification_status':'primary_metadata_reviewed_not_executed','explanation_zh':'版本/任务关联；成绩不可直接比较。','score_comparable':False})
    return bundle

def publish(root,out):
    shutil.copytree(root/'data/benchmarks',out/'benchmarks',dirs_exist_ok=True)
