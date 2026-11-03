import json, math, unittest
from pathlib import Path
from core import calculate
F=json.loads(Path(__file__).with_name('fixtures.json').read_text())
class NoiseTests(unittest.TestCase):
    def test_worked(self):
        r=calculate(**F['worked']);self.assertEqual(r['xt'],[1.1,-1.1]);self.assertAlmostEqual(r['mse'],.0225)
    def test_high(self):self.assertAlmostEqual(calculate(**F['high'])['mse'],.96)
    def test_transfer(self):
        r=calculate(**F['transfer']);self.assertAlmostEqual(r['mse'],.1)
        for a,b in zip(r['xt'],[.5,.4]):self.assertAlmostEqual(a,b)
    def test_oracle(self):
        for fixture in F.values():
            r=calculate(**dict(fixture,estimate=fixture['epsilon']));self.assertLess(r['mse'],1e-25)
    def test_identity(self):
        for a in [.01,.04,.36,.64,1]:
            for estimate in [[-10,10],[0,0],[.3,-.3]]:
                r=calculate(a,[1,-1],[.5,-.5],estimate);self.assertAlmostEqual(r['mse'],r['expected_mse'])
    def test_one(self):
        r=calculate(1,[10,-10],[-10,10],[10,-10]);self.assertEqual(r['predicted'],[10,-10]);self.assertEqual(r['mse'],0)
    def test_derived_values_not_input_clipped(self):
        r=calculate(.5,[10,10],[10,10],[-10,-10]);self.assertGreater(r['xt'][0],10);self.assertGreater(r['predicted'][0],10)
    def test_bad_alpha(self):
        for value in [0,-1,.009,1.01,10**1000,math.nan,math.inf,True,'0.5',None]:
            with self.subTest(value=value),self.assertRaises(ValueError):calculate(value,[1,1],[1,1],[1,1])
    def test_bad_vectors(self):
        for value in [[],[1],[1,2,3],[True,1],[math.nan,1],[math.inf,1],[11,1],['1',1],None]:
            for field in ['x0','epsilon','estimate']:
                fixture=dict(F['worked']);fixture[field]=value
                with self.subTest(value=value,field=field),self.assertRaises(ValueError):calculate(**fixture)
if __name__=='__main__':unittest.main()
