from pathlib import Path
import json,hashlib,collections,re
O=Path(__file__).resolve().parent;W=O.parent
P=W/'media-eval-research-r1/media-eval-research-r1.json';C=W/'github-migration-r1/public/modelatlas/docs/data.json';Q=W/'media-eval-integration-r1/modelatlas/docs/data.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs={str(p.relative_to(W)):sha(p) for p in [P,C,Q]};raw=json.loads(P.read_text());canonical=json.loads(C.read_text());checks=raw['source_checks'];groups={}
for r in raw['records']:groups.setdefault(r['official_links']['paper'],[]).append(r)
E=[]
def add(id,title,kind,date,url,nodes,locator,raw_fields,note,version=None,occurrence=None):
 matches=[i for i,s in enumerate(checks) if s['url']==url and s['status']=='public_metadata_read'];assert matches,(id,url)
 E.append(dict(id=id,title=title,event_type=kind,date=date,date_precision='day',timezone=None,timezone_note_zh='此提案只沿用已审核日期字段；原始记录未保留统一时区，故置未知，不补猜UTC或当地时间。',node_ids=nodes,version=version,source_urls=[url],source_check_refs=[{'input':'media-eval-research-r1.json','json_pointer':'/source_checks/'+str(i),'checked_at':checks[i]['checked_at'],'status':checks[i]['status']} for i in matches],evidence_locator=locator,raw_date_fields=raw_fields,verification_status='source_reviewed_metadata_only_not_replicated',execution_status='never-run',occurrence_semantics=occurrence or kind,note_zh=note,merge_status='proposal_only_not_applied'))
for url,rows in groups.items():
 aid=url.rsplit('/',1)[-1];dates={r['dates']['paper_first_arxiv'] for r in rows};assert len(dates)==1;d=dates.pop();nodes=[r['node_id'] for r in rows]
 fields=[{'node_id':r['node_id'],'field':'dates.paper_first_arxiv','value':d} for r in rows]
 add('media-paper-'+aid.replace('.','-')+'-v1',aid+' 论文首次提交','paper_submission',d,url,nodes,'arXiv abstract 页面标题上方 Submitted on；Submission history [v1]',fields,'只表示关联论文首发，不是模型、数据集、代码、权重或基准发布日期。若节点代表较新版本，原论文事件仅为学术来源背景。','arXiv:'+aid+'v1')
 updates={r['dates']['paper_last_revision'] for r in rows};assert len(updates)==1;u=updates.pop()
 if u and u!=d:
  add('media-paper-'+aid.replace('.','-')+'-revision-'+u,aid+' 论文末次已核验修订','paper_revision',u,url,nodes,'arXiv abstract 页面 last revised 与 Submission history 最后一条；仅所审核快照的末次修订',[{'node_id':r['node_id'],'field':'dates.paper_last_revision','value':u} for r in rows],'论文修订不是新基准发布；不声称覆盖所有中间修订，不从当前仓库变化推断日期。',None)
r=next(r for r in raw['records'] if r['node_id']=='bench-dpg-bench-original')
add('media-dpg-bench-release-2024-03-11','DPG-Bench 官方发布公告','benchmark_release',r['dates']['benchmark_release'],r['official_links']['repo'],[r['node_id']],'ELLA README → Changelog，2024.3.11 条目明确 Release DPG-Bench',[{'node_id':r['node_id'],'field':'dates.benchmark_release','value':r['dates']['benchmark_release']}],'日期来自基准发布条目；不是ELLA模型权重发布，也不是论文2024-03-08首发。')
r=next(r for r in raw['records'] if r['node_id']=='bench-mmau-v051525-test');assert '2026-01-30' in r['access_application_note']
add('media-mmau-test-platform-migration-announced-2026-01-30','MMAU test 评估入口迁移公告','platform_migration','2026-01-30',r['official_links']['repo'],[r['node_id']],'MMAU README → Announcement，30 Jan 2026；test evaluation moved from Eval.ai to HF Space',[{'node_id':r['node_id'],'field':'access_application_note','value':r['access_application_note']}],'这是日期明确的官方迁移公告；不声称独立观测实际切换时刻、服务可用性或获得提交权限。只关联9000条test，不关联mini。',None,'dated_platform_migration_announcement_not_observed_cutover')
E.sort(key=lambda e:(e['date'],e['id']))
unknown=[]
for r in raw['records']:
 for key in ['benchmark_release','repository_last_update']:
  if r['dates'][key] is None:unknown.append({'node_id':r['node_id'],'field':'dates.'+key,'date':None,'reason_zh':'源包为null；不从论文日期、版本名、核验日或仓库当前内容推断。'})
