"""Static bilingual delivery contract; independent fixtures stay inspectable without JS."""
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VideoSampling(unittest.TestCase):
    def test_static_reference_and_bilingual_links(self):
        for suffix, lang in [('', 'zh-CN'), ('-en', 'en')]:
            text = (ROOT / 'web' / f'video-sampling-lab{suffix}.html').read_text()
            self.assertIn(f'<html lang="{lang}">', text)
            # Independently reconstruct every source label twice (W and E).
            for anomaly, identity in [(3, 'B'), (5, 'C')]:
                for i in range(9):
                    label = identity if i == anomaly else 'A'
                    self.assertIn(f'F{i} · {i*250} ms · ID {label} · x={10+10*i}', text)
            self.assertIn('<noscript>', text)
            self.assertIn('id="report" hidden', text)
            self.assertIn(f'academy{suffix}.html#multimodal', text)
            self.assertIn(f'academy{suffix}.html#evaluation', text)
            self.assertIn(f'video-sampling-lab{suffix}.html', (ROOT/'web'/f'academy{suffix}.html').read_text())

    def test_built_local_assets_sha_and_pages_parity(self):
        for suffix in ['', '-en']:
            name = f'video-sampling-lab{suffix}.html'
            text = (ROOT/'dist'/name).read_text()
            self.assertEqual(text, (ROOT/'docs'/name).read_text())
            assets = re.findall(r'(?:src|href)="([^"?]+)\?v=([a-f0-9]{64})"', text)
            self.assertEqual(len(assets), 5)
            for path, digest in assets:
                self.assertEqual(hashlib.sha256((ROOT/'dist'/path).read_bytes()).hexdigest(), digest)


if __name__ == '__main__':
    unittest.main()
