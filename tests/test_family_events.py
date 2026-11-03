import copy, hashlib, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class FamilyEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/jamba-family-nov1.json')
 def test_exact_family_identity_and_no_openness_inference(self):
  row=h.project(self.p)[0];self.assertEqual(row['kind'],'model_family_announcement');self.assertEqual(row['date'],'2025-07-03');self.assertEqual(len(row['raw']['family_members']),2);self.assertEqual(row['nodes'],[]);self.assertEqual(row['license'],[]);self.assertEqual(row['providers'],['AI21']);self.assertEqual(len(row['sources']),3);self.assertIn('不是权重首次公开日期',row['note'])
 def test_original_225_records_preserved_in_order(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];baseline=json.loads((ROOT/'tests/fixtures/pre-family-events-digest.json').read_text());old=[r for r in rows if r['id'] in set(baseline['ids'])]
  self.assertEqual(len(rows),244);self.assertEqual([r['id'] for r in old],baseline['ids']);self.assertEqual(hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),baseline['records_sha256'])
 def test_family_rejects_borrowed_identity_dates_and_context(self):
  for k,v in [('api_alias','jamba-mini'),('timestamp_utc','2025-07-03T00:00:00Z'),('first_paper_submission','2025-07-03'),('first_public_weights_date','2025-07-03'),('pinned_api_revision','abc'),('execution_status','tested'),('context_sources',[{'url':'https://docs.ai21.com/changelog','role':'api_alias','date':'2025-07-03'}]),('family_members',[])]:
   with self.subTest(key=k):
    p=copy.deepcopy(self.p);p['events'][0][k]=v
    with self.assertRaises(ValueError):h.validate(p)
 def test_members_are_closed_unique_and_linked_to_evidence(self):
  mutations=[lambda m:m.update(extra=True),lambda m:m.update(name=''),lambda m:m.update(url='http://example.test'),lambda m:m.update(url='https://user:secret@example.test'),lambda m:m.update(source_url='https://unrelated.test'),lambda m:m.update(url='https://docs.ai21.com/changelog')]
  for change in mutations:
   p=copy.deepcopy(self.p);change(p['events'][0]['family_members'][0])
   with self.assertRaises(ValueError):h.validate(p)
  for field in ['name','url']:
   p=copy.deepcopy(self.p);m=p['events'][0]['family_members'];m[1][field]=m[0][field]
   with self.assertRaises(ValueError):h.validate(p)
 def test_other_kinds_reject_family_members(self):
  p=h.load(ROOT/'curated/historical-events/deepseek-nov1.json');p['events'][0]['family_members']=self.p['events'][0]['family_members']
  with self.assertRaises(ValueError):h.validate(p)
 def test_old_snapshot_immutable_new_count(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-01-nonweight/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-01-family/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],225);self.assertEqual(new['monthly']['events'],226);self.assertEqual(old['monthly']['weights_events'],new['monthly']['weights_events'])
