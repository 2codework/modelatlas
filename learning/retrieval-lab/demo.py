"""Print local deterministic fixture results, no external effects."""
import json
from dataclasses import asdict
from core import prepare, search, extract, hit_at_k, validate_citation
from fixtures import DOCUMENTS, ALLOWED, CURRENT, TRANSFER, TRANSFER_CURRENT

def main():
    chunks=prepare(DOCUMENTS, ALLOWED, CURRENT)
    queries=('archive retention', 'workshop host', 'astronomy', 'Internal vault code')
    results={q:extract(q,chunks) for q in queries}
    hits=search('archive retention',chunks)
    old=hits[0]['chunk']
    changed=prepare(TRANSFER,ALLOWED,TRANSFER_CURRENT)
    return {'label':'deterministic lexical retrieval; no LLM',
            'chunks':[asdict(c) for c in chunks],
            'results':{q:{**r,'citations':[asdict(c) for c in r['citations']]} for q,r in results.items()},
            'worked_hit_at_1':hit_at_k(hits[:1],('guide','r2',0)),
            'old_citation_valid_in_new_snapshot':validate_citation(old,changed),
            'transfer':{**extract('archive retention',changed),'citations':[asdict(c) for c in extract('archive retention',changed)['citations']]}}

if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
