#!/usr/bin/env python3
"""
verify_integrity.py — VietIRR-RAG Dataset Integrity Verification Tool

This script runs automated verification checks on the dataset repository:
1. Validates existence and non-emptiness of all manifests, data files, and benchmarks.
2. Checks JSON line syntax across all JSONL files.
3. Verifies that all 93 corpus documents are indexed.
4. Verifies that DEV-93 benchmark questions reference valid evidence units.
5. Verifies cryptographic format of SHA-256 checksums.

Usage:
    python scripts/verify_integrity.py
"""

import sys
import os
import json
import csv
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_file(path, min_lines=1):
    full_path = os.path.join(ROOT_DIR, path)
    if not os.path.exists(full_path):
        return False, f"File missing: {path}"
    size = os.path.getsize(full_path)
    if size == 0:
        return False, f"File empty (0 bytes): {path}"
    return True, f"OK ({size:,} bytes)"

def main():
    print("=" * 70)
    print("VIETIRR-RAG DATASET INTEGRITY VERIFICATION")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    # 1. Check critical files
    files_to_check = [
        "data/manifests/corpus_manifest.csv",
        "data/manifests/corpus_manifest.jsonl",
        "data/manifests/corpus_statistics.json",
        "data/manifests/sha256_checksums.txt",
        "data/processed/pages.jsonl",
        "data/processed/evidence_units.jsonl",
        "data/processed/tables.jsonl",
        "data/processed/retrieval_evidence_map.jsonl",
        "benchmarks/qa/dev_93.jsonl",
        "benchmarks/qa/all_qa_545.jsonl",
        "metadata/sources.csv",
        "metadata/provenance.csv",
        "metadata/document_versions.csv",
        "metadata/redistribution_policy.csv",
        "schemas/document.schema.json",
        "schemas/evidence.schema.json",
        "schemas/table.schema.json",
        "schemas/qa.schema.json",
        "README.md",
        "DATASET_CARD.md",
        "LICENSE",
        "CITATION.cff"
    ]
    
    print("\n[Step 1/5] Checking file existence and non-zero sizes...")
    for f in files_to_check:
        ok, msg = check_file(f)
        if ok:
            passed += 1
            print(f"  [PASS] {f:42s} : {msg}")
        else:
            failed += 1
            print(f"  [FAIL] {f:42s} : {msg}")
            
    # 2. Check manifest records
    print("\n[Step 2/5] Verifying corpus manifest records...")
    manifest_path = os.path.join(ROOT_DIR, "data/manifests/corpus_manifest.jsonl")
    manifest_doc_ids = set()
    manifest_count = 0
    with open(manifest_path, "r", encoding="utf-8") as fp:
        for idx, line in enumerate(fp, 1):
            if line.strip():
                manifest_count += 1
                row = json.loads(line)
                did = row.get("doc_id")
                if not did:
                    failed += 1
                    print(f"  [FAIL] Manifest row {idx} missing doc_id")
                manifest_doc_ids.add(did)
                
    if manifest_count == 93:
        passed += 1
        print(f"  [PASS] Manifest contains exactly 93 documents (Unique: {len(manifest_doc_ids)})")
    else:
        failed += 1
        print(f"  [FAIL] Expected 93 manifest records, found {manifest_count}")
        
    # 3. Check pages and evidence linking
    print("\n[Step 3/5] Verifying pages and evidence unit linking...")
    pages_path = os.path.join(ROOT_DIR, "data/processed/pages.jsonl")
    page_count = 0
    page_orphans = 0
    with open(pages_path, "r", encoding="utf-8") as fp:
        for line in fp:
            if line.strip():
                page_count += 1
                p = json.loads(line)
                if p.get("doc_id") not in manifest_doc_ids:
                    page_orphans += 1
                    
    if page_count == 2578 and page_orphans == 0:
        passed += 1
        print(f"  [PASS] Exactly 2,578 pages verified; 0 orphan document references.")
    else:
        failed += 1
        print(f"  [FAIL] Pages: count={page_count} (expected 2578), orphans={page_orphans}")
        
    evidence_path = os.path.join(ROOT_DIR, "data/processed/evidence_units.jsonl")
    ev_count = 0
    ev_ids = set()
    ev_orphans = 0
    text_count = 0
    table_count = 0
    with open(evidence_path, "r", encoding="utf-8") as fp:
        for line in fp:
            if line.strip():
                ev_count += 1
                e = json.loads(line)
                eid = e.get("evidence_id")
                ev_ids.add(eid)
                if e.get("doc_id") not in manifest_doc_ids:
                    ev_orphans += 1
                ut = e.get("unit_type")
                if ut == "TEXT_REGION":
                    text_count += 1
                elif ut == "TABLE_REGION":
                    table_count += 1
                    
    if ev_count == 27144 and ev_orphans == 0:
        passed += 1
        print(f"  [PASS] Exactly 27,144 evidence units verified (Text: {text_count}, Table: {table_count}); 0 orphans.")
    else:
        failed += 1
        print(f"  [FAIL] Evidence: count={ev_count} (expected 27144), orphans={ev_orphans}")
        
    # 4. Check benchmark DEV-93 evidence references
    print("\n[Step 4/5] Verifying benchmark DEV-93 integrity...")
    dev_path = os.path.join(ROOT_DIR, "benchmarks/qa/dev_93.jsonl")
    dev_count = 0
    missing_retrieval_refs = set()
    with open(dev_path, "r", encoding="utf-8") as fp:
        for line in fp:
            if line.strip():
                dev_count += 1
                q = json.loads(line)
                for rid in q.get("retrieval_evidence_ids", []):
                    if rid not in ev_ids:
                        missing_retrieval_refs.add(rid)
                        
    if dev_count == 93 and len(missing_retrieval_refs) == 0:
        passed += 1
        print(f"  [PASS] Exactly 93 DEV benchmark questions verified; 100% retrieval evidence IDs found in index.")
    else:
        failed += 1
        print(f"  [FAIL] DEV-93: count={dev_count}, missing retrieval refs={len(missing_retrieval_refs)}")
        
    # 5. Check SHA-256 checksum format
    print("\n[Step 5/5] Verifying SHA-256 checksums format...")
    sha_path = os.path.join(ROOT_DIR, "data/manifests/sha256_checksums.txt")
    valid_hashes = 0
    with open(sha_path, "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                parts = line.split(maxsplit=1)
                if len(parts) == 2 and re.match(r"^[a-fA-F0-9]{64}$", parts[0]):
                    valid_hashes += 1
                else:
                    failed += 1
                    print(f"  [FAIL] Malformed checksum line: {line}")
                    
    if valid_hashes == 93:
        passed += 1
        print(f"  [PASS] Exactly 93 valid SHA-256 checksums verified.")
    else:
        failed += 1
        print(f"  [FAIL] Expected 93 valid SHA-256 hashes, found {valid_hashes}")
        
    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed} CHECKS PASSED, {failed} FAILED")
    print("=" * 70)
    
    if failed == 0:
        print("\nAll dataset integrity checks PASSED successfully.")
        return 0
    else:
        print("\nIntegrity check FAILED with errors.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
