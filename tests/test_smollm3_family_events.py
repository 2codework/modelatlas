"""One family announcement, never an inferred weights date."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class SmolLM3FamilyEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/zzzzzzzzz-smollm3-family-nov2.json')
 def test_identity_members_and_date(self):
  self.assertEqual(len(self.p['events']),1);e=self.p['events'][0]
  for k,v in {'kind':'model_family_announcement','date':'2025-07-08','provider':'Hugging Face','checked_at':'2026-11-02','modalities':['text']}.items():self.assertEqual(e[k],v)
  self.assertEqual([m['name'] for m in e['family_members']],['SmolLM3-3B-Base','SmolLM3-3B'])
  self.assertEqual(e['evidence'][0]['url'],'https://huggingface.co/blog/smollm3')
  for m in e['family_members']:self.assertEqual(m['url'],'https://huggingface.co/HuggingFaceTB/'+m['name']);self.assertEqual(m['source_url'],e['evidence'][0]['url'])
 def test_caveats_capabilities_and_unknowns(self):
  e=self.p['events'][0]
  for lang in ['zh','en']:
   for phrase in ['2025-06-25','Transformers','8 languages','Apache-2.0','2026-11-02']:self.assertIn(phrase,e['note'][lang])
   for phrase in ['3B','64k','YaRN','128k']:self.assertIn(phrase,e['summary'][lang])
  for phrase in ['six main languages','not model announcement','historical license','not historical snapshots','bias','No login']:self.assertIn(phrase,e['note']['en'])
  for k in ['timestamp_utc','api_alias','first_public_weights_date','pinned_api_revision','first_paper_submission']:self.assertIsNone(e[k])
  self.assertEqual(e['execution_status'],'not_executed')
 def test_old243_exact_prefix_and_default_unchanged(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];base=json.loads((ROOT/'tests/fixtures/pre-smollm3-family-events-digest.json').read_text())
  self.assertEqual(base['count'],243);self.assertEqual(len(rows),244);self.assertEqual([e['id'] for e in rows[:243]],base['ids']);self.assertEqual(hashlib.sha256(json.dumps(rows[:243],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),base['records_sha256']);self.assertEqual(rows[243:],h.project(self.p));self.assertEqual(len({e['id'] for e in rows}),244)
  weights=[e for e in rows if e['kind'] in ['weights','weights_announcement','weights_undated']];self.assertEqual(len(weights),97);self.assertEqual(sum(bool(e['month']) for e in weights),76);self.assertEqual(len(json.loads((ROOT/'dist/data.json').read_text())['nodes']),259)
 def test_pure_projection_and_no_license_inference(self):
  before=copy.deepcopy(self.p);e=h.project(self.p)[0];self.assertEqual(self.p,before);self.assertEqual(e['license'],[]);self.assertEqual(e['nodes'],[]);self.assertEqual(len(e['sources']),3);self.assertNotIn('weight_entries',e)
 def test_reject_borrowed_dates_and_member_identity(self):
  for key,value in [('date','2025-06-25'),('api_alias','smollm3'),('timestamp_utc','2025-07-08T00:00:00Z'),('first_public_weights_date','2025-07-08'),('pinned_api_revision','v1'),('first_paper_submission','2025-07-08'),('execution_status','tested'),('family_members',[])]:
   with self.subTest(key=key):
    p=copy.deepcopy(self.p);p['events'][0][key]=value
    with self.assertRaises(ValueError):h.validate(p)
  for key,value in [('name','SmolLM3-3B-Base'),('url','https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base'),('source_url','https://example.test')]:
   p=copy.deepcopy(self.p);p['events'][0]['family_members'][1][key]=value
   with self.assertRaises(ValueError):h.validate(p)
 def test_snapshot_and_current_artifact(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-02-smolvla-paper/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-02-smollm3-family/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],243);self.assertEqual(new['monthly']['events'],244);self.assertEqual(old['catalog'],new['catalog']);self.assertEqual(old['practice'],new['practice'])
  for path in ['dist/monthly-releases.json','docs/monthly-releases.json']:self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),next(v['sha256'] for v in new['provenance'] if v['path'].endswith('dist/monthly-releases.json')))
