"""Home layout contracts, independent of storage and research data."""
from pathlib import Path
from html.parser import HTMLParser
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Parts(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if 'id' in attrs:self.ids.append(attrs['id'])
  if tag=='a':self.links.append(attrs.get('href',''))
class VisualNavigation(unittest.TestCase):
 def test_local_home_jumps_exist_in_every_language(self):
  for filename in ['index.html','academy.html','academy-en.html']:
   text=(ROOT/'dist'/filename).read_text();page=Parts(text)
   for anchor in ['academy-paths','academy-practice','academy-discover','academy-evidence']:
    self.assertEqual(page.ids.count(anchor),1)
    self.assertIn('#'+anchor,page.links)
   self.assertIn('class="academy-hero-actions"',text)
   self.assertIn('class="academy-roadmap"',text)
 def test_roadmap_uses_existing_five_canonical_chapters(self):
  for lang in ['zh','en']:
   filename='academy-en.html' if lang=='en' else 'academy.html'
   text=(ROOT/'dist'/filename).read_text()
   roadmap=text.split('<ol class="academy-roadmap">',1)[1].split('</ol>',1)[0]
   page=Parts(roadmap)
   self.assertEqual(page.links,[filename+'#'+i for i in ['foundations','tokens','tools','project','evaluation']])
   self.assertNotIn('onclick',roadmap)
 def test_no_external_assets_or_animation_added(self):
  css=(ROOT/'web/academy.css').read_text()
  self.assertNotIn('@import',css)
  self.assertNotIn('url(http',css)
  self.assertIn('@media(prefers-reduced-motion:reduce)',css)
  self.assertIn('@media(forced-colors:active)',css)
if __name__=='__main__':unittest.main()
