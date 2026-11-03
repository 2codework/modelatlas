"""Pinned revision identity and native compact navigation regression contracts."""
import copy,json,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class HeaderEvidenceQuality(unittest.TestCase):
 def setUp(self):
  self.p=h.load(ROOT/'curated/historical-events/zzzz-tspulse-nov2.json')
  self.row=next(r for r in self.p['events'] if r['kind']=='paper_revision')
 def test_ten_invalid_revision_variants(self):
  cases=[('version',v) for v in ['arXiv:2505.13033v1','arXiv:2505.13033v0','arXiv:2505.13033v02','arXiv:2505.13033','latest','arXiv:2505.13033v3']]+[('url',u) for u in ['https://arxiv.org/abs/2505.13033v1','https://arxiv.org/abs/2505.13033','https://arxiv.org/abs/2505.13033v3','https://arxiv.org/abs/2505.13034v2']]
  for key,value in cases:
   with self.subTest(key=key,value=value):
    p=copy.deepcopy(self.p);r=next(r for r in p['events'] if r['kind']=='paper_revision')
    if key=='url':r['evidence'][0]['url']=value
    else:r[key]=value
    with self.assertRaises(ValueError):h.validate(p)
 def test_multidigit_revisions_and_supplemental_evidence(self):
  for revision in [2,9,10,123]:
   p=copy.deepcopy(self.p);r=next(r for r in p['events'] if r['kind']=='paper_revision');r['version']=f'arXiv:2505.13033v{revision}';r['evidence'][0]['url']=f'https://arxiv.org/abs/2505.13033v{revision}'
   extra=copy.deepcopy(r['evidence'][0]);extra['url']='https://example.org/supplement';r['evidence'].append(extra);h.validate(p)
 def test_all_existing_packages_keep_readonly_projections(self):
  packages=list((ROOT/'curated/historical-events').glob('*.json'));self.assertEqual(len(packages),11);count=0
  for path in packages:
   p=h.load(path);before=copy.deepcopy(p);one=h.project(p);h.validate(p);self.assertEqual(one,h.project(p));self.assertEqual(p,before);count+=len(one)
  self.assertEqual(count,22)
 def test_bilingual_native_header_and_no_javascript_fallback(self):
  for name in ['index.html','academy.html','academy-en.html']:
   html=(ROOT/'dist'/name).read_text();header=re.search(r'<header class="academy-header">(.*?)</header>',html,re.S).group(1)
   desktop=re.search(r'<nav class="academy-desktop-nav".*?</nav>',header,re.S).group(0)
   mobile=re.search(r'<details class="academy-main-menu">(.*?)</details>',header,re.S).group(1)
   self.assertEqual(re.findall('href="([^"]+)"',desktop),re.findall('href="([^"]+)"',mobile));self.assertEqual(mobile.count('<a '),6)
   self.assertIn('<summary>'+('Menu' if name.endswith('-en.html') else '菜单')+'</summary>',mobile)
   self.assertNotIn('academy-preferences',mobile);self.assertNotIn('role="menu',mobile);self.assertNotIn(' id=',mobile)
   self.assertGreater(header.index('academy-preferences'),header.index('</details>'))
 def test_css_visibility_and_no_resize_mutation(self):
  css=(ROOT/'web/academy.css').read_text();js=(ROOT/'web/academy.js').read_text()
  self.assertIn('.academy .academy-main-menu{display:none;',css)
  self.assertIn('@media(max-width:800px){.academy-header nav.academy-desktop-nav{display:none!important}.academy .academy-main-menu{display:block}}',css)
  self.assertNotRegex(js,r'addEventListener\([\'\"]resize');self.assertNotIn('mainMenu.open=true',js)
