# Nine parameters: one real learning step

Python 3.9+; standard library only. No installation, API key, account, GPU, network or pretrained model. Extract `tiny-training-lab.zip`, enter `tiny-training`, then run:

```sh
python3 -B demo.py
python3 -B -m unittest -v
```

`-B` suppresses Python bytecode files. The demo computes in memory and prints JSON; it does not save weights. Read `core.py`, `fixtures.py` and `test_core.py` before execution. No user-provided code execution service exists on the website. This is actual numerical optimization of an original 3×3 logit table, not a Transformer, pretrained LLM, vendor evaluation or evidence of learning effectiveness.

## Contract
Vocabulary A/B/C; rows previous token, columns next token. One-token context. Full-batch mean cross-entropy with natural logarithm. Independent sequence boundaries are preserved. Training requires at least one transition; empty/singleton sequences contribute none. Unknown and bool tokens, nonfinite numbers, malformed tables, negative learning rates and invalid generation budgets fail with ValueError. Extremely large finite logits whose differences overflow also fail rather than return misleading values. No input is mutated. Step returns a new table; zero learning rate preserves values. Generation is deterministic greedy, tie order A/B/C, budget integer 0..32; no EOS, no promise of coherent language.

## Reproduce
TRAIN=A B A B A C yields 5 transitions. Zero table, learning rate 0.3. Expected mean loss 1.0986122886681098→1.0439803399807872; updated rows [-.06,.06,0], [.08,-.04,-.04], [0,0,0]. Floating-point near-zero residues are normal. The deliberately nonrepresentative A→A counterexample is never optimized; its loss rises to 1.159811928855196. This is not a representative held-out generalization test. For errors, restore original fixtures and zero table; do not edit expected answers to hide failures. A larger rate is not guaranteed to reduce loss.

Complete WORKSHEET-en.md before opening REFERENCE-en.md. Unit tests establish the implementation contract, not learner mastery. This lab has not undergone learner trials.

Mechanism reference: https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html (loss and optimizer sections; editorial check 2026-11-01). All ABC data, calculations and code are original teaching material; PyTorch is not a dependency. See SOURCES.md for separate source dates.
