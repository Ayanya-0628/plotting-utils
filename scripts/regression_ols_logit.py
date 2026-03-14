#!/usr/bin/env python3
"""OLS and logistic regression template."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


def load_table(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    return pd.read_csv(path)


def build_formula(y: str, x: list[str], categorical: list[str]) -> str:
    terms = [f"C({col})" if col in categorical else col for col in x]
    return f"{y} ~ " + " + ".join(terms)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--model", choices=["ols", "logit"], default="ols")
    parser.add_argument("--y", required=True)
    parser.add_argument("--x", nargs="+", required=True)
    parser.add_argument("--categorical", nargs="*", default=[])
    parser.add_argument("--outdir", default="outputs/regression")
    args = parser.parse_args()

    df = load_table(Path(args.file), args.sheet).copy()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    formula = build_formula(args.y, args.x, args.categorical)
    if args.model == "ols":
        result = smf.ols(formula, data=df).fit()
    else:
        result = smf.logit(formula, data=df).fit(disp=False)

    with open(outdir / f"{args.model}_summary.txt", "w", encoding="utf-8") as handle:
        handle.write(result.summary().as_text())

    ci = result.conf_int()
    coef = pd.DataFrame(
        {
            "coef": result.params,
            "std_err": result.bse,
            "p_value": result.pvalues,
            "ci_low": ci[0],
            "ci_high": ci[1],
        }
    )
    coef.to_csv(outdir / f"{args.model}_coefficients.csv", encoding="utf-8-sig")
    print(f"Saved outputs to {outdir.resolve()}")


if __name__ == "__main__":
    main()
