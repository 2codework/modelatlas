"""Source-reviewed event adapter. Offline metadata only, no evaluation execution."""
import copy,hashlib,json,shutil
from collections import Counter
from urllib.parse import urlsplit
EXPECTED={'paper_submission':10,'paper_revision':5,'benchmark_release':1,'platform_migration':1}
def require(ok,message):
 if not ok:raise ValueError(message)
def adapt(proposal,qa):
 require(qa['decision']=='accept_proposal_evidence_with_integration_gate','media timeline QA decision')
 require(not qa['required_proposal_fixes'],'media timeline unresolved QA fixes')
 p=copy.deepcopy(proposal);events=p['events'];require(len(events)==17 and dict(Counter(e['event_type'] for e in events))==EXPECTED,'media timeline type cardinality')
 require(len({e['id'] for e in events})==17,'media timeline duplicate ID')
 approved={e['id']:e for e in qa['events']}
 for e in events:
  q=approved.get(e['id']);require(q and q['decision']=='accept','media timeline event not approved')
  require((q['date'],q['type'],q['node_ids'],q['evidence'])==(e['date'],e['event_type'],e['node_ids'],e['source_urls']),'media timeline QA fact mismatch')
  require(e['date_precision']=='day' and e['timezone'] is None,'media timeline precision/timezone upgrade')
  require(e['execution_status']=='never-run','media timeline execution claim')
  dates={r['checked_at'] for r in e['source_check_refs']};require(len(dates)==1,'media timeline inconsistent checked dates')
  e['checked_at']=dates.pop();e['media_timeline']=True
  e['merge_status']='integrated_isolated_candidate_not_published'
  if e['event_type']=='paper_revision':e['observation_scope_zh']='末次修订仅指截至来源核验快照（'+e['checked_at']+'）已观察到的末次版本，不代表完整修订历史。'
  elif e['event_type']=='platform_migration':e['observation_scope_zh']='官方迁移公告日期，不是独立观测实际服务切换时刻；仅关联test。'
  else:e['observation_scope_zh']=e['note_zh']
  for url in e['source_urls']:
   u=urlsplit(url);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'media timeline unsafe URL')
 return dict(schema_version='media-evaluation-timeline.adapted.r1',title='媒体评测时间轴 · 17条已审核事件',scope='论文首发、截至核验快照的论文修订、基准发布与平台迁移公告分列；时区未知。',nodes=[],edges=[],sources=[],events=events,raw_proposal=copy.deepcopy(proposal),raw_qa=copy.deepcopy(qa))
def load(root):
 p=root/'learning/media-evaluation-timeline/r1';seal=json.loads((p/'approved-hashes.json').read_text())
 for name,digest in seal.items():require(hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,'media timeline approved input changed: '+name)
 return adapt(json.loads((p/'proposal/proposal.json').read_text()),json.loads((p/'qa/audit.json').read_text()))
def publish(root,out):shutil.copytree(root/'learning/media-evaluation-timeline/r1',out/'media-evaluation-timeline/r1',dirs_exist_ok=True)
def book(event):
 return ['- 媒体时间轴核验日期（不是事件日期）：'+event['checked_at']+'；时区：未知。', '- 观察范围：'+event['observation_scope_zh'], '- 原始日期字段：'+json.dumps(event['raw_date_fields'],ensure_ascii=False),'- 原始来源：'+', '.join(event['source_urls']),'- 审核提案：[原始JSON](media-evaluation-timeline/r1/proposal/proposal.json)；[独立QA](media-evaluation-timeline/r1/qa/REPORT.md)。']
