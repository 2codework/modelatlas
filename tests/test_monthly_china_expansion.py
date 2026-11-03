"""Bounded provider/month coverage, exact scope, and conflicting date semantics."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows
NAME = 'china-expansion-oct31.json'

class ChinaExpansionTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / 'curated/monthly' / NAME).read_text())
        self.events = self.package['events']

    def test_finite_coverage_and_admission(self):
        self.assertEqual(validate(self.package), 6)
        self.assertFalse(self.package['exhaustive'])
        cells = self.package['coverage']['ledger']
        self.assertEqual(len({(c['provider'], c['month']) for c in cells}), 12)
        self.assertTrue(all(not c['exhaustive'] for c in cells))
        self.assertEqual({r['vendor'] for r in self.events}, {'Tencent Hunyuan', 'Baidu', 'ByteDance'})
        self.assertFalse(any(e['month'] == '2026-08' for e in self.events))

    def test_exact_checkpoints_and_family_subset(self):
        self.assertEqual([len(r['included_models']) for r in self.events], [3, 1, 1, 4, 1, 4])
        self.assertNotIn('bf16', ' '.join(self.events[0]['included_models']))
        self.assertEqual(self.events[4]['included_models'], ['baidu/ERNIE-4.5-0.3B-Paddle'])
        self.assertEqual(self.events[4]['event_precision']['weights'], 'day_official_family_release_statement')
        self.assertIn('十款全部', ''.join(self.events[4]['notes']))
        self.assertTrue(all('/tree/main/HunyuanWorld-' in u for u in self.events[5]['weight_entries']))
        self.assertEqual(self.events[5]['modality']['output'], ['image'])

    def test_dates_are_not_interchangeable(self):
        self.assertEqual([r['weights_release_date'] for r in self.events], ['2025-05-08', '2025-05-20', '2025-05-28', '2025-06-27', '2025-06-30', '2025-07-26'])
        self.assertEqual(self.events[0]['paper_date'], '2025-06-04')
        self.assertEqual(self.events[2]['paper_date'], '2025-05-26')
        self.assertEqual(self.events[2]['code_release_date'], '2025-05-28')
        self.assertEqual(self.events[5]['paper_date'], '2025-07-29')
        self.assertEqual(self.events[5]['license_header_release_date'], '2025-07-27')
        self.assertIn('日期口径并列', ''.join(self.events[5]['notes']))
        for r in self.events:
            self.assertIsNone(r['first_upload_timestamp'])
            self.assertIsNone(r['api_release_date'])
            self.assertIsNone(r['initial_release_weights_license'])

    def test_current_license_scope_and_restrictions(self):
        for i, r in enumerate(self.events):
            lic = r['licenses'][0]
            self.assertIsNone(lic['at_initial_release'])
            self.assertEqual(lic['reviewed_on'], '2026-10-31')
            self.assertEqual(lic['full_license_text_reviewed'], i in (2, 5))
        for i in (2, 3, 5):
            self.assertIn('欧盟、英国、韩国', self.events[i]['access_note'])
            self.assertIn('不等于', self.events[i]['access_note'])
        self.assertIn('100万', ''.join(self.events[5]['notes']))
        self.assertIn('1亿', ''.join(self.events[3]['notes']))
        self.assertIn('第三方', ''.join(self.events[5]['notes']))

    def test_projection_preserves_unknowns_and_conflict(self):
        before = copy.deepcopy(self.package)
        rows = curated_rows(self.package)
        self.assertEqual(before, self.package)
        self.assertEqual(len(rows), 6)
        for r in rows:
            self.assertEqual(r['kind'], 'weights_announcement')
            self.assertIsNone(r['date_details']['first_upload'])
            self.assertIn('首次上传', r['note'])
        self.assertIn('日期口径并列', rows[5]['note'])
        self.assertIn('家族开放声明', rows[4]['note'])

    def test_no_existing_checkpoint_overlap(self):
        own = {m.lower() for r in self.events for m in r['included_models']}
        urls = {u.lower().rstrip('/') for r in self.events for u in r['weight_entries']}
        for path in (ROOT / 'curated/monthly').glob('*.json'):
            if path.name == NAME:
                continue
            data = json.loads(path.read_text())
            for r in data.get('events', data.get('records', [])):
                self.assertFalse(own.intersection(m.lower() for m in r.get('included_models', [])))
                other = r.get('weight_entries', []) + ([r['official_weights_url']] if r.get('official_weights_url') else [])
                self.assertFalse(urls.intersection(u.lower().rstrip('/') for u in other))

if __name__ == '__main__':
    unittest.main()
