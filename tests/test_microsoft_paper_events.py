"""Pinned Microsoft paper chronology, not inferred model or weights releases."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import historical_events as h

EXPECTED = [
    ('2506.14665v1', 'paper', '2025-06-17T15:56:56Z', '2025-06-17'),
    ('2506.14665v2', 'paper_revision', '2025-06-18T08:39:15Z', '2025-06-17'),
    ('2506.14665v3', 'paper_revision', '2025-06-23T17:52:42Z', '2025-06-17'),
    ('2507.06607v1', 'paper', '2025-07-09T07:27:00Z', '2025-07-09'),
    ('2507.06607v2', 'paper_revision', '2025-07-16T07:00:01Z', '2025-07-09'),
    ('2507.23779v1', 'paper', '2025-07-31T17:59:09Z', '2025-07-31'),
]


class MicrosoftPaperEvents(unittest.TestCase):
    def setUp(self):
        self.package = h.load(ROOT / 'curated/historical-events/zzzzz-microsoft-paper-nov2.json')

    def test_six_exact_version_kind_utc_date_and_source_tuples(self):
        self.assertEqual(len(self.package['events']), 6)
        for row, (version, kind, stamp, first) in zip(h.project(self.package), EXPECTED):
            with self.subTest(version=version):
                self.assertEqual(row['version'], 'arXiv:' + version)
                self.assertEqual(row['kind'], kind)
                self.assertEqual(row['date'], stamp[:10])
                self.assertEqual(row['month'], stamp[:7])
                self.assertEqual(row['raw']['timestamp_utc'], stamp)
                self.assertEqual(row['raw']['first_paper_submission'], first)
                self.assertEqual(row['sources'], ['https://arxiv.org/abs/' + version])
                self.assertEqual(row['checked_at'], '2026-11-02')
                self.assertEqual(row['providers'], ['Microsoft'])
                self.assertIn(stamp[11:19] + ' UTC', row['summary'])

    def test_historical_titles_and_specific_revision_limits(self):
        events = self.package['events']
        titles = ['Accurate and scalable exchange-correlation with deep learning'] * 3 + [
            'Decoder-Hybrid-Decoder Architecture for Efficient Reasoning with Long Generation'
        ] * 2 + ['Phi-Ground Tech Report: Advancing Perception in GUI Grounding']
        for row, title in zip(events, titles):
            for lang in ('zh', 'en'):
                self.assertIn(title, row['summary'][lang])
        self.assertIn('Safari PDF', events[1]['summary']['en'])
        self.assertIn('figure 1 and part of figure 5', events[1]['summary']['en'])
        self.assertIn('author information and a typo', events[2]['summary']['en'])
        self.assertIn('no revision reason', events[4]['note']['en'])
        self.assertIn('full-text differences were not checked', events[4]['note']['en'])
        self.assertIn('October v3 does not substitute for July v2', events[4]['note']['en'])
        self.assertIn('August 2025', events[5]['note']['en'])
        self.assertIn('selected v1 input/output section', events[5]['note']['en'])
        self.assertIn('另读 v1 正文输入/输出小节', events[5]['note']['zh'])
        self.assertNotIn('本轮只核对', events[5]['note']['zh'])

    def test_semantic_modality_not_paper_document_format(self):
        rows = h.project(self.package)
        self.assertEqual([r['modalities'] for r in rows], [['未登记']] * 3 + [['text']] * 2 + [['text', 'image']])
        self.assertIn('paper text is not a model text modality', rows[0]['raw']['note']['en'])

    def test_unknowns_and_no_execution_or_license_backfill(self):
        before = copy.deepcopy(self.package)
        for row in h.project(self.package):
            raw = row['raw']
            self.assertEqual(row['license'], [])
            self.assertEqual(row['nodes'], [])
            self.assertNotIn('weight_entries', row)
            self.assertEqual(raw['context_sources'], [])
            for key in ('api_alias', 'first_public_weights_date', 'pinned_api_revision'):
                self.assertIsNone(raw[key])
            self.assertEqual(raw['execution_status'], 'not_executed')
            self.assertIn('not six new models or weights releases', raw['note']['en'])
            self.assertIn('cannot be backdated', raw['note']['en'])
        self.assertEqual(self.package, before)

    def test_original234_exact_prefix_and_default97_unchanged(self):
        rows = json.loads((ROOT / 'dist/monthly-releases.json').read_text())['records']
        baseline = json.loads((ROOT / 'tests/fixtures/pre-microsoft-paper-events-digest.json').read_text())
        self.assertEqual(len(rows), 244)
        self.assertEqual(baseline['count'], 234)
        self.assertEqual([r['id'] for r in rows[:234]], baseline['ids'])
        digest = hashlib.sha256(json.dumps(rows[:234], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        self.assertEqual(digest, baseline['records_sha256'])
        self.assertEqual(rows[234:240], h.project(self.package))
        self.assertEqual(len({r['id'] for r in rows}), 244)
        weights = [r for r in rows if r['kind'] in ('weights', 'weights_announcement', 'weights_undated')]
        self.assertEqual(len(weights), 97)
        self.assertEqual(sum(bool(r['month']) for r in weights), 76)
        self.assertEqual(sum(not r['month'] for r in weights), 21)

    def test_all_six_reject_unpinned_and_other_version_evidence(self):
        for index, (version, _, _, _) in enumerate(EXPECTED):
            for source in ('https://arxiv.org/abs/' + version.split('v')[0],
                           'https://arxiv.org/abs/' + version.split('v')[0] + ('v2' if version.endswith('v1') else 'v1'),
                           'https://arxiv.org/abs/9999.99999' + version[version.index('v'):]):
                with self.subTest(index=index, source=source):
                    package = copy.deepcopy(self.package)
                    package['events'][index]['evidence'][0]['url'] = source
                    with self.assertRaises(ValueError):
                        h.validate(package)

    def test_all_six_reject_inferred_release_and_timezone_mutations(self):
        for index, (_, _, stamp, _) in enumerate(EXPECTED):
            for field, value in [('kind', 'weights_release'), ('first_public_weights_date', stamp[:10]),
                                 ('pinned_api_revision', 'borrowed'), ('api_alias', 'borrowed'),
                                 ('execution_status', 'tested'), ('checked_at', stamp[:10]),
                                 ('timestamp_utc', stamp[:-1] + '+08:00'),
                                 ('timestamp_utc', '2025-01-01' + stamp[10:])]:
                with self.subTest(index=index, field=field):
                    package = copy.deepcopy(self.package)
                    package['events'][index][field] = value
                    with self.assertRaises(ValueError):
                        h.validate(package)

    def test_duplicate_identity_and_cross_package_collision_rejected(self):
        duplicate = copy.deepcopy(self.package)
        row = copy.deepcopy(duplicate['events'][0])
        row['id'] = 'renamed-skala-duplicate'
        duplicate['events'].append(row)
        with self.assertRaises(ValueError):
            h.validate(duplicate)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / 'a.json').write_text(json.dumps(self.package))
            second = copy.deepcopy(self.package)
            for row in second['events']:
                row['id'] += '-duplicate'
            (path / 'b.json').write_text(json.dumps(second))
            with self.assertRaises(ValueError):
                h.collect(path, set())

    def test_old_snapshot_retained_new_snapshot_and_published_data_match(self):
        old = json.loads((ROOT / 'learning/coverage/2026-11-02-tspulse/snapshot.json').read_text())
        new = json.loads((ROOT / 'learning/coverage/2026-11-02-microsoft-paper/snapshot.json').read_text())
        self.assertEqual(old['monthly']['events'], 234)
        self.assertEqual(new['monthly']['events'], 240)
        self.assertEqual(new['monthly']['weights_events'], 97)
        self.assertEqual(old['catalog'], new['catalog'])
        self.assertEqual(old['practice'], new['practice'])
        self.assertEqual(hashlib.sha256((ROOT / 'learning/coverage/2026-11-02-microsoft-paper/snapshot.json').read_bytes()).hexdigest(), 'dc0f2fa6fca7a274797cf2f3d6aad6424e0c596f89d311dbb0ffda7f5ddab32a')



if __name__ == '__main__':
    unittest.main()
