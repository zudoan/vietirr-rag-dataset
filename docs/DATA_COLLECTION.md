# DATA COLLECTION & CORPUS PROVENANCE

## 1. Overview
The **VietIRR-RAG** corpus is curated to support research on Retrieval-Augmented Generation (RAG) over dense Vietnamese technical documentation in irrigation engineering, dam operations, hydrology, and flood management.

## 2. Institutional Issuers & Sources
The documents originate from authoritative governmental portals and research institutes in Vietnam:
- **Cục Thủy lợi (Cục Quản lý và Xây dựng công trình thủy lợi — MARD)**: Technical bulletins, weekly reservoir monitoring reports, and irrigation infrastructure maintenance reports (56 documents).
- **Cục Quản lý đê điều và Phòng, chống thiên tai (MARD)**: Special flood response reports, national disaster risk assessments (SREX Vietnam), and river basin flood mitigation summaries (11 documents).
- **Viện Quy hoạch Thủy lợi Miền Nam (SIWRP)**: Hydrological monitoring and water resources forecast reports for the Mekong Delta, Dong Nai, and Southeastern basins (8 documents).
- **Cổng Thông tin điện tử Chính phủ (chinhphu.vn)**: Prime Ministerial Decisions on inter-reservoir operating procedures (Quy trình vận hành liên hồ chứa) across major river basins: Ba, Sê San, Srêpôk, Vu Gia - Thu Bồn, Mã, Cả, Hương (7 documents).
- **Ministry of Agriculture and Rural Development (MARD) & MoNRE**: Official notices and regional water management guidelines (5 documents).
- **Other Scientific Institutes (Viện Kỹ thuật Biển, Viện Quy hoạch Thủy lợi)**: Specialized hydrodynamic and salinity intrusion reports (6 documents).

## 3. Curation & Selection Criteria
Documents were collected according to strict scientific criteria:
1. **Domain Relevance**: High density of irrigation operational metrics (reservoir water level, dead storage level, normal high water level, discharge capacity, irrigated area).
2. **Structural Diversity**: Mix of continuous narrative text, hierarchical administrative clauses, structured tabular registries, and technical annexes.
3. **Temporal Coverage**: 2015 to 2026, capturing seasonal drought, flood discharges, and long-term climate adaptation planning.
4. **Verifiability**: Each document has an official URL, issuing date, and immutable SHA-256 cryptographic hash recorded in the catalog.

## 4. Preservation & Redistribution Policy
In compliance with Vietnamese legal regulations on official administrative publications:
- **Third-Party PDFs**: Kept on local research machines or retrieved on demand via `scripts/download_corpus.py` from official agency portals.
- **Derived Research Artifacts**: Extracted layout text, bounding boxes, structured markdown tables, and QA pairs are original scientific annotations and are made openly available for academic use.
