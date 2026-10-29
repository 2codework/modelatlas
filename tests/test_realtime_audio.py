"""Reviewed research is the independent oracle; never invoke any model."""
import copy, hashlib, json, unittest
from edge_contract import legacy_view as edge_legacy
from audio_contract import ROOT, baseline, validate, legacy_view, NODE_IDS, SOURCE_IDS, EVENT_DATES, strict

RESEARCH_SHA='a05361a48710722d564d18757e5404ddb8d7103ca9541d28078429a723f2f9c2'
def research():
 raw=(ROOT/'tests/fixtures/realtime-audio-research-r2.json').read_bytes()
 assert hashlib.sha256(raw).hexdigest()==RESEARCH_SHA
 return strict(raw)

class AudioAdmission(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.live=edge_legacy(strict((ROOT/'dist/data.json').read_bytes()));cls.raw=research()
 def reject(self,fn,pattern):
  d=copy.deepcopy(self.live);fn(d)
  with self.assertRaisesRegex(ValueError,pattern):validate(d)
 def test_closed_live_admission(self):validate(self.live)
 def test_docs_dist_same_and_compact(self):
  raw=(ROOT/'dist/data.json').read_bytes();self.assertEqual(raw,(ROOT/'docs/data.json').read_bytes())
  self.assertEqual(raw,(json.dumps(strict(raw),ensure_ascii=False,separators=(',',':'))+'\n').encode())
 def test_legacy_stage_exact(self):self.assertEqual(legacy_view(self.live),baseline())
 def test_duplicate_old_node(self):self.reject(lambda d:d['nodes'].append(copy.deepcopy(d['nodes'][0])),'duplicate nodes')
 def test_duplicate_new_source(self):self.reject(lambda d:d['sources'].append(copy.deepcopy(d['sources'][-1])),'duplicate sources')
 def test_same_count_delete_duplicate(self):self.reject(lambda d:d['nodes'].__setitem__(0,copy.deepcopy(d['nodes'][1])),'duplicate nodes')
 def test_unadmitted_node(self):self.reject(lambda d:d['nodes'].append({'id':'unadmitted'}),'exact ordered nodes')
 def test_unadmitted_source(self):self.reject(lambda d:d['sources'].append({'id':'unadmitted'}),'exact ordered sources')
 def test_unadmitted_event(self):self.reject(lambda d:d['events'].append({'id':'unadmitted'}),'exact ordered events')
 def test_drop_new_node(self):self.reject(lambda d:d['nodes'].pop(),'exact ordered nodes')
 def test_old_mutation(self):self.reject(lambda d:d['nodes'][0].update(title='changed'),'complete object')
 def test_old_field_deleted(self):self.reject(lambda d:d['sources'][0].pop('url'),'complete object')
 def test_registry_mutation(self):self.reject(lambda d:d['vendor_catalog']['records'][0].update(title='changed'),'old complete field')
 def test_top_level_surplus(self):self.reject(lambda d:d.update(unadmitted=True),'top-level')
 def test_missing_collection(self):self.reject(lambda d:d.pop('events'),'top-level')
 def test_event_date_not_checked_at(self):self.reject(lambda d:d['events'][-1].update(date='2026-10-28'),'event date')
 def test_event_missing_source(self):self.reject(lambda d:d['events'][-1].update(source_ids=[]),'event source')
 def test_audio_registry_false_count(self):self.reject(lambda d:d['realtime_audio_registry']['graph_statistics_current'].update(nodes=245),'registry complete object')
 def test_new_object_extra_field(self):self.reject(lambda d:d['nodes'][-1].update(unreviewed=True),'complete golden object')
 def test_old_order_changed(self):self.reject(lambda d:d['sources'].reverse(),'exact ordered sources')
 def test_approved_raw_model_records_whole(self):
  nodes={n['id']:n for n in self.live['nodes']}
  for model in self.raw['models']:
   n=nodes[model['id']]
   self.assertEqual(n['realtime_audio'],model)
   self.assertEqual(n['type'],model['entity_kind'])
   self.assertEqual(n['source_ids'],['audio-src-'+x for x in model['source_ids']])
   self.assertEqual(n['execution_status'],'never-run');self.assertIs(n['runtime_verified'],False)
   self.assertEqual(n['verification_status'],'primary_sources_reviewed_not_executed')
   self.assertEqual(n['lifecycle'],'unknown')
 def test_exact_event_mapping_and_planned_boundary(self):
  events={e['id']:e for e in self.live['events']}
  for m in self.raw['models']:
   for record in m['dates']:
    e=events['audio-event-'+m['id']+'-'+record['kind']]
    self.assertEqual(e['date'],record['date']);self.assertEqual(e['research_event_kind'],record['kind'])
    self.assertEqual(e['source_ids'],['audio-src-'+x for x in record['source_ids']])
    if record['kind']=='old_snapshot_scheduled_shutdown':
     self.assertEqual(e['event_type'],'scheduled_shutdown');self.assertEqual(e['status'],'planned');self.assertIn('计划',e['title']);self.assertIn('尚未发生',e['title'])
 def test_exact_version_and_unknown_boundaries(self):
  nodes={n['id']:n['realtime_audio'] for n in self.live['nodes'] if n['id'] in NODE_IDS}
  moshi=nodes['speech-moshi'];self.assertIsNone(moshi['exact_version']);self.assertIsNone(moshi['reviewed_variants'][0]['first_weights_upload_date'])
  csm=nodes['speech-csm-1b'];self.assertIsNone(csm['streaming']['full_duplex'])
  vox=nodes['speech-voxtral-realtime-2602'];self.assertTrue(vox['streaming']['transport_bidirectional_streaming']);self.assertFalse(vox['streaming']['conversational_speech_to_speech']);self.assertEqual(vox['official_deployment_configuration']['gpu_memory_gb_at_least'],16)
  versions={v['exact_id']:v for v in nodes['speech-gpt-realtime-family']['version_records']}
  self.assertEqual(set(versions),{'gpt-realtime-2025-08-28','gpt-realtime-2.1'})
  self.assertEqual(versions['gpt-realtime-2025-08-28']['pricing_per_million_tokens_usd']['text_output'],16)
  self.assertEqual(versions['gpt-realtime-2.1']['pricing_per_million_tokens_usd']['text_output'],24)
  self.assertIsNone(versions['gpt-realtime-2.1']['release_date'])
 def test_no_new_edges_or_catalog_records(self):
  old=baseline();self.assertEqual(self.live['edges'],old['edges']);self.assertEqual(self.live['vendor_catalog'],old['vendor_catalog']);self.assertEqual(self.live['dataset_benchmark_registry'],old['dataset_benchmark_registry']);self.assertEqual(self.live['media_evaluation_registry'],old['media_evaluation_registry'])
 def test_registry_coverage_gap_not_new_model(self):
  r=self.live['realtime_audio_registry'];self.assertEqual(r['node_ids'],NODE_IDS);self.assertEqual(r['coverage_gaps'],self.raw['coverage_gaps']);self.assertIn('GPT-Realtime-2',json.dumps(r['coverage_gaps']))

class AudioProductionAdmission(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import sys
  sys.path.insert(0,str(ROOT/'scripts'))
  import realtime_audio
  cls.A=realtime_audio
 def test_old_production_admission_original_bytes(self):
  self.assertEqual(hashlib.sha256((ROOT/'scripts/knowledge_graph_links.py').read_bytes()).hexdigest(),'b877d7655593471edf54db2341962f783cc4b1b971a6ab3b6a15e724f50e8cab')
 def test_production_matches_independent_closed_contract(self):
  d=baseline();self.A.apply(d,ROOT);validate(d)
 def test_admission_hash(self):
  from unittest.mock import patch
  with patch.object(self.A,'sha',return_value='0'*64):
   with self.assertRaisesRegex(ValueError,'admission hash'):self.A.load(ROOT)
 def test_raw_hash(self):
  from unittest.mock import patch
  sha=self.A.sha
  with patch.object(self.A,'sha',side_effect=lambda p:'0'*64 if str(p).endswith('raw/research-r2/raw-models.json') else sha(p)):
   with self.assertRaisesRegex(ValueError,'raw inventory/hash'):self.A.load(ROOT)
 def test_overlay_hash(self):
  from unittest.mock import patch
  sha=self.A.sha
  with patch.object(self.A,'sha',side_effect=lambda p:'0'*64 if p.name=='overlay.json' else sha(p)):
   with self.assertRaisesRegex(ValueError,'overlay hash'):self.A.load(ROOT)
 def changed_overlay(self,fn,pattern,reseal=False):
  from unittest.mock import patch
  a,o,r=self.A.load(ROOT);fn(o)
  if reseal:
   for k in o:a['expected_object_sha256'][k]={x['id']:self.A.digest(x) for x in o[k]}
  with patch.object(self.A,'load',return_value=(a,o,r)):
   with self.assertRaisesRegex(ValueError,pattern):self.A.apply(baseline(),ROOT)
 def test_duplicate_derived_id(self):self.changed_overlay(lambda o:o['nodes'].append(copy.deepcopy(o['nodes'][0])),'duplicate ID')
 def test_unadmitted_id(self):self.changed_overlay(lambda o:o['nodes'][0].update(id='other'),'addition IDs')
 def test_semantic_mutation_not_just_count(self):self.changed_overlay(lambda o:o['nodes'][0].update(title='other'),'addition objects')
 def test_no_unknown_date_event_even_resealed(self):self.changed_overlay(lambda o:o['events'][0].update(date=None),'unknown date',True)
 def test_planned_not_completed_even_resealed(self):self.changed_overlay(lambda o:o['events'][-1].update(status='completed'),'planned event',True)
 def test_planned_label_required_even_resealed(self):self.changed_overlay(lambda o:o['events'][-1].update(title='shutdown'),'planned event',True)
 def test_no_execution_upgrade_even_resealed(self):self.changed_overlay(lambda o:o['nodes'][0].update(runtime_verified=True),'execution upgrade',True)
 def test_baseline_drift(self):
  d=baseline();d['nodes'][0]['title']='changed'
  with self.assertRaisesRegex(ValueError,'baseline drift'):self.A.apply(d,ROOT)
 def test_no_repeated_application(self):
  d=baseline();self.A.apply(d,ROOT)
  with self.assertRaisesRegex(ValueError,'baseline fields'):self.A.apply(d,ROOT)
 def test_sources_derive_independently_from_raw(self):
  d=strict((ROOT/'dist/data.json').read_bytes());index={s['id']:s for s in d['sources']}
  for raw in research()['sources']:
   expected={'id':'audio-src-'+raw['id'],'url':raw['url'],'title':raw['id'],'checked_at':raw['checked_at'],'evidence_scope':raw['evidence_note_zh'],'verification_status':{'failed':'not_accessible','opened_partial':'partially_accessible','opened':'primary_source_opened'}[raw['status']],'research_source_id':raw['id'],'access_status':raw['status'],'raw_record':raw}
   self.assertEqual(index[expected['id']],expected)

if __name__=='__main__':unittest.main()
