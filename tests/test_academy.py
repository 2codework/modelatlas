"""P0 static reading, compatibility and downloadable lab contracts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import unittest, zipfile, tempfile, subprocess
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.hrefs=[];self.articles=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.hrefs.append(a.get('href',''))
  if tag=='article':self.articles.append(a.get('id'))
class Academy(unittest.TestCase):
 def test_reading_path_static_fallback_and_navigation(self):
  for name in ['index.html','academy.html','academy-en.html']:
   html=(ROOT/'dist'/name).read_text(); page=Page(html)
   for ident in ['academy-progress-summary','academy-progress-next','academy-progress-list']:
    self.assertIn(ident,page.ids)
   self.assertEqual(html.count('data-progress-id='),8)
   self.assertIn('class="academy-reading-status" role="status"',html)
   self.assertIn('Device reading marks have not been loaded.' if name=='academy-en.html' else '尚未读取本机的阅读标记。',html)
   self.assertNotIn('0 / 8',html)

 def test_timeline_catalog_does_not_claim_complete_history(self):
  zh=(ROOT/'dist/academy.html').read_text()
  self.assertIn('已收录的厂商/具体版本历史记录仍由原目录承载',zh)
  self.assertNotIn('完整厂商/具体版本的历史记录',zh)

 def test_equivalent_canonical_chapters_and_no_duplicate_ids(self):
  pages=[Page((ROOT/'dist'/n).read_text()) for n in ['academy.html','academy-en.html']]
  self.assertEqual(pages[0].articles,pages[1].articles)
  self.assertEqual(len(pages[0].articles),8)
  for p in pages:self.assertEqual(len(p.ids),len(set(p.ids)))
 def test_all_local_links_resolve(self):
  for name in ['academy.html','academy-en.html']:
   page=Page((ROOT/'dist'/name).read_text())
   for href in page.hrefs:
    u=urlsplit(href)
    if u.scheme or u.netloc:continue
    dest=ROOT/'dist'/(u.path or name)
    self.assertTrue(dest.is_file(),str(dest))
    if u.fragment and dest.suffix=='.html':self.assertIn(u.fragment,Page(dest.read_text()).ids,href)
 def test_reading_needs_no_fetch(self):
  js=(ROOT/'web/academy.js').read_text()
  self.assertNotIn('fetch(',js);self.assertNotIn('innerHTML',js)
  for name in ['academy.html','academy-en.html']:
   html=(ROOT/'dist'/name).read_text()
   self.assertGreaterEqual(html.count('<p>'),45)
   self.assertIn('softmax(QKᵀ / √dₖ)V',html)
   self.assertIn('qa-agent-lab.zip',html)
   self.assertIn('python learning/qa-agent/demo.py',html)
   self.assertIn('2022-10-06',html)
   self.assertNotIn('next_action',html)
   self.assertIn('adapter.plan(question)',html)
   self.assertIn('adapter.compose(fresh_claims(evidence))',html)
   self.assertIn('BEFORE document access',html)
   self.assertIn('BEFORE answer release',html)
 def test_independent_region_and_non_destructive_progress(self):
  js=(ROOT/'web/academy.js').read_text()
  self.assertIn('modelatlas.academy.region',js)
  self.assertIn('modelatlas.academy.read.v1',js)
  self.assertNotIn("setItem('modelatlas.progress'",js)
  for forbidden in ['geolocation','navigator.language','ipapi','fetch(']:self.assertNotIn(forbidden,js)
 def test_legacy_hooks_retained(self):
  html=(ROOT/'web/index.html').read_text();p=Page(html)
  for ident in ['detail','results','catalog-detail','catalog-results','query','academy-home']:self.assertIn(ident,p.ids)
  self.assertEqual(len(p.ids),len(set(p.ids)))
  self.assertIn('portal-home',(ROOT/'web/entry.js').read_text())
 def test_zip_is_self_contained_and_passes(self):
  with tempfile.TemporaryDirectory() as directory:
   with zipfile.ZipFile(ROOT/'dist/qa-agent-lab.zip') as z:z.extractall(directory)
   result=subprocess.run(['python','-m','unittest','discover','-s','tests','-v'],cwd=directory,capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   self.assertIn('Ran 33 tests',result.stderr)
if __name__=='__main__':unittest.main()
