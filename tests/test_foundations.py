from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.hrefs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.hrefs.append(a.get('href',''))
class Foundations(unittest.TestCase):
 def test_accepted_source_exact_and_all_text_present(self):
  raw=(ROOT/'learning/foundations/r2/lessons.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),'8c8fe93cac66423d12bea51f03d1e110bd056a8e6f21be79d234cf1b7ada1053');data=json.loads(raw)
  text=unescape((ROOT/'dist/foundations.html').read_text());tags=Tags();tags.feed(text);self.assertEqual(len(tags.ids),len(set(tags.ids)))
  for l in data['lessons']:
   self.assertIn(l['id'],tags.ids);self.assertIn(l['title'],text)
   for value in l['sections'].values():self.assertIn(value,text)
   self.assertIn('index.html?node='+l['next_node_id'],tags.hrefs)
  for s in data['sources']:self.assertIn(s['url'],tags.hrefs);self.assertIn(s['claim'],text)
  self.assertNotIn('independent_draft_not_published',text)
  self.assertEqual((ROOT/'dist/foundations-source.json').read_bytes(),raw)
 def test_links_and_progress_boundary(self):
  text=(ROOT/'web/foundations.html').read_text();tags=Tags();tags.feed(text)
  for href in tags.hrefs:
   if href.startswith('#'):self.assertIn(href[1:],tags.ids)
  js=(ROOT/'web/foundations.js').read_text();self.assertNotIn('localStorage',js);self.assertNotIn('fetch(',js)
  self.assertIn('六课',text);self.assertIn('无真实模型或 Agent 执行',text)
