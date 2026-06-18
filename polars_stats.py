"""Generalized descriptive statistics for any CSV using Polars."""

from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=Path)
    parser.add_argument("--group", action="append", default=[])
    args = parser.parse_args()

    df = pl.read_csv(args.data_path, ignore_errors=True)
    print(f"File: {args.data_path}")
    print(f"Rows: {df.height:,}")
    print(f"Columns: {df.width:,}")
    print(df.schema)
    print(df.describe())
    print(df.select([pl.col(column).null_count().alias(column) for column in df.columns]))
    for group in args.group:
        keys = group.split(",")
        if any(key not in df.columns for key in keys):
            print(f"\nSkipping group {keys}; not all columns exist.")
            continue
        print(f"\nGrouped by {keys}")
        print(df.group_by(keys).len().sort("len", descending=True).head(20))


if __name__ == "__main__":
    main()
