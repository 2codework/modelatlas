"""Run: python3 -B demo.py. Prints only; no network or model downloads."""
import json
from core import zeros, gradient, step, loss, predict, generate
from fixtures import TRAIN, COUNTEREXAMPLE


def main():
    before = zeros()
    after = step(before, TRAIN, 0.3)
    frozen = [row[:] for row in after]
    output = {'parameters': 9, 'samples': 5, 'before': before,
              'gradient': gradient(before, TRAIN), 'after': after,
              'train_loss_before': loss(before, TRAIN),
              'train_loss_after': loss(after, TRAIN),
              'counterexample_loss_before': loss(before, COUNTEREXAMPLE),
              'counterexample_loss_after': loss(after, COUNTEREXAMPLE),
              'p_after_A': predict(after, ['A']), 'p_after_B': predict(after, ['B']),
              'greedy_A_8': generate(after, ['A'], 8)}
    assert after == frozen
    output['inference_parameters_unchanged'] = after == frozen
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
