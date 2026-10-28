#!/usr/bin/env python3
"""Dependency-free, fail-closed research normalizer and static book builder."""
import json, re, shutil, datetime, copy, math, sys
sys.path.insert(0,str(__import__("pathlib").Path(__file__).resolve().parent))
import asset_versions
import mcp_learning
import creative_workflows
import office_agents
import media_evaluation
import media_timeline
import vendor_catalog
import benchmark_catalog
import world_models
from pathlib import Path
from urllib.parse import urlsplit
ROOT = Path(__file__).resolve().parents[1]
EVENT_TYPES = {'paper_submission','report_publication','announcement','weights_release','api_launch','documentation_update','standard_publication','benchmark_release','paper_revision','platform_migration'}
def require(ok, message):
    if not ok: raise ValueError(message)
def url_ok(url):
    try:
        p=urlsplit(url)
        return p.scheme in {'http','https'} and bool(p.hostname) and not p.username and not p.password and not any(c.isspace() for c in url)
    except (ValueError,TypeError): return False
def date_ok(value, precision):
    try:
        if precision=='day': return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',value)) and bool(datetime.date.fromisoformat(value))
        if precision=='month': return bool(re.fullmatch(r'\d{4}-\d{2}',value)) and bool(datetime.date.fromisoformat(value+'-01'))
        if precision=='year': return bool(re.fullmatch(r'\d{4}',value)) and 1<=int(value)<=9999
    except (ValueError,TypeError): pass
    return False

# Current display only; retained research bundles remain historical evidence.
COVERAGE_DISPLAY_OVERLAYS = {
 '配图仅提供原创示意方案，未制作或复制论文图片；外部图权利尚未核查。': '原创教学SVG已制作，用于三类预测接口对照；不是论文原图或实测架构复原，未复制论文图片；外部图权利仍未核查。',
 '未覆盖3D/CAD/工业设计/字体生成/印前色彩管理等后续专题': 'CAD、3D资产与动画已有代表性未执行教学案例；更多工业设计、字体生成与印前色彩管理仍待补充，不代表完整覆盖。',
 '视频与音乐已初步纳入相关技术节点；更多独立系列、版本与教程仍待补充。3D、机器人和世界模型仍缺独立系列；不代表全领域覆盖。': '视频、音乐及CAD/3D/动画已有代表性节点或教程；世界模型、JEPA与具身对照已增加12个有限节点，机器人系统与各家完整系列仍不齐全，不代表全领域覆盖。',
}
def current_coverage_display(gaps, node_ids):
    enabled=set()
    if {'design-freecad-partdesign','design-godot-asset-pipeline','design-godot-spriteframes'} <= node_ids:
        enabled.add('未覆盖3D/CAD/工业设计/字体生成/印前色彩管理等后续专题')
    if world_models.EXPECTED <= node_ids:
        enabled.add('配图仅提供原创示意方案，未制作或复制论文图片；外部图权利尚未核查。')
        enabled.add('视频与音乐已初步纳入相关技术节点；更多独立系列、版本与教程仍待补充。3D、机器人和世界模型仍缺独立系列；不代表全领域覆盖。')
    return [COVERAGE_DISPLAY_OVERLAYS[g] if isinstance(g,str) and g in enabled else g for g in gaps]

