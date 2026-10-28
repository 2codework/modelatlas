"""Offline metadata adapter; never executes models, datasets or evaluation harnesses."""
import copy,hashlib,json,shutil
from collections import Counter
from urllib.parse import urlsplit
KINDS={'benchmark':6,'metric':3,'harness':1,'dataset':1}
def require(ok,message):
 if not ok:raise ValueError(message)
def adapt(raw):
 r=copy.deepcopy(raw);rows=r['records'];require(len(rows)==11,'media cardinality')
 require(dict(Counter(x['entity_kind'] for x in rows))==KINDS,'media type cardinality')
 require(len({x['node_id'] for x in rows})==11,'media duplicate IDs')
 sources={};nodes=[]
 for x in rows:
  require(x['execution_status']=='never-run' and not x['results_preview']['scores'],'media execution/score claim')
  require(x['counts_as_dataset']==(x['entity_kind']=='dataset') and x['counts_as_benchmark']==(x['entity_kind']=='benchmark'),'media count conflation')
  require(x['record_kind']==x['entity_kind']+'_metadata','media kind mismatch')
  ids=[]
  for url in dict.fromkeys(x['source_urls']+[u for u in x['official_links'].values() if u]):
   u=urlsplit(url);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'media unsafe URL')
   sid='media-src-'+hashlib.sha256(url.encode()).hexdigest()[:16];ids.append(sid)
   sources[sid]=dict(id=sid,url=url,checked_at=x['checked_at'],publisher_type='primary_author',evidence_scope='公开论文、项目说明或官方入口；仅metadata，入口不代表下载/标签/运行已验证。')
  nodes.append(dict(id=x['node_id'],title=x['name'],type=x['entity_kind'],entity_kind=x['entity_kind'],category='media-evaluation',description_zh=x['description_zh'],version=x['version'],checked_at=x['checked_at'],verification_status='source_reviewed_not_replicated',execution_status='never-run',runtime_verified=False,is_model=False,source_ids=ids,availability=x['availability'],license='代码、数据与原始素材许可分别核验；详见媒体评测metadata。',lifecycle='unknown',misconceptions=[x['limitations_zh'],'11个知识实体不是11个数据集或11个benchmark；本实体为'+x['entity_kind']+'。'],media_evaluation=copy.deepcopy(x)))
 return dict(schema_version='media-evaluation.adapted.r1',checked_at=r['checked_at'],nodes=nodes,edges=[],events=[],sources=list(sources.values()),media_evaluation_registry=rows,raw_research=r,coverage_gaps=['媒体评测仅补充11个代表知识实体（6 benchmark、3 metric、1 harness、1 dataset）；不代表完整目录，不导入成绩或形成统一榜单。'])
def load(root):
 p=root/'learning/media-evaluation/r1';f=p/'raw/media-eval-research-r1.json';seal=json.loads((p/'approved-hashes.json').read_text())
 for name,digest in seal.items():require(hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,'media approved source changed: '+name)
 return adapt(json.loads(f.read_text()))
def publish(root,out):shutil.copytree(root/'learning/media-evaluation/r1',out/'media-evaluation/r1',dirs_exist_ok=True)
def book(row):
 lines=['### 媒体评测 · 类型化metadata（未运行）','- 统计边界：本批11知识实体＝6 benchmark＋3 metric＋1 harness＋1 dataset；不合并到既有数据集/基准registry。']
 for key in ('entity_kind','version','split','execution_status','metric','protocol','availability','limitations_zh','reproducibility','contamination','display_policy'):
  lines.append('- '+key+'：'+str(row.get(key) or '未核验'))
 for key in ('access_semantics','license_evidence','dates','dataset_sizes','harness_metadata'):
  lines+=['- '+key+'：'+json.dumps(row[key],ensure_ascii=False).replace('null','"未核验"')]
 for label,url in row['official_links'].items():
  if url:lines.append('- ['+label+' · 官方入口]('+url+')')
 lines+=['- 原始metadata及未知项：[研究JSON](media-evaluation/r1/raw/media-eval-research-r1.json)；[来源检查](media-evaluation/r1/raw/source-checks.json)。']
 return lines
