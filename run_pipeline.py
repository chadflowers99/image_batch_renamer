import os
import sys
from renamer import BatchRenamer

RAW_DIR = os.getenv("CARD_RAW_DIR", "my_cards")
OUTPUT_DIR = os.getenv("CARD_OUTPUT_DIR", "processed_cards")
RENAME_SLUG = os.getenv("RENAME_SLUG", "sports-card")
INCLUDE_DATE = os.getenv("INCLUDE_DATE", "true").lower() == "true"
RUN_LOG_CSV = os.getenv("RUN_LOG_CSV", "renamed_files_log.csv")
REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")


def run():
    print("\n=== IMAGE RENAME PIPELINE ===\n")

    renamer = BatchRenamer(source_folder=RAW_DIR, output_folder=OUTPUT_DIR)

    print("Stage 1: Dry-run preview")
    preview = renamer.rename_images(
        slug=RENAME_SLUG,
        include_date=INCLUDE_DATE,
        dry_run=True,
    )

    if not preview:
        print("No supported image files found. Nothing to do.")
        sys.exit(0)

    print("\nStage 2: Live rename")
    results = renamer.rename_images(
        slug=RENAME_SLUG,
        include_date=INCLUDE_DATE,
        dry_run=False,
    )

    if not results:
        print("Rename stage did not produce output.")
        sys.exit(1)

    print(f"\nRenamed {len(results)} file(s) into '{OUTPUT_DIR}'.")

    print("\nStage 3: Append run log")
    renamer.append_run_log(results, log_csv_path=RUN_LOG_CSV)

    print("\nStage 4: Integrity verification")
    passed = renamer.verify_integrity()
    if not passed:
        print("Integrity verification failed. Do not delete originals.")
        sys.exit(1)

    print("\nStage 5: Audit report")
    renamer.create_audit_report(report_dir=REPORTS_DIR)

    print("\nPipeline complete.")


if __name__ == "__main__":
    run()