def normalize(bundles):
    result={'schema_version':'modelatlas.site.v1','version':'0.2.2','checked_at':'2026-10-28','nodes':[],'edges':[],'sources':[],'events':[],'research_bundles':bundles,'coverage_gaps':[]}
    for b in bundles:
        for k in ('nodes','edges','sources','events'): result[k].extend(copy.deepcopy(b.get(k,[])))
        result['coverage_gaps'].extend(b.get('coverage_gaps',[]))
    # Apply checked overlays only to derived events; historical bundles stay intact.
    patched=set()
    for bundle in bundles:
        for patch in bundle.get('event_patches',[]):
            eid=patch.get('event_id')
            require(eid not in patched,'duplicate event patch')
            matches=[e for e in result['events'] if e['id']==eid]
            require(len(matches)==1,'missing/duplicate patch target')
            require(patch.get('operation')=='merge_fields_by_existing_id','unsupported patch operation')
            before=patch.get('expected_before',{})
            require(all(k in before for k in ('date','event_type','node_ids')),'incomplete expected_before')
            require(all(k in matches[0] and matches[0][k]==v for k,v in before.items()),'event patch expected_before mismatch: '+eid)
            updates=patch.get('set',{})
            require(not set(updates).intersection({'id','node_ids','event_type'}),'patch cannot change event identity')
            matches[0].update(copy.deepcopy(updates));patched.add(eid)
    # Creative source records are preserved in research_bundles. Only derived views adapt aliases.
    case_ids=set()
    for bundle in bundles:
        for case in bundle.get('cases',[]):
            require(case['id'] not in case_ids,'duplicate cross-repo case ID')
            case_ids.add(case['id'])
            for nid in case.get('modelatlas_node_ids',[]):
                node=next((n for n in result['nodes'] if n['id']==nid),None)
                require(node is not None,'dangling cross-repo node')
                node.setdefault('agentwork_links',[]).append({'id':case['id'],'title':case['title'],'url':'https://2codework.github.io/agentwork/?case='+case['id']})
        if bundle.get('schema_version','').startswith('creative'):
            for raw in bundle.get('nodes',[]):
                node=next(n for n in result['nodes'] if n['id']==raw['id'])
                node.setdefault('type',node.get('kind','tool'))
                node.setdefault('category','creative-music')
                node.setdefault('checked_at',bundle['checked_at'])
                node.setdefault('license',node.get('license_notes','未核验'))
    # Adapt explicitly declared source schema without mutating retained research bundles.
    aliases={'paper_first_submitted':'paper_submission','technical_report':'report_publication','announced':'announcement','weights_released':'weights_release','api_launched':'api_launch'}
    for e in result['events']:
        if 'node_ids' not in e and 'node_id' in e: e['node_ids']=[e['node_id']]
        e['event_type']=aliases.get(e['event_type'],e['event_type'])
        e.setdefault('title',e['id'])
        if 'evidence' in e: e.setdefault('evidence_locator',e['evidence'])
        e.setdefault('verification_status','source_reviewed_not_replicated' if e.get('source_ids') else 'not_checked')
    for e in result['edges']:
        if e.get('evidence_type')=='editorial_learning_order': e.setdefault('verification_status','editorial_learning_relation')
    result['evaluation_snapshots']=[copy.deepcopy(r) for b in bundles for r in b.get('snapshots',[])]
    result['dataset_benchmark_registry']=[copy.deepcopy(r) for b in bundles for r in b.get('dataset_benchmark_registry',[])]
    result['media_evaluation_registry']=[copy.deepcopy(r) for b in bundles for r in b.get('media_evaluation_registry',[])]
    sets={}
    for kind in ('nodes','sources','events'):
        ids=[n['id'] for n in result[kind]]
        require(len(ids)==len(set(ids)),f'duplicate {kind} ID')
        require(all(isinstance(i,str) and re.fullmatch(r'[a-z0-9][a-z0-9._-]*',i) for i in ids),f'invalid {kind} ID')
        sets[kind]=set(ids)
    for source in result['sources']:
        require(date_ok(source.get('checked_at'),'day'),'missing/invalid source checked_at')
        require(url_ok(source['url']),f'unsafe source URL: {source["id"]}')
    def refs(item, label):
        for sid in item.get('source_ids',[]): require(sid in sets['sources'],f'missing source {sid} on {label}')
        for u in item.get('source_urls',[]): require(url_ok(u),f'unsafe URL on {label}')
    for node in result['nodes']:
        refs(node,node['id'])
        require(node.get('title') and (node.get('description_zh') or node.get('summary_zh')),f'empty node {node["id"]}')
        for ref in node.get('prerequisites',[]): require(ref in sets['nodes'],f'missing prerequisite {ref}')
        if node.get('family_id'): require(node['family_id'] in sets['nodes'],'missing family')
        require(node.get('verification_status') in {'ambiguous','not_checked','editorial_learning_relation'} or node.get('source_ids') or node.get('source_urls'),f'claim without evidence: {node["id"]}')
    for edge in result['edges']:
        require(edge['source'] in sets['nodes'] and edge['target'] in sets['nodes'],'dangling edge')
        refs(edge,'edge')
        require(edge.get('verification_status')=='editorial_learning_relation' or edge.get('source_ids') or edge.get('source_urls'),'edge without evidence')
    for event in result['events']:
        refs(event,event['id'])
        require(event.get('node_ids') and all(i in sets['nodes'] for i in event['node_ids']),'dangling event')
        require(event.get('event_type') in EVENT_TYPES,'unknown event type')
        if event.get('date') is not None:
            require(date_ok(event['date'],event.get('date_precision')),'invalid date/precision')
            require(event.get('source_ids') or event.get('source_urls'),'dated event without source')
            require(event.get('verification_status') not in {'not_checked','ambiguous'},'unverified dated event')
        else: require(event.get('date_precision') in (None,'unknown'),'unknown date precision')
        if event.get('available_by') is not None:
            require(date_ok(event['available_by'],event.get('available_by_precision')),'invalid available_by/precision')
            require(event.get('source_ids') or event.get('source_urls'),'available_by without source')
            require(event.get('note_zh'),'available_by requires scope note')
    for row in result['dataset_benchmark_registry']:
        require(row['node_id'] in sets['nodes'],'dangling registry node')
        require(not row.get('results_preview',{}).get('scores'),'score import unsupported in v0.1; full provenance schema required')
        refs(row,'registry')
        if row.get('results_preview',{}).get('official_results_url'): require(url_ok(row['results_preview']['official_results_url']),'unsafe results URL')
        for k in ('access_url','access_application_url'):
            if row.get(k): require(url_ok(row[k]),'unsafe registry URL')
    for row in result['media_evaluation_registry']:
        require(row['node_id'] in sets['nodes'],'dangling media registry node')
        require(row['entity_kind'] in media_evaluation.KINDS,'invalid media entity kind')
        require(row['execution_status']=='never-run' and not row['results_preview']['scores'],'unsupported media execution/score claim')
        refs(row,'media registry')
    for node in result['nodes']:
        life=node.get('lifecycle','unknown')
        if isinstance(life,dict):
            refs(life,'lifecycle')
            require(life.get('status') in {'current','superseded','deprecated','historical','unknown','current_documentation_reviewed','superseded_per_maintainer','historical_pinned_specification','reference_concept_or_dataset'},'invalid lifecycle')
            replacements=life.get('replacement_node_ids',[])
        else:
            require(life in {'current','superseded','deprecated','historical','unknown'},'invalid lifecycle')
            replacements=node.get('replaced_by',[])
        for rid in replacements: require(rid in sets['nodes'],'missing replacement')
    snapshot_ids=set()
    for snap in result['evaluation_snapshots']:
        require(snap.get('id') and snap['id'] not in snapshot_ids,'duplicate/missing evaluation snapshot ID')
        snapshot_ids.add(snap['id'])
        require(url_ok(snap.get('source_url')),'unsafe/missing evaluation source URL')
        require(date_ok(snap.get('checked_at'),'day'),'missing evaluation checked_at')
        require(date_ok(snap.get('report_date'),'day') if snap.get('report_date') is not None else bool(snap.get('report_date_note')),'evaluation report date requires date or unknown note')
        require(snap.get('evidence_locator'),'evaluation requires evidence locator')
        require(snap.get('model') and snap.get('benchmark') and snap.get('metric'),'evaluation requires model/benchmark/metric')
        require(isinstance(snap.get('value'),(int,float)) and not isinstance(snap.get('value'),bool) and math.isfinite(snap['value']),'evaluation requires finite numeric value')
        require(snap.get('unit'),'evaluation requires unit')
        if snap['unit'] in {'%','percent','percentage'}: require(0<=snap['value']<=100,'percentage score out of range')
        for key in ('model_version','benchmark_version'):
            require(snap.get(key) or snap.get(key+'_note'),'evaluation version requires value or unknown note')
        require('shot' in snap and (snap['shot'] is not None or snap.get('shot_note')),'evaluation requires shot or unknown note')
        require('harness' in snap,'evaluation requires harness or explicit null')
        require(snap.get('reported_by') and snap.get('verification_status'),'evaluation requires attribution and evidence status')
        require(snap.get('limitations_zh'),'evaluation requires limitations')
        if snap.get('node_id'): require(snap['node_id'] in sets['nodes'],'dangling evaluation node')
    result['coverage_gaps']=[('已收录 3 条历史自报成绩快照；不是独立复现或可比榜单，不生成排名。' if '尚未导入可比' in str(g) else g) for g in result['coverage_gaps']]
    result['coverage_gaps']=[('视频与音乐已初步纳入相关技术节点；更多独立系列、版本与教程仍待补充。3D、机器人和世界模型仍缺独立系列；不代表全领域覆盖。' if g=='视频、音乐、3D、机器人和世界模型仅有类别位置，缺独立系列' else g) for g in result['coverage_gaps']]
    result['coverage_gaps']=current_coverage_display(result['coverage_gaps'],sets['nodes'])
    # Derived view fields are separate; source records remain byte-equivalent in research/.
    org_edges={e['source']:e['target'] for e in result['edges'] if e['type'] in ('developed_by','introduced_by')}
    byid={n['id']:n for n in result['nodes']}
    result['view_nodes']=[]
    for n in result['nodes']:
        registry=next((r for r in result['dataset_benchmark_registry'] if r['node_id']==n['id']),{})
        lifecycle=n.get('lifecycle','unknown')
        raw_status=lifecycle.get('status','unknown') if isinstance(lifecycle,dict) else lifecycle
        status={'current_documentation_reviewed':'current','superseded_per_maintainer':'superseded','historical_pinned_specification':'historical','reference_concept_or_dataset':'unknown'}.get(raw_status,raw_status)
        org=n.get('organization') or n.get('vendor')
        oid=org_edges.get(n['id']) or org_edges.get(n.get('family_id'))
        if not org and oid: org=byid[oid]['title']
        result['view_nodes'].append({'id':n['id'],'lifecycle':status,'vendor':org if isinstance(org,str) else '未核验','availability':n.get('availability',registry.get('availability')) if isinstance(n.get('availability',registry.get('availability')),str) else '未核验','license':n.get('license',registry.get('license')) if isinstance(n.get('license',registry.get('license')),str) else '未核验'})
    paths=[('从语言到模型',['nlp','tokenization','embeddings','language-modeling','seq2seq','attention','transformer','pretraining','bert','gpt-3']),('从对齐到智能体',['instruction-tuning','rlhf','dpo','cot','reasoning-models','rag','agents','react']),('研究边界与阅读素养',['multimodal','clip','llava','latent-diffusion','rsi','godel-machine','stop','jev'])]
    result['learning_paths']=[{'title':t,'note':'编辑建议的学习顺序，不是历史因果关系。','node_ids':[i for i in ids if i in byid]} for t,ids in paths]
    for b in bundles:
        for p in b.get('tutorial_paths',[]):
            ids=p.get('node_ids',p.get('nodes',[]))
            require(all(i in sets['nodes'] for i in ids),'dangling tutorial path')
            result['learning_paths'].append({'title':p['title'],'note':p.get('acceptance','原创建议；未执行教程'),'node_ids':ids})
    return result

