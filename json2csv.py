#!/usr/bin/env python3
import json
import csv
import argparse
import sys
import os

# Maximum file size (in bytes) we’ll process (e.g. 5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

def sanitize(cell):
    """Prevent CSV formula injection by prefixing dangerous leading chars."""
    s = str(cell)
    if s and s[0] in ('=', '+', '-', '@'):
        return "'" + s
    return s

def is_flat_record(obj):
    """Ensure we only have a flat dict of primitives (no nested lists/dicts)."""
    if not isinstance(obj, dict):
        return False
    for v in obj.values():
        if isinstance(v, (dict, list)):
            return False
    return True

def parse_args():
    parser = argparse.ArgumentParser(
        description="Securely convert a JSON array of flat objects to CSV."
    )
    parser.add_argument("input", help="Path to input JSON file")
    parser.add_argument("output", help="Path for output CSV file")
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing output file"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    # 1) File-size check
    try:
        size = os.path.getsize(args.input)
    except OSError as e:
        sys.exit(f"Error accessing input file: {e}")  # exit code 1
    if size > MAX_FILE_SIZE:
        sys.exit("Input file too large (over 5 MB).")     # exit code 2

    # 2) Prevent accidental overwrite
    if os.path.exists(args.output) and not args.force:
        sys.exit("Output file exists. Use --force to overwrite.")  # exit code 3

    # 3) Load JSON
    try:
        with open(args.input, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
    except json.JSONDecodeError as e:
        sys.exit(f"Invalid JSON: {e}")             # exit code 4
    except OSError as e:
        sys.exit(f"Error reading JSON file: {e}")   # exit code 1

    # 4) Validate structure
    if not isinstance(data, list) or not data:
        sys.exit("JSON must be a non-empty array of objects.")     # exit code 5
    if not all(is_flat_record(rec) for rec in data):
        sys.exit("All records must be flat objects (no nested lists/dicts).")  # exit code 6

    headers = list(data[0].keys())

    # 5) Write CSV
    try:
        with open(args.output, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            for entry in data:
                # sanitize each cell
                safe = {k: sanitize(entry.get(k, "")) for k in headers}
                writer.writerow(safe)
    except OSError as e:
        sys.exit(f"Error writing CSV file: {e}")    # exit code 7

    print(f"Successfully converted '{args.input}' to '{args.output}'.")
    sys.exit(0)

if __name__ == '__main__':
    main()
    