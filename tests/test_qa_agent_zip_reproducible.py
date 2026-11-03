"""The downloadable lab is a byte-reproducible artifact, not checkout metadata."""
from pathlib import Path
import importlib.util
import os
import shutil
import tempfile
import time
import unittest
from unittest import mock
import zipfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qa_zip_academy',ROOT/'scripts/build_academy.py')
academy=importlib.util.module_from_spec(spec);spec.loader.exec_module(academy)
class ReproducibleQaZip(unittest.TestCase):
 def checkout(self,root,stamp,mode):
  shutil.copytree(ROOT/'learning/qa-agent',root/'learning/qa-agent',ignore=shutil.ignore_patterns('__pycache__'))
  (root/'tests').mkdir();shutil.copyfile(ROOT/'tests/test_qa_agent_lab.py',root/'tests/test_qa_agent_lab.py')
  for path in root.rglob('*'):
   if path.is_file():os.utime(path,(stamp,stamp));path.chmod(mode)
  (root/'out').mkdir()
  return root/'out'
 def test_different_checkout_paths_mtimes_modes_and_timezones_produce_identical_bytes(self):
  old_tz=os.environ.get('TZ')
  try:
   with tempfile.TemporaryDirectory() as directory:
    archives=[]
    for name,stamp,mode,zone in [('one',1,0o644,'UTC'),('another-long-path',1735689600,0o755,'Pacific/Honolulu')]:
     root=Path(directory)/name;out=self.checkout(root,stamp,mode)
     os.environ['TZ']=zone
     if hasattr(time,'tzset'):time.tzset()
     academy.publish(root,out);archives.append((out/'qa-agent-lab.zip').read_bytes())
    self.assertEqual(*archives)
  finally:
   if old_tz is None:os.environ.pop('TZ',None)
   else:os.environ['TZ']=old_tz
   if hasattr(time,'tzset'):time.tzset()
 def test_payloads_paths_and_explicit_metadata_match_sources(self):
  with tempfile.TemporaryDirectory() as directory:
   out=Path(directory);academy.publish(ROOT,out)
   expected={'learning/qa-agent/'+p.name:p.read_bytes() for p in sorted((ROOT/'learning/qa-agent').iterdir()) if p.is_file()}
   expected['tests/test_qa_agent_lab.py']=(ROOT/'tests/test_qa_agent_lab.py').read_bytes()
   with zipfile.ZipFile(out/'qa-agent-lab.zip') as archive:
    self.assertEqual(archive.namelist(),list(expected));self.assertIsNone(archive.testzip())
    self.assertEqual(archive.comment,b'')
    for info in archive.infolist():
     self.assertEqual(archive.read(info),expected[info.filename])
     self.assertEqual(info.date_time,(2026,11,1,0,0,0))
     self.assertEqual(info.compress_type,zipfile.ZIP_STORED)
     self.assertEqual(info.create_system,3)
     self.assertEqual(info.external_attr,0o100644 << 16)
     self.assertEqual(info.extra,b'');self.assertEqual(info.comment,b'')
 def test_no_zlib_dependency_and_repeated_publish_are_identical(self):
  with tempfile.TemporaryDirectory() as directory:
   out=Path(directory);academy.publish(ROOT,out);first=(out/'qa-agent-lab.zip').read_bytes()
   with mock.patch.object(zipfile,'zlib',None):academy.publish(ROOT,out)
   self.assertEqual((out/'qa-agent-lab.zip').read_bytes(),first)
if __name__=='__main__':unittest.main()
