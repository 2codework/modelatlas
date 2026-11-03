"""Evidence-page contracts, not model evaluation or source truth certification."""
import copy
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_evaluation_evidence as E
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.ids=[];self.links=[];self.details=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append(tag)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='details':self.details.append(a)
class Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(E.DATA.read_text());cls.text=E.render(cls.data);cls.page=Page(cls.text)
    def reject(self,key,value):
        d=copy.deepcopy(self.data);d['snapshot'][key]=value
        with self.assertRaises(ValueError):E.validate(d)
    def test_exact_bounded_contract(self):
        s=E.validate(self.data);self.assertEqual(s['value'],53.3)
        self.assertEqual(s['report_date'],'2025-06-04');self.assertIsNone(s['report_first_published_date'])
        for key,val in [('model_version','ByteDance-Seed/Seed-Coder-8B-Base'),('benchmark','BigCodeBench-Instruct'),('split','Hard'),('metric','accuracy'),('report_version','latest'),('source_url','https://arxiv.org/html/2506.03524')]:self.reject(key,val)
    def test_reject_nonfinite_out_of_range_scores(self):
        for value in [float('nan'),float('inf'),-1,100.1,True,'53.3',None]:self.reject('value',value)
    def test_reviewed_snapshot_cannot_silently_drift(self):
        for key,val in [('value',55.0),('report_date','2025-05-08'),('checked_at','2026-11-01')]:self.reject(key,val)
        self.assertIn('已核对原始报告，未独立复现',self.text)
    def test_unknown_reasons_not_guessed(self):
        for key in ['evaluated_weight_revision','benchmark_version','shot','prompt','harness','sampling','report_first_published_date']:
            self.reject(key+'_note','');self.reject(key,'guessed')
        self.reject('shot',0);self.reject('evaluated_weight_revision','1c5af72afa21c22c9272a0b60a3a404195e88fcd')
    def test_sources_required_and_safe(self):
        d=copy.deepcopy(self.data);d['sources']=[]
        with self.assertRaises(ValueError):E.validate(d)
        for value in ['javascript:alert(1)','https://a:b@example.com','https://example.com/a b']:
            d=copy.deepcopy(self.data);d['sources'][0]['url']=value
            with self.assertRaises(ValueError):E.validate(d)
        for key in ['model_version','reported_by','evidence_locator','report_date','verification_status']:self.reject(key,None)
    def test_static_compact_accessible_contract(self):
        for tag in ['script','form','iframe','input','img']:self.assertNotIn(tag,self.page.tags)
        self.assertEqual(len(self.page.details),1);self.assertNotIn('open',self.page.details[0])
        self.assertEqual(len(self.page.ids),len(set(self.page.ids)))
        for text in ['厂商论文自报 · 本站未实跑、未独立复现','BigCodeBench-Completion · Full · pass@1','原评测索引保留 3 条历史快照，本页独立补充 1 条','评测权重 SHA','最早报告公开日','2025-05-14','无需 JavaScript',"script-src 'none'","connect-src 'none'"]:self.assertIn(text,self.text)
        self.assertLess(self.text.index('厂商论文自报'),self.text.index('53.3<span>'))
        css=(ROOT/'web/evaluation-evidence.css').read_text()
        for x in ['focus-visible','overflow-wrap:anywhere','@media(max-width:600px)']:self.assertIn(x,css)
    def test_escaping_and_deterministic_generation(self):
        self.assertEqual(self.text,E.render(self.data));self.assertEqual(self.text,(ROOT/'web/evaluation-evidence.html').read_text())
        d=copy.deepcopy(self.data);d['snapshot']['title']='<script>alert("x")</script>'
        rendered=E.render(d);self.assertNotIn('<script>',rendered);self.assertIn('&lt;script&gt;',rendered)
    def test_local_links(self):
        for link in self.page.links:
            if link.startswith('https://'):continue
            path=link.split('?',1)[0].split('#',1)[0]
            if not path: self.assertIn(link[1:],self.page.ids)
            else:self.assertTrue((ROOT/'web'/path).exists() or (ROOT/path).exists(),path)
        self.assertIn('evaluation-evidence.html',(ROOT/'web/benchmark-practice.html').read_text())
    def test_legacy_snapshot_preserved(self):
        legacy=ROOT/'data/research/evaluation-snapshots.json'
        self.assertEqual(len(json.loads(legacy.read_text())['snapshots']),3)
        self.assertEqual(hashlib.sha256(legacy.read_bytes()).hexdigest(),'65b3b2520ca59db7f5a189f7c770bcef5af20e29113bef518b9c46abc162f04c')
        existing=json.loads((ROOT/'dist/data.json').read_text())
        self.assertEqual(existing['evaluation_snapshots'],json.loads(legacy.read_text())['snapshots'])
        self.assertEqual(len(existing['dataset_benchmark_registry']),33)
