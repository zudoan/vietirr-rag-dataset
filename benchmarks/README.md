# VIETIRRDOCBENCH — EVALUATION BENCHMARKS

## 1. Overview
The benchmark suite provides rigorous question-answering evaluation sets for Vietnamese retrieval-augmented generation in irrigation and hydraulic engineering.

## 2. Benchmark Splits

| Split File | Count | Reasoning Modality | Target Evaluation |
| :--- | :--- | :--- | :--- |
| `benchmarks/qa/dev_93.jsonl` | **93** | Multi-Evidence (Cross-Page, Cross-Document) | Primary benchmark for multi-hop retrieval and answer synthesis |
| `benchmarks/qa/all_qa_545.jsonl` | **545** | Comprehensive Pool (Core, Challenge, Pilot) | Full curated question pool for training/evaluation |
| `benchmarks/qa/e2e_eval_24.jsonl` | **24** | Multi-Stage R6 Traces | In-depth retrieval and faithfulness diagnostic traces |

## 3. Ground Truth & Provenance Integrity
- **No Synthesized / Fabricated Answers**: All answers are grounded directly in the verified corpus evidence units.
- **Strict Evidence Necessity**: DEV-93 questions require multiple distinct facts; answering correctly without all supporting evidence indicates hallucination or parametric memorization.
- **Canonical IDs**: Every reference points to valid `doc_id` and `evidence_id` units present in `data/manifests/corpus_manifest.jsonl` and `data/processed/evidence_units.jsonl`.
