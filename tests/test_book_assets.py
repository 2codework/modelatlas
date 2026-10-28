"""Root repository book and published books must resolve their local image URLs."""
import re,unittest
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
class BookAssets(unittest.TestCase):
 def test_all_three_books_resolve_relative_images_and_share_original_svg(self):
  source=(ROOT/'web/world-model-learning.svg').read_bytes()
  for folder in (ROOT,ROOT/'dist',ROOT/'docs'):
   with self.subTest(folder=folder.name):
    book=(folder/'BOOK.md').read_text()
    refs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',book)
    self.assertEqual(refs.count('world-model-learning.svg'),12)
    for ref in refs:
     parsed=urlsplit(ref)
     if parsed.scheme or parsed.netloc:continue
     self.assertFalse(parsed.path.startswith('/'),'book image must be relative')
     target=(folder/unquote(parsed.path)).resolve()
     self.assertTrue(target.is_relative_to(folder.resolve()),'image escapes book folder')
     self.assertTrue(target.is_file(),f'missing image: {target}')
    self.assertEqual((folder/'world-model-learning.svg').read_bytes(),source)
