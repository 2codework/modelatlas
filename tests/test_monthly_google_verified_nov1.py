"""Prepared-candidate guardrails, not source truth or legal certification."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows
NAME = 'google-verified-nov1.json'

class GooglePreparedCandidateTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / 'curated/monthly' / NAME).read_text())
        self.event = self.package['events'][0]

    def test_only_verified_member_admitted(self):
        self.assertEqual(validate(self.package), 1)
        self.assertFalse(self.package['exhaustive'])
        self.assertEqual(self.event['included_models'], ['google/t5gemma-2b-2b-ul2-it'])
        self.assertNotIn('WeatherNext', json.dumps(self.package['events']))

    def test_family_announcement_not_metadata_or_upload(self):
        r = self.event
        self.assertEqual(r['weights_release_date'], '2025-07-09')
        self.assertEqual(r['event_precision']['weights'], 'day_official_family_release_statement')
        self.assertIsNone(r['first_upload_timestamp'])
        self.assertIsNone(r['paper_date'])
        self.assertIsNone(r['code_release_date'])
        date_evidence = [e for e in r['evidence'] if 'weights_release_date' in e['supports']]
        self.assertEqual([e['url'] for e in date_evidence], ['https://developers.googleblog.com/en/t5gemma/'])
        self.assertIn('不以集合 Updated 日期', ''.join(r['notes']))

    def test_current_terms_and_gate_not_backdated(self):
        r = self.event
        self.assertEqual(r['verified_on'], '2026-11-01')
        lic = r['licenses'][0]
        self.assertEqual(lic['terms_last_modified'], '2026-04-01')
        self.assertEqual(lic['reviewed_on'], '2026-11-01')
        self.assertIsNone(lic['at_initial_release'])
        self.assertIsNone(r['initial_release_weights_license'])
        self.assertFalse(lic['full_license_text_reviewed'])
        self.assertIn('登录并同意', r['access_note'])
        self.assertIn('未接受条款、未下载', r['access_note'])
        self.assertEqual(r['open_source_ai_status'], 'not_assessed_do_not_infer_from_weights')

    def test_projection_preserves_boundaries(self):
        before = copy.deepcopy(self.package)
        row, = curated_rows(self.package)
        self.assertEqual(before, self.package)
        self.assertEqual(row['checked_at'], '2026-11-01')
        self.assertEqual(row['date'], '2025-07-09')
        self.assertIn('日期依据官方家族开放声明', row['note'])
        self.assertIn('开放权重不自动构成开源认证', row['note'])
        self.assertIn('首次上传时间未知', row['note'])
        self.assertIn('登录并同意', row['raw']['access_note'])

    def test_no_existing_member_duplicate(self):
        own = set(self.event['included_models'])
        for path in (ROOT / 'curated/monthly').glob('*.json'):
            if path.name == NAME:
                continue
            package = json.loads(path.read_text())
            for row in package.get('events', package.get('records', [])):
                self.assertFalse(own.intersection(row.get('included_models', [])))
        old = json.loads((ROOT / 'docs/monthly-releases.json').read_text())
        for row in old['records']:
            if row['id'] == 'curated-' + self.event['id']:
                continue  # Allows subsequent root integration/rebuild.
            self.assertFalse(own.intersection(row.get('included_models', [])))

if __name__ == '__main__':
    unittest.main()