suppressed=[{'node_ids':[r['node_id'] for r in rows],'paper_url':url,'date':rows[0]['dates']['paper_first_arxiv'],'reason_zh':'首发与末次修订字段同日，不另建修订事件；不能由此断言当天没有修订。'} for url,rows in groups.items() if rows[0]['dates']['paper_first_arxiv']==rows[0]['dates']['paper_last_revision']]
sm={s['id']:s for s in canonical['sources']};papers=set(groups);collisions=[]
for e in canonical['events']:
 urls=e.get('source_urls',[])+[sm[s]['url'] for s in e.get('source_ids',[]) if s in sm]
 norm=[re.sub(r'v\d+$','',u.replace('/pdf/','/abs/').removesuffix('.pdf')) for u in urls]
 if any(u in papers for u in norm):collisions.append(e['id'])
assert not collisions
assert len(E)==17 and len({e['id'] for e in E})==17
assert {str(p.relative_to(W)):sha(p) for p in [P,C,Q]}==inputs
proposal={'schema_version':'media-eval-timeline-proposal-r1','prepared_at_utc_date':'2026-10-28','status':'read_only_proposal_not_applied','input_sha256':inputs,'evidence_mode':'offline extraction from already-reviewed public metadata; no web refetch','counts':dict(collections.Counter(e['event_type'] for e in E)),'events':E,'unknown_dates':unknown,'suppressed_duplicate_date_events':suppressed,'baseline_event_overlap_check':{'events_examined':len(canonical['events']),'matched_existing_paper_event_ids':collisions,'method':'compare source URLs after /pdf/ to /abs/ and arXiv version-suffix normalization; not global semantic deduplication'},'integration_requirements':['Await root approval and current navigation/media acceptance; no merge performed.','Add paper_revision and platform_migration as explicit schema/UI/filter labels if accepted; do not silently relabel as paper_submission or benchmark_release.','Recheck latest baseline for duplicate IDs, paper-source/date/event-type collisions and existing node associations.','Group shared-paper first submissions/revisions by canonical paper URL, date and event kind; MMAU test-mini/test share one original-paper event.','MMAU-v05.15.25 node IDs retain current version identity but 2024 paper event is original-paper background, not that later dataset release.','Keep platform announcement time separate from actual service cutover, and all timezone fields unknown.','Do not add events for nulls, checked_at, paper same-day duplicate revisions, version-string dates or repository current content.','If all 17 unique events later accepted against unchanged149 baseline, arithmetic total166 is provisional, not current count.'],'execution_status':'never-run','canonical_or_candidate_modified':False}
(O/'proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n')
lines=['# 媒体评测时间轴只读衔接提案','','仅从已审核本地研究JSON提取，不访问网页、不改候选或canonical。准备日2026-10-28不是事件日期。','','## 17个建议事件','','10个论文首次提交、5个末次已核验论文修订、1个DPG-Bench发布、1个MMAU test平台迁移公告。MMAU共享论文只建1事件关联2节点。所有精度为day，时区保留未知。','','| 日期 | 类型 | 论文/事件 | 关联节点 | 证据 |','|---|---|---|---|---|']
for e in E:lines.append('| '+e['date']+' | '+e['event_type']+' | '+e['title']+' | '+', '.join(e['node_ids'])+' | [一手来源]('+e['source_urls'][0]+')；'+e['evidence_locator']+' |')
lines+=['','## 合并前边界','']+['- '+x for x in proposal['integration_requirements']]+['','## 未知与不纳入','','- 所有未核验benchmark_release和repository_last_update保持null，逐项见JSON unknown_dates。','- 同一论文的首发/末次修订同日时不另造修订事件，5篇论文共6条记录如此。','- paper_revision/platform_migration不是当前统一时间轴已有枚举，后续必须显式扩展、测试再合并。','- MusicCaps只挂MusicLM论文首发，不把2023-01-26冒充数据集精确发布日。','- 平台迁移是公告日期，不是实测切换时间；不使用已读取入口的Running状态作为时间证据。','- 当前149事件的论文URL未发现重合；这是源URL规范化检查，不是完整语义去重。','- 已阻断/不可提取页面未重访；没有题目、答案、媒体、下载或真实评测。','','## 核验','','输入研究包、canonical data和候选data的SHA-256均保持不变。17个ID唯一；所有事件指向已审核source_checks条目。proposal.json保存逐事件原始字段、证据位置、精度、未知时区与node_ids。']
(O/'README.zh-CN.md').write_text('\n'.join(lines)+'\n')
(O/'validation.json').write_text(json.dumps({'events':17,'counts':proposal['counts'],'ids_unique':True,'input_hashes_unchanged':True,'source_check_references_valid':True,'all_precision_day':True,'all_timezones_unknown':True,'canonical_written':False,'candidate_written':False,'network_access':'none'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(proposal['counts']))
