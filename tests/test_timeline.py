import copy, importlib.util, json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('timeline_builder',R/'scripts/build.py');B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
class Timeline(unittest.TestCase):
 def setUp(self):
  self.bs=[json.loads(p.read_text()) for p in sorted((R/'data/research').glob('*.json'))]
  self.overlay=next(b for b in self.bs if b.get('event_patches'))
 def test_counts_and_history(self):
  original=copy.deepcopy(self.bs);d=B.normalize(self.bs)
  self.assertEqual(self.bs,original);self.assertEqual(d['research_bundles'],original)
  self.assertEqual((len(d['nodes']),len(d['events']),sum(e.get('date') is not None for e in d['events'])),(148,87,50))
  self.assertEqual(len(d['sources']),138)
 def test_bloom_not_launch_date(self):
  d=B.normalize(self.bs);e=next(e for e in d['events'] if e['id']=='found-event-054')
  self.assertIsNone(e['date']);self.assertIsNone(e['date_precision']);self.assertEqual(e['available_by'],'2022-07-12')
  self.assertIn('不证明API精确首发日期',e['note_zh']);self.assertIn('非首发',B.book(d))
 def test_expected_before_fail_closed(self):
  self.overlay['event_patches'][0]['expected_before']['date']='2020-01-01'
  with self.assertRaisesRegex(ValueError,'expected_before mismatch'):B.normalize(self.bs)
 def test_missing_target(self):
  self.overlay['event_patches'][0]['event_id']='missing'
  with self.assertRaisesRegex(ValueError,'patch target'):B.normalize(self.bs)
 def test_duplicate_patch(self):
  self.overlay['event_patches'].append(copy.deepcopy(self.overlay['event_patches'][0]))
  with self.assertRaisesRegex(ValueError,'duplicate event patch'):B.normalize(self.bs)
 def test_identity_protected(self):
  self.overlay['event_patches'][0]['set']['event_type']='announcement'
  with self.assertRaisesRegex(ValueError,'identity'):B.normalize(self.bs)
 def test_missing_before(self):
  del self.overlay['event_patches'][0]['expected_before']['node_ids']
  with self.assertRaisesRegex(ValueError,'incomplete expected_before'):B.normalize(self.bs)
 def test_available_by_precision(self):
  next(p for p in self.overlay['event_patches'] if p['event_id']=='found-event-054')['set']['available_by']='2022-02-30'
  with self.assertRaisesRegex(ValueError,'invalid available_by'):B.normalize(self.bs)
 def test_scope_and_unknown_timezone(self):
  d=B.normalize(self.bs);events={e['id']:e for e in d['events']}
  self.assertEqual(events['found-event-034']['availability_scope'],'private_beta_approved_users')
  self.assertEqual(events['found-event-058']['availability_scope'],'public_preview_vertex_ai')
  for p in self.overlay['event_patches']:self.assertIsNone(events[p['event_id']]['timezone'])
  book=B.book(d)
  for token in ['private_beta_approved_users','public_preview_vertex_ai','https://huggingface.co/mistralai/Mistral-7B-v0.1']:self.assertIn(token,book)
 def test_unrelated_unknowns_unchanged(self):
  d=B.normalize(self.bs);base=next(b for b in self.bs if any(e['id']=='found-event-036' for e in b.get('events',[])))
  for eid in ['found-event-036','found-event-037','found-event-038']:
   before=next(e for e in base['events'] if e['id']==eid);after=next(e for e in d['events'] if e['id']==eid)
   self.assertIsNone(after['date']);self.assertEqual(after,before)
