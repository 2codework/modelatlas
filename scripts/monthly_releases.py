"""Read-only event projection. No date or openness inference from URLs."""
import json,re,datetime
VISIBLE_HISTORY_ZH={'meta-llama-3-2024-04-18': ('Meta Llama 3 首批 8B / 70B', '采用自定义许可，不自动认定为开源 AI；仅含首批 8B、70B 基础与指令版本，不含 3.1 及后续版本。'), 'qwen2-2024-06-07': ('Qwen2 首批语言模型', '官方博客区分不同尺寸的许可，72B 不适用其他尺寸的 Apache 许可；不含 Qwen2-VL 与音频模型。许可文件的历史日期不是模型发布日期。'), 'deepseek-v3-2024-12-26': ('DeepSeek-V3 初始 Base / Chat', '仅含初始 V3 的 Base 与 Chat 权重，不含 V3-0324、V3.1、V3.2；权重开放声明不构成开源 AI 认证，首次文件上传时间未核实。'), 'deepseek-r1-2025-01-20': ('DeepSeek-R1 初始推理模型', '仅含初始 DeepSeek-R1，不含 R1-0528、R1-Zero 或蒸馏版本；蒸馏模型需另查上游许可，不能沿用本记录。'), 'qwen3-2025-04-29': ('Qwen3 首批后训练语言模型', '仅含官方公告列出的八个后训练版本与对应 Apache 2.0 许可；不含单独 Base 检查点、Qwen3-2507、Coder、VL 及后续版本。'), 'gpt-oss-2025-08-05': ('gpt-oss 首批两款推理模型', '仅含文本推理模型，不含 gpt-oss-safeguard。型号数字不是精确参数量；本次未下载权重或调用模型。')}
MODEL_TYPES={'model','model_release','model_family','research_system','model_service'}
KINDS={'announcement':'announcement','paper_submission':'paper','paper_publication':'paper','paper_revision':'paper_revision','report_publication':'report','weights_release':'weights','api_launch':'api'}

def event_month(date,precision,checked_at=None):
    if not isinstance(date,str) or precision not in ('day','month'):return None
    try:
        if precision=='day':
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date):return None
            parsed=datetime.date.fromisoformat(date)
        else:
            if not re.fullmatch(r'\d{4}-\d{2}',date):return None
            parsed=datetime.date.fromisoformat(date+'-01')
        if checked_at and parsed>datetime.date.fromisoformat(checked_at[:10]):return None
        return date[:7]
    except (ValueError,TypeError):return None

def project(data):
    nodes={n['id']:n for n in data['nodes']};sources={s['id']:s for s in data['sources']};rows=[]
    for e in data['events']:
        related=[nodes[i] for i in e.get('node_ids',[]) if i in nodes and nodes[i].get('type') in MODEL_TYPES]
        if not related:continue
        special=e.get('research_event_kind');kind=KINDS.get(e['event_type'])
        if special=='weights_release_announcement':kind='weights_announcement'
        elif special=='repo_first_public':kind='code'
        elif special=='weights_available_by':kind='weights_available_by'
        if not kind:continue
        date=e.get('date');precision=e.get('date_precision');month=event_month(date,precision,e.get('checked_at'))
        urls=list(dict.fromkeys(e.get('source_urls',[])+[sources[i]['url'] for i in e.get('source_ids',[]) if i in sources and sources[i].get('url')]))
        rows.append({'id':e['id'],'title':e.get('title') or '；'.join(n['title'] for n in related),'kind':kind,'date':date,'precision':precision,'month':month,'providers':sorted({str(n['organization']) for n in related if n.get('organization')}) or ['未登记'],'modalities':sorted({m for n in related for m in (n.get('modalities') or n.get('input_modalities') or [])+(n.get('output_modalities') or []) if isinstance(m,str)}) or ['未登记'],'nodes':[{'id':n['id'],'title':n['title']} for n in related],'version':e.get('version') or '；'.join(str(n['version']) for n in related if n.get('version')) or '未登记','sources':urls,'checked_at':e.get('checked_at'),'note':e.get('note_zh'),'summary':e.get('evidence_summary_zh'),'license':[{'node':n['id'],'record':n['license']} for n in related if n.get('license')],'raw':e})
    for r in data.get('vendor_catalog',{}).get('records',[]):
        date=r.get('dates',{}).get('weights_released')
        if not isinstance(date,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date):continue
        rows.append({'id':'catalog-weights-'+r['id'],'title':r['title']+' · 权重开放登记','kind':'weights','date':date,'precision':'day','month':event_month(date,'day',r.get('checked_at')),'providers':[r.get('provider') or '未登记'],'modalities':sorted(set((r.get('inputs') or [])+(r.get('outputs') or []))) or ['未登记'],'nodes':[{'id':r['id'],'title':r['title'],'catalog':True}],'version':r.get('version') or r.get('exact_id') or '未登记','sources':list(dict.fromkeys(s['url'] for s in r.get('sources',[]) if s.get('url'))),'checked_at':r.get('checked_at'),'note':r.get('license_scope_note'),'summary':r.get('summary') or '日期来自目录明确的 weights_released 字段；不据论文日期或通用发布日期推算。','license':[{'weights':r.get('weights_license'),'code':r.get('code_license')}],'raw':r})
    return {'schema_version':'modelatlas.monthly-projection.v1','scope':'既有模型事件与官方来源补录；非全球完整目录，非实时更新。','records':rows}
