import copy,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import historical_events as h
class LtxApiEvents(unittest.TestCase):
 def setUp(self):self.p=h.load(ROOT/'curated/historical-events/ltx-api-nov1.json')
 def test_exact_two_alias_events_one_source(self):
  rows=h.project(self.p);self.assertEqual(len(rows),2);self.assertEqual([r['raw']['api_alias'] for r in rows],['ltx-2-5-fast','ltx-2-5-pro'])
  for r in rows:
   self.assertEqual(r['kind'],'api_availability_announcement');self.assertEqual(r['date'],'2026-08-11');self.assertEqual(r['providers'],['Lightricks']);self.assertEqual(r['sources'],['https://docs.ltx.io/api-changelog/2026/8/11']);self.assertEqual(r['modalities'],['text','image','audio','video']);self.assertEqual(r['license'],[]);self.assertEqual(r['nodes'],[]);self.assertIsNone(r['raw']['timestamp_utc']);self.assertIsNone(r['raw']['pinned_api_revision']);self.assertIsNone(r['raw']['first_public_weights_date']);self.assertEqual(r['raw']['execution_status'],'not_executed');self.assertIn('同一篇公告',r['note'])
  self.assertIn('最高4K',rows[0]['summary']);self.assertIn('音频输入的视频为1080p',rows[0]['summary']);self.assertIn('720p或1080p',rows[1]['summary']);self.assertNotIn('4K',rows[1]['summary'])
 def test_previous_226_records_byte_semantics_and_order(self):
  rows=json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'];b=json.loads((ROOT/'tests/fixtures/pre-ltx-api-events-digest.json').read_text());old=rows[:226];self.assertEqual(len(rows),244);self.assertEqual([r['id'] for r in old],b['ids']);self.assertEqual(hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),b['records_sha256']);self.assertEqual(sum(r['kind'] in ['weights','weights_announcement','weights_undated'] for r in rows),97)
 def test_old_and_new_snapshots_separate(self):
  old=json.loads((ROOT/'learning/coverage/2026-11-01-family/snapshot.json').read_text());new=json.loads((ROOT/'learning/coverage/2026-11-01-ltx-api/snapshot.json').read_text());self.assertEqual(old['monthly']['events'],226);self.assertEqual(new['monthly']['events'],228);self.assertEqual(new['monthly']['weights_events'],97)
 def test_unsupported_semantics_rejected(self):
  for key,value in [('kind','weights'),('api_alias',None),('first_public_weights_date','2026-08-11'),('pinned_api_revision','ltx-2.5'),('timestamp_utc','2026-08-11T00:00:00Z'),('first_paper_submission','2026-08-11'),('execution_status','tested')]:
   p=copy.deepcopy(self.p);p['events'][0][key]=value
   with self.assertRaises(ValueError):h.validate(p)
 def test_source_date_kind_and_support_required(self):
  for key,value in [('date','2026-08-10'),('kind','api_ga_announcement'),('supports',['event_date'])]:
   p=copy.deepcopy(self.p);p['events'][0]['evidence'][0][key]=value
   with self.assertRaises(ValueError):h.validate(p)
 def test_neutral_label_does_not_change_deepseek_experimental_identity(self):
  p=h.load(ROOT/'curated/historical-events/deepseek-nov1.json');row=p['events'][2];self.assertIn('实验',row['title']['zh']);self.assertIn('experimental',row['title']['en'].lower());self.assertIn("api_availability_announcement:'API 可用公告'",(ROOT/'web/monthly.js').read_text())
