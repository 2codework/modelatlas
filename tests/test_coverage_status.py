import copy,importlib.util,json,pathlib,unittest
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('coverage_status',ROOT/'scripts/build_coverage_status.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class CoverageStatus(unittest.TestCase):
 def setUp(self):self.s=json.loads((ROOT/'learning/coverage/2026-11-02-smollm3-family/snapshot.json').read_text());self.html=mod.render(self.s);self.tags=Tags();self.tags.feed(self.html)
 def test_matches_checked_in(self):self.assertEqual((ROOT/'web/coverage-status.html').read_text(),self.html+'\n')
 def test_previous_snapshot_retained(self):
  old=json.loads((ROOT/'learning/coverage/2026-10-31/snapshot.json').read_text());self.assertEqual(old['checked_on'],'2026-10-31');self.assertEqual(old['monthly']['events'],221)
 def test_no_javascript_and_closed_details(self):
  self.assertNotIn('script',[t for t,a in self.tags.tags]);details=[a for t,a in self.tags.tags if t=='details'];self.assertEqual(len(details),4);self.assertTrue(all('open' not in a for a in details))
 def test_denominators(self):
  for n in self.s['catalog']['urls'].values():self.assertIn(f'{n} / {self.s["catalog"]["records"]}',self.html)
  self.assertIn('不表示当月全球没有发布',self.html);self.assertIn('不代表世界上不存在',self.html)
 def test_snapshot_visible_and_no_internal_coordination(self):
  self.assertIn('核验快照 2026-11-02',self.html);self.assertIn(self.s['snapshot_note'],self.html)
  for forbidden in ['recovered-sites/','campus-rollout/','worker','root task','SHA256']:self.assertNotIn(forbidden,self.html)
 def test_practice_counts_are_separate_historical_and_new_teaching_scopes(self):
  self.assertEqual(self.s['practice']['cases'],138)
  self.assertEqual(self.s['practice']['synthetic_cases'],138)
  for phrase in ['138个为历史合成教学案例','另有9个新增完整双语教学案例','不计入这份历史快照','不应相加称为已核验案例总数','不代表真实产品实测','截至2026-11-01的本地改版','不是线上实时清单']:
   self.assertIn(phrase,self.html)
  self.assertNotIn('142',self.html)
  self.assertNotIn('AgentWork当前快照',self.html)
 def test_invalid_counts(self):
  for key,val in [('dated',-1),('dated',True),('undated',999)]:
   s=copy.deepcopy(self.s);s['monthly'][key]=val
   with self.assertRaises(ValueError):mod.render(s)
 def test_html_escape(self):
  s=copy.deepcopy(self.s);s['snapshot_note']='<img src=x onerror=alert(1)>';result=mod.render(s);self.assertIn('&lt;img',result);self.assertNotIn('<img src=x',result)
 def test_links_and_styles_exist(self):
  for tag,a in self.tags.tags:
   if tag in ['a','link'] and a.get('href') and not a['href'].startswith('#'):
    target=a['href'].split('?')[0];self.assertTrue((ROOT/'web'/target).exists(),target)
 def test_single_h1_and_landmark(self):
  self.assertEqual(sum(t=='h1' for t,a in self.tags.tags),1);self.assertTrue(any(t=='main' and a.get('id')=='main' for t,a in self.tags.tags))
if __name__=='__main__':unittest.main()
