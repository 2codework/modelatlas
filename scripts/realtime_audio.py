"""Finite, pinned post-graph additive admission. Metadata only; never execute raw files."""
import copy, hashlib, html, json, shutil
import knowledge_graph_links as graph
REL='learning/realtime-audio/r1'
ADMISSION_SHA='5de29a453d196dc5ccd47376248f8898e10e8694d43c8cca18d5a4038ce4b74f'
def need(ok,msg):
 if not ok:raise ValueError('realtime audio: '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def read(p):return json.loads(p.read_text(),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite')))
def load(root):
 p=root/REL;need(sha(p/'admission.json')==ADMISSION_SHA,'admission hash');a=read(p/'admission.json')
 files={str(f.relative_to(p)):sha(f) for f in (p/'raw').rglob('*') if f.is_file()}
 need(files==a['raw_files_sha256'],'raw inventory/hash');need(sha(p/'overlay.json')==a['overlay_sha256'],'overlay hash')
 need(sha(p/'raw/qa-r2/VALIDATION.json')==a['qa_validation_sha256'],'QA hash');qa=read(p/'raw/qa-r2/VALIDATION.json');need(qa['verdict']=='accept_scoped_research' and qa['open_fix_count']==0,'QA acceptance')
 need(sha(p/'raw/research-r2/raw-models.json')==a['research_sha256'],'research hash')
 return a,read(p/'overlay.json'),read(p/'raw/research-r2/raw-models.json')
def apply(data,root):
 a,o,raw=load(root)
 need(set(data)==set(a['base_object_sha256']),'baseline fields')
 for k,v in data.items():need(digest(v)==a['base_object_sha256'][k],'baseline drift '+k)
 for k in ('nodes','sources','events','view_nodes'):
  ids=[x['id'] for x in data[k]];new=[x['id'] for x in o[k]]
  need(len(ids)==len(set(ids)) and len(new)==len(set(new)),'duplicate ID '+k)
  need(new==a['expected_ids'][k] and not set(ids)&set(new),'addition IDs '+k)
  need({x['id']:digest(x) for x in o[k]}==a['expected_object_sha256'][k],'addition objects '+k)
 source_ids={s['id'] for s in data['sources']+o['sources']};node_ids={n['id'] for n in data['nodes']+o['nodes']}
 for n in o['nodes']:
  need(n['execution_status']=='never-run' and n['runtime_verified'] is False,'execution upgrade');need(set(n['source_ids'])<=source_ids,'node sources')
 for e in o['events']:
  need(set(e['source_ids'])<=source_ids and set(e['node_ids'])<=node_ids,'event refs')
  need(e['date'] is not None,'invented unknown date event')
  if e['event_type']=='scheduled_shutdown':need(e['status']=='planned' and '计划·尚未发生' in e['title'],'planned event semantics')
 need(a['new_edges']==[],'edges prohibited')
 for k in ('nodes','sources','events','view_nodes'):data[k].extend(copy.deepcopy(o[k]))
 for k,n in a['expected_counts'].items():need(len(data[k])==n,'count '+k)
 need([v['id'] for v in data['view_nodes']]==[n['id'] for n in data['nodes']],'view-node pairing')
 data['realtime_audio_registry']={'schema_version':'realtime-audio.registry.r1','admission_sha256':ADMISSION_SHA,'node_ids':a['expected_ids']['nodes'],'coverage_gaps':copy.deepcopy(raw['coverage_gaps']),'scope_zh':'四家四模型/家族有限样本；不是全球完整版本史。原knowledge_graph_links_application.after为r1接纳阶段统计，不是当前全图。','execution_status':'never-run','graph_statistics_current':graph.statistics(data)}
 return data

def readable(v):
 if v is None:return '未知（未证实，不补日期）'
 if isinstance(v,bool):return '是' if v else '否'
 if isinstance(v,(dict,list)):return json.dumps(v,ensure_ascii=False,indent=2)
 return str(v)
FIELDS=[('exact_version','精确版本（家族与checkpoint分开）'),('reviewed_variants','已核变体'),('date_scope_zh','日期作用域'),('inputs','输入模态'),('outputs','输出模态'),('streaming','流式与双向的条件'),('license','许可分层'),('runtime_zh','运行与硬件'),('official_deployment_configuration','官方配置（非实测最低）'),('account_cost_zh','账号与费用'),('latency_zh','延迟口径'),('latency_evidence','目标配置与端到端证据'),('version_records','精确版本、价格与生命周期表'),('current_2_1_release_date','2.1首发日期'),('weights_first_upload_date','权重首次上传日期'),('revision_sha','固定修订SHA'),('paper_date','独立论文日期'),('separate_entities','不能混同的服务与客户端')]
def markdown(data):
 lines=['# 实时语音模型 · 四个有限样本','', '只读来源研究 / never-run。模型、API、客户端分开；不是全球完整目录。',data['realtime_audio_registry']['scope_zh'],'当前全图统计：'+readable(data['realtime_audio_registry']['graph_statistics_current']),'']
 for n in data['nodes']:
  if 'realtime_audio' not in n:continue
  m=n['realtime_audio'];lines+=['## '+n['title'],n['description_zh'],'类型：'+n['type']+'；版本：'+n['version']]
  for k,label in FIELDS:
   if k in m:lines+=['### '+label,readable(m[k])]
  lines+=['### 日期证据（不以核验日期冒充发布）']
  for e in data['events']:
   if e.get('realtime_audio_event') and n['id'] in e['node_ids']:lines+=['- '+e['date']+' · '+e['title']+' · '+e['event_type']+' · '+e['note_zh']]
  lines+=['### 学习路径（未执行）','1. 先核模型/协议/产品边界与精确版本。','2. 阅读官方模型卡、论文与运行要求；保留未知与访问条件。','3. 仅设计经同意的合成音频测试；未获授权不下载、登录、收费或调用设备。','4. 如将来获批测试，分别记录目标delay、端到端P50/P95、硬件、并发、网络、版本和失败；不能拿官方自报代替实测。','### 官方学习入口']
  for sid in n['source_ids']:
   s=next(x for x in data['sources'] if x['id']==sid);lines+=['- '+s['url']+' · '+s['access_status']]
 lines+=['## 覆盖缺口',readable(data['realtime_audio_registry']['coverage_gaps'])]
 return '\n\n'.join(lines)+'\n'
def book(data):return ['','## 实时语音模型专题（有限样本，未执行）','完整可读版本表、输入输出、许可/硬件/费用与时间证据见 [实时语音学习页](realtime-audio.html) 和 [同源专题书稿](REALTIME_AUDIO.md)。','旧12边知识图接纳章节中的242节点/72孤点/108弱分量仅是r1接纳阶段统计；本批零新边，当前全图246节点/151边/76孤点/112弱分量。']
def publish(root,out,data):
 p=root/REL;shutil.copytree(p,out/'realtime-audio',dirs_exist_ok=True)
 text=markdown(data);(root/'REALTIME_AUDIO.md').write_text(text);(out/'REALTIME_AUDIO.md').write_text(text)
 esc=lambda x:html.escape(readable(x),quote=True)
 parts=['<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>实时语音模型 · ModelAtlas</title><link rel="stylesheet" href="style.css"><script src="topic.js" defer></script></head><body class="topic-page"><main><h1>实时语音模型 · 四个有限样本</h1><p><a href="index.html">返回知识地图</a> · <a href="REALTIME_AUDIO.md">专题书稿</a></p><p>来源审阅 / never-run；模型、API和客户端分开。不是全球完整目录。</p><p>'+esc(data['realtime_audio_registry']['scope_zh'])+'</p><nav aria-label="模型目录">']
 for n in data['nodes']:
  if 'realtime_audio' in n:parts+=['<a href="#'+esc(n['id'])+'">'+esc(n['title'])+'</a> ·']
 parts+=['</nav>']
 for n in data['nodes']:
  if 'realtime_audio' not in n:continue
  m=n['realtime_audio'];parts+=['<article id="'+esc(n['id'])+'"><h2>'+esc(n['title'])+'</h2><p>'+esc(n['description_zh'])+'</p><p>类型：'+esc(n['type'])+'；精确版本：'+esc(n['version'])+'</p><p><a href="index.html?node='+esc(n['id'])+'">模型详情与事件</a></p>']
  for k,label in FIELDS:
   if k in m:parts+=['<h3>'+label+'</h3><pre>'+esc(m[k])+'</pre>']
  parts+=['<h3>日期证据 · 公告/权重/论文不同事件</h3><ul>']
  for e in data['events']:
   if e.get('realtime_audio_event') and n['id'] in e['node_ids']:parts+=['<li><strong>'+esc(e['date']+' · '+e['title'])+'</strong><p>'+esc(e['availability_scope']+' '+e['note_zh'])+'</p></li>']
  parts+=['</ul><h3>官方入口及实际打开状态</h3><ul>']
  for sid in n['source_ids']:
   s=next(x for x in data['sources'] if x['id']==sid);parts+=['<li><a href="'+esc(s['url'])+'" rel="noopener noreferrer">'+esc(s['research_source_id'])+'</a> · '+esc(s['access_status'])+'</li>']
  parts+=['</ul><h3>未执行学习练习</h3><ol><li>将模型、传输协议、客户端分成三栏。</li><li>对比公告、论文、权重发布与未知上传日期。</li><li>设计经同意合成音频的测试表；未获批不调用模型、设备或收费服务。</li><li>若将来获批，固定修订/硬件，区分目标delay和端到端P50/P95，不复制作者成绩。</li></ol></article>']
 parts+=['<details class="topic-evidence"><summary>覆盖缺口、图统计与封存证据</summary><h2>覆盖缺口</h2><pre>'+esc(data['realtime_audio_registry']['coverage_gaps'])+'</pre><h2>图统计作用域</h2><p>r1接纳阶段是242节点/151边/72孤点/108弱分量；下列为当前全图，不代表覆盖完整。</p><pre>'+esc(data['realtime_audio_registry']['graph_statistics_current'])+'</pre><p>封存研究与独立QA：<a href="realtime-audio/admission.json">精确接纳清单</a> · <a href="realtime-audio/raw/research-r2/source-checks.json">打开/失败记录</a></p></details></main></body></html>']
 (out/'realtime-audio.html').write_text('\n'.join(parts))
