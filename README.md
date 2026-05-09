# Image Batch Renamer

Deterministic, audit-safe image processing pipeline for inventory normalization and batch organization workflows.

---

## Overview

Image Batch Renamer is a modular Python pipeline that standardizes messy image inventories into clean, reproducible outputs using deterministic naming rules, integrity verification, and automated audit reporting.

The project was designed around operational reliability principles:

* deterministic outputs
* reproducible batch processing
* collision-safe renaming
* integrity verification
* audit traceability
* non-destructive file handling

Instead of simply renaming files in-place, the pipeline performs staged processing with dry-run previews, logging, integrity checks, and audit report generation.

---

# Pipeline Workflow

```text
RAW IMAGE INVENTORY
        ↓
Stage 1: Dry-Run Preview
        ↓
Stage 2: Live Rename + Copy
        ↓
Stage 3: Run Log Append
        ↓
Stage 4: Integrity Verification
        ↓
Stage 5: Audit Report Generation
        ↓
PROCESSED INVENTORY OUTPUT
```

---

# Features

## Deterministic Filename Generation

Images are renamed using a reproducible slug/date/sequence pattern:

```text
sports-card-2026-05-09-01.jpg
sports-card-2026-05-09-02.jpg
```

This ensures:

* stable naming conventions
* sortable inventories
* batch reproducibility
* cleaner downstream catalog systems

---

## Dry-Run Preview

Before files are copied or renamed, the pipeline generates a full preview of all proposed output filenames.

Example:

```text
[DRY RUN] card_01_f.jpg -> sports-card-2026-05-09-01.jpg
```

This provides operational safety before execution.

---

## Collision-Safe Renaming

The pipeline detects when filenames already exist in the output directory and automatically resolves naming conflicts without overwriting existing files. In normal operation, this is transparent—the pipeline produces clean, deterministic filenames without collision suffixes.

---

## MD5 Integrity Verification

The pipeline verifies copied files using MD5 hash comparison.

Each processed image is validated to ensure:

* no corruption during copy
* no accidental overwrites
* source/destination integrity consistency

Example output:

```text
Integrity check passed.
```

---

## Audit Report Generation

Every pipeline run produces a timestamped audit report.

The report includes:

* original filename
* new filename
* original MD5 hash
* copied MD5 hash
* integrity status

Example:

| Original Filename | New Filename                  | Status |
| ----------------- | ----------------------------- | ------ |
| card_01_f.jpg     | sports-card-2026-05-09-01.jpg | PASS   |
| card_07_f.jpg     | sports-card-2026-05-09-02.jpg | PASS   |

---

## Run Logging

The pipeline appends rename activity into a cumulative CSV log:

```text
renamed_files_log.csv
```

This creates historical traceability across batch runs.

---

# Example Terminal Output

```text
=== IMAGE RENAME PIPELINE ===

Stage 1: Dry-run preview
[DRY RUN] card_01_f.jpg -> sports-card-2026-05-09-01.jpg
[DRY RUN] card_07_f.jpg -> sports-card-2026-05-09-02.jpg

Stage 2: Live rename
Renamed: card_01_f.jpg -> sports-card-2026-05-09-01.jpg
Renamed: card_07_f.jpg -> sports-card-2026-05-09-02.jpg

Stage 3: Append run log
Run log updated: renamed_files_log.csv

Stage 4: Integrity verification
Integrity check passed.

Stage 5: Audit report
=== AUDIT REPORT ===

   Original Filename | New Filename                  | Status
  ------------------+-------------------------------+-------
  card_01_f.jpg     | sports-card-2026-05-09-01.jpg | PASS  
  card_07_f.jpg     | sports-card-2026-05-09-02.jpg | PASS  
Audit report saved: reports/audit_report_20260509_1502.csv
```

---

# Project Structure

```text
image_batch_renamer/
│
├── my_cards/
├── processed_cards/
├── reports/
├── renamed_files_log.csv
├── renamer.py
├── run_pipeline.py
└── README.md
```

---

# Usage

## 1. Add source images

Place supported images into:

```text
my_cards/
```

Supported formats:

* .jpg
* .jpeg
* .png
* .webp

---

## 2. Run the pipeline

```bash
python run_pipeline.py
```

---

## 3. Review outputs

Processed files:

```text
processed_cards/
```

Audit reports:

```text
reports/
```

Run logs:

```text
renamed_files_log.csv
```

---

# Configuration

The pipeline supports environment-variable configuration.

| Variable        | Purpose                |
| --------------- | ---------------------- |
| CARD_RAW_DIR    | Source image directory |
| CARD_OUTPUT_DIR | Output directory       |
| RENAME_SLUG     | Output filename slug   |
| INCLUDE_DATE    | Include date stamp     |
| RUN_LOG_CSV     | Rename log path        |
| REPORTS_DIR     | Audit report directory |
| BATCH_DATE      | Override batch date    |

Example:

```powershell
$env:BATCH_DATE = "2026-05-09"
python run_pipeline.py
```

---

# Design Goals

This project focuses on operational reliability rather than simple file renaming.

Core engineering priorities:

* deterministic processing
* audit-safe workflows
* reproducible outputs
* integrity verification
* staged execution visibility
* non-destructive processing

---

# Example Use Cases

* sports card inventory normalization
* ecommerce product image organization
* catalog preparation workflows
* digital archive cleanup
* marketplace listing preparation
* media inventory standardization

---

# Technologies Used

* Python
* hashlib
* CSV logging
* deterministic slug generation
* MD5 integrity verification
* filesystem automation

---

# Portfolio Notes

Only source code, safe sample artifacts, and demonstration outputs are tracked in version control.
