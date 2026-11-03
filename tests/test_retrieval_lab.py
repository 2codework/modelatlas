import html,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('retrieval_builder',ROOT/'scripts/build_retrieval_lab.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class RetrievalPackagingTests(unittest.TestCase):
 def test_exact_zip_readers(self):
  with zipfile.ZipFile(ROOT/'web/retrieval-lab.zip') as z:
   self.assertEqual(set(z.namelist()),{'retrieval-lab/'+n for n in builder.FILES})
   for n in builder.FILES:
    raw=(ROOT/'learning/retrieval-lab'/n).read_bytes()
    self.assertEqual(z.read('retrieval-lab/'+n),raw)
    for suffix in ('','-en'):self.assertIn(html.escape(raw.decode()),(ROOT/'web'/f'retrieval-lab{suffix}.html').read_text())
 def test_extracted_demo_and_tests(self):
  with tempfile.TemporaryDirectory() as d:
   with zipfile.ZipFile(ROOT/'web/retrieval-lab.zip') as z:z.extractall(d)
   p=Path(d)/'retrieval-lab'
   run=subprocess.run([sys.executable,'-B','demo.py'],cwd=p,capture_output=True,text=True,check=True)
   data=json.loads(run.stdout)
   self.assertEqual(len(data['chunks']),4);self.assertTrue(data['worked_hit_at_1'])
   self.assertFalse(data['old_citation_valid_in_new_snapshot'])
   self.assertEqual(data['results']['workshop host']['status'],'needs_review')
   tests=subprocess.run([sys.executable,'-B','-m','unittest','-v'],cwd=p,capture_output=True,text=True,check=True)
   self.assertIn('Ran 11 tests',tests.stderr);self.assertFalse((p/'__pycache__').exists())
 def test_core_entry_and_transfer(self):
  for suffix in ('','-en'):
   s=(ROOT/'web'/f'retrieval-lab{suffix}.html').read_text()
   self.assertLess(s.index('id="transfer"'),s.index('id="reference"'))
   self.assertIn("connect-src 'none'",s);self.assertIn('2026-11-02',s)
   self.assertGreaterEqual((ROOT/'web'/f'academy{suffix}.html').read_text().count(f'href="retrieval-lab{suffix}.html"'),3)
  self.assertIn("destinations:['retrieval-lab.html','retrieval-lab-en.html']",(ROOT/'web/academy.js').read_text())

 def test_monthly_display_generated_from_projection(self):
  n=len(json.loads((ROOT/'dist/monthly-releases.json').read_text())['records'])
  for name in ('academy.html','index.html'):
   self.assertIn(str(n)+' 条月度事件',(ROOT/'dist'/name).read_text())
  self.assertIn(str(n)+' monthly events',(ROOT/'dist/academy-en.html').read_text())
  self.assertIn(str(n)+' 条事件',(ROOT/'dist/academy.html').read_text())
  self.assertIn(str(n)+' events',(ROOT/'dist/academy-en.html').read_text())
  self.assertNotIn('226 monthly events',(ROOT/'scripts/build_academy.py').read_text())
  sys.path.insert(0,str(ROOT/'scripts'))
  import build_academy
  self.assertIn('7 monthly events',build_academy.home('en',7))
  self.assertIn('7 条月度事件',build_academy.home('zh',7))
