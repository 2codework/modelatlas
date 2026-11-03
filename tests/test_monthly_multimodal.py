"""Modality, licensing and date boundaries for the multimodal supplement."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_monthly_curated import validate
import monthly_releases as monthly


class MultimodalReleaseTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / 'curated/monthly/multimodal-oct31.json').read_text())
        self.events = self.package['events']
        self.by_id = {r['id']: r for r in self.events}

    def test_admission_and_scope(self):
        self.assertEqual(validate(self.package), 11)
        self.assertEqual(sum(bool(r['weights_release_date']) for r in self.events), 10)
        self.assertFalse(any('chatterbox' in r['id'] for r in self.events))
        for r in self.events:
            self.assertIsNone(r['first_upload_timestamp'])
            self.assertIsNone(r['paper_date'])
            self.assertIsNone(r['code_release_date'])
            self.assertTrue(any('\u4e00' <= c <= '\u9fff' for c in r['name']))
            for license_record in r['licenses']:
                self.assertTrue(license_record['applies_to'])
                self.assertTrue(license_record['review_note'])

    def test_whisper_initial_identity_not_current_alias(self):
        r = self.by_id['whisper-initial-2022-09-21']
        self.assertEqual(r['weights_release_date'], '2022-09-21')
        self.assertEqual(len(r['included_models']), 9)
        self.assertIn('large-v1', r['included_models'])
        self.assertNotIn('large', r['included_models'])
        self.assertNotIn('large-v2', r['included_models'])
        self.assertTrue(any(e['url'].endswith('/discussions/661') and 'checkpoint_identity' in e['supports'] for e in r['evidence']))
        self.assertEqual(r['licenses'][0]['name'], 'MIT')

    def test_ltx_versions_have_different_licenses_and_date_evidence(self):
        old = self.by_id['ltx-video-2b-09-undated']
        new = self.by_id['ltx-video-2b-095-2025-03-05']
        self.assertIsNone(old['weights_release_date'])
        self.assertIsNone(old['month'])
        self.assertEqual(old['announcement_date'], '2024-11-21')
        self.assertIn('研究', ''.join(old['notes']))
        self.assertTrue(old['weight_entries'][0].endswith('/ltx-video-2b-v0.9.safetensors'))
        self.assertEqual(new['weights_release_date'], '2025-03-05')
        evidence = [e for e in new['evidence'] if 'weights_release_date' in e['supports']]
        self.assertTrue(evidence)
        self.assertIn('README.md', evidence[0]['url'])
        self.assertIn('New checkpoint', evidence[0]['locator'])
        self.assertNotEqual(old['licenses'][0]['name'], new['licenses'][0]['name'])

    def test_flux_access_is_separate_from_license(self):
        for name in ('dev', 'schnell'):
            r = self.by_id[f'flux1-{name}-2024-08-01']
            self.assertEqual(r['availability'], 'gated_open_weights')
            self.assertIn('接受', ''.join(r['notes']))
            self.assertIn('gated', r['download_verification'])
        self.assertEqual(self.by_id['flux1-schnell-2024-08-01']['licenses'][0]['name'], 'Apache-2.0')
        self.assertIn('Non-Commercial', self.by_id['flux1-dev-2024-08-01']['licenses'][0]['name'])

    def test_modalities_and_model_scope(self):
        self.assertEqual(self.by_id['qwen2-audio-2024-08-09']['modality'], {'input':['audio','text'], 'output':['text']})
        self.assertEqual(self.by_id['wan22-ti2v5b-2025-07-28']['included_models'], ['Wan2.2-TI2V-5B'])
        self.assertEqual(self.by_id['sdxl-base-2023-07-26']['included_models'], ['stable-diffusion-xl-base-1.0'])
        self.assertEqual({m for r in self.events for m in r['modality']['output']}, {'image','video','text'})

    def test_adapter_read_only_and_uncertainty_visible(self):
        before = copy.deepcopy(self.package)
        rows = monthly.curated_rows(self.package)
        self.assertEqual(before, self.package)
        self.assertEqual(len(rows), 11)
        self.assertEqual(sum(r['kind']=='weights_undated' for r in rows), 1)
        for r in rows:
            self.assertIn('不等于', r['note']) if r['date'] else self.assertIn('未核实', r['note'])
        for r in rows:
            if 'flux1-' in r['id']: self.assertIn('接受', r['note'])

    def test_no_duplicate_curated_checkpoint_day(self):
        pairs=[]
        for path in (ROOT / 'curated/monthly').glob('*.json'):
            p=json.loads(path.read_text())
            for r in p.get('events',p.get('records',[])):
                for model in r.get('included_models',[]): pairs.append((model,r.get('weights_release_date')))
        self.assertEqual(len(pairs), len(set(pairs)))

if __name__ == '__main__':
    unittest.main()
