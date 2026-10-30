# DATA FORMAT SPECIFICATION

## 1. Directory Structure
```text
vietirr-rag-dataset/
├── data/
│   ├── manifests/
│   │   ├── corpus_manifest.csv       # Tabular manifest of all 93 documents
│   │   ├── corpus_manifest.jsonl     # Full JSONL metadata with provenance
│   │   ├── corpus_statistics.json    # Aggregated corpus counts
│   │   └── sha256_checksums.txt      # SHA-256 checksums of source PDFs
│   ├── processed/
│   │   ├── pages.jsonl               # 2,578 page records
│   │   ├── evidence_units.jsonl      # 27,144 text & table units
│   │   ├── tables.jsonl              # 406 structured table records
│   │   └── retrieval_evidence_map.jsonl # Mapping between coarse and fine units
│   └── samples/
│       └── sample_evidence_units.jsonl
├── benchmarks/
│   ├── qa/
│   │   ├── dev_93.jsonl              # Frozen 93 multi-evidence benchmark
│   │   ├── all_qa_545.jsonl          # Complete 545 QA evaluation pool
│   │   └── e2e_eval_24.jsonl         # 24 E2E evaluation traces
│   └── manifests/
│       └── benchmark_manifest.json
├── schemas/                          # Draft-07 JSON schemas
├── metadata/                         # Sources, provenance, and license CSVs
├── scripts/                          # Verification, validation, and loaders
└── docs/                             # Scientific documentation
```

## 2. Record Schemas

### 2.1 Manifest Record (`data/manifests/corpus_manifest.jsonl`)
```json
{
  "doc_id": "IRR_GOV_2015_b1eee844",
  "document_title": "srex vietnam report",
  "issuing_organization": "Cục Quản lý đê điều và Phòng, chống thiên tai",
  "document_type": "Technical Report",
  "publication_year": "2015",
  "page_count": 451,
  "file_size_bytes": 10563412,
  "sha256": "b1eee8445ee77201b4ecb64ef45e18a8468600d6cd84ea887969156a2298bd2f",
  "source_url": "https://phongchongthientai.mard.gov.vn/...",
  "corpus_layer": "LEGACY_V3_2_REFERENCE",
  "access_status": "PUBLIC_OFFICIAL",
  "redistribution_status": "SOURCE_LINK_ONLY",
  "text_evidence_count": 3669,
  "table_evidence_count": 0,
  "total_evidence_count": 3669
}
```

### 2.2 Evidence Unit Record (`data/processed/evidence_units.jsonl`)
```json
{
  "doc_id": "IRR_CP_2018_b4331af5",
  "evidence_id": "REG_IRR_CP_2018_b4331af5_P0001_B001",
  "page_id": "PAGE_IRR_CP_2018_b4331af5_0001",
  "page_number": 1,
  "unit_type": "TEXT_REGION",
  "index_text": "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM...",
  "raw_text": "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM...",
  "source_sha256": "b4331af5..."
}
```

### 2.3 Benchmark QA Record (`benchmarks/qa/dev_93.jsonl`)
```json
{
  "qa_id": "V3_1_CHAL_00018",
  "question": "Theo chuỗi tài liệu liên quan, diện tích đáp ứng tháng 06/2019...",
  "answer": "Diện tích đáp ứng tháng 06/2019 của Hồ Thác La là 342 ha...",
  "gold_doc_ids": ["IRR_CTL_2019_1fc21515", "IRR_CTL_2019_2154c957"],
  "gold_page_ids": ["PAGE_IRR_CTL_2019_1fc21515_0003", "PAGE_IRR_CTL_2019_2154c957_0004"],
  "gold_evidence_ids": [
    "TAB_IRR_CTL_2019_1fc21515_P0003_02_R002_C003",
    "TAB_IRR_CTL_2019_2154c957_P0004_02_R002_C003"
  ],
  "retrieval_evidence_ids": [
    "TAB_IRR_CTL_2019_1fc21515_P0003_02",
    "TAB_IRR_CTL_2019_2154c957_P0004_02"
  ],
  "location_type": "CROSS_DOCUMENT",
  "modality": "TABLE",
  "split": "dev"
}
```
