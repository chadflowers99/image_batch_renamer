import csv
import hashlib
import os
import re
import shutil
from datetime import datetime

SOURCE_FOLDER = "./my_cards"
OUTPUT_FOLDER = "./processed_cards"
RUN_LOG_CSV = "./renamed_files_log.csv"


class BatchRenamer:
    """Renames image files using deterministic slug naming."""

    SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

    def __init__(self, source_folder=SOURCE_FOLDER, output_folder=OUTPUT_FOLDER):
        self.source_folder = source_folder
        self.output_folder = output_folder
        self._integrity_log = {}  # src_path -> (original_hash, dst_path)

    def _get_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _slugify(self, value):
        text = value.strip().lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-") or "image"

    def build_filename(self, src_path, slug, sequence, total, include_date=True):
        ext = os.path.splitext(src_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            ext = ".jpg"

        pad = len(str(total))
        safe_slug = self._slugify(slug)
        parts = [safe_slug]

        if include_date:
            mtime = os.path.getmtime(src_path)
            parts.append(datetime.fromtimestamp(mtime).strftime("%Y-%m-%d"))

        parts.append(str(sequence).zfill(pad))
        return "-".join(parts) + ext

    def rename_images(self, slug="sports-card", include_date=True, dry_run=False):
        if not os.path.isdir(self.source_folder):
            print(f"Error: source folder not found: {self.source_folder}")
            return []

        files = sorted([
            f for f in os.listdir(self.source_folder)
            if f.lower().endswith(self.SUPPORTED_EXTENSIONS)
        ])

        if not files:
            print(f"Warning: no supported images found in {self.source_folder}")
            return []

        if not dry_run:
            os.makedirs(self.output_folder, exist_ok=True)

        total = len(files)
        results = []

        for seq, filename in enumerate(files, start=1):
            src_path = os.path.join(self.source_folder, filename)
            new_name = self.build_filename(src_path, slug, seq, total, include_date=include_date)
            dst_path = os.path.join(self.output_folder, new_name)

            if dry_run:
                print(f"[DRY RUN] {filename} -> {new_name}")
            else:
                original_hash = self._get_hash(src_path)
                shutil.copy2(src_path, dst_path)
                self._integrity_log[src_path] = (original_hash, dst_path)
                print(f"Renamed: {filename} -> {new_name}")

            results.append((filename, new_name))

        return results

    def verify_integrity(self):
        if not self._integrity_log:
            print("Warning: no rename session to verify.")
            return False

        all_passed = True
        for src_path, (original_hash, dst_path) in self._integrity_log.items():
            if not os.path.exists(dst_path):
                print(f"FAIL missing: {os.path.basename(dst_path)}")
                all_passed = False
                continue

            copied_hash = self._get_hash(dst_path)
            if copied_hash != original_hash:
                print(f"FAIL hash mismatch: {os.path.basename(dst_path)}")
                all_passed = False

        if all_passed:
            print("Integrity check passed.")
        else:
            print("Integrity check failed.")

        return all_passed

    def create_audit_report(self, report_dir=None):
        if not self._integrity_log:
            print("Warning: no rename session to report.")
            return None

        target_dir = report_dir or self.output_folder
        os.makedirs(target_dir, exist_ok=True)

        report_name = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        report_path = os.path.join(target_dir, report_name)

        with open(report_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Original Filename",
                "New Filename",
                "Original MD5",
                "New MD5",
                "Integrity Check",
            ])

            for src_path, (orig_hash, dst_path) in self._integrity_log.items():
                new_hash = self._get_hash(dst_path) if os.path.exists(dst_path) else "MISSING"
                status = "PASS" if orig_hash == new_hash else "FAIL"
                writer.writerow([
                    os.path.basename(src_path),
                    os.path.basename(dst_path),
                    orig_hash,
                    new_hash,
                    status,
                ])

        print(f"Audit report generated: {report_path}")
        return report_path

    def append_run_log(self, results, log_csv_path=RUN_LOG_CSV):
        """Appends this run's filename mappings to a cumulative CSV log."""
        if not results:
            print("Warning: no rename results to log.")
            return None

        log_dir = os.path.dirname(log_csv_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file_exists = os.path.exists(log_csv_path)
        run_timestamp = datetime.now().isoformat(timespec="seconds")

        with open(log_csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "run_timestamp",
                    "original_filename",
                    "new_filename",
                    "source_path",
                    "destination_path",
                ])

            for original_name, new_name in results:
                writer.writerow([
                    run_timestamp,
                    original_name,
                    new_name,
                    os.path.join(self.source_folder, original_name),
                    os.path.join(self.output_folder, new_name),
                ])

        print(f"Run log updated: {log_csv_path}")
        return log_csv_path


if __name__ == "__main__":
    renamer = BatchRenamer()
    renamer.rename_images(slug="sports-card", include_date=True, dry_run=True)
