"""Source-bound optional readers. Static projection only; never import request programs.
Preflight covers this renderer's inputs/registered destinations before main build writes.
It is not a filesystem race defense or an atomic guarantee for the entire legacy build.
"""
import hashlib,json,re
from pathlib import Path
from html import escape as h
from urllib.parse import urlsplit
REL='learning/api-local/r1/raw'
MANIFEST_SHA='d97213641811aaa9dec82ccbef5bd1dc259a5fb5db5a24a3cb5837ab8ec061c8'
FULL_RAW_NAMES={'FIRST_API.zh-CN.md','FIRST_LOCAL.zh-CN.md','README.zh-CN.md','first_request.py','local_request.sh','integration-notes.json','source-ledger.json','secondary-source-ledger.json','validate.py','validation.json'}
PUBLIC_RAW=('FIRST_API.zh-CN.md','FIRST_LOCAL.zh-CN.md','first_request.py','local_request.sh','source-ledger.json')
RAW_NAMES=set(PUBLIC_RAW)
ASSETS={'practice-api.html','practice-local.html','practice.js','practice.css'}
PUBLIC=set(PUBLIC_RAW)|{'projection.json'}
ROUTES=(('api','FIRST_API.zh-CN.md','first_request.py','第一次 API 请求','API 账户与额度 · 可能收费 · macOS/Linux Bash + 已安装 Python 3.8+；Windows 不直接照抄','A','1．准备文件'),('local','FIRST_LOCAL.zh-CN.md','local_request.sh','第一次本地模型','仅 macOS 14+ · 需要安装与下载 · 先核对设备资源','L','3．给模型一次完整输入'))
def need(ok,msg):
 if not ok:raise ValueError('optional practice: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict_json(data):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
def no_symlinks(path,root):
 need(path.is_relative_to(root),'path outside repository')
 current=root
 need(not current.is_symlink(),'symlink repository root')
 for part in path.relative_to(root).parts:
  current=current/part;need(not current.is_symlink(),'symlink '+str(current.relative_to(root)))
def load(root):
 root=Path(root).absolute();p=root/REL;no_symlinks(p,root)
 need(p.is_dir(),'missing frozen guide package')
 names={x.name for x in p.iterdir()};need(names==RAW_NAMES|{'SHA256SUMS'},'closed raw file inventory')
 for x in p.iterdir():need(not x.is_symlink() and x.is_file(),'raw must be regular files')
 manifest=(p/'SHA256SUMS').read_bytes();need(sha(manifest)==MANIFEST_SHA,'admitted manifest SHA')
 expected={}
 for line in manifest.decode().splitlines():
  m=re.fullmatch(r'([a-f0-9]{64})  ([A-Za-z0-9_.-]+)',line);need(m is not None,'manifest format')
  digest,name=m.groups();need(name not in expected,'duplicate manifest entry');expected[name]=digest
 need(set(expected)==FULL_RAW_NAMES,'manifest registered names')
 raw={name:(p/name).read_bytes() for name in RAW_NAMES}
 for name in RAW_NAMES:need(sha(raw[name])==expected[name],'source hash '+name)
 ledger=strict_json(raw['source-ledger.json']);sources=ledger['sources'];ids=[x['id'] for x in sources]
 need(len(ids)==len(set(ids))==20,'source IDs/cardinality')
 need(set(ids)=={f'A{i}' for i in range(1,9)}|{f'L{i}' for i in range(1,11)}|{'R1','R2'},'closed source IDs')
 for s in sources:
  need(set(s)=={'id','url','kind','read_status','supports'},'source fields')
  u=urlsplit(s['url']);need(u.scheme=='https' and u.hostname and not u.username and not u.password and not re.search(r'\s',s['url']),'safe official URL')
  need(s['kind']=='official_primary' and s['read_status']=='readable','source reading scope')
 return raw,ledger,expected

def preflight(root):
 root=Path(root).absolute();load(root)
 for directory in ('web','dist','docs'):
  dest=root/directory;no_symlinks(dest,root)
  if dest.exists():
   need(dest.is_dir(),'output directory shape')
   # Legacy build copies and pins many outputs: reject preexisting symlinks in these trees.
   for x in dest.rglob('*'):need(not x.is_symlink(),'output symlink '+str(x.relative_to(root)))
   for x in dest.glob('practice*'):need(x.name in ASSETS|{'practice'},'unregistered practice asset '+x.name)
  for name in ASSETS:no_symlinks(dest/name,root);need(not (dest/name).exists() or (dest/name).is_file(),'asset must be regular')
  folder=dest/'practice';no_symlinks(folder,root)
  if folder.exists():
   need(folder.is_dir(),'practice directory shape')
   need({x.name for x in folder.iterdir()}<=PUBLIC,'unregistered download asset')
   for x in folder.iterdir():need(x.is_file() and not x.is_symlink(),'download must be regular file')
  for name in PUBLIC:no_symlinks(folder/name,root)
 for name in ('practice.css','practice.js'):need((root/'web'/name).is_file(),'missing registered static asset '+name)
 return True

def inline(text,sources):
 allowed={s['url'] for s in sources.values()};pattern=r'`[^`]+`|\[[^\]]+\]\([^)]+\)|\*\*.+?\*\*|\[(?:A|L)\d+(?:,(?:A|L)\d+)*\]';out=[];end=0
 for m in re.finditer(pattern,text):
  out.append(h(text[end:m.start()]));token=m.group()
  if token.startswith('`'):out.append('<code>'+h(token[1:-1])+'</code>')
  elif token.startswith('**'):out.append('<strong>'+inline(token[2:-2],sources)+'</strong>')
  elif '](' in token:
   label,url=token[1:-1].split('](',1);need(url in allowed,'unregistered external Markdown link '+url)
   out.append('<a href="'+h(url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+inline(label,sources)+'</a>')
  else:
   citations=token[1:-1].split(',');need(all(x in sources for x in citations),'dangling citation')
   out.append('['+', '.join('<a href="#source-'+x+'">'+x+'</a>'for x in citations)+']')
  end=m.end()
 out.append(h(text[end:]));result=''.join(out)
 return result

def plain_heading(text):
 # TOC anchors own navigation; never nest citation/external links inside them.
 text=re.sub(r'\[(?:A|L)\d+(?:,(?:A|L)\d+)*\]','',text)
 text=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',text)
 return text.replace('**','').replace('`','').strip()

def code_block(text,cid,label='复制代码'):
 return '<div class="code-card"><pre id="'+cid+'"><code>'+h(text)+'</code></pre><button type="button" data-copy="'+cid+'">'+label+'</button><p id="'+cid+'-status" role="status"></p></div>'
def markdown(text,sources,route,script_panel,insert_prefix):
 lines=text.splitlines();out=[];toc=[];i=0;seq=0;head=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('# '):i+=1;continue # accessible page title is supplied once
  if line.startswith('## '):
   head+=1;title=line[3:];ident='section-'+str(head);toc.append((ident,title));out.append('<h2 id="'+ident+'" tabindex="-1">'+inline(title,sources)+'</h2>')
   if title.startswith(insert_prefix):out.append(script_panel)
   i+=1;continue
  if line.startswith('```'):
   lang=line[3:].strip();need(lang in ('bash','json','text'),'registered fence language');buf=[];i+=1
   while i<len(lines)and not lines[i].startswith('```'):buf.append(lines[i]);i+=1
   need(i<len(lines),'unclosed code fence');seq+=1;out.append(code_block('\n'.join(buf),route+'-code-'+str(seq)));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines)and lines[i].startswith('|'):
    cells=[c.strip()for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',c)for c in cells):rows.append(cells)
    i+=1
   need(rows and all(len(row)==len(rows[0])for row in rows),'table column structure')
   out.append('<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+inline(c,sources)+'</th>'for c in rows[0])+'</tr></thead><tbody>')
   for row in rows[1:]:out.append('<tr>'+''.join('<td>'+inline(c,sources)+'</td>'for c in row)+'</tr>')
   out.append('</tbody></table></div>');continue
  ordered=bool(re.match(r'^\d+\. ',line));bullet=line.startswith('- ')
  if ordered or bullet:
   tag='ol'if ordered else'ul';out.append('<'+tag+'>')
   while i<len(lines)and(bool(re.match(r'^\d+\. ',lines[i]))if ordered else lines[i].startswith('- ')):
    out.append('<li>'+inline(re.sub(r'^(?:\d+\.|-) ','',lines[i]),sources)+'</li>');i+=1
   out.append('</'+tag+'>');continue
  if line.startswith('> '):
   seq+=1;out.append(code_block(line[2:],route+'-correction-'+str(seq),'复制纠错提示词'));i+=1;continue
  paragraph=[line];i+=1
  while i<len(lines)and lines[i].strip()and not re.match(r'^(?:#|```|\||>|- |\d+\. )',lines[i]):paragraph.append(lines[i]);i+=1
  rendered='<p>'+inline(' '.join(paragraph),sources)+'</p>'
  if line.startswith('**范围：**'):out.append('<details class="sources"><summary>适用版本、文档日期与核验范围</summary>'+rendered+'</details>')
  else:out.append(rendered)
 return ''.join(out),toc

def projection_record(hashes):
 return {'schema':'modelatlas.optional-practice-projection.v1','admitted_manifest_sha256':MANIFEST_SHA,'raw_archive':'learning/api-local/r1/raw','published_files_sha256':{n:hashes[n]for n in PUBLIC_RAW},'omitted_files':{n:'internal integration, QA or package-overview material; intentionally not published in repository or site; admitted package remains separately archived by publisher'for n in sorted(FULL_RAW_NAMES-set(PUBLIC_RAW))},'source_binding':{'practice-api.html':'FIRST_API.zh-CN.md','practice-local.html':'FIRST_LOCAL.zh-CN.md'},'runtime_execution':'never-run','scope':'closed static projection; no new graph nodes, events or license grant'}

def render(root):
 root=Path(root).absolute();preflight(root);raw,ledger,hashes=load(root);sources={s['id']:s for s in ledger['sources']};outputs={}
 for route,doc,script,title,scope,prefix,insert in ROUTES:
  panel='<div class="script-download"><a class="primary-action" href="practice/'+script+'" download="'+script+'">下载 '+script+'（仅文件，不自动执行）</a><details><summary>查看并复制完整脚本</summary>'+code_block(raw[script].decode(),route+'-full-script','复制完整脚本')+'</details></div>'
  route_sources={k:v for k,v in sources.items()if k.startswith(prefix)}
  body,toc=markdown(raw[doc].decode(),route_sources,route,panel,insert)
  nav=''.join('<a href="#'+ident+'">'+h(plain_heading(title))+'</a>'for ident,title in toc)
  evidence='<details id="practice-evidence" class="sources"><summary>原始教程、官方依据与核验范围</summary><p>以下核验日是文档读取日期，不是软件发布日期。页面和脚本未替你运行；参考答案为作者编写，不是服务返回。</p><a href="practice/'+doc+'">下载原始教程</a><ul>'
  for sid,s in sources.items():
   if sid.startswith(prefix):evidence+='<li id="source-'+sid+'"><a href="'+h(s['url'])+'" target="_blank" rel="noopener noreferrer">'+sid+' · '+h(s['url'])+'</a><p>'+h(s['supports'])+'</p></li>'
  evidence+='</ul><p>来源读取：'+h(ledger['access_date_utc'])+'。失败读取保持独立，不作为已读证据。</p><a href="practice/source-ledger.json">完整来源与失败记录</a> · <a href="practice/projection.json">公开投影范围</a></details>'
  html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>'''+h(title)+''' · ModelAtlas</title><link rel="stylesheet" href="learn.css"><link rel="stylesheet" href="practice.css"><script src="practice.js" defer></script></head><body><a class="skip" href="#practice-main">跳至正文</a><header><a class="brand" href="index.html">MODEL ATLAS</a><nav aria-label="主导航"><a href="learn.html#step-3">← 回到网页练习</a><a href="index.html?view=learn">进阶资料</a></nav></header><div class="learn-layout"><aside><details class="chapter-menu" open><summary>本页步骤 · 可选进阶</summary><nav aria-label="本页步骤">'''+nav+'''</nav></details><p class="side-note">不想安装或承担额外费用？<br><a href="learn.html#step-2">继续原来的网页练习</a></p></aside><main id="practice-main"><article><p class="eyebrow">可选进阶 · 不属于四步入门必做项</p><h1>'''+h(title)+'''</h1><div class="caution"><strong>'''+h(scope)+'''</strong><p>本页只展示教程和下载文件，不接收密钥、不发模型请求。API / 本地运行不是 MCP；这两条练习不需要 MCP、Skill 或外部办公权限。</p></div>'''+body+evidence+'''<nav class="lesson-next"><a class="primary-action" href="learn.html#step-3">回到网页练习 →</a><a href="'''+('practice-local.html'if route=='api'else'practice-api.html')+'''">查看另一条可选路线</a></nav></article><noscript>全文无需脚本即可阅读。复制按钮不可用时，直接选中文字复制；下载链接仍可用。</noscript><footer>原创教学示例；第三方软件、模型及服务各自适用其条款。没有运行或效果保证。</footer></main></div></body></html>'''
  outputs['practice-'+route+'.html']=html.encode()
 projection=projection_record(hashes)
 outputs.update({'practice/'+n:raw[n]for n in PUBLIC_RAW});outputs['practice/projection.json']=(json.dumps(projection,ensure_ascii=False,indent=2)+'\n').encode()
 # Construct and validate all new content before this renderer starts writing its destinations.
 for name,content in outputs.items():need(name in {'practice-api.html','practice-local.html'}|{'practice/'+n for n in PUBLIC},'closed publication output')
 for name,content in outputs.items():
  target=root/'web'/name;target.parent.mkdir(exist_ok=True);target.write_bytes(content)
 return outputs

def publish(root,out):
 root=Path(root).absolute();out=Path(out).absolute();need(out==root/'dist','registered output root');preflight(root)
 raw,_,hashes=load(root)
 payload={name:(root/'web/practice'/name).read_bytes()for name in PUBLIC}
 for name in PUBLIC_RAW:need(payload[name]==raw[name],'public download source drift '+name)
 expected=(json.dumps(projection_record(hashes),ensure_ascii=False,indent=2)+'\n').encode()
 need(payload['projection.json']==expected,'public projection drift')
 for name,content in sorted(payload.items()):
  target=out/'practice'/name;target.parent.mkdir(exist_ok=True);target.write_bytes(content)
