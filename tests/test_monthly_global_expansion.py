"""Finite provider-month supplement: identity, evidence and historical semantics."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows

class GlobalExpansionTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT/'curated/monthly/global-expansion-oct31.json').read_text())
        self.events = self.package['events']

    def test_admission_and_finite_ledger(self):
        self.assertEqual(validate(self.package), 4)
        self.assertFalse(self.package['exhaustive'])
        ledger = self.package['coverage']['ledger']
        self.assertEqual(len(ledger), 12)
        self.assertEqual(len({(r['provider'], r['month']) for r in ledger}), 12)
        self.assertTrue(all(r['status'].startswith('searched_') and not r['exhaustive'] for r in ledger))
        self.assertEqual(sum(r['status']=='searched_candidates_found' for r in ledger), 4)

    def test_dates_and_family_scope(self):
        self.assertEqual([r['weights_release_date'] for r in self.events], ['2025-05-30','2025-07-15','2025-07-31','2026-08-18'])
        self.assertEqual([len(r['included_models']) for r in self.events], [6,2,1,2])
        self.assertEqual([r['event_granularity'] for r in self.events], ['family_release','family_release','exact_model','family_release'])
        self.assertEqual(self.events[1]['paper_date'],'2025-07-15')
        self.assertEqual(self.events[2]['api_release_date'],'2025-07-31')
        for r in self.events:
            self.assertIsNone(r['first_upload_timestamp'])
            self.assertIsNone(r['code_release_date'])
            self.assertIsNone(r['code_license'])
            self.assertIsNone(r['initial_release_weights_license'])
            for field in ['weights_release_date','paper_date','api_release_date']:
                if r[field]: self.assertTrue(any(field in e['supports'] for e in r['evidence']))

    def test_current_licenses_not_backdated(self):
        expected=['Apache-2.0','EXAONE AI Model License Agreement 1.2 - NC','CC-BY-NC-4.0','Apache-2.0']
        for r, name in zip(self.events,expected):
            self.assertEqual(len(r['licenses']),len(r['included_models']))
            for lic in r['licenses']:
                self.assertEqual(lic['name'],name)
                self.assertEqual(lic['reviewed_on'],'2026-10-31')
                self.assertIsNone(lic['at_initial_release'])
                self.assertFalse(lic['full_license_text_reviewed'])
        self.assertIn('不能倒填',''.join(self.events[1]['notes']))
        self.assertTrue(all('已更新' in lic['review_note'] for lic in self.events[1]['licenses']))

    def test_projection_preserves_qualification_and_sources(self):
        before=copy.deepcopy(self.package)
        rows=curated_rows(self.package)
        self.assertEqual(self.package,before)
        self.assertEqual(len(rows),4)
        for source,row in zip(self.events,rows):
            self.assertEqual(row['kind'],'weights_announcement')
            self.assertEqual(row['sources'],list(dict.fromkeys(e['url'] for e in source['evidence'])))
            self.assertIsNone(row['date_details']['first_upload'])
            self.assertIn('首次上传',row['note'])
            self.assertIn('未复核完整许可文本',row['note'])
        self.assertIn('不能倒填',rows[1]['note'])
        self.assertIn('API公告日期为2025-07-31',rows[2]['note'])

    def test_no_same_checkpoint_day_in_other_packages(self):
        own={(m,r['weights_release_date']) for r in self.events for m in r['included_models']}
        for path in (ROOT/'curated/monthly').glob('*.json'):
            if path.name=='global-expansion-oct31.json': continue
            package=json.loads(path.read_text())
            for r in package.get('events',package.get('records',[])):
                for model in r.get('included_models',[]):
                    self.assertNotIn((model,r.get('weights_release_date')),own)

if __name__=='__main__': unittest.main()
