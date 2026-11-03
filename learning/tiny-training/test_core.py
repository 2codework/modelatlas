import copy
import math
import unittest
from core import *
from fixtures import TRAIN, TRANSFER, COUNTEREXAMPLE

class TrainingTests(unittest.TestCase):
    def assertTable(self, actual, expected):
        for row, wanted in zip(actual, expected):
            for x, y in zip(row, wanted): self.assertAlmostEqual(x, y, places=10)

    def test_worked(self):
        self.assertEqual(len(pairs(TRAIN)), 5)
        self.assertAlmostEqual(loss(zeros(), TRAIN), math.log(3))
        self.assertTable(gradient(zeros(), TRAIN), [[.2,-.2,0],[-4/15,2/15,2/15],[0,0,0]])
        w=step(zeros(), TRAIN)
        self.assertTable(w, [[-.06,.06,0],[.08,-.04,-.04],[0,0,0]])
        self.assertAlmostEqual(loss(w, TRAIN), 1.0439803399807872)
        self.assertAlmostEqual(loss(w, COUNTEREXAMPLE), 1.159811928855196)
        self.assertGreater(loss(w, COUNTEREXAMPLE),loss(zeros(),COUNTEREXAMPLE))

    def test_transfer(self):
        self.assertTable(step(zeros(),TRANSFER), [[-.06,0,.06],[0,0,0],[.08,-.04,-.04]])

    def test_finite_difference_all_nine(self):
        w=[[.2,-.4,.7],[.3,.1,-.8],[-.1,.5,.9]]
        g=gradient(w, TRAIN)
        for i in range(3):
            for j in range(3):
                a=copy.deepcopy(w); b=copy.deepcopy(w)
                a[i][j]+=1e-6; b[i][j]-=1e-6
                self.assertAlmostEqual(g[i][j],(loss(a,TRAIN)-loss(b,TRAIN))/2e-6, places=7)

    def test_stability(self):
        for a,b in zip(softmax([1000,1001,999]),softmax([0,1,-1])): self.assertAlmostEqual(a,b)
        self.assertAlmostEqual(sum(softmax([-1000,0,1000])),1)
        self.assertEqual(loss([[1000,-1000,0],[0,0,0],[0,0,0]], [('A','B')]),2000)

    def test_boundaries(self):
        self.assertEqual(pairs([['A','B'],['C','A']]),[(0,1),(2,0)])
        self.assertEqual(pairs([[],['A'],['B','C']]),[(1,2)])

    def test_zero_rate_and_immutability(self):
        w=zeros(); seq=[list(TRAIN[0])]; old=copy.deepcopy((w,seq))
        result=step(w,seq,0); loss(w,seq); gradient(w,seq); predict(w,['A']); generate(w,['A'],8)
        self.assertEqual((w,seq),old); self.assertEqual(result,w)
        result[0][0]=99; self.assertEqual(w,zeros())

    def test_frozen_context_and_budget(self):
        w=step(zeros(),TRAIN); before=copy.deepcopy(w); context=['A']
        self.assertEqual(predict(w,['A','B']),predict(w,['C','B']))
        self.assertEqual(generate(w,context,0),context)
        self.assertEqual(len(generate(w,context,32)),33)
        self.assertEqual(generate(w,['A'],8),list('ABABABABA'))
        self.assertEqual(w,before); self.assertEqual(context,['A'])
        for v in [-1,33,True,1.5,'2',None]:
            with self.assertRaises(ValueError): generate(w,['A'],v)

    def test_invalid_data(self):
        for seq in [[],[[]],[['A']],[[True,'B']],[['D','A']],['AB'],None]:
            with self.assertRaises(ValueError): loss(zeros(),seq)
        for context in [[],[False],['Z'],'A']:
            with self.assertRaises(ValueError): predict(zeros(),context)

    def test_invalid_numbers_and_shapes(self):
        for v in [True, float('nan'), float('inf'),float('-inf'),'1',None,10**400]:
            w=zeros(); w[0][0]=v
            with self.assertRaises(ValueError): loss(w,TRAIN)
            with self.assertRaises(ValueError): step(zeros(),TRAIN,v)
        for w in [[],[[0,0,0]],[[0]*2]*3,None]:
            with self.assertRaises(ValueError): predict(w,['A'])
        with self.assertRaises(ValueError): step(zeros(),TRAIN,-.1)
        with self.assertRaises(ValueError): softmax([1e308,-1e308,0])
        self.assertEqual(softmax([1e308]*3),[1/3]*3)

if __name__=='__main__': unittest.main()
