"""Approved book-only compatibility exception; archived source is never executed."""
import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA = 'b877d7655593471edf54db2341962f783cc4b1b971a6ab3b6a15e724f50e8cab'
CURRENT_SHA = '4e2b69df4d64f87f3e0c9ad15323079fc7ef2d4695a0fad8aa4f597c5b41487e'
BASELINE_PATH = ROOT / 'tests/fixtures/knowledge-graph-links-pre-book-stability.py.txt'


def without_book(source):
    """Remove exactly one top-level book function, retaining all other bytes."""
    tree = ast.parse(source)
    books = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'book']
    if len(books) != 1 or books[0].decorator_list:
        raise ValueError('expected exactly one undecorated book function')
    node = books[0]
    lines = source.splitlines(keepends=True)
    return b''.join(lines[:node.lineno - 1] + lines[node.end_lineno:])


def validate_nonbook(current, baseline):
    if without_book(current) != without_book(baseline):
        raise ValueError('nonbook source changed')


def validate(current=None, baseline=None):
    current = (ROOT / 'scripts/knowledge_graph_links.py').read_bytes() if current is None else current
    baseline = BASELINE_PATH.read_bytes() if baseline is None else baseline
    if hashlib.sha256(baseline).hexdigest() != BASELINE_SHA:
        raise ValueError('archived baseline SHA mismatch')
    if hashlib.sha256(current).hexdigest() != CURRENT_SHA:
        raise ValueError('approved current module SHA mismatch')
    validate_nonbook(current, baseline)
