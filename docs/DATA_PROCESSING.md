# DATA PROCESSING & EVIDENCE EXTRACTION PIPELINE

## 1. Overview
The processing pipeline transforms raw scanned or digitally authored PDF documents into fine-grained, provenance-preserving evidence units.

```text
Raw Source PDFs (93 documents, 190.6 MB)
         │
         ▼
[1] Document Splitting & Layout Analysis (2,578 pages)
         │
         ├── Text Extraction & OCR Normalization
         │       └── 27,053 Text Region Units (REG_...)
         │
         └── Table Detection & Matrix Extraction
                 └── 91 Table Region Units (TAB_...)
                 └── 400+ Structured Table Matrices (cells, rows, columns)
         │
         ▼
[2] Canonical Evidence Index Serialization
    ├── data/processed/pages.jsonl (13.6 MB)
    ├── data/processed/evidence_units.jsonl (21.1 MB)
    ├── data/processed/tables.jsonl (13.0 MB)
    └── data/processed/retrieval_evidence_map.jsonl (0.5 MB)
```

## 2. Processing Stages

### Stage 1: Document Splitting & Layout Parsing
- Each document is serialized into individual page records (`PAGE_{doc_id}_{page_number}`).
- Page dimensions, reading order, and block boundaries are calculated.
- Total pages: **2,578 pages**.

### Stage 2: Text Normalization & Region Extraction
- Vietnamese diacritics and character encodings are normalized to Unicode UTF-8 (NFC form).
- Text paragraphs and administrative headings are grouped into coherent layout blocks (`TEXT_REGION`).
- Total text regions: **27,053 units**.

### Stage 3: Table Parsing & Cell Matrix Representation
- Table regions (`TABLE_REGION`) are extracted with bounding boxes.
- For each table:
  - Header hierarchy is parsed and normalized.
  - Rows and columns are indexed.
  - Individual data cells are assigned fine-grained coordinates (e.g. `_R006_C012`).
  - Markdown representations are generated for LLM context windows.
- Total table regions: **91 units**; total extracted structured table matrices in `tables.jsonl`: **406 tables**.

### Stage 4: Evidence Unit Indexing
- Each evidence unit retains:
  - `doc_id`: Link to parent document manifest.
  - `page_number`: 1-based page location.
  - `source_sha256`: Hash of source PDF for strict provenance verification.
  - `unit_type`: Modality indicator (`TEXT_REGION` or `TABLE_REGION`).
