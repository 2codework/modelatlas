"""Lossless, hash-gated catalog adapter; never changes historical graph entities."""
import copy, hashlib, json, re, datetime, shutil
from urllib.parse import urlsplit

def require(ok,msg):
    if not ok: raise ValueError(msg)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def day(v):
    try: return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',v)) and bool(datetime.date.fromisoformat(v))
    except (TypeError,ValueError): return False
def safe(u):
    try:
        p=urlsplit(u);return p.scheme=='https' and bool(p.hostname) and not p.username and not p.password and not any(c.isspace() for c in u)
    except (TypeError,ValueError): return False

def load(root,nodes):
    directory=root/'data/vendor-catalog'; manifest=json.loads((directory/'admission.json').read_text())
    records=[];bundles=[];ids=set();identities=set();existing={n['id'] for n in nodes}
    for entry in manifest['accepted']:
        p=directory/entry['file'];require(digest(p)==entry['sha256'],'catalog hash mismatch')
        require(entry['disposition'] in {'approve_with_limits','accept_with_caveats'},'catalog not approved')
        b=json.loads(p.read_text())
        if entry.get('decision_file'):
            dp=directory/entry['decision_file'];require(digest(dp)==entry['decision_sha256'],'QA decision hash mismatch')
            decision=json.loads(dp.read_text());require(decision['rechecked_input_sha256']==entry['sha256'],'QA input hash mismatch')
            require(all(x['disposition']=='accept_with_caveats' for x in decision['records']),'unapproved QA record')
            require({x['exactid'] for x in decision['records']}=={x['exactid'] for x in b['records']},'QA identity mismatch')
        bundles.append({'file':entry['file'],'sha256':entry['sha256'],'disposition':entry['disposition'],'raw':b})
        source_ids={s['id'] for s in b['sources']}
        require(len(source_ids)==len(b['sources']),'duplicate catalog source')
        for s in b['sources']:
            require(safe(s['url']),'unsafe catalog source')
            require(day(s.get('sourcecheckdate',s.get('checked_at'))),'invalid catalog source checked date')
        for raw in b['records']:
            r=copy.deepcopy(raw);exact=r.get('exact_id',r.get('exactid'));kind=r['entity_type'];vendor=r['vendor']
            rid=r.get('id') or 'asia-'+hashlib.sha256((vendor+'|'+kind+'|'+exact).encode()).hexdigest()[:16]
            require(rid not in ids and rid not in existing,'duplicate catalog id');ids.add(rid)
            identity=(vendor,kind,exact if exact is not None else r.get('title'));require(identity not in identities,'duplicate catalog identity');identities.add(identity)
            checked=r.get('source_checked_date',r.get('sourcecheckdate'));require(day(checked),'invalid catalog checked date')
            require(all(s in source_ids for s in r['source_ids']),'dangling catalog source')
            dates=r.get('release_dates',{'release_date':r.get('release_date')})
            for value in dates.values():require(value is None or day(value),'invalid catalog release date')
            require(not any(dates.values()) or r.get('release_date_evidence') or r.get('date_evidenceURL'),'catalog date without evidence')
            modality=r.get('modality');inputs=modality.get('input',[]) if isinstance(modality,dict) else r.get('input_modalities',[]);outputs=modality.get('output',[]) if isinstance(modality,dict) else r.get('output_modalities',[])
            life=r['lifecycle'];status=life.get('status',life.get('access_status','unknown'))
            urls={}
            for name,keys in {'model_card':['model_card_url','modelcardURL'],'report':['report_url','paperURL'],'tutorial':['tutorial_url','tutorialURL'],'weights_license':['weights_license_url','official_licenseURL'],'repository':['repositoryURL']}.items():
                u=next((r[k] for k in keys if r.get(k)),None);require(u is None or safe(u),'unsafe catalog URL');urls[name]=u
            links=[];unresolved=[]
            suggestions=r.get('dedup_suggestions',[{'existing_id':i,'relation':'editorial_related','action':r.get('dedup_recommendation')} for i in r.get('existingIDs',[])])
            for s in suggestions:
                if s['existing_id'] in existing:links.append({'target':s['existing_id'],'type':s['relation'],'verification_status':'editorial_learning_relation','note':s.get('action')})
                else:unresolved.append(s)
            sources=[copy.deepcopy(s) for s in b['sources'] if s['id'] in r['source_ids']]
            for source in sources:
                if source['id'] in {'kimi-base-card-qa','kimi-instruct-card-qa'}:
                    source['checked_at']='2026-10-28T19:46Z';source['time_precision']='minute (raw seconds are placeholder)' 
            records.append({'id':rid,'type':'catalog_record','title':r.get('title',exact),'exact_id':exact,'entity_type':kind,'provider':vendor,'family':r.get('family'),'version':r.get('version'),'inputs':inputs,'outputs':outputs,'modality':modality,'lifecycle':life,'status':status,'access':r.get('access'),'weights_license':r.get('weights_license',r.get('official_license')),'code_license':r.get('code_license',r.get('repository_code_license')),'license_scope_note':'权重许可不继承代码许可；open weights 不等于 open source；null 表示未核验。','dates':dates,'checked_at':checked,'qa_disposition':entry['disposition'],'limitations':{k:copy.deepcopy(r[k]) for k in ('notes_zh','legal_terms_status','license_url_status','paper_scope','paper_status','correction_history','field_evidence','resolved_snapshot','tutorial_status') if k in r},'access_observations':[{**obs,'checked_at':obs['checked_at'][:16]+'Z','time_precision':'minute (QA observation, not measured seconds)'} if obs.get('observer')=='independent_audit_asia_catalog_facts' else copy.deepcopy(obs) for obs in r.get('access_observations',[])],'summary':r.get('summary_zh',r.get('notes_zh','')),'urls':urls,'sources':sources,'links':links,'unresolved_links':unresolved,'relations':r.get('relations',[]),'source_bundle':entry['file'],'raw':r})
    # Resolve only exact, same-provider targets. Unresolved external identifiers remain text, not graph nodes.
    for r in records:
        for rel in r['relations']:
            matches=[x for x in records if x['provider']==r['provider'] and x['exact_id']==rel.get('target_exact_id')]
            if len(matches)==1:r['links'].append({'target':matches[0]['id'],'type':rel['type'],'verification_status':'source_documented_relation','note':rel})
            else:r['unresolved_links'].append(rel)
    return {'schema_version':'modelatlas.vendor-catalog.v1','records':records,'bundles':bundles,'admission':manifest,'count_label':'目录记录（不是新增模型数量）','ranking_policy':'不生成价格或性能排名；来源自报不可直接横比；教程链接未执行。'}

def book(catalog):
    lines=['','## 厂商目录记录（非全量历史，非新增模型计数）',catalog['ranking_policy'],'null 表示未知 / 本轮未核验，不表示不存在。原始来源与修订记录逐字段保留。']
    for r in catalog['records']:
        lines += ['','### '+r['title'],'- 深链接：?catalog='+r['id']]
        for k,v in r.items():lines += ['- '+k+'：'+json.dumps(v,ensure_ascii=False)]
    lines+=['','### 目录来源、覆盖、修订与接纳边界',json.dumps({'bundles':catalog['bundles'],'admission':catalog['admission']},ensure_ascii=False,indent=2)]
    return '\n'.join(lines)+'\n'
def publish(root,out):shutil.copytree(root/'data/vendor-catalog',out/'vendor-catalog',dirs_exist_ok=True)
