"""Generalized descriptive statistics for any CSV using Pandas."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=Path)
    parser.add_argument("--group", action="append", default=[])
    args = parser.parse_args()

    df = pd.read_csv(args.data_path)
    print(f"File: {args.data_path}")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")
    print(df.dtypes.to_string())
    print("\nMissing values")
    print(pd.DataFrame({"missing_count": df.isna().sum(), "missing_percent": df.isna().mean() * 100}).to_string())
    print("\nNumeric describe")
    print(df.describe().to_string())
    print("\nNon-numeric describe")
    print(df.describe(include="object").to_string())
    for group in args.group:
        keys = group.split(",")
        if any(key not in df.columns for key in keys):
            print(f"\nSkipping group {keys}; not all columns exist.")
            continue
        print(f"\nGrouped by {keys}")
        print(df.groupby(keys, dropna=False).size().sort_values(ascending=False).head(20).to_string())


if __name__ == "__main__":
    main()
