"""Offline contract checks for the Oct 31 evidence supplement; no network or build."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import monthly_releases


class RecentOct31Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads((ROOT / 'curated/monthly/recent-oct31.json').read_text())
        cls.rows = cls.package['records']

    def test_six_exact_current_candidates_not_future_promises(self):
        self.assertEqual({r['model_name'] for r in self.rows}, {
            'GLM-5.3', 'GLM-5.3-Flash', 'Timestral-5M', 'Timestral-28M',
            'Timestral-123M', 'Timestral-209M'})
        self.assertTrue(all(r['event_granularity'] == 'exact_model' for r in self.rows))
        self.assertTrue(all(r['availability'] == 'open_weights' for r in self.rows))

    def test_no_unsupported_weight_dates_or_month_counts(self):
        for r in self.rows:
            self.assertIsNone(r['weights_release_date'])
            self.assertIsNone(r['first_upload_timestamp'])
            self.assertFalse(r['monthly_open_weights_eligible'])
            self.assertIsNone(r['monthly_open_weights_month'])
            self.assertTrue(r['uncertainties'])
            self.assertTrue(r['notes'])
        self.assertEqual(self.package['monthly_open_weights'], {})

    def test_announcement_dates_have_explicit_primary_evidence(self):
        for r in self.rows:
            if r['model_name'].startswith('Timestral-'):
                self.assertEqual(r['announcement_date'], '2026-10-15')
                self.assertTrue(any(e['url'] == 'https://mistral.ai/news/timestral/'
                                    and 'announcement_date' in e['supports'] for e in r['evidence']))
            else:
                self.assertIsNone(r['announcement_date'])

    def test_licenses_and_modalities_do_not_leak_between_models(self):
        by_name = {r['model_name']: r for r in self.rows}
        self.assertIsNone(by_name['GLM-5.3']['license']['spdx_id'])
        self.assertEqual(by_name['GLM-5.3']['license']['name'], 'GLM-5.3 License')
        self.assertEqual(by_name['GLM-5.3-Flash']['license']['spdx_id'], 'MIT')
        self.assertEqual(by_name['GLM-5.3']['modalities']['input'], ['text'])
        self.assertIn('image', by_name['GLM-5.3-Flash']['modalities']['input'])
        for r in self.rows:
            self.assertIn(r['model_name'], r['license']['applies_to'])
            if r['model_name'].startswith('Timestral-'):
                self.assertEqual(r['license']['name'], 'Modified MIT')
                self.assertIsNone(r['license']['spdx_id'])
                self.assertEqual(r['code_license']['spdx_id'], 'Apache-2.0')
                self.assertEqual(r['modalities']['input'], ['time_series'])
                self.assertNotIn('text', r['modalities']['output'])

    def test_adapter_is_readonly_and_preserves_uncertainty_and_links(self):
        before = copy.deepcopy(self.package)
        projected = monthly_releases.curated_rows(self.package)
        self.assertEqual(self.package, before)
        self.assertEqual(len(projected), 6)
        for source, row in zip(self.rows, projected):
            self.assertIsNone(row['date'])
            self.assertIsNone(row['month'])
            self.assertEqual(row['weight_entries'], [source['official_weights_url']])
            self.assertEqual(row['raw']['uncertainties'], source['uncertainties'])
            self.assertEqual(row['curated_licenses'][0]['applies_to'], source['license']['applies_to'])

    def test_ids_do_not_collide_with_existing_packages(self):
        ids = []
        for path in (ROOT / 'curated/monthly').glob('*.json'):
            p = json.loads(path.read_text())
            ids.extend(r['id'] for r in monthly_releases.curated_rows(p))
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == '__main__':
    unittest.main()
