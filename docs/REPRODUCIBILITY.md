# REPRODUCIBILITY GUIDE

## 1. Environment & Requirements
The VietIRR-RAG dataset and inspection scripts are designed to be 100% reproducible on Linux, macOS, and Windows with standard Python 3.9+:

```bash
# Clone the dataset repository
git clone https://github.com/zudoan/vietirr-rag-dataset.git
cd vietirr-rag-dataset

# Standard Python — no heavy external dependencies required for data reading
python --version
```

## 2. Integrity Verification
Run the automated integrity verification tool to confirm all files, manifest rows, line counts, and checksums:

```bash
python scripts/verify_integrity.py
```
Expected output:
```text
SUMMARY: 27 CHECKS PASSED, 0 FAILED
All dataset integrity checks PASSED successfully.
```

## 3. Schema & Referential Integrity Validation
Run the schema validation script to confirm that all records adhere to the JSON schemas and all document/evidence references are valid:

```bash
python scripts/validate_dataset.py
```
Expected output:
```text
RESULT: ALL RECORDS PASSED SCHEMA & REFERENTIAL INTEGRITY VALIDATION.
```

## 4. Re-calculating Checksums
You can verify the SHA-256 hash of any downloaded PDF document against `data/manifests/sha256_checksums.txt`:

```bash
# On Linux / macOS
sha256sum -c data/manifests/sha256_checksums.txt

# On Windows PowerShell
Get-FileHash data/documents/*.pdf -Algorithm SHA256
```
