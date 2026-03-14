#!/usr/bin/env python3
"""One-way or two-way ANOVA template."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def load_table(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--dv", required=True, help="Dependent variable")
    parser.add_argument("--factor-a", required=True)
    parser.add_argument("--factor-b")
    parser.add_argument("--outdir", default="outputs/anova")
    args = parser.parse_args()

    df = load_table(Path(args.file), args.sheet).copy()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.factor_b:
        formula = f"{args.dv} ~ C({args.factor_a}) * C({args.factor_b})"
    else:
        formula = f"{args.dv} ~ C({args.factor_a})"

    model = smf.ols(formula, data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)
    anova.to_csv(outdir / "anova_table.csv", encoding="utf-8-sig")

    with open(outdir / "model_summary.txt", "w", encoding="utf-8") as handle:
        handle.write(model.summary().as_text())

    if not args.factor_b:
        tukey = pairwise_tukeyhsd(df[args.dv], df[args.factor_a])
        with open(outdir / "tukey_result.txt", "w", encoding="utf-8") as handle:
            handle.write(str(tukey))

    print(f"Saved outputs to {outdir.resolve()}")


if __name__ == "__main__":
    main()
