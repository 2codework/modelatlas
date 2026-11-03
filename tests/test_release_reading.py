"""Real-release lesson contract: source/date precision, offline delivery, isolation."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReleaseReading(unittest.TestCase):
    def test_exact_sources_and_date_boundaries(self):
        for suffix,lang in [('', 'zh-CN'),('-en','en')]:
            page=(ROOT/'web'/f'release-reading{suffix}.html').read_text()
            self.assertIn(f'<html lang="{lang}">',page)
            for url in ['https://qwenlm.github.io/blog/qwen3/', 'https://huggingface.co/Qwen/Qwen3-8B', 'https://arxiv.org/abs/2505.09388v1', 'https://huggingface.co/Qwen/Qwen3-8B/tree/main', 'https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE']:
                self.assertIn(f'href="{url}"',page)
            for fact in ['2025-04-29', '2025-05-14T13:41:34 UTC', '2026-11-01', '2026-10-28', '32,768', '131,072', 'YaRN', '8.2B', 'Apache 2.0', 'main']:
                self.assertIn(fact,page)
            for section in ['evidence','worked','practice','reference','template']:
                self.assertIn(f'id="{section}"',page)
            for kind in ['template','example']:
                name=f'release-brief-{kind}{suffix}.md'
                self.assertIn(f'download href="{name}"',page)
                for folder in ['dist','docs']:
                    self.assertEqual((ROOT/'web'/name).read_bytes(),(ROOT/folder/name).read_bytes())
            self.assertIn(f'academy{suffix}.html#timeline',page)
            self.assertIn(f'academy{suffix}.html#resources',page)
            academy=(ROOT/'web'/f'academy{suffix}.html').read_text()
            self.assertEqual(academy.count(f'href="release-reading{suffix}.html"'),2)
            self.assertIn('<noscript>',page)
            for kind in ['template','example']:
                text=(ROOT/'web'/f'release-brief-{kind}{suffix}.md').read_text()
                self.assertIn('not independently checked' if suffix else '未独立核验', text)
                self.assertIn('Evidence mode' if suffix else '证据模式', text)
                self.assertIn('2026-11-01',text)
            self.assertNotIn('<input',page)
            self.assertNotIn('data-read=',page)

    def test_existing_identity_and_check_date_unchanged(self):
        record=json.loads((ROOT/'data/vendor-catalog/asia.json').read_text())['records'][1]
        self.assertEqual(record['exactid'],'Qwen/Qwen3-8B')
        self.assertEqual(record['sourcecheckdate'],'2026-10-28')
        self.assertTrue(all(value is None for value in record['release_dates'].values()))

    def test_asset_versions_parity_and_no_side_effects(self):
        for suffix in ['', '-en']:
            name=f'release-reading{suffix}.html'
            page=(ROOT/'dist'/name).read_text()
            self.assertEqual(page,(ROOT/'docs'/name).read_text())
            assets=re.findall(r'(?:src|href)="([^"?]+)\?v=([a-f0-9]{64})"',page)
            self.assertEqual(len(assets),3)
            for path,digest in assets:
                self.assertEqual(hashlib.sha256((ROOT/'dist'/path).read_bytes()).hexdigest(),digest)
        script=(ROOT/'web/release-reading.js').read_text()
        for denied in ['localStorage','sessionStorage','fetch(','XMLHttpRequest','eval(']:
            self.assertNotIn(denied,script)

if __name__=='__main__': unittest.main()
