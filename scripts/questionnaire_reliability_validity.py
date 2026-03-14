#!/usr/bin/env python3
"""Questionnaire reliability and optional validity checks."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def load_table(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    return pd.read_csv(path)


def cronbach_alpha(df: pd.DataFrame) -> float:
    item_var = df.var(axis=0, ddof=1)
    total_var = df.sum(axis=1).var(ddof=1)
    n_items = df.shape[1]
    return (n_items / (n_items - 1)) * (1 - item_var.sum() / total_var)


def item_total_corr(df: pd.DataFrame) -> pd.Series:
    total = df.sum(axis=1)
    result = {}
    for col in df.columns:
        result[col] = df[col].corr(total - df[col])
    return pd.Series(result, name="item_total_corr")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--items", nargs="+", required=True)
    parser.add_argument("--reverse-items", nargs="*", default=[])
    parser.add_argument("--scale-min", type=float, default=1)
    parser.add_argument("--scale-max", type=float, default=5)
    parser.add_argument("--outdir", default="outputs/questionnaire")
    args = parser.parse_args()

    df = load_table(Path(args.file), args.sheet).copy()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    items = df[args.items].apply(pd.to_numeric, errors="coerce")
    for col in args.reverse_items:
        items[col] = args.scale_max + args.scale_min - items[col]

    alpha = cronbach_alpha(items)
    pd.DataFrame({"metric": ["cronbach_alpha"], "value": [alpha]}).to_csv(
        outdir / "reliability_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    item_total_corr(items).to_frame().to_csv(
        outdir / "item_total_correlation.csv",
        encoding="utf-8-sig",
    )

    notes = ["Cronbach alpha and item-total correlations were computed."]
    try:
        from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

        clean = items.dropna()
        chi_square_value, p_value = calculate_bartlett_sphericity(clean)
        kmo_per_item, kmo_model = calculate_kmo(clean)
        pd.DataFrame(
            {
                "metric": ["bartlett_chi2", "bartlett_p", "kmo_model"],
                "value": [chi_square_value, p_value, kmo_model],
            }
        ).to_csv(outdir / "validity_summary.csv", index=False, encoding="utf-8-sig")
        pd.DataFrame({"item": clean.columns, "kmo": kmo_per_item}).to_csv(
            outdir / "kmo_per_item.csv",
            index=False,
            encoding="utf-8-sig",
        )
    except ImportError:
        notes.append("Install factor_analyzer if you need KMO and Bartlett tests.")

    with open(outdir / "notes.txt", "w", encoding="utf-8") as handle:
        handle.write("\n".join(notes) + "\n")

    print(f"Saved outputs to {outdir.resolve()}")


if __name__ == "__main__":
    main()
