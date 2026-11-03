import unittest,subprocess,sys,tempfile,zipfile,json,html,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bpe_builder',R/'scripts/build_bpe_lab.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
class BPEPacket(unittest.TestCase):
 def test_zip_and_source_parity(self):
  with zipfile.ZipFile(R/'web/tokenization-lab.zip') as z:
   self.assertEqual(set(z.namelist()),{'bpe-tokenizer/'+n for n in builder.FILES})
   for n in builder.FILES:
    raw=(R/'learning/bpe-tokenizer'/n).read_bytes();self.assertEqual(z.read('bpe-tokenizer/'+n),raw);self.assertEqual((R/'web'/('tokenization-'+n)).read_bytes(),raw)
    for suffix in ('','-en'):self.assertIn(html.escape(raw.decode()),(R/'web'/f'tokenization-lab{suffix}.html').read_text())
 def test_extracted_execution(self):
  with tempfile.TemporaryDirectory() as d:
   with zipfile.ZipFile(R/'web/tokenization-lab.zip') as z:z.extractall(d)
   folder=Path(d)/'bpe-tokenizer';p=subprocess.run([sys.executable,'-B','demo.py'],cwd=folder,capture_output=True,text=True,check=True);out=json.loads(p.stdout);self.assertEqual(out['encoded']['ababc'],[4,2]);self.assertTrue(out['frozen_tokenizer_unchanged']);self.assertEqual(out['trace'][0]['counts'],[['a','b',5],['a','c',1],['b','a',3]])
   t=subprocess.run([sys.executable,'-B','-m','unittest','-v'],cwd=folder,capture_output=True,text=True,check=True);self.assertIn('Ran 12 tests',t.stderr)
 def test_readme_commands_are_copyable(self):
  import shlex
  for language in ('zh','en'):
   text=(R/'learning/bpe-tokenizer'/f'README-{language}.md').read_text()
   commands=[line.strip() for line in text.splitlines() if line.startswith('    ')]
   self.assertEqual(commands,['python3 -B demo.py','python3 -B -m unittest -v'])
   for command in commands:
    result=subprocess.run(shlex.split(command),cwd=R/'learning/bpe-tokenizer',capture_output=True,text=True,check=True)
    self.assertEqual(result.returncode,0)
  self.assertIn('U+72D7',(R/'learning/bpe-tokenizer/REFERENCE-en.md').read_text())
  self.assertIn('chapter6/5',(R/'learning/bpe-tokenizer/SOURCES.md').read_text())
 def test_content_and_shared_anchors(self):
  import re
  pages=[(R/'web'/f'tokenization-lab{s}.html').read_text() for s in ('','-en')]
  ids=[re.findall(r'id="([^"]+)"',p) for p in pages];self.assertEqual(ids[0],ids[1]);self.assertEqual(len(ids[0]),len(set(ids[0])))
  for p in pages:
   for item in ('abab','abac','ababc','猫猫狗','猫狗猫狗','1508.07909','2026-11-02'):self.assertIn(item,p)
   self.assertLess(p.index('id="transfer"'),p.index('id="reference"'));self.assertIn('connect-src \'none\'',p)
 def test_discoverability(self):
  for suffix in ('','-en'):
   p=(R/'web'/f'academy{suffix}.html').read_text();self.assertIn(f'tokenization-lab{suffix}.html',p)
  self.assertIn('tokenization-lab.html',(R/'web/academy.js').read_text())
