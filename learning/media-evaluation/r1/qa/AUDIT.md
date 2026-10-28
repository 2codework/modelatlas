# Media evaluation independent QA r1

Decision: **accept for metadata-only integration**, with explicit unknowns. No required factual fixes. 11 entities = 6 benchmark records, 3 metrics, 1 harness and 1 dataset; not 11 datasets.

## Per-entity decisions

### bench-geneval-original
- Accept: Author paper confirms object co-occurrence, position, count and color; repository labels MIT for code.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/djghosh13/geneval · https://arxiv.org/abs/2310.11513

### bench-dpg-bench-original
- Accept: Paper confirms 1K dense prompts; author changelog says DPG-Bench released 2024-03-11; README recommends four images per prompt in a 2x2 grid; repository labels Apache-2.0.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/TencentQQGYLab/ELLA · https://arxiv.org/abs/2403.05135

### metric-fid-original
- Accept: Author paper introduces FID; TTUR README specifies Inception pool_3 distribution statistics, warns old unbatched implementation is buggy, and labels repository Apache-2.0. Not a dataset.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/bioinf-jku/TTUR · https://arxiv.org/abs/1706.08500

### bench-vbench-original
- Accept: Original paper states 16 dimensions. Repository distinguishes standard prompt suite and custom_input. Original protocol must not merge with 2.0, I2V or other variants.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/Vchitect/VBench · https://arxiv.org/abs/2311.17982

### bench-vbench-2-0
- Accept: Paper confirms five dimensions (human fidelity, controllability, creativity, physics, commonsense); author subdirectory and paper identify separate 2.0 protocol.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/Vchitect/VBench/tree/master/VBench-2.0 · https://arxiv.org/abs/2503.21755

### metric-fvd-original
- Accept: Paper explicitly separates FVD metric from SCV benchmark; author README identifies implementation and real/generated video tensor preprocessing. Not a dataset.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/google-research/google-research/tree/master/frechet_video_distance · https://arxiv.org/abs/1812.01717

### metric-fad-original
- Accept: Paper identifies music-enhancement metric; author implementation depends on VGGish. Background distribution, embedding and preprocessing must remain explicit. Not a dataset.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/google-research/google-research/tree/master/frechet_audio_distance · https://arxiv.org/abs/1812.08466

### harness-audiobench
- Accept: Author current README says 50+ datasets; paper abstract says 8 tasks and 26 datasets. Harness entity is an explicit registry modeling choice, not denial that paper calls it a benchmark.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license
- Sources: https://github.com/AudioLLMs/AudioBench · https://arxiv.org/abs/2406.16020

### bench-mmau-v051525-test-mini
- Accept: Author README confirms version v05.15.25 and 1000 mini samples; linked HF dataset page license tag confirms CC-BY-NC-4.0. Card-revision-to-version mapping remains unpinned.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; dataset card revision not pinned to v05.15.25
- Sources: https://github.com/Sakshi113/MMAU · https://arxiv.org/abs/2410.19168 · https://huggingface.co/datasets/gamma-lab-umd/MMAU-test-mini

### bench-mmau-v051525-test
- Accept: Author README confirms 9000 test samples with answers/explanations withheld, and 2026-01-30 move from Eval.ai to linked HF Space. No evaluation submission performed.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license; dataset card revision not pinned to v05.15.25
- Sources: https://github.com/Sakshi113/MMAU · https://arxiv.org/abs/2410.19168 · https://huggingface.co/datasets/gamma-lab-umd/MMAU-test

### data-musiccaps-original
- Accept: MusicLM abstract confirms approximately 5.5k expert-described music-text pairs and links official project/Kaggle. Exact size, split, license and access remain unknown; existing unreadable targets not retried.
- Unknown: harness/data revisions and actual execution not verified; no download or scoring access claim; data/media license not verified; implementation license is not dataset license; exact count, split and anonymous access not verified
- Sources: https://google-research.github.io/seanet/musiclm/examples/ · https://arxiv.org/abs/2301.11325 · https://www.kaggle.com/datasets/googleai/musiccaps

## Dates and access
All ten distinct arXiv first/revision date pairs match the input. Paper date, benchmark release and repository update remain separate. DPG-Bench release is independently supported by the author changelog. Checked date is observation date; some web pages were cached, not proof of current runtime.

## Optional clarity
In the mini limitation text, explicitly attribute withholding to the separate 9,000-test split. Existing wording is factual but easy to skim incorrectly.

## Retained source limitations
Kaggle MusicCaps: zero-line body in prior check; unknown retained, not retried. Google MusicCaps old detail URL: generic index redirect in prior check; excluded, not retried. Neither is represented as a download-permission denial. Exact count, split, license and anonymous access remain unknown.

## Scope
No third-party code, models, benchmarks, submissions, downloads or credentials used. No canonical, candidate or research-pack changes. Public descriptions, aggregate facts and official links only. Incidental dataset-viewer content from metadata lookup was not retained.
