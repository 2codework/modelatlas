from audio_contract import legacy_view
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('creative_gaps',ROOT/'scripts/creative_gaps.py');G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
class CreativeGapTests(unittest.TestCase):
 def setUp(self):self.raw=json.loads((ROOT/'learning/creative-gaps/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text())
 def reject(self,fn):
  fn(self.raw)
  with self.assertRaises((ValueError,KeyError,TypeError)):G.adapt(self.raw)
 def test_raw_unchanged(self):
  old=copy.deepcopy(self.raw);b,r=G.adapt(self.raw);self.assertEqual(old,self.raw);self.assertEqual(b['raw_research'],old);self.assertEqual(len(b['nodes']),5);self.assertEqual(len(r['cases']),6)
 def test_byte_manifests(self):G.load(ROOT)
 def test_no_new_events_or_edges(self):
  b,r=G.adapt(self.raw);self.assertEqual(b['events'],[]);self.assertEqual(b['edges'],[]);self.assertNotIn('vid-kdenlive',[n['id'] for n in b['nodes']])
 def test_type_separation(self):
  b,_=G.adapt(self.raw);self.assertEqual(sum(n['type']=='tool' for n in b['nodes']),3);self.assertEqual(sum(n['type']=='application_feature' for n in b['nodes']),2);self.assertTrue(all(n['type']!='model' for n in b['nodes']))
 def test_failed_and_conflicted_sources_preserved(self):
  b,_=G.adapt(self.raw);ss={s['id']:s for s in b['sources']};self.assertEqual(ss[G.PREFIX+'kden-broken']['status'],'tool_open_error');self.assertEqual(ss[G.PREFIX+'express-faq-redirect']['status'],'redirect_with_search_body_conflict');self.assertEqual(ss[G.PREFIX+'font-rights']['independent_qa']['qa_status'],'tool_open_error')
 def test_current_session_and_project_wide_boundary(self):
  _,r=G.adapt(self.raw);text=G.book(r)
  for token in ['当前session','刷新','Version history','compositions/files','协作者','批准','Chats','中国','未列中文','首发日期：unknown']:self.assertIn(token,text)
 def test_reverse_mapping(self):
  _,r=G.adapt(self.raw)
  for c in r['cases']:self.assertIn(c['id'],r['node_to_cases'][c['modelatlas_node_id']])
 def test_sources_and_stable_aw_links_in_html(self):
  text=(ROOT/'dist/creative-learning.html').read_text();self.assertEqual(text.count('href="https://2codework.github.io/agentwork/?case='),6);self.assertIn('never-run',text)
  for c in self.raw['candidates']:
   self.assertIn('id="'+c['id']+'"',text)
   for source in c['source_ids']:
    url=next(s['url'] for s in self.raw['sources'] if s['id']==source);self.assertIn(url,text)
 def test_static_navigation(self):
  self.assertIn('creative-learning.html',(ROOT/'web/index.html').read_text());self.assertIn('D.creative_learning_registry?.node_to_cases?.[id]',(ROOT/'web/app.js').read_text())
 def test_unknown_date(self):self.reject(lambda d:d['candidates'][0]['lifecycle'].update(release_date='2026-10-28'))
 def test_model_misclassification(self):self.reject(lambda d:d['candidates'][2].update(entity_type='agentic_application_feature'))
 def test_run_claim(self):self.reject(lambda d:d['candidates'][0]['verification'].update(product_run=True))
 def test_duplicate_case(self):self.reject(lambda d:d['candidates'].__setitem__(1,copy.deepcopy(d['candidates'][0])))
 def test_duplicate_source(self):self.reject(lambda d:d['sources'].__setitem__(1,copy.deepcopy(d['sources'][0])))
 def test_source_missing(self):self.reject(lambda d:d['candidates'][0].update(source_ids=['missing']))
 def test_unsafe_source(self):self.reject(lambda d:d['sources'][0].update(url='javascript:alert(1)'))
 def test_source_status_upgrade(self):self.reject(lambda d:d['sources'][0].update(status='product_tested'))
 def test_empty_acceptance(self):self.reject(lambda d:d['candidates'][0]['original_exercise'].update(acceptance_checks=[]))
 def test_dangling_registry(self):
  b,r=G.adapt(self.raw)
  with self.assertRaises(ValueError):G.validate_registry({'creative_learning_registry':r,'nodes':b['nodes'],'sources':b['sources']})
 def test_unsupported_link_status(self):
  b,r=G.adapt(self.raw);r['cases'][0]['agentwork_link']['status']='runtime_verified'
  with self.assertRaises(ValueError):G.validate_registry({'creative_learning_registry':r,'nodes':b['nodes']+[{'id':'vid-kdenlive'}],'sources':b['sources']})
 def test_baseline_objects_and_registries_unchanged(self):
  import hashlib
  h=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  frozen=json.loads((ROOT/'learning/creative-gaps/baseline-object-hashes.json').read_text());actual=legacy_view(json.loads((ROOT/'dist/data.json').read_text()))
  self.assertEqual(len(frozen['nodes']),237);self.assertEqual(len(actual['nodes']),242)
  for kind in ['nodes','sources']:
   current={x['id']:x for x in actual[kind]}
   for id,digest in frozen[kind].items():self.assertEqual(h(current[id]),digest,id)
  self.assertEqual(len(actual['edges']),151)
  for key,digest in frozen['preserved_fields'].items():
   preserved=actual[key][:139] if key=='edges' else actual[key]
   self.assertEqual(h(preserved),digest,key)
 def test_source_r2_sha_matches_final_qa(self):
  import hashlib
  p=ROOT/'learning/creative-gaps/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json'
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'530aaf53c18574618b2dcfec44796be769aab75f6f9f9945cd773b2f03b7dc88')
 def test_original_exercise_plan_visible_and_never_run(self):
  _,r=G.load(ROOT);text=(ROOT/'dist/creative-learning.html').read_text();book=G.book(r)
  for c in r['cases']:
   p=c['exercise_plan'];self.assertEqual(len(p['steps']),4)
   for phrase in [p['task']]+p['steps']+p['expected_artifacts']+p['stop_conditions']:
    self.assertIn(phrase,book)
    import html
    self.assertIn(html.escape(phrase),text)
   self.assertIn('不是厂商推荐',c['exercise_plan_note'])
 def test_final_registry_includes_external_mapping_without_node_mutation(self):
  d=legacy_view(json.loads((ROOT/'dist/data.json').read_text()));G.validate_registry(d);old=json.loads((ROOT/'learning/creative-gaps/baseline-object-hashes.json').read_text());self.assertIn('vid-kdenlive',old['nodes']);self.assertEqual(len(d['creative_learning_registry']['node_to_cases']),6)
