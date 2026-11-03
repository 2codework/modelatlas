"""Boundaries for the four May–June official availability announcements."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows

class MayJuneGapTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / 'curated/monthly/gaps-may-june-oct31.json').read_text())
        self.events = self.package['events']

    def test_four_precise_announcement_dates(self):
        self.assertEqual(validate(self.package), 4)
        self.assertEqual([r['weights_release_date'] for r in self.events], ['2025-05-21', '2025-05-28', '2025-06-05', '2025-06-10'])
        for r in self.events:
            self.assertEqual(r['event_type'], 'weights_release_announcement')
            self.assertEqual(r['month'], r['weights_release_date'][:7])
            self.assertTrue(r['evidence'][0]['date_text'])
            for key in ['first_upload_timestamp', 'paper_date', 'code_release_date', 'api_release_date']:
                self.assertIsNone(r[key])

    def test_family_and_exact_scopes(self):
        self.assertEqual([len(r['included_models']) for r in self.events], [1, 1, 6, 1])
        self.assertEqual(self.events[2]['event_granularity'], 'family_release')
        self.assertEqual(len(self.events[2]['weight_entries']), 2)
        self.assertNotIn('Medium', ''.join(self.events[3]['included_models']))
        self.assertEqual(self.events[1]['included_models'], ['deepseek-ai/DeepSeek-R1-0528'])

    def test_license_declarations_not_full_text_and_code_separate(self):
        self.assertEqual([r['code_license'] for r in self.events], [None, 'MIT', None, None])
        self.assertEqual(len(self.events[1]['licenses']), 2)
        for r in self.events:
            self.assertIn('未逐条审核完整许可正文', r['licenses'][0]['review_note'])
            self.assertIn('模型权重', r['licenses'][0]['applies_to'])

    def test_adapter_readonly_and_public_provenance(self):
        before = copy.deepcopy(self.package)
        rows = curated_rows(self.package)
        self.assertEqual(self.package, before)
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r['kind'] == 'weights_announcement' for r in rows))
        text = json.dumps(self.package)
        for private in ['campus-rollout', '/workspace/', 'transcript_evidence', 'research_missing']:
            self.assertNotIn(private, text)

if __name__ == '__main__':
    unittest.main()
