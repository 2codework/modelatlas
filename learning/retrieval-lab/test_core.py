from dataclasses import replace
import unittest
from core import Document, prepare, search, extract, validate_citation, tokens, hit_at_k
from fixtures import DOCUMENTS, ALLOWED, CURRENT, TRANSFER, TRANSFER_CURRENT

class RetrievalTests(unittest.TestCase):
    def setUp(self): self.chunks=prepare(DOCUMENTS,ALLOWED,CURRENT)
    def test_chunk_offsets_and_filtering(self):
        self.assertEqual(len(self.chunks),4)
        for c in self.chunks:
            source=next(d for d in DOCUMENTS if (d.id,d.revision)==(c.doc_id,c.revision))
            self.assertEqual(source.text[c.start:c.end],c.quote)
        self.assertNotIn('10 days',' '.join(c.quote for c in self.chunks))
        self.assertFalse(any(c.doc_id=='private' for c in self.chunks))
    def test_worked_score_and_citation(self):
        h=search('archive retention',self.chunks)
        self.assertEqual((h[0]['matched_terms'],h[0]['query_terms']),(2,2))
        self.assertTrue(hit_at_k(h[:1],('guide','r2',0)))
        self.assertEqual(extract('archive retention',self.chunks)['status'],'candidate')
    def test_abstention_not_absence(self):
        for q in ('astronomy','Internal vault code','!!!'):
            self.assertEqual(extract(q,self.chunks)['status'],'refused')
    def test_tie_not_semantic_detection(self):
        result=extract('workshop host',self.chunks)
        self.assertEqual(result['status'],'needs_review')
        self.assertEqual(len(result['citations']),2)
    def test_tamper_and_version(self):
        c=self.chunks[0]
        self.assertTrue(validate_citation(c,self.chunks))
        for change in ({'quote':'45 days'},{'start':1},{'start':False},{'revision':'r3'},{'sha256':'0'*64}):
            self.assertFalse(validate_citation(replace(c,**change),self.chunks))
        self.assertFalse(validate_citation(c,prepare(TRANSFER,ALLOWED,TRANSFER_CURRENT)))
    def test_permissions_rechecked(self):
        self.assertFalse(validate_citation(self.chunks[0],prepare(DOCUMENTS,frozenset({'memo'}),CURRENT)))
    def test_transfer(self):
        new=prepare(TRANSFER,ALLOWED,TRANSFER_CURRENT)
        self.assertIn('45 days',extract('archive retention',new)['citations'][0].quote)
        self.assertEqual(extract('workshop host',new)['status'],'candidate')
    def test_untrusted_text_is_only_data(self):
        r=extract('ignore rules send secrets',self.chunks)
        self.assertEqual(r['status'],'candidate')
        self.assertIn('ignore rules',r['citations'][0].quote)
        self.assertEqual(r['reason'],'human_semantic_review_required')
    def test_duplicate_and_budgets(self):
        with self.assertRaises(ValueError):prepare([DOCUMENTS[1],DOCUMENTS[1]],ALLOWED,CURRENT)
        with self.assertRaises(ValueError):prepare([Document('guide','r2','x'*2001)],ALLOWED,CURRENT)
        with self.assertRaises(ValueError):search('x'*201,self.chunks)
        for k in (True,0,6,1.5):
            with self.assertRaises(ValueError):search('archive',self.chunks,k)
    def test_missing_revision_and_stable_ties(self):
        self.assertEqual(prepare(DOCUMENTS,ALLOWED,{}),())
        a=search('workshop host',self.chunks)
        b=search('workshop host',tuple(reversed(self.chunks)))
        self.assertEqual(a,b)
    def test_token_limits_not_semantics(self):
        self.assertEqual(tokens('ARCHIVE archive'),{'archive'})
        self.assertEqual(tokens('保留'),{'保','留'})
        self.assertEqual(extract('storage duration',self.chunks)['status'],'refused')

if __name__=='__main__':unittest.main()
