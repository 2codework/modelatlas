import hashlib, json, sys, unittest
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import audio_diagram
class Document(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.links=[];self.images=[];self.tags=[]
 def handle_data(self,data):self.text.append(data)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append(tag)
  if tag=='img':self.images.append(a)
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
class AudioDiagramTests(unittest.TestCase):
 def test_input_manifest_sources_and_equivalent(self):
  content,mapping=audio_diagram.load(ROOT)
  self.assertEqual(len(mapping['panels']),4)
  self.assertGreater(len(content['ordered_text']),25)
 def test_published_svg_and_mapped_assets(self):
  for directory in ['dist','docs']:
   for f in (ROOT/audio_diagram.REL).iterdir():
    self.assertEqual(f.read_bytes(),(ROOT/directory/'audio-diagram'/f.name).read_bytes())
 def test_static_html_equivalent_links_and_accessibility(self):
  s=(ROOT/'dist/realtime-audio.html').read_text();block=s.split('<section id="audio-learning-diagram"')[1].split('</section>')[0]
  d=Document();d.feed('<section '+block+'</section>')
  content,_=audio_diagram.load(ROOT)
  for line in content['ordered_text']:self.assertIn(line,d.text)
  self.assertNotIn('script',d.tags);self.assertNotIn('iframe',d.tags)
  self.assertEqual(d.images[0]['alt'],content['alt'])
  self.assertIn('details open',block);self.assertIn('font-size:1rem',block)
  for url in d.links:
   if not url.startswith('https://'):self.assertTrue((ROOT/'dist'/url).is_file(),url)
  self.assertEqual(s.count('<article id="speech-'),4)
 def test_no_published_temporary_artifacts(self):
  for p in (ROOT/'dist/audio-diagram').rglob('*'):
   if p.is_file():
    self.assertNotIn('/workspace/',p.read_text())
    self.assertNotIn('render.stderr',p.name)
if __name__=='__main__':unittest.main()
