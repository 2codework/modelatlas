"""Book-helper probes only: synthetic extra edges are NOT production admissions."""
import copy
import hashlib
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import knowledge_graph_links as K


class RelationBookStability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'dist/data.json').read_text())
        cls.ids = json.loads((ROOT / K.REL / 'admission.json').read_text())['accepted_candidate_ids']
        cls.expected = K.book(cls.data)

    def setUp(self):
        self.data = copy.deepcopy(type(self).data)

    def edge(self):
        return next(e for e in self.data['edges'] if e.get('id') == self.ids[0])

    def test_current_real_output_fixed_baseline(self):
        self.assertEqual(hashlib.sha256('\n'.join(self.expected).encode()).hexdigest(), '7f39ad9f5405a7cea6e99363e055e17d1db54441063be365998bcd34ae43ced8')
        self.assertEqual([line.split(' · ')[0][4:] for line in self.expected if line.startswith('### ')], self.ids)

    def test_unrelated_later_edge_does_not_change_chapter(self):
        self.data['edges'].append({'id': 'synthetic-unadmitted-probe', 'source': 'probe-a', 'target': 'probe-b'})
        self.assertEqual(K.book(self.data), self.expected)

    def test_edge_array_reorder_retains_admitted_order(self):
        self.data['edges'].reverse()
        self.assertEqual(K.book(self.data), self.expected)

    def test_missing_stage_edge_rejected(self):
        self.data['edges'].remove(self.edge())
        with self.assertRaisesRegex(ValueError, 'book missing stage edge'): K.book(self.data)

    def test_duplicate_stage_edge_rejected(self):
        self.data['edges'].insert(0, copy.deepcopy(self.edge()))
        with self.assertRaisesRegex(ValueError, 'book duplicate stage edge'): K.book(self.data)

    def test_duplicate_record_rejected(self):
        records = self.data['knowledge_graph_links_application']['records']
        records[1] = copy.deepcopy(records[0])
        with self.assertRaisesRegex(ValueError, 'book candidate identity/order'): K.book(self.data)

    def test_missing_record_rejected(self):
        self.data['knowledge_graph_links_application']['records'].pop()
        with self.assertRaisesRegex(ValueError, 'book application records'): K.book(self.data)

    def test_reordered_application_rejected(self):
        self.data['knowledge_graph_links_application']['records'].reverse()
        with self.assertRaisesRegex(ValueError, 'book candidate identity/order'): K.book(self.data)

    def test_wrong_stage_rejected(self):
        self.edge()['admission_id'] = 'another-stage'
        with self.assertRaisesRegex(ValueError, 'book stage binding'): K.book(self.data)

    def test_unknown_stage_edge_rejected(self):
        extra = copy.deepcopy(self.edge()); extra['id'] = 'synthetic-unregistered-stage-edge'
        self.data['edges'].append(extra)
        with self.assertRaisesRegex(ValueError, 'book unregistered stage edge'): K.book(self.data)

    def test_modified_candidate_rejected(self):
        self.edge()['explanation_zh'] += ' synthetic drift'
        with self.assertRaisesRegex(ValueError, 'book candidate content mismatch'): K.book(self.data)

    def test_record_hash_mismatch_rejected(self):
        self.data['knowledge_graph_links_application']['records'][0]['candidate_object_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'book candidate hash binding'): K.book(self.data)

    def test_source_binding_mismatch_rejected(self):
        self.data['knowledge_graph_links_application']['records'][0]['source_object_sha256'] = {}
        with self.assertRaisesRegex(ValueError, 'book source binding'): K.book(self.data)

    def test_missing_application_with_stage_rejected(self):
        del self.data['knowledge_graph_links_application']
        with self.assertRaisesRegex(ValueError, 'book missing application'): K.book(self.data)

    def referenced_source(self):
        sid = self.edge()['source_ids'][0]
        return next(source for source in self.data['sources'] if source['id'] == sid)

    def test_missing_referenced_source_rejected(self):
        self.data['sources'].remove(self.referenced_source())
        with self.assertRaisesRegex(ValueError, 'book missing referenced source'): K.book(self.data)

    def test_duplicate_referenced_source_rejected(self):
        self.data['sources'].append(copy.deepcopy(self.referenced_source()))
        with self.assertRaisesRegex(ValueError, 'book duplicate referenced source'): K.book(self.data)

    def test_referenced_source_url_drift_rejected(self):
        self.referenced_source()['url'] = 'https://synthetic.invalid/drift'
        with self.assertRaisesRegex(ValueError, 'book referenced source content mismatch'): K.book(self.data)

    def test_referenced_source_other_field_drift_rejected(self):
        self.referenced_source()['synthetic_extra_field'] = 'unapproved'
        with self.assertRaisesRegex(ValueError, 'book referenced source content mismatch'): K.book(self.data)

    def test_unrelated_extra_source_and_edge_leave_chapter_unchanged(self):
        # Helper-only synthetic probe, not an approved production source/edge.
        self.data['sources'].append({'id': 'synthetic-unreferenced-source', 'url': 'https://synthetic.invalid/'})
        self.data['edges'].append({'id': 'synthetic-unrelated-edge'})
        self.assertEqual(K.book(self.data), self.expected)

    def test_application_qa_binding_rejected(self):
        self.data['knowledge_graph_links_application']['qa_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'book application identity binding: qa_sha256'): K.book(self.data)

    def test_application_research_binding_rejected(self):
        self.data['knowledge_graph_links_application']['research_manifest_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'book application identity binding: research_manifest_sha256'): K.book(self.data)

    def test_application_baseline_binding_rejected(self):
        self.data['knowledge_graph_links_application']['baseline_commit'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'book application identity binding: baseline_commit'): K.book(self.data)

    def test_application_identity_status_drift_rejected(self):
        for field in ('schema_version', 'status', 'raw_candidate_status'):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['knowledge_graph_links_application'][field] = 'synthetic-drift'
                with self.assertRaisesRegex(ValueError, 'book application identity/status'): K.book(data)

    def test_no_stage_retains_empty_book_behavior(self):
        del self.data['knowledge_graph_links_application']
        self.data['edges'] = [e for e in self.data['edges'] if e.get('id') not in self.ids]
        self.assertEqual(K.book(self.data), [])


class BookOnlySourceContract(unittest.TestCase):
    def test_approved_exception_retains_original_nonbook_bytes(self):
        from relation_book_contract import validate
        validate()

    def test_unknown_book_change_rejected(self):
        from relation_book_contract import validate
        current = (ROOT / 'scripts/knowledge_graph_links.py').read_bytes()
        changed = current.replace(b'def book(data):', b'def book(data):\n # unapproved book change', 1)
        with self.assertRaisesRegex(ValueError, 'approved current module SHA'): validate(current=changed)

    def test_nonbook_change_rejected_independently_of_pin(self):
        from relation_book_contract import BASELINE_PATH, validate, validate_nonbook
        current = (ROOT / 'scripts/knowledge_graph_links.py').read_bytes()
        changed = current.replace(b'def apply(data,root):', b'def apply(data,root):\n # nonbook drift', 1)
        with self.assertRaisesRegex(ValueError, 'approved current module SHA'): validate(current=changed)
        with self.assertRaisesRegex(ValueError, 'nonbook source changed'): validate_nonbook(changed, BASELINE_PATH.read_bytes())

    def test_archived_baseline_tampering_rejected(self):
        from relation_book_contract import BASELINE_PATH, validate
        with self.assertRaisesRegex(ValueError, 'archived baseline SHA'): validate(baseline=BASELINE_PATH.read_bytes() + b'\n')


if __name__ == '__main__': unittest.main()
