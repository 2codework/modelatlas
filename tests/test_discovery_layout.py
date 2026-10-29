"""Original static layout contracts, not pixel/browser or mobile certification."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Controls(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.searches=[];self.advanced=[];self.summaries=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='search':self.searches.append((a,list(self.stack)))
  if tag=='select' and any(t=='details' and 'advanced-filters' in x.get('class','') for t,x in self.stack):self.advanced.append(a.get('id'))
  if tag not in ['input','meta','link','img','br','hr']:self.stack.append((tag,a))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
class DiscoveryLayout(unittest.TestCase):
 def test_exactly_one_real_search_per_searchable_view(self):
  html=(ROOT/'web/index.html').read_text();d=Controls();d.feed(html)
  expected={'explore':'query','vendor-catalog':'catalog-query','timeline':'event-query','evaluation':'evaluation-query','learn':'path-query'}
  self.assertEqual(len(d.searches),5)
  for attrs,stack in d.searches:
   sections=[a.get('id') for t,a in stack if t=='section'];self.assertEqual(len(sections),1);self.assertEqual(attrs['id'],expected[sections[0]]);self.assertNotIn('hidden',attrs);self.assertFalse(any(t=='details' for t,a in stack))
  self.assertNotIn('global-query',html)
 def test_advanced_filters_preserve_all_controls_but_not_primary_searches(self):
  d=Controls();d.feed((ROOT/'web/index.html').read_text());self.assertCountEqual(d.advanced,['type','category','availability','vendor','catalog-provider','catalog-entity_type','catalog-modality','catalog-status','event-type','evaluation-kind'])
 def test_boundaries_and_scope_options_remain_visible_in_source(self):
  text=(ROOT/'web/index.html').read_text();self.assertIn('不是完整目录或最新排行榜',text);self.assertIn('来源核验 ≠ 独立实测；未知保持未知',text);self.assertIn('当前', (ROOT/'web/app.js').read_text());self.assertIn('<option value="learn">学习路线</option>',text)
