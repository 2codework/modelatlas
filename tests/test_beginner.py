import unittest,re,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Beginner(unittest.TestCase):
 def test_complete_course_and_bindings(self):
  html=(ROOT/'web/learn.html').read_text();source=json.loads((ROOT/'web/foundations-source.json').read_text())
  self.assertEqual(len(re.findall('data-lesson',html)),6)
  for lesson in source['lessons']:self.assertIn('foundations.html#'+lesson['id'],html)
  for text in ['first-prompt','原创纸面参考答案','未注明','查看答案','费用','隐私','API','MCP','Skill','RAG','Agent','停止','撤销']:self.assertIn(text,html)
  self.assertNotIn('http-equiv="refresh"',html)
  for tag in ['script','style']:self.assertNotRegex(html,fr'<{tag}>(?!</)')
 def test_default_entry_and_library_routes(self):
  html=(ROOT/'web/index.html').read_text()
  for route in ['explore','vendor-catalog','timeline','evaluation','learn','coverage']:self.assertIn('href="?view='+route+'"',html)
  self.assertIn('id="start-here"',html);self.assertIn('learn.html#step-1',html)
  self.assertNotIn('prefill',html.split('id="start-here"',1)[1].split('id="discovery-intro"',1)[0])
 def test_accessibility_and_responsive_contract(self):
  html=(ROOT/'web/learn.html').read_text();css=(ROOT/'web/learn.css').read_text();js=(ROOT/'web/learn.js').read_text()
  self.assertIn('href="#lesson-main"',html);self.assertIn('role="status"',html);self.assertIn('focus-visible',css);self.assertIn('@media(max-width:760px)',css)
  self.assertNotIn('localStorage',js);self.assertNotIn('fetch(',js);self.assertIn('hashchange',js)
 def test_connection_routes_are_complete_and_source_bound(self):
  source=json.loads((ROOT/'learning/task-first/connections.json').read_text());html=(ROOT/'web/connections.html').read_text()
  from html import escape
  for route in source['routes']:
   self.assertIn('id="'+route['id']+'"',html)
   for key in ['start_url','accounts_cost','minimum_access','prompt','reference_output','disconnect','test_input']:
    self.assertIn(escape(route[key]),html)
   for key in ['onboarding_steps','steps','expected_observations','platform_notes']:
    for value in route[key]:self.assertIn(escape(value),html)
  for key in ['followup_prompt_label','file_correction_prompt']:
   self.assertIn(escape(source['routes'][0][key]),html)
  for key in ['disable_path_note','windows_disable_config']:
   self.assertIn(escape(source['routes'][2][key]),html)
  self.assertEqual((ROOT/'web/connections-source.json').read_bytes(),(ROOT/'learning/task-first/connections.json').read_bytes())
 def test_beginner_route_prioritizes_tool_setup_before_prompt(self):
  html=(ROOT/'web/learn.html').read_text()
  articles={m.group(1):m.group(2) for m in re.finditer(r'<article id="(step-\d)"[^>]*>(.*?)</article>',html,re.S)}
  self.assertIn('class="primary-action" href="#step-3">下一步',articles['step-1'])
  self.assertIn('class="primary-action" href="#step-2">下一步',articles['step-3'])
  self.assertIn('class="primary-action" href="#step-6">下一步',articles['step-2'])
  self.assertIn('https://chatgpt.com/',articles['step-3'])
  self.assertIn('Log in',articles['step-3']);self.assertIn('Sign up',articles['step-3'])
  self.assertIn('只看示例',articles['step-1'])

 def test_semantic_headings_navigation_and_deliberate_print(self):
  for name in ['learn.html','connections.html']:
   html=(ROOT/'web'/name).read_text()
   self.assertNotIn('<h3>',html);self.assertIn('<h2>',html)
   self.assertIn('<noscript>',html)
  self.assertIn('aria-label="入门步骤与选读"',(ROOT/'web/learn.html').read_text())
  css=(ROOT/'web/learn.css').read_text();self.assertIn('@media print',css);self.assertIn('[data-lesson][hidden],[data-route][hidden]{display:block!important}',css)

 def test_setup_is_one_preparation_phase_not_a_missing_prompt(self):
  html=(ROOT/'web/learn.html').read_text();body=re.search(r'<article id="step-3"[^>]*>(.*?)</article>',html,re.S).group(1)
  self.assertEqual(body.count('class="setup-primary"'),1)
  for phrase in ['下方样例','现在就做','此刻的默认选择','提交后等待','现成聊天应用</h2>']:self.assertNotIn(phrase,body)
  self.assertIn('现在不用输入或提交内容',body)
  self.assertIn('href="#step-2">工具已打开，去复制练习',body)
  self.assertIn('只看示例，不登录也能继续',body)
  route=json.loads((ROOT/'learning/task-first/connections.json').read_text())['routes'][0]
  from html import escape
  for key in ['accounts_cost','minimum_access']:self.assertEqual(body.count(escape(route[key])),1)
  self.assertEqual(body.count('class="route-option"'),2)
  self.assertNotIn('<pre',body)
 def test_header_explicitly_resets_sidebar_and_subtitle(self):
  css=(ROOT/'web/start.css').read_text();self.assertIn('flex-direction:row;align-items:center;justify-content:space-between',css)
  self.assertIn('display:block;color:#586a67;font-size:13px',css)
  self.assertIn('nav a[aria-current=page]',css)
