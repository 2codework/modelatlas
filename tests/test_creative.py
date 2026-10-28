import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('creative_builder',R/'scripts/build.py');B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
class Creative(unittest.TestCase):
 def setUp(self):self.d=json.loads((R/'data/research/creative-music.json').read_text())
 def test_preserve_node_type(self):
  result=B.normalize([self.d]);self.assertEqual(result['nodes'][0]['type'],self.d['nodes'][0]['kind'])
 def test_dangling_case_node_fails(self):
  self.d['cases'][0]['modelatlas_node_ids']=['missing']
  with self.assertRaisesRegex(ValueError,'dangling'):B.normalize([self.d])
 def test_duplicate_case_fails(self):
  self.d['cases'].append(copy.deepcopy(self.d['cases'][0]))
  with self.assertRaisesRegex(ValueError,'duplicate'):B.normalize([self.d])

 def test_current_coverage_keeps_real_gaps(self):
  bundles=[json.loads(p.read_text()) for p in (R/'data/research').glob('*.json')]
  result=B.normalize(bundles);text=' '.join(map(str,result['coverage_gaps']))
  self.assertNotIn('视频、音乐、3D、机器人和世界模型仅有类别位置',text)
  self.assertIn('视频与音乐已初步纳入相关技术节点',text)
  self.assertIn('3D、机器人和世界模型仍缺独立系列',text)
