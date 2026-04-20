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
| After | 2020_Panini_Prizm_LeBron_James_PSA10_001.jpg |

| Stage | Example Filename |
|---|---|
| Before | DSC10294.jpeg |
| After | 2018_Topps_Update_Ronald_Acuna_Jr_US250_SGC9_002.jpg |

## Run

Use the main entrypoint:

python run_pipeline.py

## Notes

- This repository intentionally excludes private image inventories and generated reports.
- Only source code and safe project artifacts are tracked in version control.
