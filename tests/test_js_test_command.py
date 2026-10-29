"""Explicit complete bounded JS suite; no fallback or altered assertions."""
import hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class JSCommand(unittest.TestCase):
 def test_ci_only_changes_explicit_scheduling(self):
  current=(ROOT/'.github/workflows/checks.yml').read_bytes()
  command=b'node --test --test-concurrency=1 tests/*.test.js'
  self.assertEqual(current.count(command),1)
  old=current.replace(command,b'node --test tests/*.test.js')
  self.assertEqual(hashlib.sha256(old).hexdigest(),'0003074aca8ee24bf9fa48a1c9f20be93e89d83b034a5672dc5d5103d2e6826a')
 def test_development_command_is_complete_and_explained(self):
  text=(ROOT/'README.md').read_text()
  self.assertIn('node --test --test-concurrency=1 tests/*.test.js',text)
  self.assertIn('find web tests',text)
  self.assertNotIn('node --test tests/core.test.js',text)
  for phrase in ['全部测试文件和断言仍执行','不自动回退','不修改 timeout','原因未确定','不能声称已证 OOM','任何断言失败仍直接失败']:self.assertIn(phrase,text)
