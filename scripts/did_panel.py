#!/usr/bin/env python3
"""Difference-in-differences template."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


def load_table(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treat", required=True)
    parser.add_argument("--post", required=True)
    parser.add_argument("--unit")
    parser.add_argument("--time")
    parser.add_argument("--controls", nargs="*", default=[])
    parser.add_argument("--outdir", default="outputs/did")
    args = parser.parse_args()

    df = load_table(Path(args.file), args.sheet).copy()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    terms = [args.treat, args.post, f"{args.treat}:{args.post}", *args.controls]
    if args.time:
        terms.append(f"C({args.time})")
    formula = f"{args.outcome} ~ " + " + ".join(terms)

    if args.unit:
        result = smf.ols(formula, data=df).fit(
            cov_type="cluster",
            cov_kwds={"groups": df[args.unit]},
        )
    else:
        result = smf.ols(formula, data=df).fit()

    with open(outdir / "did_summary.txt", "w", encoding="utf-8") as handle:
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
    coef.to_csv(outdir / "did_coefficients.csv", encoding="utf-8-sig")
    print(f"Saved outputs to {outdir.resolve()}")


if __name__ == "__main__":
    main()
