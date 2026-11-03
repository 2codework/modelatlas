"""Original nine-logit bigram teaching model. Python 3.9+, standard library only."""
import math

VOCAB = ('A', 'B', 'C')
MAX_NEW_TOKENS = 32


def number(value):
    if type(value) not in (int, float):
        raise ValueError('Expected a finite number, not a bool')
    try:
        value = float(value)
    except (OverflowError, ValueError):
        raise ValueError('Number outside finite float range') from None
    if not math.isfinite(value):
        raise ValueError('Expected finite number')
    return value


def vector(values):
    if not isinstance(values, (list, tuple)) or len(values) != 3:
        raise ValueError('Expected three logits')
    return [number(v) for v in values]


def weights(w):
    if not isinstance(w, (list, tuple)) or len(w) != 3:
        raise ValueError('Expected a 3 by 3 table')
    return [vector(row) for row in w]


def zeros():
    return [[0.0] * 3 for _ in VOCAB]


def tokens(sequence):
    if not isinstance(sequence, (list, tuple)):
        raise ValueError('Sequence must be a list/tuple of A/B/C strings')
    if any(type(t) is not str or t not in VOCAB for t in sequence):
        raise ValueError('Closed vocabulary: A, B, C only')
    return list(sequence)


def pairs(sequences):
    if not isinstance(sequences, (list, tuple)):
        raise ValueError('Expected a list/tuple of independent sequences')
    result = []
    for sequence in sequences:
        seq = tokens(sequence)
        result.extend((VOCAB.index(a), VOCAB.index(b)) for a, b in zip(seq, seq[1:]))
    if not result:
        raise ValueError('Training requires at least one within-sequence transition')
    return result


def shifted(row):
    row = vector(row)
    maximum = max(row)
    values = [x - maximum for x in row]
    # Finite inputs may still exceed representable differences: reject explicitly.
    if not all(math.isfinite(x) for x in values):
        raise ValueError('Logit differences exceed finite arithmetic range')
    return values


def softmax(row):
    values = shifted(row)
    exp = [math.exp(x) for x in values]
    denominator = math.fsum(exp)
    return [x / denominator for x in exp]


def loss(w, sequences):
    w = weights(w)
    samples = pairs(sequences)
    losses = []
    for a, b in samples:
        row = shifted(w[a])
        # Do not take log(softmax): probabilities can underflow to zero.
        losses.append(math.log(math.fsum(math.exp(x) for x in row)) - row[b])
    # Divide before summing to avoid avoidable overflow in the sum.
    result = math.fsum(x / len(samples) for x in losses)
    return number(result)


def gradient(w, sequences):
    w = weights(w)
    samples = pairs(sequences)
    grad = zeros()
    for a, b in samples:
        p = softmax(w[a])
        for j in range(3):
            grad[a][j] += (p[j] - int(j == b)) / len(samples)
    return grad


def step(w, sequences, learning_rate=0.3):
    old = weights(w)
    rate = number(learning_rate)
    if rate < 0:
        raise ValueError('Learning rate must be nonnegative')
    grad = gradient(old, sequences)
    return weights([[old[i][j] - rate * grad[i][j] for j in range(3)] for i in range(3)])


def predict(w, context):
    table = weights(w)
    seq = tokens(context)
    if not seq:
        raise ValueError('Prediction requires context')
    return softmax(table[VOCAB.index(seq[-1])])


def generate(w, context, max_new_tokens=8):
    table = weights(w)
    result = tokens(context)
    if not result:
        raise ValueError('Generation requires context')
    if type(max_new_tokens) is not int or not 0 <= max_new_tokens <= MAX_NEW_TOKENS:
        raise ValueError('Generation budget must be integer 0..32')
    for _ in range(max_new_tokens):
        p = predict(table, result)
        # Greedy; ties use fixed A,B,C order. No EOS token in this tiny vocabulary.
        result.append(VOCAB[max(range(3), key=lambda j: p[j])])
    return result
