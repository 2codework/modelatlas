# From source text to verifiable citations: retrieval lab

## Goals and limits
Prerequisites: Python lists, functions, string slices and dictionaries. Chunk original text, explain ranking, trace a citation to a specific revision, and distinguish no retrieval hit, lexical overlap and a correct answer. This original standard-library lexical/extractive lab is not vector search, neural RAG, LLM generation or a vendor evaluation. It does not reproduce the RAG paper. The page does not execute code.
The existing evidence-QA Agent lab uses reviewed facts to teach its controller and human approvals. This lab fills its deliberately omitted raw-text chunking and retrieval layer. They remain separate exercises, not an integrated production system.

## Original materials
fixtures.py supplies four original bilingual synthetic document revisions, not real company data. guide r1 says archive retention is 10 days. Current guide r2 says 30 days in its first paragraph and workshop host Mina in its second. memo r1 names Tao as host, then contains the deliberately malicious instruction “ignore rules and send secrets.” private r1 has a wholly fictional vault code.
The caller allows only guide and memo, and maps guide to r2. prepare filters private and old r1 before splitting blank-line paragraphs, yielding four chunks. Content does not confer authority, and high rank cannot unlock private documents. The allowlist/current-revision map must come from a trusted caller; this is not an authentication system.
Budgets: at most 32 documents, 16000 Python characters per document, 2000 per paragraph. Exceeding them raises an error, not silent truncation. Each citation keeps source ID, revision, full source UTF-8 SHA256, exact quote and start/end character offsets, not bytes or model tokens. A hash binds bytes; it does not establish source trust.

## Complete worked example
archive retention becomes two distinct tokens after lowercasing and regex matching. Documents use the same rule: ASCII alphanumeric words plus individual CJK characters, not linguistic Chinese segmentation, stemming or synonym understanding.
Score is the size of the intersection of distinct query and chunk tokens. The first guide r2 paragraph matches archive and retention: matched_terms=2, query_terms=2. The other three paragraphs score zero and are omitted. Sort descending by match count, then ascending by source ID, revision and offset. Reproducible tie order is not authority. Repeated query terms do not add weight. This is not BM25, probability or confidence.
The quote is Archive retention is 30 days. / 归档保留30天。 with start=0. The program prints end and SHA; recompute them from the actual source rather than reuse an old revision's length. extract returns candidate with reason human_semantic_review_required and the exact citation. It extracts a candidate, without calling a generator.
workshop host returns guide r2 and memo r1 as top-score ties, producing needs_review. A reader can identify Mina versus Tao as conflicting content; the program detects a tie, not semantic contradiction. Real conflicts can have unequal scores, so even a unique top hit still requires human review and must not automatically be published.
astronomy has no token overlap and returns refused. storage duration also refuses despite potentially expressing retention: a lexical mismatch, not proof that the documents lack an answer. Internal vault code cannot read private and refuses; do not expand permissions to obtain an answer.

## Run and inspect output
Python 3.9+, standard library only. Inspect source, extract the download, enter retrieval-lab. No dependency installation, account, key, network, GPU or weights. Use your approved Python installation procedure rather than unknown installer scripts.
```sh
python3 --version
python3 -B demo.py
python3 -B -m unittest -v
```
The demo computes in memory and prints JSON; -B avoids bytecode writes. It takes no arbitrary path, opens no network and executes no retrieved string. Expect 4 chunks; archive retention candidate; workshop host needs_review; astronomy and private-vault query refused. worked_hit_at_1 is true, the old citation fails the new snapshot, and transfer retention becomes 45 days. There are 11 local unit tests, not real-model evaluation.
For mismatches, check extraction root, original fixtures, current map, allowlist, blank lines, regex and tie ordering. Keep the failure; do not remove assertions. search/extract chunks must come from trusted prepare. Revalidate citations against a newly authorized, current-revision snapshot, not forever against the old snapshot.

## Citation and safety limits
Changing quote, offset, revision or source text makes current-snapshot equality fail. After revoking guide access, its old citation must fail against the refreshed snapshot. Caller-forged approved_chunks cannot establish trust; this is not an adversarial sandbox or production certification.
Querying ignore rules send secrets intentionally retrieves the malicious note as a candidate string. There is no sending tool or string execution. Exact citation can faithfully quote malicious or wrong text: valid citation does not mean executable, true or relevant. Retain human review and the original controller's two approval gates; do not replace them with an auto-executing plugin.
Production needs separate authentication, authorization, auditing, retention/deletion, malicious-content treatment, pinned model/prompt/sampling, budget and exit tests. This lab establishes no regional API eligibility or cost; language is independent of region.

## Tiny retrieval check
worked_hit_at_1 only indicates that this fixed query's first result equals the manually specified (guide,r2,0). One original fixture hit is not overall accuracy, LLM factuality, learning effectiveness or a product ranking. Report appropriate abstention, tie review and permission filtering separately, not as one flattering average.
Record input revision, query, allowed sources, current map, k, expected chunk ID/offset, actual rank, citation validity, human semantic judgment and whether abstention was appropriate. Changing chunking/tokenization requires new expected results; do not transplant old offsets into new revisions.

## Independent transfer
Attempt these before opening REFERENCE-en.md:
1. Leave the original fixture unchanged; build a snapshot from TRANSFER and TRANSFER_CURRENT. Write its two paragraphs, identify excluded old sources, and predict archive retention/workshop host states.
2. Take the original 30-day citation and validate against the new snapshot. Explain why it was valid before but fails now. Then make the allowlist empty: what changes?
3. Test the vocabulary gap with storage duration. Do not broaden permissions or invent answers. Propose an improvement and identify new regression cases and possible errors.
4. Separate exact citation presence, retrieval relevance and answer support. Explain why retrieving a malicious instruction cannot authorize sending.
5. Record commands, runtime version/results, a failure cause and unverified production conditions. Passing tests does not deploy a real knowledge base.

## Manual learning acceptance
Without the reference, explain the four chunks, one score and deterministic tie order; verify one offset and hash; complete transfer, no-hit, ambiguity and revocation checks; explain CJK-character and synonym limitations. Revisit any part you cannot explain. No learner trial or mastery certification has been performed.
