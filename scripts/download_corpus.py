#!/usr/bin/env python3
"""
download_corpus.py — Automated Source Document Retrieval & Verification Tool

In accordance with publication rights and intellectual property policies, raw
third-party government PDF documents are retained locally or downloaded directly
from official governmental portals.

This helper script:
1. Reads data/manifests/corpus_manifest.csv.
2. Queries the official public source URL for each document.
3. Downloads the PDF to data/documents/<filename>.
4. Computes the cryptographic SHA-256 hash and verifies against manifest.

Usage:
    python scripts/download_corpus.py [--doc-id DOC_ID] [--target-dir data/documents]
"""

import sys
import os
import csv
import hashlib
import argparse

try:
    import urllib.request as request
except ImportError:
    pass

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Download and verify official VietIRR-RAG source PDFs.")
    parser.add_argument("--doc-id", type=str, default=None, help="Specific doc_id to download (default: all).")
    parser.add_argument("--target-dir", type=str, default="data/documents", help="Target output folder.")
    parser.add_argument("--dry-run", action="store_true", help="Print URLs without downloading.")
    args = parser.parse_args()

    manifest_path = os.path.join(ROOT_DIR, "data/manifests/corpus_manifest.csv")
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest not found at {manifest_path}")
        return 1

    target_dir = os.path.join(ROOT_DIR, args.target_dir)
    os.makedirs(target_dir, exist_ok=True)

    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        docs = list(reader)

    print("=" * 75)
    print(f"VIETIRR-RAG OFFICIAL SOURCE RETRIEVAL (Target: {target_dir})")
    print("=" * 75)

    downloaded = 0
    verified = 0
    skipped = 0
    failed = 0

    for doc in docs:
        did = doc["doc_id"]
        if args.doc_id and did != args.doc_id:
            continue

        url = doc.get("source_url", "").strip()
        expected_sha = doc.get("sha256", "").strip()
        filename = f"{did}.pdf"
        target_file = os.path.join(target_dir, filename)

        if not url:
            print(f"  [SKIP] {did}: No public URL recorded.")
            skipped += 1
            continue

        if os.path.exists(target_file):
            actual_sha = compute_sha256(target_file)
            if actual_sha.lower() == expected_sha.lower():
                print(f"  [EXISTS] {did}: Already downloaded and SHA-256 verified.")
                verified += 1
                continue

        if args.dry_run:
            print(f"  [DRY-RUN] {did} -> {url}")
            continue

        print(f"  [DOWNLOADING] {did} from {url[:60]}...")
        try:
            req = request.Request(url, headers={"User-Agent": "VietIrrResearch/1.0"})
            with request.urlopen(req, timeout=30) as response, open(target_file, "wb") as out_file:
                out_file.write(response.read())

            actual_sha = compute_sha256(target_file)
            if actual_sha.lower() == expected_sha.lower():
                print(f"    -> Success: SHA-256 matched ({actual_sha[:16]}...)")
                verified += 1
                downloaded += 1
            else:
                print(f"    -> Warning: Hash mismatch! Expected {expected_sha[:16]}, got {actual_sha[:16]}")
                failed += 1
        except Exception as e:
            print(f"    -> Download failed: {e}")
            failed += 1

    print("\n" + "=" * 75)
    print(f"Summary: {verified} verified, {downloaded} downloaded, {skipped} skipped, {failed} failed.")
    print("=" * 75)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
