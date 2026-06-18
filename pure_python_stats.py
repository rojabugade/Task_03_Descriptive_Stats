"""Generalized descriptive statistics for any CSV using pure Python."""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


MISSING = {"", "na", "n/a", "null", "none", "nan", "missing", "-"}


def is_missing(value: object) -> bool:
    return value is None or str(value).strip().lower() in MISSING


def number(value: object) -> float | None:
    if is_missing(value):
        return None
    text = str(value).strip().replace(",", "").replace("$", "").replace("%", "")
    text = re.sub(r"^\((.*)\)$", r"-\1", text)
    try:
        return float(text)
    except ValueError:
        return None


def median(values: list[float]) -> float | None:
    if not values:
        return None
    values = sorted(values)
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2


def std(values: list[float]) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return 0.0
    avg = sum(values) / len(values)
    return math.sqrt(sum((value - avg) ** 2 for value in values) / (len(values) - 1))


def load(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader), list(reader.fieldnames or [])


def analyze(path: Path, groups: list[str]) -> None:
    rows, columns = load(path)
    print(f"File: {path}")
    print(f"Rows: {len(rows):,}")
    print(f"Columns: {len(columns):,}")
    print(f"Column names: {columns}")

    for column in columns:
        values = [str(row.get(column, "")).strip() for row in rows if not is_missing(row.get(column))]
        nums = [num for value in values if (num := number(value)) is not None]
        print(f"\nColumn: {column}")
        print(f"Missing: {len(rows) - len(values):,}")
        if values and len(nums) / len(values) >= 0.9:
            print("Type: numeric")
            print(f"Count: {len(nums):,}; Mean: {sum(nums) / len(nums):,.4f}; Min: {min(nums):,.4f}; Max: {max(nums):,.4f}; Std: {std(nums):,.4f}; Median: {median(nums):,.4f}")
        else:
            counts = Counter(values)
            print("Type: categorical")
            print(f"Count: {len(values):,}; Unique: {len(counts):,}; Top 5: {counts.most_common(5)}")

    for group in groups:
        keys = group.split(",")
        if any(key not in columns for key in keys):
            print(f"\nSkipping group {keys}; not all columns exist.")
            continue
        counts: dict[tuple[str, ...], int] = defaultdict(int)
        for row in rows:
            counts[tuple(row.get(key, "") for key in keys)] += 1
        print(f"\nGrouped by {keys}")
        for key, count in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20]:
            print(f"{key}: {count:,}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=Path)
    parser.add_argument("--group", action="append", default=[])
    args = parser.parse_args()
    analyze(args.data_path, args.group)


if __name__ == "__main__":
    main()
