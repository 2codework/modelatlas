"""Original tiny training numerical, download and static lesson contracts."""
import html
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ma_build_tiny_training',ROOT/'scripts/build_tiny_training.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class TinyTrainingPackagingTests(unittest.TestCase):
 def test_download_source_reader_parity(self):
  with zipfile.ZipFile(ROOT/'web/tiny-training-lab.zip') as z:
   self.assertEqual(set(z.namelist()),{'tiny-training/'+n for n in builder.FILES})
   for n in builder.FILES:
    raw=(ROOT/'learning/tiny-training'/n).read_bytes()
    self.assertEqual(z.read('tiny-training/'+n),raw)
    self.assertEqual((ROOT/'web'/('tiny-training-'+n)).read_bytes(),raw)
    for suffix in ('','-en'):
     page=(ROOT/'web'/f'tiny-training{suffix}.html').read_text()
     self.assertIn(html.escape(raw.decode()),page)
 def test_actual_extracted_zip(self):
  with tempfile.TemporaryDirectory() as d:
   with zipfile.ZipFile(ROOT/'web/tiny-training-lab.zip') as z:z.extractall(d)
   lab=Path(d)/'tiny-training'
   result=subprocess.run([sys.executable,'-B','demo.py'],cwd=lab,text=True,capture_output=True,check=True)
   data=json.loads(result.stdout)
   self.assertTrue(data['inference_parameters_unchanged'])
   self.assertAlmostEqual(data['train_loss_after'],1.0439803399807872)
   tests=subprocess.run([sys.executable,'-B','-m','unittest','-v'],cwd=lab,text=True,capture_output=True,check=True)
   self.assertIn('Ran 9 tests',tests.stderr)
   self.assertFalse((lab/'__pycache__').exists())
 def test_bilingual_independent_transfer_and_boundaries(self):
  for suffix in ('','-en'):
   s=(ROOT/'web'/f'tiny-training{suffix}.html').read_text()
   self.assertLess(s.index('id="transfer"'),s.index('id="reference"'))
   self.assertIn('1.159811928855196',s); self.assertIn('1.0439803399807872',s)
   self.assertIn("connect-src 'none'",s);self.assertNotIn('<iframe',s)
   self.assertIn('2026-11-01',s);self.assertIn('Python 3.9+',s)
 def test_academy_routes_and_search(self):
  for suffix in ('','-en'):
   s=(ROOT/'web'/f'academy{suffix}.html').read_text()
   self.assertGreaterEqual(s.count(f'href="tiny-training{suffix}.html"'),3)
  self.assertIn("destinations:['tiny-training.html','tiny-training-en.html']",(ROOT/'web/academy.js').read_text())
