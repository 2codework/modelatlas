from pathlib import Path
from html.parser import HTMLParser
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import foundation_self_checks
class Structure(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,attrs):self.tags.append((t,dict(attrs)))
class SelfChecks(unittest.TestCase):
 def test_all_labeled_groups_are_optional_local_and_initially_empty(self):
  for n in range(6):
   markup=foundation_self_checks.render(n,f'foundation-{n+1:02}')
   parsed=Structure();parsed.feed(markup)
   radios=[a for t,a in parsed.tags if t=='input'];labels=[a['for'] for t,a in parsed.tags if t=='label']
   self.assertEqual(len(radios),3);self.assertEqual(labels,[r['id'] for r in radios]);self.assertEqual(len({r['name'] for r in radios}),1)
   self.assertTrue(all('checked' not in r and r['type']=='radio' for r in radios))
   self.assertEqual(sum(t=='fieldset' for t,a in parsed.tags),1);self.assertEqual(sum(t=='legend' for t,a in parsed.tags),1)
   self.assertTrue(any(a.get('aria-live')=='polite' and a.get('aria-atomic')=='true' for t,a in parsed.tags))
   self.assertTrue(all(a.get('type')=='button' for t,a in parsed.tags if t=='button'))
   self.assertIn('hidden data-correct',markup);self.assertIn('<noscript>',markup);self.assertNotIn('<form',markup)
   for text in ['作者合成教学','不是真模型执行或能力认证','选择仅在当前页面使用，不上传、不写入学习进度','核对我的选择','清除选择，重试']:self.assertIn(text,markup)
 def test_generated_order_preserves_original_answer_before_optional_check(self):
  html=(ROOT/'web/foundations.html').read_text()
  self.assertEqual(html.count('class="self-check"'),6)
  for article in html.split('<article ')[1:]:
   self.assertLess(article.index('class="answer"'),article.index('class="self-check"'))
  self.assertIn('script-src \'self\'',html);self.assertIn('form-action \'none\'',html)
