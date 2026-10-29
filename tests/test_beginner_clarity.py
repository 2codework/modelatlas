"""Additive explanations only; frozen TOC candidate's prompt/table bytes remain pinned."""
from pathlib import Path
import hashlib,re,unittest
from html import unescape
ROOT=Path(__file__).resolve().parents[1]
class BeginnerClarity(unittest.TestCase):
 def setUp(self):self.html=(ROOT/'web/learn.html').read_text()
 def test_copyable_prompts_and_reference_table_remain_exact(self):
  digest=lambda s:hashlib.sha256(s.encode()).hexdigest()
  self.assertEqual([digest(x)for x in re.findall(r'<pre(?: [^>]*)?>.*?</pre>',self.html,re.S)],['582f77f4185ee575791d72f8aeb0275adc8a89b9e5e8f7add7a2c092cb493836','e7c6f65cd78c48639ff4b2c6c297ea44de1e99e66ddb427474d99e8180a363b1','0155e6b301e655220f2670b897f49b5575646a6274cb5d1dad85b2a690c051d2'])
  self.assertEqual([digest(x)for x in re.findall(r'<table>.*?</table>',self.html,re.S)],['c67ee76bb55112301d7297cd34bf951baf6d312cb53bb64ba3abbbde0bc2f082'])
 def test_material_boundary_is_only_two_example_sentences(self):
  prompt=unescape(re.search(r'<pre id="first-prompt">(.*?)</pre>',self.html,re.S).group(1))
  self.assertEqual(prompt.count('\n【资料】\n'),1);instructions,material=prompt.split('\n【资料】\n')
  self.assertEqual(material.strip(),'阿禾负责海报，周五前完成。场地尚未确定。')
  for constraint in ['输出表格：事项｜负责人｜截止时间｜事实或建议','缺失信息写“未注明”','只生成草稿，不发消息、不修改外部系统']:self.assertIn(constraint,instructions)
  self.assertNotIn('下一次仍用',prompt);self.assertNotIn('概念',material)
 def test_fact_label_explains_source_claim_not_real_world_verification(self):
  note=re.search(r'<p class="fact-boundary">(.*?)</p>',self.html,re.S).group(1)
  self.assertIn('只表示原文明确写了',note);self.assertIn('不表示已经核实实际情况',note);self.assertIn('不是“海报已经完成”',note)
  self.assertIn('完成状态也要能从原文找到依据',self.html);self.assertIn('即使姓名和时间都对，“阿禾已经完成海报”也不符合原文',self.html)
  self.assertLess(self.html.index('</table>'),self.html.index('class="fact-boundary"'))
 def test_reuse_card_returns_to_existing_prompt_without_new_execution_ui(self):
  card=re.search(r'<section class="self-check reuse-card">(.*?)</section>',self.html,re.S).group(1)
  self.assertIn('只把提示词末尾、单独一行【资料】下面的两句示例换成你的记录',card);self.assertIn('开头“请仅根据【资料】”等任务要求不改',card);self.assertIn('不要把示例和真实记录混在一起',card)
  self.assertIn('保留输出格式',card);self.assertIn('不发消息、不修改系统',card);self.assertIn('href="#step-2"',card)
  self.assertIn('有权处理、已去掉隐私',card);self.assertNotRegex(card,r'<(?:input|form|textarea|button|pre)\b')
 def test_concept_bridge_matches_this_task_without_model_or_plan_claim(self):
  bridge=re.search(r'<p class="concept-bridge">(.*?)</p>',self.html,re.S).group(1)
  for text in ['ChatGPT 是聊天应用','模型是处理这次输入、生成草稿的组件','API 则是让程序发请求的一种入口','不是另一个模型名称','这次你在网页里手动输入','先不需要申请 API key']:self.assertIn(text,bridge)
  self.assertNotRegex(bridge,r'gpt-\d|默认模型|免费无限|自动选择|性能保证')
