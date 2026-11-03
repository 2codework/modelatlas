"""Exact checkpoint dates, gated access and deliberately unresolved date leads."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows
NAME='ai2-baai-sarvam-oct31.json'
class ProviderMonthTests(unittest.TestCase):
    def setUp(self):
        self.package=json.loads((ROOT/'curated/monthly'/NAME).read_text())
        self.events=self.package['events']
    def test_finite_admission(self):
        self.assertEqual(validate(self.package),5)
        self.assertFalse(self.package['exhaustive'])
        ledger=self.package['coverage']['ledger']
        self.assertEqual(len({(r['provider'],r['month']) for r in ledger}),12)
        self.assertTrue(all(not r['exhaustive'] for r in ledger))
        self.assertEqual({r['vendor'] for r in self.events},{'BAAI','Sarvam AI'})
        self.assertNotIn('saaras',' '.join(r['id'] for r in self.events))
    def test_exact_dates_not_family_dates(self):
        dates={r['included_models'][0]:r['weights_release_date'] for r in self.events}
        self.assertEqual(dates,{'sarvamai/sarvam-m':'2025-05-23','BAAI/RoboBrain2.0-7B':'2025-06-06','BAAI/RoboBrain2.0-32B':'2025-07-03','BAAI/RoboBrain2.0-3B':'2025-07-23','sarvamai/sarvam-translate':'2025-06-07'})
        for r in self.events:
            self.assertEqual(r['event_granularity'],'exact_model')
            self.assertIsNone(r['first_upload_timestamp'])
            self.assertIsNone(r['code_release_date'])
            self.assertIsNone(r['initial_release_weights_license'])
        self.assertEqual(self.events[1]['paper_date'],'2025-07-02')
        self.assertEqual(self.events[2]['paper_date'],'2025-07-02')
        self.assertIsNone(self.events[3]['paper_date'])
    def test_gates_and_license_scope(self):
        for r in self.events[1:4]:
            self.assertIn('分享 Hugging Face 信息',r['access_note'])
            self.assertEqual(r['evidence'][0]['url'],r['weight_entries'][0])
            self.assertIsNone(r['code_license'])
        for r in self.events:
            lic=r['licenses'][0]
            self.assertFalse(lic['full_license_text_reviewed'])
            self.assertIsNone(lic['at_initial_release'])
            self.assertEqual(lic['reviewed_on'],'2026-10-31')
    def test_translate_conflict_and_modality(self):
        r=self.events[-1]
        self.assertEqual(r['api_release_date'],'2025-06-01')
        self.assertEqual(r['weights_release_date'],'2025-06-07')
        self.assertEqual(r['licenses'][0]['name'],'GPL-3.0')
        self.assertEqual(r['modality'],{'input':['text'],'output':['text']})
        self.assertIn('Gemma 3',r['access_note'])
        self.assertIn('日期口径并列',''.join(r['notes']))
        self.assertTrue(any('api_release_date' in e['supports'] for e in r['evidence']))
    def test_projection_and_no_mutation(self):
        before=copy.deepcopy(self.package)
        rows=curated_rows(self.package)
        self.assertEqual(before,self.package)
        self.assertEqual(len(rows),5)
        for r in rows:
            self.assertEqual(r['kind'],'weights_announcement')
            self.assertIn('首次上传',r['note'])
            self.assertIn('未复核完整许可文本',r['note'])
            self.assertIsNone(r['date_details']['first_upload'])
        self.assertIn('日期口径并列',rows[-1]['note'])
    def test_no_duplicate_checkpoint_day(self):
        own={(m,r['weights_release_date']) for r in self.events for m in r['included_models']}
        for path in (ROOT/'curated/monthly').glob('*.json'):
            if path.name==NAME:continue
            data=json.loads(path.read_text())
            for r in data.get('events',data.get('records',[])):
                for m in r.get('included_models',[]):
                    self.assertNotIn((m,r.get('weights_release_date')),own)
if __name__=='__main__':unittest.main()
