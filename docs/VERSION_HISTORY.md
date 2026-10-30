# DATASET VERSION HISTORY & PROVENANCE LEDGER

## 1. Version Comparison Matrix

| Version Identifier | Status | Documents | Pages | Evidence Units | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1.0 - V2.4** | Archived | 40-75 | ~1,200 | ~15,000 | Pilot and early ablation corpora. |
| **V3.2_FINAL_SEMANTIC** | Baseline Benchmark | 89 PDFs | 2,479 | 27,045 units | Historical baseline used in initial experiments. |
| **V4_R6_FROZEN** | **Current Official Release** | **93 PDFs** | **2,578** | **27,144 units** | Authoritative frozen corpus for VietIRR-RAG. |

## 2. Inconsistency Clarification: 89 vs 93 Documents
In earlier research notes and interim sprint reviews, two distinct document counts appeared:
- **89 Documents**: Corresponds to `LEGACY_V3_2_REFERENCE`.
- **93 Documents**: The current operational corpus, which incorporates 4 new official irrigation management documents:
  1. `V4_CTTL_2025_77c60f84` (Quy trình vận hành hệ thống Bắc Nam Hưng)
  2. `V4_BNNMT_2025_594e7382` (Kế hoạch khai thác tài nguyên nước)
  3. `V4_CTTL_2024_dda51c21` (Dự thảo Quy trình vận hành hệ thống Cầu Cung)
  4. `V4_IWRP_2021_3031564c` (Báo cáo an toàn công trình CT02)

These 4 expansion documents contribute exactly 99 pages and 99 evidence units:
- **Pages**: 2,479 (V3.2) + 99 (V4.1) = **2,578 pages**.
- **Evidence Units**: 27,045 (V3.2) + 99 (V4.1) = **27,144 evidence units**.

## 3. Immutability & Freezing Policy
- `data/processed/pages.jsonl` and `data/processed/evidence_units.jsonl` are strictly immutable for V4.
- All evaluation benchmarks (DEV-93) are evaluated against this frozen index.
