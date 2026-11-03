# From characters to token IDs: a tiny BPE

Original, runnable Unicode-character BPE lesson, not a vendor tokenizer, byte-level BPE or language model. Prerequisites: lists, dictionaries, loops and integer arithmetic. Outcome: count pairs, learn two rules, freeze a tokenizer, encode/decode a new word and explain failure boundaries. No learner trial or completion-time claim.

## Contract

A corpus is 1..32 distinct nonempty word strings with positive integer frequencies 1..1000. Each word has at most 64 Unicode code points; the frequency-weighted total is at most 10000. Whitespace and surrogate code points are rejected, not normalized or discarded. Words are independent: no pair crosses a boundary. This is not a sentence pre-tokenizer. There is no Unicode normalization, special-token protocol, chat template or byte fallback.

Training counts adjacent token pairs weighted by word frequency. Choose maximum count; ties use Python tuple ordering of Unicode code-point strings. Recount after every merge. Replace left-to-right without overlap. Initial IDs follow sorted unique characters; each new merged string gets the next ID. If a merged string already exists, reuse its ID, without overwriting it. Stop after the integer budget 0..32 or when no pairs remain. Training returns immutable tuple-based rules/vocabulary plus a separate inspection trace.

Encoding uses frozen rules in their learned order; it does not learn from the new input. One word of 1..256 code points is supported; unknown characters fail explicitly. Decoding joins vocabulary strings; 1..256 exact integer IDs are required and decoded length is capped at 256. Empty input is rejected. IDs are local to this tokenizer, not semantic labels shared by models. A decoded arbitrary valid ID sequence need not be the canonical encoding of that word. These are teaching bounds, not general BPE requirements.

## Worked corpus and full trace

W = {"abab":2, "abac":1}. Alphabet a,b,c receives IDs 0,1,2.

Initial pairs: (a,b)=5, (b,a)=3, (a,c)=1. The two occurrences of ab inside abab each count twice because the word frequency is 2; abac contributes one more. Merge(a,b)→ ab, ID 3.

Pieces: abab→[ab,ab], abac→[ab,a,c]. New pairs: (ab,ab)=2, (ab,a)=1, (a,c)=1. Merge(ab,ab)→ abab, ID 4. Vocabulary is [a,b,c,ab,abab].

Frozen encoding: abab→[4]; abac→[3,0,2]; new combination ababc→[4,2]. Decoding reconstructs each exact word. The 5 characters of ababc become 2 toy tokens; neither count estimates a real API bill or proves understanding.

Pair counting and replacement differ: aaa contains two overlapping(a,a) pairs, but one left-to-right merge produces[aa,a], not[aa,aa]. With corpus {"ac":1,"ab":1}, the tied first choice is(a,b), regardless of dictionary insertion order.

## Run and inspect

Python 3.9+, standard library only. Inspect core.py first, extract the ZIP, enter bpe-tokenizer, then run:

    python3 -B demo.py
    python3 -B -m unittest -v

No package installation, account, network, GPU, weights or API key. The page does not execute Python. The demo computes in memory and prints JSON; it does not write a tokenizer file. Check trace, vocabulary, encoded, roundtrips and frozen_tokenizer_unchanged=true. Tests are algorithm contracts, not model performance or learner mastery.

For manual zero/one/two-merge comparisons, change the demo train budget to 0,1,2 in your own copy and record outputs. Restore the original before running tests. Tokenizer training learns symbol rules; it is not neural language-model weight training. Do not feed these IDs into an unrelated model.

## Independent transfer

Use T={"猫猫狗":2,"猫狗":1}, budget 2. Before opening REFERENCE-en.md, fill WORKSHEET-en.md: first pair counts, two selected rules, vocabulary with IDs, frozen encoding/decoding of 猫狗猫狗, and what happens for 猫鸟. Explain why ordering uses code points rather than pronunciation; why new input does not change rules; why fewer tokens is not a language-quality result.

## Recover and accept

If counts differ, check word frequencies and count every adjacent pair before merging; do not join separate words. If IDs differ, restore alphabetical code-point order and merge budget. Unknown characters: retain the failing input and error; do not silently delete a character. A new corpus or normalization policy means a different tokenizer and incompatible IDs, not a patch to existing output. Preserve the old artifact and rerun tests.

Acceptance: independently recover the worked counts and rules, explain overlap/ties/boundaries, complete the transfer with reasons, run demo/tests and record Python version, commands and outputs. State at least three missing production features. No statement of mastery, compression quality or real-model compatibility follows from passing.
