"""A static evidence-reading exercise, not new catalog facts or executed products."""
from pathlib import Path
from html.parser import HTMLParser
import re,unittest
ROOT=Path(__file__).resolve().parents[1]
class SourceReading(unittest.TestCase):
 def setUp(self):
  self.html=(ROOT/'web/index.html').read_text().split('id="source-reading-lesson"',1)[1].split('<div id="coverage-table">',1)[0]
 def test_default_collapsed_two_explicit_answers_and_pinned_sources(self):
  page=(ROOT/'web/index.html').read_text()
  self.assertIn('<details class="source-reading-lesson" id="source-reading-lesson">',page)
  self.assertEqual(self.html.count('查看第一题参考答案与理由'),1);self.assertEqual(self.html.count('查看第二题参考答案与理由'),1)
  urls=set(re.findall(r'href="([^"]+)"',self.html));self.assertEqual(urls,{'https://arxiv.org/abs/1706.03762v7','https://arxiv.org/abs/2005.11401v4'})
 def test_information_verification_boundary_and_unknowns(self):
  for text in ['信息核验，不是产品实测','不能证明，不等于已证明没有公开','未由本来源核实','不改变知识目录的来源核验日期','不下载权重','2017-06-12','2023-08-02','2020-05-22','2021-04-12']:
   self.assertIn(text,self.html)
  self.assertNotIn('候选短课',self.html);self.assertNotIn('约 10 分钟',self.html)
 def test_static_accessible_content_no_new_execution(self):
  self.assertNotRegex(self.html,r'<(?:script|iframe|form|input)\b');self.assertIn('scope="col"',self.html);self.assertIn('class="table-scroll"',self.html)
