# DATASET LIMITATIONS & UNCERTAINTIES

## 1. Known Scientific Limitations
Users and researchers should be aware of the following technical characteristics and limitations:

### 1.1 Optical Character Recognition (OCR) Artifacts
- Documents from 2015 to 2018 (e.g. older scanned administrative notices) contain historical scanning artifacts, stamp watermarks, and occasional diacritic substitution in raw OCR text.
- Clean normalized text is provided in `index_text`, but `raw_text` preserves authentic extraction noise.

### 1.2 Complex Table Structure Ambiguities
- Several irrigation reports feature nested headers, multi-row merged cells, and irregular multi-level column groupings.
- While 406 structured tables were parsed, tables with extreme visual hierarchy retain extraction uncertainty flags in `tables.jsonl` (field `quality_reasons`).

### 1.3 Domain Specificity
- The documents and benchmark questions focus exclusively on Vietnamese hydraulic and water resources engineering terminology (e.g. MNDBT, MNC, mực nước dâng gia cường, lưu lượng xả tràn, lưu vực liên hồ chứa).
- Evaluation results should not be generalized to general open-domain Vietnamese NLP without adaptation.

### 1.4 Source PDF Redistribution Restrictions
- Raw PDF documents are government publications subject to the publishing policies of the issuing ministries.
- To prevent copyright complications, the dataset repository provides authoritative URLs, cryptographic SHA-256 hashes, and retrieval automation rather than redistributing full raw PDF binaries.
