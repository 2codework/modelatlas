"""Coverage wording changes must not rewrite original case/snapshot bytes."""
import hashlib
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={'learning/coverage/2026-10-31/snapshot.json': 'fcc55fdae66d3c3332bd5d4a1bcda2ee7c495f4eb13d7c950c2f125e13cd2560', 'learning/coverage/2026-11-01/snapshot.json': '573984606dd978f705b3afaf6b75453a5c15b42a5d6240c60b00463450d00d69'}
class CoveragePreservation(unittest.TestCase):
 def test_original_inputs_remain_byte_identical(self):
  for name, digest in EXPECTED.items():
   with self.subTest(path=name):
    self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
