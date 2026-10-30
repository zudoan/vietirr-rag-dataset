#!/usr/bin/env python3
"""
summarize_dataset.py — VietIRR-RAG Dataset Summary & Statistics CLI

Generates and displays concise tabular statistics of the VietIRR-RAG dataset:
- Documents by publisher
- Pages and evidence distribution
- Benchmark composition

Usage:
    python scripts/summarize_dataset.py
"""

import sys
import os
import json
import csv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    stat_file = os.path.join(ROOT_DIR, "data/manifests/corpus_statistics.json")
    if os.path.exists(stat_file):
        with open(stat_file, "r", encoding="utf-8") as fp:
            stats = json.load(fp)
    else:
        stats = {}

    print("=" * 75)
    print("  VIETIRR-RAG DATASET — CORPUS & BENCHMARK SUMMARY")
    print("=" * 75)
    print(f"  Dataset Name   : {stats.get('dataset_name', 'VietIRR-RAG Dataset')}")
    print(f"  Version        : {stats.get('dataset_version', 'V4_R6_FROZEN')}")
    print(f"  Release Date   : {stats.get('release_date', '2026-10-30')}")
    print(f"  Language       : Vietnamese (vi)")
    print(f"  Domain         : {stats.get('domain', 'Irrigation & Water Engineering')}")
    print("-" * 75)
    
    docs = stats.get("documents", {})
    ev = stats.get("evidence_units", {})
    bm = stats.get("benchmarks", {})
    
    print("\n[1] CORPUS TOTALS")
    print(f"  * Total Promulgated Documents : {docs.get('total_documents', 93)} PDFs")
    print(f"    - Baseline V3.2 Documents   : {docs.get('legacy_v3_documents', 89)}")
    print(f"    - Expansion V4 Documents    : {docs.get('v4_new_documents', 4)}")
    print(f"  * Total Document Pages        : {docs.get('total_pages', 2578):,} pages")
    print(f"  * Total Evidence Units        : {ev.get('total_evidence_units', 27144):,} units")
    print(f"    - Text Regions (OCR/Layout) : {ev.get('text_regions', 27053):,}")
    print(f"    - Table Regions             : {ev.get('table_regions', 91)}")
    print(f"  * Structured Tables Extracted : {ev.get('structured_tables_extracted', 91)} tables")
    
    print("\n[2] EVALUATION BENCHMARKS")
    print(f"  * DEV-93 Multi-Evidence Test  : {bm.get('dev_93_evaluation_items', 93)} questions")
    print(f"  * Full Curated QA Pool        : {bm.get('all_qa_evaluation_pool', 545)} questions")
    print(f"  * E2E Multi-Stage Traces      : {bm.get('e2e_retrieval_traces', 24)} queries")

    # Read publisher breakdown from manifest
    manifest_csv = os.path.join(ROOT_DIR, "data/manifests/corpus_manifest.csv")
    publishers = {}
    if os.path.exists(manifest_csv):
        with open(manifest_csv, "r", encoding="utf-8") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                pub = row.get("issuing_organization", "Unknown")
                publishers[pub] = publishers.get(pub, 0) + 1

    print("\n[3] ISSUING ORGANIZATIONS")
    print(f"  {'Organization':<55} | {'Count':>6}")
    print("  " + "-" * 55 + "-+-" + "-" * 6)
    for pub, cnt in sorted(publishers.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pub:<55} | {cnt:>6}")

    print("=" * 75)

if __name__ == "__main__":
    main()
