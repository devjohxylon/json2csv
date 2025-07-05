#!/usr/bin/env python3
import json
import csv
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a JSON array to CSV."
    )
    parser.add_argument("input", help="Path to input JSON file containing an array of objects")
    parser.add_argument("output", help="Path for the output CSV file")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        with open(args.input, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
    except (IOError, json.JSONDecodeError) as e:
        sys.exit(f"Error reading JSON: {e}")

    if not isinstance(data, list) or not data:
        sys.exit("Input JSON must be a non-empty array of objects.")

    headers = data[0].keys()

    try:
        with open(args.output, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
    except IOError as e:
        sys.exit(f"Error writing CSV: {e}")

    print(f"Successfully converted '{args.input}' to '{args.output}'.")

if __name__ == '__main__':
    main()
