"""Compare schemas across multiple CSV datasets."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def columns_for(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file)
        return set(next(reader, []))


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare CSV schemas across datasets.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    schemas = {path: columns_for(path) for path in args.paths}
    common = set.intersection(*schemas.values()) if schemas else set()
    print("Common columns across all datasets")
    for column in sorted(common):
        print(f"- {column}")

    for path, columns in schemas.items():
        unique = columns - set.union(*(other for other_path, other in schemas.items() if other_path != path)) if len(schemas) > 1 else columns
        print(f"\n{path}")
        print(f"Column count: {len(columns)}")
        print("Unique columns:")
        for column in sorted(unique):
            print(f"- {column}")


if __name__ == "__main__":
    main()
