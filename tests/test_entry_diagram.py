"""Static accessible concept routes; not pixel or browser layout verification."""
import unittest,re,hashlib
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
OLD='<div class="flow" aria-label="从输入到验收的教学流程"><span>你给材料</span><b>→</b><span>应用把材料交给模型</span><b>→</b><span>生成草稿</span><b>→</b><span>你核对</span></div>'
BASELINE_HTML='efd7371becec324dda536955681aa4dd28ec146aa8983bc8743cd7d1f5f81c30'
class Tree(HTMLParser):
 def __init__(self):super().__init__();self.root={'tag':'root','attrs':{},'children':[]};self.stack=[self.root]
 def handle_starttag(self,tag,attrs):
  n={'tag':tag,'attrs':dict(attrs),'children':[]};self.stack[-1]['children'].append(n)
  if tag not in ['meta','link','br','hr','input','img']:self.stack.append(n)
 def handle_endtag(self,tag):
  if self.stack[-1]['tag']==tag:self.stack.pop()
 def handle_data(self,text):self.stack[-1]['children'].append(text)
def nodes(n):
 if isinstance(n,str):return []
 return [n]+[x for c in n['children'] for x in nodes(c)]
def text(n):return n if isinstance(n,str) else ''.join(text(c) for c in n['children'])
def normal(html):return re.sub(r'learn.css\?v=[a-f0-9]{64}','learn.css',html)
class EntryDiagram(unittest.TestCase):
 def setUp(self):
  self.html=(ROOT/'web/learn.html').read_text();self.figure=re.search(r'<figure class="entry-diagram".*?</figure>',self.html,re.S).group();p=Tree();p.feed(self.figure);self.tree=p.root
 def test_only_existing_first_flow_replaced_all_remaining_course_bytes_preserved(self):
  self.assertEqual(self.html.count('class="entry-diagram"'),1)
  self.assertLess(self.html.index(self.figure),self.html.index('id="step-2"'))
  # Explicit later editorial addition: pin its whole bytes before projecting the unchanged historical stage.
  access=re.findall(r'<div class="caution editorial-access">.*?</div>',self.html,re.S)
  self.assertEqual(len(access),1)
  step3=re.search(r'<article id="step-3"[^>]*>(.*?)</article>',self.html,re.S).group(1)
  self.assertEqual(step3.count(access[0]),1)
  self.assertLess(step3.index(access[0]),step3.index('class="primary-action"'))
  self.assertEqual(hashlib.sha256(access[0].encode()).hexdigest(),'8783f15736509e7cc4bd5feffe189100824a2f177680a98267cca54575a042c2')
  self.assertEqual(hashlib.sha256(normal(self.html.replace(access[0],'').replace(self.figure,OLD)).encode()).hexdigest(),BASELINE_HTML)
  self.assertIn('提出下一步',self.html);self.assertIn('concept-bridge',self.html)
 def test_two_real_text_ordered_routes_and_unambiguous_labels(self):
  routes=[n for n in nodes(self.tree) if n['attrs'].get('class')=='entry-route'];self.assertEqual(len(routes),2);self.assertTrue(all(any(n['tag']=='h2' for n in nodes(route)) for route in routes))
  expected=[['你写任务','聊天应用','模型处理','生成草稿','你核对'],['你的程序','API 入口','模型处理','得到输出','程序处理']]
  for route,want in zip(routes,expected):
   lists=[n for n in nodes(route) if n['tag']=='ol'];self.assertEqual(len(lists),1)
   cells=[n for n in nodes(route) if n['tag']=='li'];self.assertEqual(len(cells),5)
   self.assertEqual([text(next(n for n in nodes(c) if n['tag']=='span')) for c in cells],want)
  self.assertIn('本课先用这条路',text(routes[0]));self.assertIn('需要时再学',text(routes[1]))
 def test_accessible_caption_description_and_decorative_arrows(self):
  ns=nodes(self.tree);ids={n['attrs']['id']:n for n in ns if 'id' in n['attrs']}
  for n in ns:
   for key in ['aria-labelledby','aria-describedby']:
    if key in n['attrs']:self.assertTrue(text(ids[n['attrs'][key]]).strip())
  self.assertEqual(sum(n['tag']=='figcaption' for n in ns),1)
  arrows=[n for n in ns if n['attrs'].get('class')=='route-arrow'];self.assertEqual(len(arrows),8)
  self.assertTrue(all(n['attrs'].get('aria-hidden')=='true' for n in arrows))
  self.assertNotIn('role="img"',self.figure)
 def test_scope_no_execution_or_smartness_promise_and_no_external_action(self):
  body=text(self.tree)
  for s in ['不是另一种更聪明的模型','不是本课的先决条件','仍需安排检查','概念简图','省略工具、路由','不是 ChatGPT 的真实内部架构','不表示所有请求都只经过一个模型']:self.assertIn(s,body)
  self.assertFalse(any(n['tag'] in ['a','button','input','form','script','img','svg','iframe','audio'] for n in nodes(self.tree)))
  self.assertNotRegex(self.figure,r'https?://|onclick=|src=')
 def test_responsive_css_no_fixed_width_or_network_for_diagram(self):
  css=(ROOT/'web/learn.css').read_text().split('/* Original conceptual diagram:')[1]
  self.assertIn('grid-template-columns:repeat(5,minmax(0,1fr))',css);self.assertIn('@media(max-width:620px)',css)
  self.assertIn('grid-template-columns:minmax(0,1fr)',css);self.assertIn('overflow-wrap:anywhere',css)
  self.assertIn('list-style-position:inside',css);self.assertIn('rotate(90deg)',css)
  self.assertNotRegex(css,r'url\(|@import|[;{]\s*width:\s*\d+px|position:fixed')
if __name__=='__main__':unittest.main()