def book(data):
    lines=['# ModelAtlas · 大模型知识地图','', '> v0.2.2 · 代表性知识地图；不是全厂商、全版本目录。最后核验：'+data['checked_at']+'。来源核验不是独立复现实验。','', '## 阅读路径']
    for p in data['learning_paths']: lines += ['','### '+p['title'],p['note'],' → '.join(p['node_ids'])]
    for n in data['nodes']:
        lines+=['','## '+n['title'],'',n.get('description_zh',n.get('summary_zh','')),'','- ID / 类型：'+n['id']+' / '+n['type'],'- 生命周期：'+str(n.get('lifecycle','unknown')),'- 版本：'+str(n.get('version') or '未核验'),'- 核验：'+str(n.get('checked_at','未核验'))+' · '+str(n.get('verification_status','未核验'))]
        if 'tutorial_markdown' in n: lines += [n['tutorial_markdown']]
        if 'media_evaluation' in n: lines += media_evaluation.book(n['media_evaluation'])
        if 'office_agent' in n:
            w=n['office_agent']
            lines += ['### 办公系统 · 权限与未执行实践']
            for key in ('entity_type','platform_family_id','execution_status','proof_level','permission_boundary','confirmation_boundary','lifecycle_note','synthetic_input','expected_not_observed'):
                lines += ['- '+key+'：'+str(w[key])]
            for note in w['source_notes']: lines += ['- '+note]
        if 'world_model_learning' in n:
            w=n['world_model_learning']
            lines += ['- 语义子类：'+w['semantic_subtype'],'- 参数与口径：'+str(w['parameters']),'- '+w['diagram_note'],'![原创世界模型教学对照](world-model-learning.svg)']
        for x in n.get('agentwork_links',[]): lines+=['- 对应实践（编辑学习关系）：['+x['title']+']('+x['url']+')']
        for key in ['license','license_notes','cost','cost_notes','historical_context']:
            if key in n: lines+=['- '+key+'：'+str(n[key])]
        for step in n.get('steps_zh',[]): lines+=['- 学习步骤（未执行）：'+step]
        for row in data['dataset_benchmark_registry']:
            if row['node_id']==n['id']:
                if row.get('access_semantics'):
                    lines+=['### 评测介绍与官方入口']
                    for key in ('split','availability','access_application_note','metric','protocol','harness','contamination','reproducibility'):
                        lines+=['- '+key+'：'+str(row.get(key,'未核验'))]
                    for label,url in row['official_links'].items():
                        if url: lines+=['- ['+label+' · 官方入口]('+url+')']
                    lines+=['- '+row['display_policy'],'- 原始元数据：benchmarks/raw/records.json；访问修订：benchmarks/overlay.json。']
                else: lines+=['- 评测/数据集登记：'+json.dumps(row,ensure_ascii=False)]
        for pit in n.get('misconceptions',n.get('pitfalls',[])): lines+=['- 注意：'+pit]
        urls=list(n.get('source_urls',[]))
        for sid in n.get('source_ids',[]):
            source=next(s for s in data['sources'] if s['id']==sid)
            if source['url'] not in urls: urls.append(source['url'])
        for u in urls: lines+=['- 来源：'+u]
        for e in data['events']:
            if n['id'] in e['node_ids']: lines+=['- 事件：'+e['event_type']+' · '+str(e.get('date') or '未知 / 待核验')+' · '+e['title']+' · 精度 '+str(e.get('date_precision') or 'unknown')+' · 时区 '+str(e.get('timezone') or '未知')+' · 范围 '+str(e.get('availability_scope') or '未核验')+' · 版本 '+str(e.get('version') or '未核验')+' · 截至已可用（非首发） '+str(e.get('available_by') or '无独立观察')+' · 说明 '+str(e.get('note_zh') or '')+' · 证据 '+str(e.get('evidence_locator','见原始来源'))+' · 来源 '+', '.join(next(s['url'] for s in data['sources'] if s['id']==sid) for sid in e.get('source_ids',[]))]
        for e in data['events']:
            if e.get('media_timeline') and n['id'] in e['node_ids']: lines += media_timeline.book(e)
    lines+=['','## 历史报告成绩快照（非排行榜，非独立复现）']
    for snap in data.get('evaluation_snapshots',[]):
        lines+=['','### '+snap.get('title',snap['id'])]
        for key,value in snap.items(): lines+=['- '+key+'：'+('未知' if value is None else str(value))]
    lines+=['','## 关系索引（教学建议不代表历史因果）']
    for e in data['edges']: lines+=['- '+e['source']+' → '+e['type']+' → '+e['target']+' · '+str(e.get('verification_status',e.get('evidence_type','未核验')))+' · '+', '.join(e.get('source_ids',[]))]
    lines+=['','## 来源目录']
    for source in data['sources']: lines+=['- '+source['id']+' · '+source['url']+' · 核验 '+str(source.get('checked_at','未核验'))+' · '+str(source.get('evidence_scope',source.get('evidence_summary_zh',source.get('notes_zh','原始来源页面'))))]
    lines+=['','## 覆盖缺口']+[('- '+str(g)) for g in data['coverage_gaps']]
    return '\n'.join(line.rstrip() for line in lines)+'\n'+(vendor_catalog.book(data['vendor_catalog']) if 'vendor_catalog' in data else '')
