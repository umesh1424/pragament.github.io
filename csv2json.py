import argparse
import csv
import json
import sys
from pathlib import Path

def csv_to_json(csv_path: Path, json_path: Path) -> None:
    """Convert a CSV file to JSON.

    Reads the CSV file assuming the first row contains headers and writes a JSON
    file containing a list of objects, each object representing a row.
    """
    if not csv_path.is_file():
        sys.stderr.write(f"Error: CSV file '{csv_path}' does not exist.\n")
        sys.exit(1)
    try:
        with csv_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    except Exception as e:
        sys.stderr.write(f"Failed to read CSV: {e}\n")
        sys.exit(1)
    try:
        with json_path.open('w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
    except Exception as e:
        sys.stderr.write(f"Failed to write JSON: {e}\n")
        sys.exit(1)
    print(f"Successfully converted '{csv_path}' to '{json_path}'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a JSON file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Path for the output JSON file. If omitted, the JSON file will be created next to the CSV with the same base name.",
    )
    args = parser.parse_args()

    csv_path = args.csv_file
    json_path = args.output
    if json_path is None:
        json_path = csv_path.with_suffix('.json')

    csv_to_json(csv_path, json_path)


if __name__ == "__main__":
    main()
