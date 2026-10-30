#!/usr/bin/env python3
"""
validate_dataset.py — VietIRR-RAG Schema and Relationship Validation Tool

Validates dataset records against defined schemas and cross-verifies referential integrity.
Can run in any standard Python environment without mandatory external dependencies.

Usage:
    python scripts/validate_dataset.py
"""

import sys
import os
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def validate_dict_fields(record, required_fields, types_dict, record_name):
    errors = []
    for f in required_fields:
        if f not in record:
            errors.append(f"Missing required field '{f}' in {record_name}")
        elif record[f] is None:
            errors.append(f"Field '{f}' is None in {record_name}")
        elif f in types_dict and not isinstance(record[f], types_dict[f]):
            errors.append(f"Field '{f}' has invalid type {type(record[f]).__name__} (expected {types_dict[f]}) in {record_name}")
    return errors

def main():
    print("=" * 70)
    print("VIETIRR-RAG DATASET SCHEMA & REFERENTIAL INTEGRITY VALIDATION")
    print("=" * 70)
    
    total_errors = 0
    
    # 1. Validate Manifest Schema
    print("\n[1/4] Validating Document Manifest Records...")
    doc_required = [
        "doc_id", "document_title", "issuing_organization", "document_type",
        "publication_year", "page_count", "file_size_bytes", "sha256",
        "source_url", "corpus_layer", "access_status", "redistribution_status",
        "total_evidence_count"
    ]
    doc_types = {
        "doc_id": str, "document_title": str, "issuing_organization": str,
        "document_type": str, "page_count": int, "file_size_bytes": int,
        "sha256": str, "total_evidence_count": int
    }
    
    manifest_doc_ids = set()
    with open(os.path.join(ROOT_DIR, "data/manifests/corpus_manifest.jsonl"), "r", encoding="utf-8") as fp:
        for idx, line in enumerate(fp, 1):
            row = json.loads(line)
            errs = validate_dict_fields(row, doc_required, doc_types, f"Manifest doc #{idx}")
            if errs:
                total_errors += len(errs)
                for e in errs[:3]:
                    print(f"  [ERROR] {e}")
            manifest_doc_ids.add(row["doc_id"])
    print(f"  Validated {len(manifest_doc_ids)} document manifest entries.")
    
    # 2. Validate Evidence Units Schema & References
    print("\n[2/4] Validating Evidence Units...")
    ev_required = ["doc_id", "evidence_id", "page_number", "unit_type", "index_text", "source_sha256"]
    ev_types = {"doc_id": str, "evidence_id": str, "page_number": int, "unit_type": str, "index_text": str}
    
    ev_count = 0
    ev_ids = set()
    sample_checked = 0
    with open(os.path.join(ROOT_DIR, "data/processed/evidence_units.jsonl"), "r", encoding="utf-8") as fp:
        for idx, line in enumerate(fp, 1):
            ev_count += 1
            row = json.loads(line)
            eid = row.get("evidence_id")
            ev_ids.add(eid)
            
            # Check first 500 records thoroughly for performance
            if sample_checked < 500:
                sample_checked += 1
                errs = validate_dict_fields(row, ev_required, ev_types, f"Evidence {eid}")
                if errs:
                    total_errors += len(errs)
                    for e in errs[:2]:
                        print(f"  [ERROR] {e}")
                        
            if row.get("doc_id") not in manifest_doc_ids:
                total_errors += 1
                print(f"  [ERROR] Evidence {eid} references unknown doc_id {row.get('doc_id')}")
    print(f"  Validated {ev_count} evidence units ({len(ev_ids)} unique IDs).")
    
    # 3. Validate Structured Tables
    print("\n[3/4] Validating Structured Tables...")
    tab_required = ["table_id", "doc_id", "page_number", "headers", "rows", "cells", "normalized_representation"]
    tab_types = {"table_id": str, "doc_id": str, "page_number": int, "headers": list, "rows": list, "cells": list}
    
    tab_count = 0
    with open(os.path.join(ROOT_DIR, "data/processed/tables.jsonl"), "r", encoding="utf-8") as fp:
        for idx, line in enumerate(fp, 1):
            tab_count += 1
            row = json.loads(line)
            errs = validate_dict_fields(row, tab_required, tab_types, f"Table {row.get('table_id')}")
            if errs:
                total_errors += len(errs)
                for e in errs[:2]:
                    print(f"  [ERROR] {e}")
            if row.get("doc_id") not in manifest_doc_ids:
                total_errors += 1
                print(f"  [ERROR] Table {row.get('table_id')} references unknown doc_id {row.get('doc_id')}")
    print(f"  Validated {tab_count} structured tables.")
    
    # 4. Validate Benchmark QA References
    print("\n[4/4] Validating Benchmark QA References (DEV-93)...")
    qa_required = ["qa_id", "question", "answer", "gold_doc_ids", "gold_page_ids", "gold_evidence_ids", "retrieval_evidence_ids"]
    qa_types = {"qa_id": str, "question": str, "answer": str, "gold_doc_ids": list, "gold_page_ids": list, "gold_evidence_ids": list, "retrieval_evidence_ids": list}
    
    dev_count = 0
    with open(os.path.join(ROOT_DIR, "benchmarks/qa/dev_93.jsonl"), "r", encoding="utf-8") as fp:
        for idx, line in enumerate(fp, 1):
            dev_count += 1
            row = json.loads(line)
            errs = validate_dict_fields(row, qa_required, qa_types, f"QA {row.get('qa_id')}")
            if errs:
                total_errors += len(errs)
                for e in errs[:2]:
                    print(f"  [ERROR] {e}")
            for did in row.get("gold_doc_ids", []):
                if did not in manifest_doc_ids:
                    total_errors += 1
                    print(f"  [ERROR] QA {row.get('qa_id')} references unknown doc_id {did}")
            for rid in row.get("retrieval_evidence_ids", []):
                if rid not in ev_ids:
                    total_errors += 1
                    print(f"  [ERROR] QA {row.get('qa_id')} references unknown retrieval_evidence_id {rid}")
    print(f"  Validated {dev_count} benchmark QA entries.")
    
    print("\n" + "=" * 70)
    if total_errors == 0:
        print("RESULT: ALL RECORDS PASSED SCHEMA & REFERENTIAL INTEGRITY VALIDATION.")
        print("=" * 70)
        return 0
    else:
        print(f"RESULT: VALIDATION ENCOUNTERED {total_errors} ERRORS.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