def publish(data,out):
    from pathlib import Path
    from validate_monthly_curated import validate
    result=project(data)
    for path in sorted((Path(__file__).resolve().parents[1]/'curated/monthly').glob('*.json')):
        package=json.loads(path.read_text())
        validate(package)
        result['records'].extend(curated_rows(package))
    import historical_events
    result['records'].extend(historical_events.collect(Path(__file__).resolve().parents[1]/'curated/historical-events', {r['id'] for r in result['records']}))
    assert len(result['records'])==len({r['id'] for r in result['records']}), 'duplicate monthly ID'
    (out/'monthly-releases.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')

def curated_rows(package):
    """Adapter for separately reviewed research; caller controls admission."""
    rows=[]
    for r in package.get('events',package.get('records',[])):
        date=r.get('weights_release_date')
        if date is not None:
            assert event_month(date,'day'), 'invalid curated weight date'
            assert any('weights_release_date' in s.get('supports',[]) for s in r.get('evidence',[])), 'weight date needs explicit evidence'
        override=VISIBLE_HISTORY_ZH.get(r['id'])
        notes=[override[1]] if override else r.get('notes',[])
        if isinstance(notes,str):notes=[notes]
        date_note=('官方声明可取得权重的日期；不等于各文件首次上传时间。' if date else '已找到权重入口，但权重开放日期未核实，不据公告日期或文件更新时间补填。')
        if date and r.get('event_precision',{}).get('weights')=='day_official_family_release_statement':date_note='日期依据官方家族开放声明，不是各检查点首次上传时间。'
        note=date_note+'开放权重不自动构成开源认证。'+''.join(n for n in notes if isinstance(n,str))
        title=override[0] if override else (r.get('name') or r['model_name']);mods=r.get('modality',r.get('modalities',{}));licenses=r.get('licenses') or ([r['license']] if r.get('license') else [])
        rows.append({'id':'curated-'+r['id'],'title':title,'kind':'weights_announcement' if date else 'weights_undated','date':date,'precision':'day' if date else None,'month':event_month(date,'day',r.get('verified_on') or package.get('verified_on') or package.get('as_of')),'providers':[r.get('vendor') or r.get('provider') or '未登记'],'modalities':sorted(set(mods.get('input',[])+mods.get('output',[]))) or ['未登记'],'nodes':[],'version':'；'.join(r.get('included_models',[])) or title,'sources':list(dict.fromkeys(s['url'] for s in r.get('evidence',[]) if s.get('url'))),'checked_at':r.get('verified_on') or package.get('verified_on') or package.get('as_of'),'note':note,'summary':'家族发布记录：包含多个已列明版本，不作为单个精确模型计数。' if r.get('event_granularity')=='family_release' else '精确版本的开放记录；不外推同家族其他版本。','license':[],'weight_entries':r.get('weight_entries') or ([r['official_weights_url']] if r.get('official_weights_url') else []),'included_models':r.get('included_models') or [title],'curated_licenses':licenses,'date_details':{'announcement':r.get('announcement_date'),'paper':r.get('paper_date'),'code':r.get('code_release_date'),'first_upload':r.get('first_upload_timestamp')},'raw':r})
    return rows
