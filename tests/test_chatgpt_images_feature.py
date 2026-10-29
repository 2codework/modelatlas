"""Finite offline web-feature admission and preservation, not product execution."""
import copy,json,sys,tempfile,shutil,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
from images_contract import ROOT,legacy_view,encoded,BASE_DATA_SHA
sys.path.insert(0,str(ROOT/'scripts'))
import chatgpt_images_feature as C
class ChatGPTImagesFeature(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'dist/data.json').read_text());cls.old=legacy_view(cls.data)
 def test_complete_original_graph_and_additive_scope(self):
  self.assertEqual(hashlib.sha256(encoded(self.old)).hexdigest(),BASE_DATA_SHA)
  self.assertEqual([len(self.data[k]) for k in ['nodes','sources','events','edges']],[259,427,211,151])
  self.assertEqual(len(self.data['vendor_catalog']['records']),77)
  self.assertEqual(self.data['checked_at'],self.old['checked_at'])
  self.assertEqual(C.apply(copy.deepcopy(self.old),ROOT),self.data)
 def test_unknowns_and_source_partition(self):
  a,o=C.load(ROOT);n=o['nodes'][0]
  self.assertEqual(n['type'],'application_feature');self.assertFalse(n['runtime_verified'])
  for k in ['architecture','exact_backend_model','first_feature_release_date','weights_release_date']:self.assertIsNone(n[k])
  self.assertEqual(len(n['source_ids']),5);self.assertNotIn('cgw-src-api-sunburst',n['source_ids'])
  self.assertEqual(len({s['id'] for s in self.data['sources']}),427)
  for s in o['sources']:self.assertIn('unknown_boundary',s)
  self.assertEqual(o['events'],[]);self.assertEqual(o['edges'],[])
 def test_full_stage_mutations_rejected(self):
  for mutate in [lambda d:d['nodes'][0].update(title='drift'),lambda d:d['sources'][0].update(checked_at='2026-10-29'),lambda d:d['nodes'][-1].update(type='model'),lambda d:d['nodes'][-1].update(exact_backend_model='Sunburst'),lambda d:d['events'].append({'date':'2026-10-29'}),lambda d:d['edges'].append({'source':C.NODE_ID,'target':'gpt-4'}),lambda d:d['chatgpt_images_feature_registry'].update(execution_status='run')]:
   d=copy.deepcopy(self.data);mutate(d)
   with self.assertRaises(ValueError):legacy_view(d)
 def test_semantic_boundary_negatives(self):
  mutations=[lambda o:o['nodes'][0].update(type='model'),lambda o:o['nodes'][0].update(architecture='diffusion'),lambda o:o['nodes'][0].update(runtime_verified=0),lambda o:o['nodes'][0]['source_ids'].append('cgw-src-api-sunburst'),lambda o:o['events'].append({'id':'fake'}),lambda o:o['edges'].append({'type':'implemented_by'}),lambda o:o['sources'][3].update(evidence_mode='fresh_official_web_read'),lambda o:o['sources'][0].update(url='javascript:alert(1)'),lambda o:o['sources'][0].update(url='https://user@learn.chatgpt.com/x')]
  for mutate in mutations:
   _,o=C.load(ROOT);mutate(o)
   with self.assertRaises(ValueError):C.validate_overlay(o)
 def test_duplicate_baseline_and_second_apply_rejected(self):
  d=copy.deepcopy(self.old);d['nodes'].append(copy.deepcopy(d['nodes'][0]))
  with self.assertRaises(ValueError):C.apply(d,ROOT)
  with self.assertRaises(ValueError):C.apply(copy.deepcopy(self.data),ROOT)
 def test_closed_public_inventory_and_parity(self):
  for folder in ['dist','docs']:
   p=ROOT/folder/C.PUBLIC_REL;self.assertEqual({x.name for x in p.iterdir()},C.FILES)
   for name in C.FILES:self.assertEqual((p/name).read_bytes(),(ROOT/C.REL/name).read_bytes())
  for p in (ROOT/C.REL).iterdir():
   text=p.read_text();self.assertNotIn('/workspace/',text);self.assertNotIn('internal/',text)
 def test_reject_extra_and_symlink_assets_before_publish(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);shutil.copytree(ROOT/C.REL,r/C.REL)
   (r/C.REL/'unregistered.js').write_text('bad')
   with self.assertRaises(ValueError):C.preflight(r)
   (r/C.REL/'unregistered.js').unlink();(r/'dist').mkdir();(r/'outside').mkdir();(r/'dist'/C.PUBLIC_REL).symlink_to(r/'outside',target_is_directory=True)
   with self.assertRaises(ValueError):C.preflight(r)
   self.assertEqual(list((r/'outside').iterdir()),[])
 def test_content_hash_pin(self):
  with patch.object(C,'sha',return_value='0'*64):
   with self.assertRaises(ValueError):C.load(ROOT)

 def test_book_old_text_and_counts_preserved(self):
  text=(ROOT/'BOOK.md').read_text()
  start=text.index('\n## ChatGPT 网页图片创建与编辑\n');end=text.index('\n## ',start+2)
  old=text[:start]+text[end:]
  old='\n'.join(line for line in old.split('\n') if not line.startswith('- cgw-src-'))
  self.assertEqual(hashlib.sha256(old.encode()).hexdigest(),'6ffdea8041ab3ea2c94d5d82f384832d7a9038d1cbc7cbd75946127def6ba120')

 def test_shared_golden_negative_matrix_and_no_mutation(self):
  from runtime_contract import validate
  cases=json.loads((ROOT/'tests/fixtures/images-negative-cases.json').read_text())
  for case in cases:
   d=copy.deepcopy(self.data);target=d
   for key in case['path'][:-1]:target=target[key]
   key=case['path'][-1];action=case['action']
   if action=='set':target[key]=case['value']
   elif action=='delete':del target[key]
   elif action=='append':target[key].append(case['value'])
   elif action=='reverse':target[key].reverse()
   else:raise AssertionError(action)
   before=encoded(d)
   with self.subTest(case=case['name']),self.assertRaises((ValueError,KeyError)):legacy_view(d)
   with self.subTest(case=case['name']),self.assertRaises((ValueError,KeyError)):validate(d)
   self.assertEqual(encoded(d),before)
  before=encoded(self.data);validate(self.data);legacy_view(self.data);self.assertEqual(encoded(self.data),before)
  validate(self.old)
