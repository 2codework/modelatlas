"""Editorial exercise contracts, not legal review or actual user testing."""
from pathlib import Path
from html.parser import HTMLParser
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.tags=[]; self.details=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append(tag)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag=='details': self.details.append(a)

class LicensePractice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=(ROOT/'web/license-practice.html').read_text()
        cls.page=Page(cls.text)
    def test_two_exact_objects_and_four_primary_links_match_existing_evidence(self):
        evidence=json.loads((ROOT/'learning/catalog-license/2026-10-31/evidence.json').read_text())
        chosen={'ai21labs/AI21-Jamba2-3B','mistralai/Mistral-Large-4-1T-A52B'}
        rows=[r for r in evidence['rows'] if r['checkpoint'] in chosen]
        self.assertEqual(len(rows),2)
        expected=[]
        for row in rows:
            self.assertIn(row['checkpoint'], self.text)
            self.assertIn(row['license_name'], self.text)
            expected.extend(x['url'] for x in row['links'][:2])
        self.assertEqual(set(x for x in self.page.links if x.startswith('https://')),set(expected))
    def test_self_contained_reading_has_no_script_form_or_remote_fetch(self):
        for tag in ['script','form','iframe','img','input']: self.assertNotIn(tag,self.page.tags)
        self.assertIn("script-src 'none'",self.text)
        self.assertIn("connect-src 'none'",self.text)
        self.assertIn('本页无需JavaScript',self.text)
        self.assertIn('页面不保存填写内容',self.text)
    def test_blank_worksheet_answers_and_current_reading_boundary(self):
        for copy in ['精确检查点：________','本次原文URL、版本/页面定位、实际阅读日期：________','本次未阅读或无法访问的项目：________','未知或冲突：________','不是本次重新访问','未固定文件提交版本','不是法律放行','纸面题完成不等于当前原文核验','不以搜索摘要冒充全文','不绕过访问限制']:
            self.assertIn(copy,self.text)
        self.assertEqual(len(self.page.details),3)
        self.assertTrue(all('open' not in d for d in self.page.details))
    def test_entry_local_links_and_anchor_targets(self):
        self.assertEqual(len(self.page.ids),len(set(self.page.ids)))
        for href in self.page.links:
            if href.startswith('#'): self.assertIn(href[1:],self.page.ids)
            elif not href.startswith('https://'): self.assertTrue((ROOT/'web'/href.split('?')[0]).exists(),href)
        self.assertIn('href="license-practice.html"',(ROOT/'web/index.html').read_text())
        css=(ROOT/'web/license-practice.css').read_text()
        for token in ['minmax(0,800px)','white-space:pre-wrap','overflow-wrap:anywhere','focus-visible','@media(max-width:760px)']: self.assertIn(token,css)
