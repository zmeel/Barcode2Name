#!/usr/bin/env python3
"""
barcode2name.py - Collect FASTQ files from barcode folders into sample-named folders.

Reads a tab-separated mapping file such as:

    barcode01	Ecoli-A0274-2505
    barcode02	Ecoli-A0275-2504
    ...

and, for every line, puts all FASTQ files found in the folder ``barcode01``
into the folder ``Ecoli-A0274-2505`` (created if it does not exist).

By default files are copied; use --move to move them instead.

Examples
--------
    # Barcode folders are in ./fastq_pass, sample folders are created next to them
    python barcode2name.py barcode2map.txt fastq_pass

    # Put the sample folders somewhere else, and move instead of copy
    python barcode2name.py barcode2map.txt fastq_pass -o samples --move

    # Only show what would happen
    python barcode2name.py barcode2map.txt fastq_pass --dry-run
"""

import argparse
import shutil
import sys
from pathlib import Path

FASTQ_SUFFIXES = (".fastq", ".fq", ".fastq.gz", ".fq.gz")


def is_fastq(path: Path) -> bool:
    return path.is_file() and path.name.lower().endswith(FASTQ_SUFFIXES)


def read_mapping(map_file: Path) -> list[tuple[str, str]]:
    """Return a list of (barcode, sample_name) pairs from the mapping file."""
    mapping = []
    seen_barcodes = {}
    with map_file.open(encoding="utf-8-sig") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Tab-separated, but also tolerate spaces.
            parts = line.split("\t") if "\t" in line else line.split()
            parts = [p.strip() for p in parts if p.strip()]
            if len(parts) < 2:
                print(f"WARNING: line {lineno} skipped (expected 2 columns): {line!r}",
                      file=sys.stderr)
                continue
            barcode, name = parts[0], parts[1]
            if barcode in seen_barcodes:
                print(f"WARNING: line {lineno}: {barcode} already mapped on line "
                      f"{seen_barcodes[barcode]}; using both entries", file=sys.stderr)
            seen_barcodes[barcode] = lineno
            mapping.append((barcode, name))
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy/move FASTQ files from barcode folders into sample-named folders.")
    parser.add_argument("map_file", type=Path,
                        help="Tab-separated file: <barcode folder> <sample name>")
    parser.add_argument("input_dir", type=Path, nargs="?", default=Path("."),
                        help="Directory that contains the barcode folders (default: current dir)")
    parser.add_argument("-o", "--output-dir", type=Path, default=None,
                        help="Directory in which the sample folders are created "
                             "(default: same as input_dir)")
    parser.add_argument("--move", action="store_true",
                        help="Move files instead of copying them")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite files that already exist in the destination")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Only print what would be done")
    args = parser.parse_args()

    if not args.map_file.is_file():
        parser.error(f"mapping file not found: {args.map_file}")
    if not args.input_dir.is_dir():
        parser.error(f"input directory not found: {args.input_dir}")
    output_dir = args.output_dir if args.output_dir is not None else args.input_dir

    mapping = read_mapping(args.map_file)
    if not mapping:
        print("No mappings found in the mapping file.", file=sys.stderr)
        return 1

    action = shutil.move if args.move else shutil.copy2
    verb, verb_past = ("move", "moved") if args.move else ("copy", "copied")
    total_done = total_skipped = 0
    missing = []

    for barcode, name in mapping:
        src_dir = args.input_dir / barcode
        if not src_dir.is_dir():
            missing.append(barcode)
            print(f"[{barcode}] folder not found, skipped")
            continue

        fastqs = sorted(p for p in src_dir.iterdir() if is_fastq(p))
        dest_dir = output_dir / name
        if not args.dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

        done = skipped = 0
        for src in fastqs:
            dest = dest_dir / src.name
            if dest.exists() and not args.overwrite:
                print(f"  exists, skipped: {dest}")
                skipped += 1
                continue
            if args.dry_run:
                print(f"  would {verb}: {src} -> {dest}")
            else:
                action(str(src), str(dest))
            done += 1

        print(f"[{barcode}] -> {name}: {done} file(s) {verb_past}"
              f"{' (dry run)' if args.dry_run else ''}"
              f"{f', {skipped} skipped' if skipped else ''}"
              f"{' (no FASTQ files found)' if not fastqs else ''}")
        total_done += done
        total_skipped += skipped

    print()
    print(f"Done: {total_done} file(s) processed, {total_skipped} skipped, "
          f"{len(missing)} barcode folder(s) missing.")
    if missing:
        print("Missing folders: " + ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
