import copy,importlib.util,json,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('world_models',ROOT/'scripts/world_models.py');W=importlib.util.module_from_spec(spec);spec.loader.exec_module(W)
class WorldModels(unittest.TestCase):
 def setUp(self):
  p=ROOT/'learning/world-models/r1';self.r=json.loads((p/'world-model-research-r1.json').read_text());self.q=json.loads((p/'qa-overlay.json').read_text())
 def reject(self,change):
  change(self.r,self.q)
  with self.assertRaises((ValueError,KeyError,TypeError)):W.adapt(self.r,self.q)
 def test_lossless_raw(self):
  r=copy.deepcopy(self.r);q=copy.deepcopy(self.q);b=W.adapt(r,q);self.assertEqual(r,self.r);self.assertEqual(q,self.q);self.assertEqual(b['raw_research'],r);self.assertEqual(b['qa_overlay'],q)
 def test_structure_paths_dates(self):
  b=W.adapt(self.r,self.q);self.assertEqual(len(b['nodes']),12);self.assertEqual(len(b['tutorial_paths']),3);self.assertEqual(len(b['events']),62)
  for e in b['events']:self.assertIsNone(e['time']);self.assertIsNone(e['timezone'])
  for e in b['edges']:self.assertEqual(e['verification_status'],'editorial_learning_relation');self.assertTrue(e['source_ids']);self.assertNotIn('jev',[e['source'],e['target']])
 def test_availability_is_not_first_file(self):
  b=W.adapt(self.r,self.q)
  for e in b['events']:
   if e['raw_event_key']=='weights_first_available':self.assertEqual(e['event_type'],'announcement');self.assertIn('首次文件',e['title']);self.assertIn('未下载',e['note_zh'])
  for n in b['nodes']:self.assertNotIn('weights_first_available',n['dates'])
 def test_semantics_and_unknown_venue(self):
  ns={n['id']:n for n in W.adapt(self.r,self.q)['nodes']};self.assertEqual(ns['wm-openvla']['semantic_subtype'],'action_policy_not_world_state_predictor');self.assertIsNone(ns['wm-ijepa']['dates']['publication']['date']);self.assertEqual(ns['wm-jepa-concept']['type'],'concept')
 def test_dates_conflict_retained(self):
  es=[e for e in W.adapt(self.r,self.q)['events'] if e['node_ids']==['wm-vjepa2']];self.assertEqual(next(e['date'] for e in es if e['raw_event_key']=='announcement'),'2025-06-11');self.assertEqual(next(e['date'] for e in es if e['raw_event_key']=='repo_release_label'),'2025-06-25')
 def test_no_new_scores(self):self.assertNotIn('snapshots',W.adapt(self.r,self.q))
 def test_original_svg_safe(self):
  text=(ROOT/'web/world-model-learning.svg').read_text();ET.fromstring(text)
  for bad in ['<script','<foreignObject','href=','onload=','http://','https://']:
   if bad=='http://':self.assertEqual(text.count(bad),1)
   else:self.assertNotIn(bad,text)
 def test_raw_output_byte_preserved(self):
  for p in (ROOT/'learning/world-models/r1').iterdir():self.assertEqual(p.read_bytes(),(ROOT/'docs/world-models/r1'/p.name).read_bytes())
 def test_duplicate_node_rejected(self):self.reject(lambda r,q:r['nodes'].__setitem__(1,copy.deepcopy(r['nodes'][0])))
 def test_bad_source_rejected(self):self.reject(lambda r,q:r['sources'][0].update(url='javascript:alert(1)'))
 def test_execution_claim_rejected(self):self.reject(lambda r,q:r['execution_boundary'].update(models_executed=True))
 def test_timestamp_rejected(self):self.reject(lambda r,q:r['nodes'][0]['dates']['publication'].update(time='00:00:00'))
 def test_wrong_qa_date_rejected(self):self.reject(lambda r,q:q['records'][0].update(paper_first_submitted='2020-01-01'))
 def test_unresolved_venue_rejected(self):self.reject(lambda r,q:next(n for n in r['nodes'] if n['id']=='wm-ijepa')['dates']['publication'].update(date='2023'))
 def test_unaccepted_qa_rejected(self):self.reject(lambda r,q:q['records'][0].update(verdict='reject'))
 def test_unknown_source_rejected(self):self.reject(lambda r,q:r['nodes'][0].update(source_ids=['missing']))
 def test_missing_reading_node(self):self.reject(lambda r,q:r['reading_paths'][0]['nodes'].append('missing'))

 def test_current_coverage_display_only_precise_matches(self):
  import sys
  sys.path.insert(0,str(ROOT/'scripts'));import build as B
  original=list(B.COVERAGE_DISPLAY_OVERLAYS)+['其他缺口保持原样',{'scope':'structured gap'}]
  before=copy.deepcopy(original);ids=set(W.EXPECTED)|{'design-freecad-partdesign','design-godot-asset-pipeline','design-godot-spriteframes'}
  current=B.current_coverage_display(original,ids)
  self.assertEqual(original,before);self.assertEqual(current[-2:],original[-2:]);self.assertEqual(current[:-2],list(B.COVERAGE_DISPLAY_OVERLAYS.values()))
 def test_coverage_overlay_requires_actual_nodes(self):
  import build as B
  gaps=list(B.COVERAGE_DISPLAY_OVERLAYS);self.assertEqual(B.current_coverage_display(gaps,set()),gaps)
 def test_raw_gaps_remain_historical_current_stale_absent(self):
  import build as B
  d=json.loads((ROOT/'docs/data.json').read_text());raw=json.dumps(d['research_bundles'],ensure_ascii=False)
  for stale in B.COVERAGE_DISPLAY_OVERLAYS:self.assertNotIn(stale,d['coverage_gaps'])
  self.assertIn('未覆盖3D/CAD/工业设计/字体生成/印前色彩管理等后续专题',raw)
  self.assertIn('视频、音乐、3D、机器人和世界模型仅有类别位置，缺独立系列',raw)

 def test_dated_event_checkdate_uses_research_and_sources_not_build_clock(self):
  b=W.adapt(self.r,self.q);sources={s['id']:s for s in self.r['sources']}
  for event in b['events']:
   if event['date']:
    self.assertEqual(event['checked_at'],self.r['checked_at'])
    for sid in event['source_ids']:self.assertEqual(event['checked_at'],sources[sid.removeprefix('wm-src-')]['checked_at'])
  historical=copy.deepcopy(self.r);historical['checked_at']='2026-09-01'
  for source in historical['sources']:source['checked_at']='2026-09-01'
  self.assertTrue(all(e['checked_at']=='2026-09-01' for e in W.adapt(historical,self.q)['events'] if e['date']))
 def test_created_svg_gap_overlays_current_only(self):
  import build as B
  stale='配图仅提供原创示意方案，未制作或复制论文图片；外部图权利尚未核查。'
  d=json.loads((ROOT/'docs/data.json').read_text());self.assertNotIn(stale,d['coverage_gaps']);self.assertIn(stale,json.dumps(d['research_bundles'],ensure_ascii=False));self.assertIn(B.COVERAGE_DISPLAY_OVERLAYS[stale],d['coverage_gaps']);self.assertIn('不是论文原图或实测架构',B.COVERAGE_DISPLAY_OVERLAYS[stale]);self.assertEqual(B.current_coverage_display([stale],set()),[stale])
