"""Historical release boundaries for the October 31 source-backed supplement."""
import copy
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import monthly_releases as monthly

PACKAGE = ROOT / 'curated/monthly/history-oct31.json'


class October31HistoryTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads(PACKAGE.read_text())
        self.events = self.package['events']
        self.by_id = {event['id']: event for event in self.events}

    def test_twelve_dated_events_no_held_phi4(self):
        self.assertEqual(len(self.events), 12)
        self.assertEqual(len(self.by_id), 12)
        self.assertFalse(any('phi4' in e['id'] for e in self.events))
        for event in self.events:
            self.assertEqual(event['month'], event['weights_release_date'][:7])
            self.assertTrue(any('weights_release_date' in s['supports'] for s in event['evidence']))
            for field in ('first_upload_timestamp', 'paper_date', 'code_release_date'):
                self.assertIsNone(event[field])

    def test_adapter_preserves_dates_and_is_read_only(self):
        before = copy.deepcopy(self.package)
        rows = monthly.curated_rows(self.package)
        self.assertEqual(self.package, before)
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(r['kind'] == 'weights_announcement' for r in rows))
        self.assertEqual({r['date'] for r in rows}, {
            '2024-02-21', '2024-04-23', '2024-05-06', '2024-05-16',
            '2024-06-27', '2024-07-31', '2024-08-29', '2024-09-19',
            '2024-10-21', '2024-11-12', '2025-03-12'})

    def test_unique_against_existing_projection_and_all_curated_packages(self):
        base = monthly.project(json.loads((ROOT / 'dist/data.json').read_text()))['records']
        rows = list(base)
        for path in sorted((ROOT / 'curated/monthly').glob('*.json')):
            rows.extend(monthly.curated_rows(json.loads(path.read_text())))
        ids = [r['id'] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        # Same checkpoint/day must not be repeated under distinct curated IDs.
        pairs = []
        for path in sorted((ROOT / 'curated/monthly').glob('*.json')):
            package = json.loads(path.read_text())
            for e in package.get('events', package.get('records', [])):
                for name in e.get('included_models', []):
                    pairs.append((name, e.get('weights_release_date')))
        self.assertEqual(len(pairs), len(set(pairs)))

    def test_qwen_coder_launch_does_not_backdate_expansion(self):
        initial = self.by_id['qwen25-coder-initial-2024-09-19']
        expansion = self.by_id['qwen25-coder-expansion-2024-11-12']
        self.assertEqual(len(initial['included_models']), 4)
        self.assertEqual(len(expansion['included_models']), 8)
        self.assertTrue(all(any('-'+s in m for s in ['1.5B', '7B']) for m in initial['included_models']))
        self.assertFalse(set(initial['included_models']) & set(expansion['included_models']))
        self.assertEqual(expansion['weights_release_date'], '2024-11-12')
        self.assertEqual(len(expansion['licenses']), 2)

    def test_qwen_vl_excludes_api_only_72b(self):
        event = self.by_id['qwen2-vl-initial-2024-08-29']
        self.assertEqual(event['included_models'], ['Qwen2-VL-2B-Instruct', 'Qwen2-VL-7B-Instruct'])
        self.assertIn('72B', event['notes'][0])
        self.assertEqual(event['modality']['input'], ['text', 'image', 'video'])

    def test_gemma_sizes_and_dates_remain_separate(self):
        initial = self.by_id['gemma2-initial-2024-06-27']
        addition = self.by_id['gemma2-2b-2024-07-31']
        self.assertEqual(initial['weights_release_date'], '2024-06-27')
        self.assertEqual(addition['weights_release_date'], '2024-07-31')
        self.assertFalse(any('-2b' in x for x in initial['included_models']))
        self.assertEqual(set(addition['included_models']), {'gemma-2-2b', 'gemma-2-2b-it'})
        gemma3 = self.by_id['gemma3-initial-2025-03-12']
        self.assertEqual(len(gemma3['included_models']), 8)
        self.assertIn('1B 仅文本', gemma3['modality']['scope_note'])
        self.assertNotIn('audio', gemma3['modality']['input'])

    def test_model_and_code_license_scopes_are_not_conflated(self):
        qwen = self.by_id['qwen25-initial-2024-09-19']
        self.assertEqual(len(qwen['licenses']), 3)
        self.assertEqual({l['name'] for l in qwen['licenses']}, {'Apache-2.0', 'Qwen Research License', 'Qwen License'})
        for key in ['deepseek-v2-base-2024-05-06', 'deepseek-v2-lite-base-2024-05-16']:
            event = self.by_id[key]
            self.assertEqual(len(event['included_models']), 1)
            self.assertEqual(event['licenses'][0]['name'], 'DeepSeek License Agreement v1.0')
            self.assertIn('仅仓库代码', event['licenses'][1]['applies_to'])
        self.assertIn('未核定发布日许可', self.by_id['phi3-mini-2024-04-23']['licenses'][0]['applies_to'])

    def test_downloads_modalities_and_chinese_caveats(self):
        for event in self.events:
            self.assertTrue(event['notes'])
            self.assertTrue(event['modality']['input'])
            self.assertEqual(event['modality']['output'], ['text'])
            self.assertTrue(any('modality' in s['supports'] for s in event['evidence']))
            self.assertTrue(event['weight_entries'])
            for url in event['weight_entries']:
                self.assertEqual(urlparse(url).hostname, 'huggingface.co')
            for license_record in event['licenses']:
                self.assertTrue(license_record['applies_to'])
                self.assertNotIn('scope', license_record)
            for text in [event['name'], *event['notes'], *(l['applies_to'] for l in event['licenses'])]:
                self.assertTrue(any('\u4e00' <= c <= '\u9fff' for c in text), text)
            self.assertNotIn('uncertainty', event)
            self.assertNotIn('status', event)

    def test_granite_excludes_other_model_families(self):
        event = self.by_id['granite3-dense-2024-10-21']
        self.assertEqual(set(event['included_models']), {
            'granite-3.0-2b-base', 'granite-3.0-2b-instruct',
            'granite-3.0-8b-base', 'granite-3.0-8b-instruct'})
        self.assertEqual(event['weights_release_date'], '2024-10-21')
        self.assertIn('未能读取', event['licenses'][0]['review_note'])


if __name__ == '__main__':
    unittest.main()
