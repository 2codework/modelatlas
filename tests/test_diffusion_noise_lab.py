import unittest,subprocess,sys,tempfile,zipfile,json,html,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
FILES=('core.py','fixtures.json','demo.py','test_core.py','README-zh.md','README-en.md','WORKSHEET-zh.md','WORKSHEET-en.md','REFERENCE-zh.md','REFERENCE-en.md','SOURCES.md')
class DiffusionPacket(unittest.TestCase):
 def test_zip_and_raw_source_parity(self):
  with zipfile.ZipFile(R/'web/diffusion-noise-lab.zip') as z:
   self.assertEqual(set(z.namelist()),{'diffusion-noise/'+n for n in FILES})
   for n in FILES:
    raw=(R/'learning/diffusion-noise'/n).read_bytes();self.assertEqual(z.read('diffusion-noise/'+n),raw)
    self.assertEqual((R/'web'/('diffusion-noise-'+n)).read_bytes(),raw)
    for suffix in ('','-en'):self.assertIn(html.escape(raw.decode()),(R/'web'/f'diffusion-noise-lab{suffix}.html').read_text())
 def test_extracted_readme_commands(self):
  import shlex
  with tempfile.TemporaryDirectory() as d:
   with zipfile.ZipFile(R/'web/diffusion-noise-lab.zip') as z:z.extractall(d)
   folder=Path(d)/'diffusion-noise'
   for lang in ('zh','en'):
    commands=[line.strip() for line in (folder/f'README-{lang}.md').read_text().splitlines() if line.startswith('    ')]
    self.assertEqual(commands,['python3 -B demo.py','python3 -B -m unittest -v'])
    for c in commands:
     p=subprocess.run(shlex.split(c),cwd=folder,capture_output=True,text=True,check=True)
     if 'demo.py' in c:
      outputs=json.loads(p.stdout);self.assertEqual(set(outputs),{'worked','high'})
      for k,expected in [('worked',.0225),('high',.96)]:self.assertAlmostEqual(outputs[k]['mse'],expected)
     else:self.assertIn('Ran 9 tests',p.stderr)
 def test_shared_anchors_and_independent_exercise(self):
  pages=[(R/'web'/f'diffusion-noise-lab{s}.html').read_text() for s in ('','-en')]
  ids=[re.findall('id="([^"]+)"',p) for p in pages];self.assertEqual(ids[0],ids[1]);self.assertEqual(len(ids[0]),len(set(ids[0])))
  for p in pages:
   self.assertLess(p.index('id="transfer"'),p.index('id="reference"'));self.assertIn('<details id="reference">',p);self.assertIn('id="result" hidden',p)
   for x in ('2006.11239v2','2020-06-19','2020-12-16','2026-11-02',"connect-src 'none'",'Markov'):self.assertIn(x,p)
 def test_search_and_links(self):
  for suffix in ('','-en'):self.assertIn(f'diffusion-noise-lab{suffix}.html',(R/'web'/f'academy{suffix}.html').read_text())
  self.assertIn('diffusion-noise-lab.html',(R/'web/academy.js').read_text())
 def test_transfer_not_revealed_by_default_demo_or_pretransfer_prose(self):
  for suffix in ('','-en'):
   page=(R/'web'/f'diffusion-noise-lab{suffix}.html').read_text()
   run=page.split('<section id="run">',1)[1].split('</section>',1)[0]
   self.assertNotIn('0.1',run)
  p=subprocess.run([sys.executable,'-B','demo.py','--include-transfer'],cwd=R/'learning/diffusion-noise',capture_output=True,text=True,check=True)
  self.assertAlmostEqual(json.loads(p.stdout)['transfer']['mse'],.1)
 def test_js_python_parity(self):
  sys.path.insert(0,str(R/'learning/diffusion-noise'))
  try:
   import importlib.util
   spec=importlib.util.spec_from_file_location('noise_core',R/'learning/diffusion-noise/core.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
   cases=[dict(alpha_bar=a,x0=[10,-10],epsilon=[-10,10],estimate=e) for a in [.01,.04,.36,.64,.995,1] for e in [[0,0],[-10,10],[.3,-.3]]]
   cases+=list(json.loads((R/'learning/diffusion-noise/fixtures.json').read_text()).values())
   js="const m=require('./web/diffusion-noise.js');const fs=require('node:fs');console.log(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>m.calculate(x.alpha_bar,x.x0,x.epsilon,x.estimate))));"
   outputs=json.loads(subprocess.run(['node','-e',js],input=json.dumps(cases),cwd=R,capture_output=True,text=True,check=True).stdout)
   for fixture,j in zip(cases,outputs):
    py=m.calculate(**fixture)
    for key,val in py.items():
     if isinstance(val,list):
      for x,y in zip(val,j[key]):self.assertAlmostEqual(x,y,places=10)
     else:self.assertAlmostEqual(val,j[key],places=10)
  finally:sys.path.pop(0)
