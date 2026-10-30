---
annotations_creators:
- expert-generated
language:
- vi
language_creators:
- found
license:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
pretty_name: VietIRR-RAG Dataset
size_categories:
- 10K<n<100K
source_datasets:
- original
tags:
- retrieval-augmented-generation
- vietnamese
- document-ai
- hydrology
- irrigation
- table-qa
- multi-hop-qa
task_categories:
- question-answering
- text-retrieval
task_ids:
- open-domain-qa
- document-retrieval
---

# Dataset Card for VietIRR-RAG Dataset

## Dataset Summary
The **VietIRR-RAG** dataset is an open, reproducible, and provenance-grounded dataset comprising 93 official Vietnamese technical documents, 2,578 pages, 27,144 layout-aware evidence units (27,053 text regions and 91 table regions), 406 structured table matrices, and the **VietIrrDocBench** multi-evidence evaluation suite (DEV-93 and ALL-QA-545).

It addresses the lack of high-density domain technical corpora in Vietnamese by providing granular paragraph/table extraction and multi-evidence QA pairs requiring cross-page and cross-document reasoning.

## Supported Tasks
- **Multi-Evidence Document Retrieval**: Evaluating dense/sparse and hybrid retrieval models on retrieving precise paragraphs and tables from a large corpus of technical engineering documents.
- **Complex Question Answering**: Testing LLMs (such as Qwen 2.5, GPT-4, etc.) on generating faithful, cited answers without hallucinating irrigation telemetry numbers.
- **Table Understanding & QA**: Extracting metrics from complex hierarchical Vietnamese tables.

## Dataset Composition
- **Documents**: 93 official Vietnamese PDFs (190.6 MB source, 2,578 pages).
- **Evidence Units**: 27,144 units (27,053 text regions, 91 table regions).
- **Structured Tables**: 406 structured tables with cell-level bounding boxes and row/column coordinate maps.
- **Evaluation Suite**:
  - `dev_93.jsonl`: 93 frozen questions requiring multi-evidence synthesis.
  - `all_qa_545.jsonl`: 545 QA pairs spanning pilot, core, and challenge splits.
  - `e2e_eval_24.jsonl`: 24 complete multi-stage R6 retrieval and generation traces.

## Languages
Monolingual Vietnamese (`vi`). Technical terminology adheres to Vietnamese hydraulic engineering norms (TCVN standards, inter-reservoir operational terminology).

## Data Schema & Fields
See [`schemas/`](schemas/) for official JSON Schema specifications:
- `document.schema.json`
- `evidence.schema.json`
- `table.schema.json`
- `qa.schema.json`

## Curation Rationale & Provenance
Documents were sourced from public government portals of the Ministry of Agriculture and Rural Development (Cục Thủy lợi, Cục Quản lý đê điều và Phòng chống thiên tai), the Government Office (chinhphu.vn), and Southern Institute of Water Resources Planning (SIWRP).

All documents are cryptographically fingerprinted using SHA-256 to ensure data immutability and provenance tracking.

## Licensing
- Annotations, layout text, tables, and benchmarks: **CC BY-NC-SA 4.0**
- Code and verification scripts: **MIT License**
- Third-party source PDFs retain their original agency terms.
