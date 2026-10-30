#!/usr/bin/env python3
"""
load_dataset.py — Quickstart Example for VietIRR-RAG Dataset

Demonstrates how to:
1. Load document manifest and query statistics.
2. Stream processed evidence units (text and tables).
3. Access structured tables by table_id.
4. Iterate over DEV-93 benchmark questions and inspect gold evidence links.

Usage:
    python examples/load_dataset.py
"""

import sys
import os
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 75)
    print("VIETIRR-RAG DATASET QUICKSTART DEMONSTRATION")
    print("=" * 75)

    # 1. Load Manifest
    manifest_path = os.path.join(ROOT_DIR, "data/manifests/corpus_manifest.jsonl")
    manifest = {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                manifest[d["doc_id"]] = d

    print(f"\n[1] Manifest Loaded:")
    print(f"    Total Documents: {len(manifest)}")
    sample_doc_id = list(manifest.keys())[0]
    sample_doc = manifest[sample_doc_id]
    print(f"    Sample Document:")
    print(f"      - ID          : {sample_doc['doc_id']}")
    print(f"      - Title       : {sample_doc['document_title']}")
    print(f"      - Publisher   : {sample_doc['issuing_organization']}")
    print(f"      - Pages       : {sample_doc['page_count']}")
    print(f"      - Evidence    : {sample_doc['total_evidence_count']} units")
    print(f"      - SHA-256     : {sample_doc['sha256'][:16]}...")

    # 2. Inspect Evidence Units
    evidence_path = os.path.join(ROOT_DIR, "data/processed/evidence_units.jsonl")
    print(f"\n[2] Reading Processed Evidence Units (Streaming Sample):")
    sample_text_unit = None
    sample_table_unit = None
    with open(evidence_path, "r", encoding="utf-8") as f:
        for line in f:
            unit = json.loads(line)
            if unit.get("unit_type") == "TEXT_REGION" and not sample_text_unit:
                sample_text_unit = unit
            elif unit.get("unit_type") == "TABLE_REGION" and not sample_table_unit:
                sample_table_unit = unit
            if sample_text_unit and sample_table_unit:
                break

    print(f"    Sample Text Evidence Unit:")
    print(f"      - Evidence ID : {sample_text_unit['evidence_id']}")
    print(f"      - Doc ID      : {sample_text_unit['doc_id']} (Page {sample_text_unit['page_number']})")
    print(f"      - Text Snippet: {sample_text_unit['index_text'][:120]}...")

    print(f"\n    Sample Table Evidence Unit:")
    print(f"      - Evidence ID : {sample_table_unit['evidence_id']}")
    print(f"      - Doc ID      : {sample_table_unit['doc_id']} (Page {sample_table_unit['page_number']})")
    print(f"      - Raw Caption : {sample_table_unit['index_text'][:120]}...")

    # 3. Inspect Structured Table
    tables_path = os.path.join(ROOT_DIR, "data/processed/tables.jsonl")
    print(f"\n[3] Reading Structured Table Matrices:")
    with open(tables_path, "r", encoding="utf-8") as f:
        sample_tab = json.loads(f.readline())
    print(f"    Table ID       : {sample_tab['table_id']}")
    print(f"    Columns        : {sample_tab.get('headers', [])[:4]}...")
    print(f"    Row Count      : {len(sample_tab.get('rows', []))}")
    print(f"    Structured Cells: {len(sample_tab.get('cells', []))} cells parsed")

    # 4. Inspect DEV-93 Benchmark Question
    dev_path = os.path.join(ROOT_DIR, "benchmarks/qa/dev_93.jsonl")
    print(f"\n[4] Inspecting DEV-93 Benchmark Item:")
    with open(dev_path, "r", encoding="utf-8") as f:
        dev_sample = json.loads(f.readline())
    print(f"    QA ID          : {dev_sample['qa_id']}")
    print(f"    Question       : {dev_sample['question']}")
    print(f"    Answer         : {dev_sample['answer'][:120]}...")
    print(f"    Gold Docs      : {dev_sample.get('gold_doc_ids')}")
    print(f"    Retrieval Units: {dev_sample.get('retrieval_evidence_ids')}")
    print(f"    Location Type  : {dev_sample.get('location_type', 'CROSS_DOCUMENT')}")

    print("\n" + "=" * 75)
    print("Dataset reader completed successfully without errors.")
    print("=" * 75)

if __name__ == "__main__":
    main()
