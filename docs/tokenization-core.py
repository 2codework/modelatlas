"""Original bounded Unicode-character BPE lesson; not a vendor tokenizer."""
from collections import Counter
from dataclasses import dataclass


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError('integer outside allowed range')


def word(value, maximum=256):
    if type(value) is not str or not 1 <= len(value) <= maximum:
        raise ValueError('one nonempty bounded word string required')
    if any(c.isspace() or 0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise ValueError('whitespace and surrogate code points are unsupported')


def merge_once(symbols, pair):
    """Left-to-right non-overlapping replacement, returning a new tuple."""
    result, i = [], 0
    while i < len(symbols):
        if i + 1 < len(symbols) and (symbols[i], symbols[i+1]) == pair:
            result.append(pair[0] + pair[1]); i += 2
        else:
            result.append(symbols[i]); i += 1
    return tuple(result)


@dataclass(frozen=True)
class Tokenizer:
    alphabet: tuple
    merges: tuple
    vocabulary: tuple


def validate(model):
    if type(model) is not Tokenizer or type(model.alphabet) is not tuple or type(model.merges) is not tuple or type(model.vocabulary) is not tuple:
        raise ValueError('invalid tokenizer')
    if not model.alphabet or any(type(s) is not str or len(s) != 1 for s in model.alphabet):
        raise ValueError('invalid alphabet')
    for s in model.alphabet: word(s)
    if model.alphabet != tuple(sorted(set(model.alphabet))) or len(model.merges) > 32:
        raise ValueError('invalid alphabet order or merge count')
    vocab = list(model.alphabet)
    for pair in model.merges:
        if type(pair) is not tuple or len(pair) != 2 or any(type(s) is not str or s not in vocab for s in pair):
            raise ValueError('merge depends on unavailable symbols')
        token = ''.join(pair)
        if len(token) > 64: raise ValueError('merged symbol too long')
        if token not in vocab: vocab.append(token)
    if tuple(vocab) != model.vocabulary: raise ValueError('invalid vocabulary IDs')


def train(corpus, budget=2):
    integer(budget, 0, 32)
    if type(corpus) is not dict or not 1 <= len(corpus) <= 32:
        raise ValueError('1..32 distinct word strings required')
    for text, frequency in corpus.items():
        word(text, 64); integer(frequency, 1, 1000)
    if sum(len(text)*frequency for text, frequency in corpus.items()) > 10000:
        raise ValueError('weighted corpus exceeds 10000 characters')
    alphabet = tuple(sorted(set(''.join(corpus))))
    vocab, rules, trace = list(alphabet), [], []
    pieces = {text: tuple(text) for text in sorted(corpus)}
    for _ in range(budget):
        counts = Counter()
        for text, symbols in pieces.items():
            for pair in zip(symbols, symbols[1:]): counts[pair] += corpus[text]
        if not counts: break
        pair = min(counts, key=lambda p: (-counts[p], p))
        pieces = {text: merge_once(symbols, pair) for text, symbols in pieces.items()}
        token = ''.join(pair)
        if token not in vocab: vocab.append(token)
        rules.append(pair)
        trace.append({'counts': [(a,b,counts[(a,b)]) for a,b in sorted(counts)],
                      'selected': pair, 'pieces': dict(pieces)})
    model = Tokenizer(alphabet, tuple(rules), tuple(vocab))
    validate(model)
    return model, trace


def encode(model, text):
    validate(model); word(text)
    unknown = sorted(set(text) - set(model.alphabet))
    if unknown: raise ValueError('unknown characters: ' + repr(unknown))
    symbols = tuple(text)
    for pair in model.merges: symbols = merge_once(symbols, pair)
    return tuple(model.vocabulary.index(s) for s in symbols)


def decode(model, ids):
    validate(model)
    if type(ids) not in (tuple, list) or not 1 <= len(ids) <= 256:
        raise ValueError('1..256 token IDs required')
    for i in ids: integer(i, 0, len(model.vocabulary)-1)
    result = ''.join(model.vocabulary[i] for i in ids)
    if len(result) > 256: raise ValueError('decoded word exceeds 256 characters')
    return result
