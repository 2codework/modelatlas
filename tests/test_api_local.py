"""Static renderer/AST/mock checks only. Never import or execute reader request scripts."""
import ast,hashlib,importlib.util,json,re,shutil,sys,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import build_api_local as P
class ReaderHTML(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.tags=[];self.code={};self.current=None;self.text=[]
 def handle_starttag(self,t,a):
  a=dict(a);self.tags.append((t,a));self.ids.extend([a['id']]if'id'in a else[])
  if'href'in a:self.links.append(a['href'])
  if t=='pre':self.current=a.get('id');self.code[self.current]=''
 def handle_endtag(self,t):
  if t=='pre':self.current=None
 def handle_data(self,x):
  self.text.append(x)
  if self.current is not None:self.code[self.current]+=x
class OptionalPractice(unittest.TestCase):
 def temp(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);r=Path(t.name);shutil.copytree(ROOT/P.REL,r/P.REL);return r
 def test_frozen_public_subset_and_full_manifest_binding(self):
  raw,ledger,hashes=P.load(ROOT);self.assertEqual(set(raw),set(P.PUBLIC_RAW));self.assertEqual(len(ledger['sources']),20)
  self.assertEqual(P.sha((ROOT/P.REL/'SHA256SUMS').read_bytes()),P.MANIFEST_SHA)
  for name in raw:self.assertEqual(P.sha(raw[name]),hashes[name])
 def test_public_repo_omits_internal_package_material(self):
  for n in P.FULL_RAW_NAMES-set(P.PUBLIC_RAW):self.assertFalse((ROOT/P.REL/n).exists())
  projection=json.loads((ROOT/'web/practice/projection.json').read_text());self.assertEqual(set(projection['omitted_files']),P.FULL_RAW_NAMES-set(P.PUBLIC_RAW))
  for folder in ['learning/api-local','web/practice','dist/practice','docs/practice']:
   for p in (ROOT/folder).rglob('*'):
    if p.is_file():self.assertNotRegex(p.read_text(),r'/workspace/|/home/agent/|/tmp/')
 def test_pages_complete_copyable_downloads_and_source_anchors(self):
  raw,ledger,_=P.load(ROOT)
  for route,doc,script,title,scope,prefix,insert in P.ROUTES:
   html=(ROOT/'web'/('practice-'+route+'.html')).read_text();p=ReaderHTML();p.feed(html)
   self.assertEqual(p.code[route+'-full-script'],raw[script].decode())
   self.assertIn('practice/'+script,p.links);self.assertIn('practice/'+doc,p.links);self.assertEqual(len(p.ids),len(set(p.ids)))
   for href in p.links:
    if href.startswith('#'):self.assertIn(href[1:],p.ids)
   self.assertTrue(any(k.startswith(route+'-correction-')for k in p.code))
   for tag,a in p.tags:self.assertNotIn(tag,['input','form','iframe','object','embed'])
   self.assertIn("connect-src 'none'",html);self.assertIn('不接收密钥',html);self.assertIn('可选进阶',html)
   self.assertIn('learn.html#step-3',p.links)
   for name in P.PUBLIC_RAW:self.assertEqual((ROOT/'web/practice'/name).read_bytes(),raw[name])
 def test_original_fenced_code_exact(self):
  raw,_,_=P.load(ROOT)
  for route,doc,*_ in P.ROUTES:
   p=ReaderHTML();p.feed((ROOT/'web'/('practice-'+route+'.html')).read_text())
   original=re.findall(r'```(?:bash|json|text)\n(.*?)\n```',raw[doc].decode(),re.S)
   for code in original:self.assertIn(code,p.code.values())
 def test_api_reader_ast_and_pure_parser_mocks_no_client_import(self):
  tree=ast.parse((ROOT/P.REL/'first_request.py').read_text());payload=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='PAYLOAD'for t in n.targets)))
  self.assertEqual(payload['model'],'gpt-5.4-mini-2026-03-17');self.assertEqual(payload['max_output_tokens'],160);self.assertIs(payload['store'],False);self.assertNotIn('tools',payload)
  fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='text_parts');self.assertFalse(any(isinstance(n,(ast.Import,ast.ImportFrom))for n in ast.walk(fn)))
  calls=[n.func for n in ast.walk(fn)if isinstance(n,ast.Call)];self.assertTrue(all(isinstance(c,ast.Name)and c.id=='isinstance' or isinstance(c,ast.Attribute)and c.attr in ['get','append']for c in calls))
  scope={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'pure-author-mocks','exec'),scope);extract=scope['text_parts']
  self.assertEqual(extract({'output':[{'type':'reasoning'},{'type':'message','content':[{'type':'output_text','text':'AUTHOR MOCK'}]}]}),['AUTHOR MOCK'])
  for value in [None,[],{},'x',{'output':None},{'output':[3,None,{'type':'message','content':None}]},{'output':[{'type':'message','content':[{'type':'refusal'},3]}]}]:self.assertEqual(extract(value),[])
  src=(ROOT/P.REL/'first_request.py').read_text();self.assertIn("sys.argv[1:] != ['--send-once']",src);self.assertEqual(src.count('opener.open('),1);self.assertIn('NoRedirect()',src);self.assertIn('read(8192)',src)
 def test_local_reader_static_bounds_no_execution(self):
  s=(ROOT/P.REL/'local_request.sh').read_text();self.assertIn("curl --disable --noproxy '*'",s);self.assertIn('--max-time 120',s);self.assertNotIn('--retry',s);self.assertNotIn('--location',s);self.assertNotIn('OPENAI_API_KEY',s)
  payload=json.loads(re.search(r"-d '(.*?)'",s,re.S).group(1));self.assertEqual(payload['model'],'qwen3:0.6b');self.assertEqual(payload['keep_alive'],0);self.assertIs(payload['stream'],False)
  self.assertEqual(s.count('http://127.0.0.1:11434/api/chat'),1)
 def test_optional_links_do_not_change_core_order(self):
  html=(ROOT/'web/learn.html').read_text();body=re.search(r'<article id="step-3"[^>]*>(.*?)</article>',html,re.S).group(1)
  for kind in ['api','local']:self.assertRegex(body,r'<details class="route-option">.*?href="practice-'+kind+r'.html".*?</details>')
  self.assertIn('href="#step-2">工具已打开',body);self.assertIn('practice-api.html',(ROOT/'web/index.html').read_text())
 def test_version_scope_secondary_but_requirements_before_operations(self):
  for route in ['api','local']:
   html=(ROOT/'web'/('practice-'+route+'.html')).read_text();self.assertIn('<summary>适用版本、文档日期与核验范围</summary>',html)
   requirement='API 账户与额度'if route=='api'else'仅 macOS 14+'
   self.assertLess(html.index(requirement),html.index('class="code-card"'))
 def test_unsafe_links_dangling_sources_and_raw_html(self):
  _,ledger,_=P.load(ROOT);sources={s['id']:s for s in ledger['sources']}
  for s in ['[x](javascript:alert(1))','[x](https://evil.example)','[x](//evil.example)','[A99]']:
   with self.assertRaises(ValueError):P.inline(s,sources)
  out=P.inline('<img src=x onerror=alert(1)> `</code><script>x</script>`',sources);self.assertNotIn('<script>',out);self.assertNotIn('<img',out);self.assertIn('&lt;script&gt;',out)
 def test_changed_missing_extra_or_symlink_raw_rejected(self):
  for mode in ['change','missing','extra','symlink']:
   with self.subTest(mode=mode):
    r=self.temp();f=r/P.REL/'first_request.py'
    if mode=='change':f.write_text(f.read_text()+'\n# mutation')
    if mode=='missing':f.unlink()
    if mode=='extra':(r/P.REL/'extra.txt').write_text('x')
    if mode=='symlink':f.unlink();f.symlink_to(ROOT/P.REL/'first_request.py')
    with self.assertRaises(ValueError):P.preflight(r)
    self.assertFalse((r/'web').exists())
 def test_output_symlinks_and_unregistered_assets_rejected_without_write(self):
  for rel in ['web','dist/practice','docs/practice/first_request.py','web/practice-api.html']:
   with self.subTest(rel=rel):
    r=self.temp();sentinel=r/'outside';sentinel.write_text('unchanged');target=r/rel;target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(sentinel)
    with self.assertRaises(ValueError):P.preflight(r)
    self.assertEqual(sentinel.read_text(),'unchanged')
  for rel in ['web/practice-hidden.js','dist/practice/unknown.py']:
   r=self.temp();f=r/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('unchanged')
   with self.assertRaises(ValueError):P.preflight(r)
   self.assertEqual(f.read_text(),'unchanged')
 def test_root_build_preflights_before_first_write(self):
  from unittest.mock import patch
  import build
  r=self.temp();(r/'web').mkdir();(r/'web/practice-hidden.js').write_text('sentinel')
  with patch.object(build,'ROOT',r):
   with self.assertRaisesRegex(ValueError,'unregistered practice'):build.build()
  self.assertFalse((r/'dist').exists());self.assertEqual((r/'web/practice-hidden.js').read_text(),'sentinel')
 def test_render_is_deterministic_and_only_registered_outputs(self):
  r=self.temp();(r/'web').mkdir();[(r/'web'/n).write_bytes((ROOT/'web'/n).read_bytes())for n in ('practice.css','practice.js')];a=P.render(r);b=P.render(r);self.assertEqual(a,b)
  self.assertEqual(set(a),{'practice-api.html','practice-local.html'}|{'practice/'+n for n in P.PUBLIC})

 def test_missing_registered_static_asset_rejected(self):
  r=self.temp();(r/'web').mkdir()
  with self.assertRaisesRegex(ValueError,'missing registered static asset'):P.preflight(r)
  self.assertFalse((r/'web/practice-api.html').exists())
 def test_publish_rejects_download_or_mapping_drift_before_own_writes(self):
  for name in ['first_request.py','projection.json']:
   r=self.temp();(r/'web').mkdir();(r/'dist').mkdir()
   for n in ('practice.css','practice.js'):(r/'web'/n).write_bytes((ROOT/'web'/n).read_bytes())
   P.render(r);f=r/'web/practice'/name;f.write_bytes(f.read_bytes()+b' ')
   with self.assertRaises(ValueError):P.publish(r,r/'dist')
   self.assertEqual(list((r/'dist').iterdir()),[])