def build():
    bundles=[json.loads(p.read_text()) for p in sorted((ROOT/'data/research').glob('*.json'))]
    _, _, course = mcp_learning.load(ROOT)
    bundles.append(course)
    _, creative_bundle = creative_workflows.load(ROOT)
    bundles.append(creative_bundle)
    bundles.append(benchmark_catalog.load(ROOT))
    bundles.append(world_models.load(ROOT))
    _, office_bundle = office_agents.load(ROOT)
    bundles.append(office_bundle)
    bundles.append(media_evaluation.load(ROOT))
    bundles.append(media_timeline.load(ROOT))
    data=normalize(bundles)
    data['vendor_catalog']=vendor_catalog.load(ROOT,data['nodes'])
    out=ROOT/'dist'; out.mkdir(exist_ok=True)
    for p in (ROOT/'web').iterdir():
        if p.is_file(): shutil.copy2(p,out/p.name)
    (out/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'BOOK.md').write_text(book(data)); shutil.copy2(ROOT/'BOOK.md',out/'BOOK.md')
    # Root BOOK.md uses the same relative image URL as the published book.
    shutil.copy2(ROOT/'web/world-model-learning.svg',ROOT/'world-model-learning.svg')
    shutil.copytree(ROOT/'data/research',out/'research',dirs_exist_ok=True)
    mcp_learning.publish(ROOT,out)
    creative_workflows.publish(ROOT,out)
    vendor_catalog.publish(ROOT,out)
    benchmark_catalog.publish(ROOT,out)
    world_models.publish(ROOT,out)
    office_agents.publish(ROOT,out)
    media_evaluation.publish(ROOT,out)
    media_timeline.publish(ROOT,out)
    (out/'.nojekyll').touch()
    asset_versions.pin(out)
    shutil.copytree(out,ROOT/'docs',dirs_exist_ok=True)
    print(json.dumps({'nodes':len(data['nodes']),'edges':len(data['edges']),'sources':len(data['sources']),'events':len(data['events']),'output':str(out)},ensure_ascii=False))
    return data
if __name__=='__main__': build()
