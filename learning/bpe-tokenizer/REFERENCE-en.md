# Transfer reference — use after an independent attempt
Base IDs: 狗=0 (U+72D7), 猫=1 (U+732B), code-point order, not pronunciation.
First counts: (猫,猫)=2; (猫,狗)=3. Select (猫,狗), token 猫狗 ID 2.
Pieces: 猫猫狗→[猫,猫狗] with frequency 2; 猫狗→[猫狗] with frequency 1.
Second count: (猫,猫狗)=2. Select it; 猫猫狗 becomes ID 3.
Vocabulary: [狗,猫,猫狗,猫猫狗]. Frozen 猫狗猫狗→[2,2] and back to the same word; 猫猫狗→[3]. 猫鸟 fails because 鸟 was absent from the base alphabet. Do not remove it or claim reversible unknown replacement.
Encoding uses existing rules and does not add tokens. A new corpus/rule budget can change IDs and token boundaries. aaa has 2 overlapping pairs but only 1 non-overlapping replacement in one scan. This algorithm learns symbols, not neural weights; no byte fallback, pre-tokenization, normalization, special tokens or chat templates. Its token count says nothing about a vendor's bill or model understanding.
