import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from monthly_releases import curated_rows
class VisibleBoundaries(unittest.TestCase):
 def test_null_date_does_not_imply_dated_availability(self):
  r=curated_rows({'records':[{'id':'unknown','name':'X','notes':['仅确认当前可下载。'],'evidence':[]}]})[0]
  self.assertEqual(r['kind'],'weights_undated');self.assertIsNone(r['date']);self.assertIn('权重开放日期未核实',r['note']);self.assertIn('仅确认当前可下载。',r['note'])
  self.assertNotIn('官方声明可取得权重的日期；',r['note'])
 def test_string_note_preserved(self):
  r=curated_rows({'records':[{'id':'known','name':'Y','notes':'不包含后来版本。','weights_release_date':'2024-01-01','evidence':[{'supports':['weights_release_date']}]}]})[0]
  self.assertIn('不包含后来版本。',r['note']);self.assertIn('官方声明可取得权重的日期',r['note'])
