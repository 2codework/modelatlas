"""Original lexical retrieval teaching core. No model, network, or file writes.

Caller supplies trusted allowed document IDs and current revisions. These inputs
are not authentication. Citations bind exact characters, not truth or relevance.
"""
from dataclasses import dataclass
import hashlib
import re


@dataclass(frozen=True)
class Document:
    id: str
    revision: str
    text: str


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    revision: str
    sha256: str
    start: int
    end: int
    quote: str


def tokens(text):
    """ASCII word tokens + individual CJK characters; not linguistic segmentation."""
    if not isinstance(text, str):
        raise ValueError('text must be str')
    return set(re.findall(r'[a-z0-9]+|[\u4e00-\u9fff]', text.lower()))


def prepare(documents, allowed_ids, current_revisions):
    """Filter before chunking. Blank-line paragraphs; no cross-document chunks."""
    if not isinstance(allowed_ids, (set, frozenset)) or not all(isinstance(x, str) for x in allowed_ids):
        raise ValueError('trusted allowlist required')
    if not isinstance(current_revisions, dict):
        raise ValueError('trusted revisions required')
    if not isinstance(documents, (list, tuple)) or len(documents) > 32:
        raise ValueError('at most 32 documents')
    seen = set()
    result = []
    for doc in documents:
        if not isinstance(doc, Document) or not all(isinstance(x, str) and x for x in (doc.id, doc.revision, doc.text)):
            raise ValueError('invalid document')
        if len(doc.text) > 16000 or len(doc.id) > 80 or len(doc.revision) > 80:
            raise ValueError('document budget exceeded')
        key = (doc.id, doc.revision)
        if key in seen:
            raise ValueError('duplicate identity/revision')
        seen.add(key)
        if doc.id not in allowed_ids or current_revisions.get(doc.id) != doc.revision:
            continue
        digest = hashlib.sha256(doc.text.encode('utf-8')).hexdigest()
        # Split blank lines, retaining exact offsets in the original Python string.
        start = 0
        for boundary in list(re.finditer(r'\n[ \t]*\n', doc.text)) + [None]:
            end = boundary.start() if boundary else len(doc.text)
            while start < end and doc.text[start].isspace(): start += 1
            while end > start and doc.text[end-1].isspace(): end -= 1
            if end > start:
                if end-start > 2000: raise ValueError('paragraph exceeds 2000 characters; split explicitly')
                result.append(Chunk(doc.id, doc.revision, digest, start, end, doc.text[start:end]))
            if boundary: start = boundary.end()
    return tuple(result)


def search(query, chunks, k=3):
    if not isinstance(query, str) or not 1 <= len(query) <= 200:
        raise ValueError('query must contain 1..200 characters')
    if type(k) is not int or not 1 <= k <= 5:
        raise ValueError('k must be an integer in 1..5')
    terms = tokens(query)
    # Coverage of distinct query terms, NOT probability or semantic confidence.
    scored = [(len(terms & tokens(c.quote)), c) for c in chunks]
    scored = [(n, c) for n, c in scored if n > 0]
    scored.sort(key=lambda x: (-x[0], x[1].doc_id, x[1].revision, x[1].start))
    return tuple({'matched_terms': n, 'query_terms': len(terms), 'chunk': c} for n, c in scored[:k])


def extract(query, chunks):
    """A local extractive candidate, never an automatic semantic answer."""
    hits = search(query, chunks, k=5)
    if not hits: return {'status':'refused', 'reason':'no_lexical_match', 'citations':()}
    tied = [h for h in hits if h['matched_terms'] == hits[0]['matched_terms']]
    if len(tied) > 1:
        return {'status':'needs_review', 'reason':'top_score_tie_not_proven_conflict', 'citations':tuple(h['chunk'] for h in tied)}
    return {'status':'candidate', 'reason':'human_semantic_review_required', 'citations':(hits[0]['chunk'],)}


def validate_citation(citation, approved_chunks):
    """Exact equality against a fresh, trusted, filtered snapshot; fail closed."""
    return (type(citation) is Chunk and type(citation.start) is int
            and type(citation.end) is int and 0 <= citation.start < citation.end
            and all(type(x) is str for x in (citation.doc_id,citation.revision,citation.sha256,citation.quote))
            and citation in approved_chunks)


def hit_at_k(hits, expected):
    """One fixture's rank hit; expected is (doc_id, revision, start)."""
    return any((h['chunk'].doc_id,h['chunk'].revision,h['chunk'].start) == expected for h in hits)
