import copy
import unittest
from core import train, encode, decode, merge_once, Tokenizer
from fixtures import WORKED, TRANSFER
class BPE(unittest.TestCase):
 def test_worked(self):
  m,t=train(WORKED); self.assertEqual(t[0]['counts'],[('a','b',5),('a','c',1),('b','a',3)]); self.assertEqual(m.merges,(('a','b'),('ab','ab'))); self.assertEqual(m.vocabulary,('a','b','c','ab','abab')); self.assertEqual(encode(m,'abac'),(3,0,2)); self.assertEqual(encode(m,'ababc'),(4,2))
 def test_transfer(self):
  m,t=train(TRANSFER); self.assertEqual(m.alphabet,('狗','猫')); self.assertEqual(m.merges,(('猫','狗'),('猫','猫狗'))); self.assertEqual(encode(m,'猫狗猫狗'),(2,2)); self.assertEqual(encode(m,'猫猫狗'),(3,))
 def test_tie(self):
  m,_=train({'ac':1,'ab':1},1); self.assertEqual(m.merges,(('a','b'),))
 def test_overlap(self):
  m,t=train({'aaa':1},1); self.assertEqual(t[0]['counts'],[('a','a',2)]); self.assertEqual(t[0]['pieces']['aaa'],('aa','a')); self.assertEqual(merge_once(tuple('aaaa'),('a','a')),('aa','aa'))
 def test_boundaries_and_early_stop(self):
  m,t=train({'a':2,'b':1},32); self.assertEqual(t,[]); self.assertEqual(m.merges,())
 def test_immutable_and_deterministic(self):
  c=copy.deepcopy(WORKED);m,t=train(c);before=repr(m);encode(m,'ababc');self.assertEqual(before,repr(m));self.assertEqual(c,WORKED);self.assertEqual((m,t),train(dict(reversed(list(c.items())))))
 def test_roundtrip(self):
  import itertools
  for budget in range(3):
   m,_=train(WORKED,budget)
   for n in range(1,5):
    for chars in itertools.product('abc',repeat=n):
     text=''.join(chars);self.assertEqual(decode(m,encode(m,text)),text)
 def test_unknown_and_whitespace(self):
  m,_=train(WORKED)
  for s in ('','a b','ab\n','x','a\ud800'):
   with self.assertRaises(ValueError):encode(m,s)
 def test_bad_corpus(self):
  for c in ({},{'':1},{'a b':1},{'a':True},{'a':0},{'a':1.5},{'a'*65:1},{'a'*64:1000},[],{'a':1001}):
   with self.assertRaises(ValueError):train(c)
 def test_bad_budget(self):
  for b in (True,-1,33,1.1,'2'):
   with self.assertRaises(ValueError):train(WORKED,b)
 def test_bad_ids(self):
  m,_=train(WORKED)
  for ids in ([],[True],[-1],[5],[0.0],'0',[4]*257):
   with self.assertRaises(ValueError):decode(m,ids)
 def test_bad_model_and_lengths(self):
  m,_=train(WORKED)
  for bad in (None,Tokenizer(('a',),(('a','b'),),('a','ab')),Tokenizer(('a',),(),('x',))):
   with self.assertRaises(ValueError):encode(bad,'a')
  with self.assertRaises(ValueError):encode(m,'a'*257)
  with self.assertRaises(ValueError):decode(m,[4]*65)
if __name__=='__main__': unittest.main()
