"""Only static author-created reading aids; never execute a product or reader script."""
import hashlib,json,re,unittest
from pathlib import Path
from html import unescape
ROOT=Path(__file__).resolve().parents[1]
class BeginnerAccessResponse(unittest.TestCase):
 def test_only_additive_overlays_and_original_api_page(self):
  expected={'learn.html': {'web': '7a0860e45bfa04e985322dcc277595e1dfe6d5dd102f8c9ed48c5fe0f870a26b', 'dist': '5121670481c7c39ac81029ec55523526b529202071b650dc4bf80fcd0b6ed4bb', 'docs': '5121670481c7c39ac81029ec55523526b529202071b650dc4bf80fcd0b6ed4bb'}, 'practice-local.html': {'web': '0c113b101da4e753c84b1fc0f0edec54eb337f26347df2440e2b3c574671cc82', 'dist': 'ec500846350cf9a1344c2c01c2e2798936f215d528078d2f779d8ba58a45e2a4', 'docs': 'ec500846350cf9a1344c2c01c2e2798936f215d528078d2f779d8ba58a45e2a4'}, 'practice-api.html': {'web': 'b9634518230fc4f40a60e28799ef5dbde0fb9d33b0d616a4124e4d4ae8555813', 'dist': 'c40929767bdd1a324e361a85a415996970e745ee358d8a712005ab8da7a26298', 'docs': 'c40929767bdd1a324e361a85a415996970e745ee358d8a712005ab8da7a26298'}}
  for name,digest in expected.items():
   for folder in ['web','dist','docs']:
    text=(ROOT/folder/name).read_text()
    if name=='learn.html':text,n=re.subn(r'<div class="caution editorial-access">.*?</div>','',text,flags=re.S);self.assertEqual(n,1)
    if name=='practice-local.html':text,n=re.subn(r'<section class="editorial-response".*?</section>','',text,flags=re.S);self.assertEqual(n,1)
    self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),digest[folder])
 def test_region_notice_precedes_open_and_registration_with_paper_escape(self):
  html=(ROOT/'web/learn.html').read_text();step=re.search(r'<article id="step-3"[^>]*>(.*?)</article>',html,re.S).group(1)
  notice=re.search(r'<div class="caution editorial-access">(.*?)</div>',step,re.S).group(1)
  self.assertLess(step.index('class="caution editorial-access"'),step.index('class="primary-action"'))
  self.assertLess(step.index('class="caution editorial-access"'),step.index('Log in'))
  for phrase in ['官方支持地区','账户无法使用','资格尚未确认','不要为了跟做绕过地区限制','href="#step-2"','在纸上整理示例','不算真实产品已运行','不是本轮重新抓取']:self.assertIn(phrase,notice)
  source=next(s for s in json.loads((ROOT/'learning/chatgpt-images-feature/r1/overlay.json').read_text())['sources'] if s['id']=='cgw-src-regions-reused')
  self.assertEqual(source['url'],'https://help.openai.com/en/articles/7947663-chatgpt-supported-countries')
  self.assertIn('href="'+source['url']+'" target="_blank" rel="noopener noreferrer"',notice)
  self.assertIn(source['checked_at'],notice)
  self.assertNotRegex(notice,r'<(?:button|input|form|script|iframe)\b')
 def test_local_bridge_has_readable_escaped_json_and_three_success_layers(self):
  html=(ROOT/'web/practice-local.html').read_text();bridge=re.search(r'<section class="editorial-response".*?</section>',html,re.S).group()
  self.assertLess(html.index('id="section-5"'),html.index(bridge));self.assertLess(html.index(bridge),html.index('屏幕应出现 HTTP'))
  for phrase in ['作者示意，不是真实运行结果','不是可执行命令','--include','message.content','不是要寻找的一整个键名','换行的转义写法','curl exit=0','不等于 HTTP 200','更不等于答案正确','不能证明服务端没有执行','未执行','href="#source-L6"','href="#source-L10"']:self.assertIn(phrase,bridge)
  sample=unescape(re.search(r'<pre id="local-response-example"><code>(.*?)</code></pre>',bridge,re.S).group(1));headers,payload=sample.split('\n\n')
  self.assertIn('HTTP/1.1 200 OK',headers);obj=json.loads(payload)
  self.assertEqual(obj['message']['content'],'提交海报｜小林｜2026-10-30｜L1\n跟进场地报价｜待确认｜待确认｜L2')
  self.assertIn('\\n',payload);self.assertNotRegex(bridge,r'<(?:button|input|form|script|iframe)\b')
 def test_raw_and_downloads_are_frozen(self):
  for name,digest in {'source-ledger.json': 'bd92b8527bd1ba7f046e7bb32aa9bb712c1f7a67a29f3008be016f392eeae67f', 'FIRST_API.zh-CN.md': '70511698541247c4612f60810167929fb0a939c0a5658cb279251d72842fa463', 'FIRST_LOCAL.zh-CN.md': 'da2f9b83b8031a7907dabc2e56772a6443d047f9d908e980b89864abb6b7df4c', 'local_request.sh': '88fca2dfc4b0036ffa9a139432592da322d5034f4085c46365e1b3cd172e3d7b', 'SHA256SUMS': 'd97213641811aaa9dec82ccbef5bd1dc259a5fb5db5a24a3cb5837ab8ec061c8', 'first_request.py': '10838181aab8df8fae709488ed609c795b3719250ad3ffbb73a6b199191b6b04'}.items():
   self.assertEqual(hashlib.sha256((ROOT/'learning/api-local/r1/raw'/name).read_bytes()).hexdigest(),digest)
   if name!='SHA256SUMS':
    for folder in ['web','dist','docs']:self.assertEqual(hashlib.sha256((ROOT/folder/'practice'/name).read_bytes()).hexdigest(),digest)
