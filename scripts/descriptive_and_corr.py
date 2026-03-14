#!/usr/bin/env python3
"""Descriptive statistics and correlation template."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def load_table(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--cols", nargs="*")
    parser.add_argument("--method", choices=["pearson", "spearman"], default="pearson")
    parser.add_argument("--outdir", default="outputs/descriptive")
    args = parser.parse_args()

    path = Path(args.file)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_table(path, args.sheet)
    cols = args.cols or df.select_dtypes(include="number").columns.tolist()
    numeric = df[cols].apply(pd.to_numeric, errors="coerce")

    desc = numeric.describe().T
    desc["median"] = numeric.median()
    desc["missing_n"] = numeric.isna().sum()
    desc["missing_pct"] = numeric.isna().mean().mul(100).round(2)
    desc.to_csv(outdir / "descriptive_stats.csv", encoding="utf-8-sig")

    corr = numeric.corr(method=args.method)
    corr.to_csv(outdir / f"correlation_{args.method}.csv", encoding="utf-8-sig")

    missing = df.isna().sum().rename("missing_n").to_frame()
    missing["missing_pct"] = df.isna().mean().mul(100).round(2)
    missing.to_csv(outdir / "missing_summary.csv", encoding="utf-8-sig")

    print(f"Saved outputs to {outdir.resolve()}")


if __name__ == "__main__":
    main()
