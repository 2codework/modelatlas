import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_monthly_curated import validate,valid_url
class AdmissionTests(unittest.TestCase):
 def seed(self):return json.loads((ROOT/'curated/monthly/history-oct31.json').read_text())
 def test_all_packages_pass_without_mutation(self):
  for p in (ROOT/'curated/monthly').glob('*.json'):
   d=json.loads(p.read_text());before=copy.deepcopy(d);self.assertGreater(validate(d),0);self.assertEqual(d,before)
 def test_duplicate_id_rejected(self):
  d=self.seed();d['events'].append(copy.deepcopy(d['events'][0]));self.assertRaises(ValueError,validate,d)
 def test_missing_source_rejected(self):
  d=self.seed();d['events'][0]['evidence']=[];self.assertRaises(ValueError,validate,d)
 def test_credential_and_script_urls_rejected(self):
  for u in ['javascript:alert(1)','https://user:secret@example.org/x','file:///tmp/x','data:text/plain,x']:
   self.assertFalse(valid_url(u));d=self.seed();d['events'][0]['weight_entries']=[u];self.assertRaises(ValueError,validate,d)
 def test_future_release_not_admitted(self):
  d=self.seed();d['events'][0]['weights_release_date']='2030-01-01';self.assertRaises(ValueError,validate,d)
 def test_date_needs_linked_evidence(self):
  d=self.seed()
  for s in d['events'][0]['evidence']:s['supports']=[]
  self.assertRaises(ValueError,validate,d)
 def test_license_source_required(self):
  d=self.seed();d['events'][0]['licenses'][0]['url']='';self.assertRaises(ValueError,validate,d)
 def test_unknown_date_allowed_not_inferred(self):
  d=self.seed();d['events'][0]['weights_release_date']=None;validate(d);self.assertIsNone(d['events'][0]['weights_release_date'])
