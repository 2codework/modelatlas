"""Static lesson contracts; not benchmark execution or performance validation."""
from pathlib import Path
from html.parser import HTMLParser
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

class BenchmarkPractice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=(ROOT/'web/benchmark-practice.html').read_text()
        cls.page=Page(cls.text)
    def test_exact_official_sources_and_date_scopes(self):
        self.assertEqual(set(x for x in self.page.links if x.startswith('https://')), {
            'https://github.com/ByteDance-Seed/Bagel/blob/main/README.md',
            'https://github.com/ByteDance-Seed/Bagel/blob/main/EVAL.md'})
        for text in ['News中','KRIS与RISE各自的Evaluation','2025-06-15是更正公告日期',
                     '2026-10-31','未固定提交SHA','不能把当前文档全部当作历史公告当日的内容']:
            self.assertIn(text,self.text)
    def test_no_execution_or_collection(self):
        for tag in ['form','iframe','img','input']: self.assertNotIn(tag,self.page.tags)
        for text in ["script-src 'self'", "connect-src 'none'",'本页无需JavaScript',
                     '页面不保存填写内容','本站未运行这些基准','不要求跟随原文的下载、安装或API步骤']:
            self.assertIn(text,self.text)
    def test_worksheet_and_three_collapsed_answers(self):
        for text in ['编辑估计15–20分钟','模型精确版本：________','基准数据版本与子集：________',
                     'harness版本、改动与环境：________','提示词 / 思考模式：________',
                     '判分模型版本：________','实际运行配置及其证据：________',
                     '未知1 /','未知2 /','人工复核人与日期：________','人工编写的待核主张',
                     '停止条件：','不等于断言官方全文也没有']:
            self.assertIn(text,self.text)
        self.assertEqual(len(self.page.details),5)
        self.assertTrue(all('open' not in d for d in self.page.details))
    def test_configuration_difference_is_unresolved_not_error_claim(self):
        for text in ['cfg_img_scale=2.0','cfg_img_scale=1.5','两处不同范围的标注',
                     '实际运行配置与对应关系仍待核','不能仅据此认定哪一处错误',
                     '不能据此认定文档错误或推导性能差异','未独立复现']:
            self.assertIn(text,self.text)
    def test_local_links_ids_and_responsive_styles(self):
        self.assertEqual(len(self.page.ids),len(set(self.page.ids)))
        for href in self.page.links:
            if href.startswith('#'): self.assertIn(href[1:],self.page.ids)
            elif not href.startswith('https://'): self.assertTrue((ROOT/'web'/href.split('?')[0].split('#')[0]).exists(),href)
        css=(ROOT/'web/benchmark-practice.css').read_text()
        for token in ['minmax(0,800px)','white-space:pre-wrap','overflow-wrap:anywhere','focus-visible','@media(max-width:760px)']:
            self.assertIn(token,css)

    def test_bilingual_transfer_and_downloads(self):
        for suffix in ('', '-en'):
            page=(ROOT/'web'/f'benchmark-practice{suffix}.html').read_text()
            parsed=Page(page)
            self.assertEqual(len(parsed.details),5)
            self.assertTrue(all('open' not in d for d in parsed.details))
            for ident in ['prepare','materials','worksheet','questions','finish','transfer','t-a','t-b','t-c']:
                self.assertIn(ident,parsed.ids)
            for term in ['Cedar-r1','Cedar-latest','LedgerQA-v1','Full','Hard','2026-10-31','2026-11-01']:
                self.assertIn(term,page)
            for kind in ['template','reference']:
                target=f'benchmark-ledger-{kind}{suffix}.md'
                self.assertIn(target,parsed.links)
                self.assertTrue((ROOT/'web'/target).exists())
            self.assertIn('data-benchmark-language',page)
            self.assertEqual(page.count('<script '),1)
            self.assertIn('src="benchmark-practice.js"',page)
    def test_navigation_only_and_discoverability(self):
        js=(ROOT/'web/benchmark-practice.js').read_text()
        for forbidden in ['localStorage','sessionStorage','fetch(','XMLHttpRequest','innerHTML','eval(']:
            self.assertNotIn(forbidden,js)
        for suffix in ('', '-en'):
            self.assertIn(f'benchmark-practice{suffix}.html',(ROOT/'web'/f'academy{suffix}.html').read_text())
            self.assertIn(f'benchmark-practice{suffix}.html',(ROOT/'web/academy.js').read_text())
    def test_templates_are_source_of_generated_pages(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('benchmark_builder',ROOT/'scripts/build_benchmark_practice.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        before={p:p.read_bytes() for p in (ROOT/'web').glob('benchmark-*') if p.suffix in {'.html','.md'}}
        module.render(ROOT)
        self.assertTrue(all(p.read_bytes()==data for p,data in before.items()))
