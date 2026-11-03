"""Finite July/August supplement: date semantics, checkpoint and license scope."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
from monthly_releases import curated_rows

class JulyAugustGapTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT/'curated/monthly/gaps-july-august-oct31.json').read_text())
        self.events = self.package['events']
        self.models = {m:r for r in self.events for m in r['included_models']}

    def test_admission_finite_scope(self):
        self.assertEqual(validate(self.package), 6)
        self.assertFalse(self.package['exhaustive'])
        self.assertEqual(len(self.package['coverage']['searched_providers']), 2)
        self.assertEqual(len(self.package['coverage']['unsearched_providers']), 18)
        self.assertEqual([sum(r['month']==m for r in self.events) for m in ['2025-07','2026-08']], [3,3])

    def test_august_official_news_not_api_promise(self):
        for model, date in [('Qwen3.8-2.4T-A95B','2026-08-12'),('Qwen3.8-27B','2026-08-14'),('Qwen3.8-Flash-Next','2026-08-26')]:
            r=self.models[model]
            self.assertEqual(r['weights_release_date'],date)
            e=next(e for e in r['evidence'] if 'weights_release_date' in e['supports'])
            self.assertTrue(e['url'].startswith('https://github.com/QwenLM/Qwen3.8'))
            self.assertIn(date,e['locator'])
            self.assertEqual(e['explicit_date_text'],date)

    def test_license_scope_not_repo_license(self):
        expected={'Qwen3.8-2.4T-A95B':'qwen3.8-max','Qwen3.8-27B':'Apache-2.0','Qwen3.8-Flash-Next':'qwen-community-1.0'}
        for model,license_name in expected.items():
            self.assertEqual(self.models[model]['licenses'][0]['name'],license_name)
        for r in self.events:
            self.assertIsNone(r['code_license'])
            for lic in r['licenses']:
                self.assertFalse(lic['full_license_text_reviewed'])
                self.assertIn('模型权重',lic['applies_to'])

    def test_family_and_july_exact_scope(self):
        v=self.models['Voxtral-Small-24B-2507']
        self.assertEqual(v['event_granularity'],'family_release')
        self.assertEqual(v['included_models'],['Voxtral-Small-24B-2507','Voxtral-Mini-3B-2507'])
        self.assertEqual(self.models['Qwen3-235B-A22B-Instruct-2507']['weights_release_date'],'2025-07-21')
        self.assertEqual(self.models['Qwen3-235B-A22B-Thinking-2507']['weights_release_date'],'2025-07-25')

    def test_projection_preserves_unknowns(self):
        before=copy.deepcopy(self.package)
        rows=curated_rows(self.package)
        self.assertEqual(self.package,before)
        self.assertEqual(len(rows),6)
        for r in rows:
            self.assertEqual(r['kind'],'weights_announcement')
            for field in ['first_upload','paper','code']: self.assertIsNone(r['date_details'][field])
            self.assertIn('首次上传',r['note'])
            self.assertIn('未复核完整许可文本',r['note'])

    def test_no_duplicate_curated_checkpoint_day(self):
        pairs=[]
        for path in (ROOT/'curated/monthly').glob('*.json'):
            p=json.loads(path.read_text())
            for r in p.get('events',p.get('records',[])):
                pairs.extend((m,r.get('weights_release_date')) for m in r.get('included_models',[]))
        self.assertEqual(len(pairs),len(set(pairs)))

if __name__=='__main__': unittest.main()
