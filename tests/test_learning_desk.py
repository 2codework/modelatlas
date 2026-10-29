"""Editorial learning UI contracts; no claim of browser or curriculum certification."""
from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
class LearningDesk(unittest.TestCase):
 def test_all_curated_entry_ids_exist_and_first_read_has_no_prerequisites(self):
  text=(ROOT/'web/index.html').read_text();data=json.loads((ROOT/'dist/data.json').read_text());nodes={n['id']:n for n in data['nodes']}
  links=re.findall(r'href="\?node=([^"&]+)"',text)
  self.assertGreaterEqual(len(links),6)
  for nid in links:self.assertIn(nid,nodes)
  self.assertEqual(nodes['nlp'].get('prerequisites'),[])
  self.assertIn('href="foundations.html#foundation-01"',text)
  self.assertIn('不是完整课程',text);self.assertIn('非技术依赖或图谱关系',text)
 def test_progress_is_derived_without_new_storage_keys(self):
  text=(ROOT/'web/app.js').read_text();self.assertIn('function renderContinue()',text)
  self.assertEqual(set(re.findall(r"localStorage\.(?:getItem|setItem)\('([^']+)'",text)),{'modelatlas.progress'})
 def test_six_navigation_and_raw_book_remain(self):
  text=(ROOT/'web/index.html').read_text()
  for k in ['explore','vendor-catalog','timeline','evaluation','learn','coverage']:self.assertIn('id="nav-'+k+'"',text)
  self.assertIn('href="BOOK.md"',text);self.assertIn('href="?node=mcp-lab-roles-tutorial"',text)

 def test_sidebar_link_background_does_not_inherit_old_light_mobile_pills(self):
  css=(ROOT/'web/style.css').read_text()
  self.assertIn('.atlas-workspace>header nav a{background:transparent;color:#d0dcd7;',css)
  self.assertIn('.atlas-workspace>header nav a[aria-current=true]{background:#d6e8ba;color:#263c32;',css)
  text=(ROOT/'web/index.html').read_text();self.assertEqual(text.count('<b aria-hidden="true">→</b>'),3);self.assertNotIn('<b>↗</b>',text)

 def test_sidebar_interaction_colors_have_explicit_pairs_and_visible_focus(self):
  css=(ROOT/'web/style.css').read_text()
  for state,bg,fg in [('hover','#344647','#fff'),('focus-visible','#344647','#fff'),('active','#d6e8ba','#263c32')]:self.assertIn(f'.atlas-workspace>header nav a:{state}{{background:{bg};color:{fg}',css)
  self.assertIn('outline:3px solid #d6e8ba;outline-offset:2px',css)
