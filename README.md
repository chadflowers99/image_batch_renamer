# Image Batch Renamer

Deterministic, metadata-aware image processing pipeline for sports card inventory workflows.

## What This Project Does

- Standardizes image filenames using card metadata and deterministic naming rules.
- Resizes and normalizes images for downstream listing and catalog systems.
- Produces consistent outputs that are easy to audit and re-run.

## Workflow

1. Place source images in a local input folder.
2. Run the pipeline.
3. The tool validates metadata, renames images, and generates organized output files.

## Sample Output

This section shows a representative before-vs-after result so non-technical reviewers can quickly see the transformation.

| Stage | Example Filename |
|---|---|
| Before | IMG_4837.JPG |
| After | sports-card-2026-04-27-01.jpg |

| Stage | Example Filename |
|---|---|
| Before | DSC10294.jpeg |
| After | sports-card-2026-04-27-02.jpeg |

The live renamer uses an audit-safe pattern of `slug-YYYY-MM-DD-sequence.ext`, so the output stays deterministic for a given batch date and processing order.

## Run

Use the main entrypoint:

python run_pipeline.py

For reproducible batch naming in automated runs, you can set `BATCH_DATE` to override the default current-date stamp used in renamed files.

PowerShell example:

`$env:BATCH_DATE = "2026-04-27"`
`python run_pipeline.py`

## Notes

- This repository intentionally excludes private image inventories and generated reports.
- Only source code and safe project artifacts are tracked in version control.
