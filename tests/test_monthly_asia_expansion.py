"""Finite Asian-provider availability evidence and scope boundaries."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows

class AsiaExpansionTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / 'curated/monthly/asia-expansion-oct31.json').read_text())
        self.events = self.package['events']

    def test_four_dated_announcements_not_uploads(self):
        self.assertEqual(validate(self.package), 4)
        self.assertFalse(self.package['exhaustive'])
        self.assertEqual([e['weights_release_date'] for e in self.events], ['2025-06-16','2025-06-21','2025-07-02','2026-08-03'])
        for e in self.events:
            self.assertEqual(e['month'], e['weights_release_date'][:7])
            self.assertEqual(e['event_type'], 'weights_release_announcement')
            for key in ['first_upload_timestamp','code_release_date','api_release_date']:
                self.assertIsNone(e[key])

    def test_exact_and_family_scopes(self):
        self.assertEqual([len(e['included_models']) for e in self.events],[2,1,1,2])
        self.assertEqual([e['event_granularity'] for e in self.events], ['family_release','exact_model','exact_model','family_release'])
        self.assertEqual(self.events[1]['included_models'],['moonshotai/Kimi-VL-A3B-Thinking-2506'])
        self.assertEqual(self.events[2]['included_models'],['zai-org/GLM-4.1V-9B-Thinking'])
        self.assertEqual(self.events[3]['included_models'],['MiniMaxAI/MiniMax-H3:FL2VA/','MiniMaxAI/MiniMax-H3:Ref2VA/'])

    def test_paper_api_and_license_dates_separate(self):
        self.assertEqual([e['paper_date'] for e in self.events],['2025-06-16',None,'2025-07-01',None])
        self.assertEqual(self.events[0]['api_announcement_date'],'2025-06-16')
        self.assertEqual(self.events[3]['license_date'],'2026-08-02')
        self.assertNotEqual(self.events[3]['license_date'], self.events[3]['weights_release_date'])
        self.assertTrue(any('/2507.01006v1' in s['url'] for s in self.events[2]['evidence']))

    def test_h3_restrictions_and_hosted_scope_are_visible(self):
        e=self.events[3]
        self.assertEqual(e['licenses'][0]['name'],'MiniMax H3 Community License Agreement')
        self.assertEqual(e['licenses'][0]['review_status'],'official_full_license_text_inspected')
        for text in ['地域限制','托管 API','全本地','零费用']:
            self.assertIn(text,e['access_note'])
            self.assertIn(text,curated_rows(self.package)[3]['note'])
        joined=''.join(e['notes'])
        for text in ['768p','H3-Context-IR','H3-Regenerate-2K']:
            self.assertIn(text,joined)
        lic=e['evidence'][-1]
        self.assertIn('IV.1',lic['evidence_locator'])
        for text in ['欧盟','英国','韩国','美国','2000 万美元']:
            self.assertIn(text,lic['summary_zh'])

    def test_license_declarations_do_not_spread_to_code(self):
        self.assertEqual([e['licenses'][0]['name'] for e in self.events[:3]],['Apache-2.0','MIT','MIT'])
        for e in self.events[:3]:
            self.assertIn('未逐条审核',e['licenses'][0]['review_note'])
            self.assertIsNone(e['code_license'])

    def test_adapter_readonly_dedupe_and_no_private_provenance(self):
        before=copy.deepcopy(self.package)
        rows=curated_rows(self.package)
        self.assertEqual(before,self.package)
        self.assertEqual(len(rows),4)
        self.assertTrue(all(r['kind']=='weights_announcement' for r in rows))
        ids={e['id'] for e in self.events}
        for path in (ROOT/'curated/monthly').glob('*.json'):
            if path.name=='asia-expansion-oct31.json': continue
            data=json.loads(path.read_text())
            self.assertFalse(ids & {e['id'] for e in data.get('events',data.get('records',[]))})
        for forbidden in ['campus-rollout','/workspace/','transcript_evidence']:
            self.assertNotIn(forbidden,json.dumps(self.package))

if __name__=='__main__': unittest.main()
