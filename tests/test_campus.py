"""Production D theme contracts; data and established interaction hooks are untouched."""
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit, parse_qs

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','foundations.html','learn.html','connections.html','practice-api.html','practice-local.html','creative-learning.html','realtime-audio.html']
class Page(HTMLParser):
 def __init__(self):super().__init__();self.body={};self.assets=[];self.ids=[];self.hrefs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='body':self.body=a
  if tag=='link' and a.get('rel')=='stylesheet':self.assets.append(a['href'])
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.hrefs.append(a.get('href',''))
class Campus(unittest.TestCase):
 def test_all_eight_real_page_families_use_same_versioned_theme(self):
  for name in PAGES:
   with self.subTest(page=name):
    page=Page();page.feed((ROOT/'dist'/name).read_text())
    self.assertIn('campus',page.body['class'].split());self.assertEqual(page.body['data-site'],'modelatlas')
    urls=[urlsplit(u) for u in page.assets if urlsplit(u).path=='campus.css']
    self.assertEqual(len(urls),1)
    self.assertEqual(parse_qs(urls[0].query),{'v':[hashlib.sha256((ROOT/'web/campus.css').read_bytes()).hexdigest()]})
    self.assertEqual(len(page.ids),len(set(page.ids)))
 def test_home_keeps_real_practice_and_research_routes(self):
  page=Page();html=(ROOT/'web/index.html').read_text();page.feed(html)
  for target in ['learn.html#step-1','learn.html#step-2','learn.html#step-3','learn.html#step-6','?view=explore','?view=vendor-catalog','?view=timeline','?view=evaluation','?view=learn','?view=coverage']:
   self.assertIn(target,page.hrefs)
  for target in ['query','catalog-query','event-query','evaluation-query','detail','catalog-detail','detail-toc','results','catalog-results']:
   self.assertIn(target,page.ids)
  self.assertIn('教学示例，不是真实模型输出',html)
  self.assertNotIn('示例路线',html)
 def test_original_art_is_local_and_accessible(self):
  html=(ROOT/'web/index.html').read_text()
  self.assertIn('src="campus-garden.svg" alt="',html)
  svg=(ROOT/'web/campus-garden.svg').read_text()
  self.assertIn('xmlns="http://www.w3.org/2000/svg"',svg)
  self.assertNotIn('<script',svg);self.assertNotIn('http://',svg.replace('http://www.w3.org/2000/svg',''))
 def test_no_theme_script_dependency_or_motion_requirement(self):
  css=(ROOT/'web/campus.css').read_text()
  self.assertIn('prefers-reduced-motion',css);self.assertIn('forced-colors',css);self.assertIn(':focus-visible',css)
  self.assertNotIn('url(http',css);self.assertNotIn('@import',css)
