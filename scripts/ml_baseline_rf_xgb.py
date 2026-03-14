#!/usr/bin/env python3
"""ML baseline template with optional XGBoost."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score, roc_auc_score
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_table(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    return pd.read_csv(path)


def build_preprocessor(frame: pd.DataFrame, features: list[str]) -> ColumnTransformer:
    numeric = [col for col in features if pd.api.types.is_numeric_dtype(frame[col])]
    categorical = [col for col in features if col not in numeric]
    return ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--task", choices=["classification", "regression"], required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--features", nargs="+", required=True)
    parser.add_argument("--use-xgb", action="store_true")
    parser.add_argument("--outdir", default="outputs/ml")
    args = parser.parse_args()

    df = load_table(Path(args.file), args.sheet).copy()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    X = df[args.features]
    y = df[args.target]
    preprocessor = build_preprocessor(df, args.features)

    if args.task == "classification":
        models = {
            "logistic": LogisticRegression(max_iter=2000),
            "random_forest": RandomForestClassifier(n_estimators=300, random_state=42),
        }
        scoring = {"accuracy": "accuracy", "f1": "f1_weighted", "roc_auc": "roc_auc_ovr"}
    else:
        models = {
            "linear": LinearRegression(),
            "random_forest": RandomForestRegressor(n_estimators=300, random_state=42),
        }
        scoring = {"r2": "r2", "mae": "neg_mean_absolute_error"}

    if args.use_xgb:
        try:
            if args.task == "classification":
                from xgboost import XGBClassifier

                models["xgboost"] = XGBClassifier(
                    n_estimators=300,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    eval_metric="logloss",
                    random_state=42,
                )
            else:
                from xgboost import XGBRegressor

                models["xgboost"] = XGBRegressor(
                    n_estimators=300,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=42,
                )
        except ImportError:
            print("xgboost is not installed; skipping XGBoost.")

    rows = []
    for name, estimator in models.items():
        pipeline = Pipeline([("prep", preprocessor), ("model", estimator)])
        cv = cross_validate(pipeline, X, y, cv=5, scoring=scoring)
        row = {"model": name}
        for key, values in cv.items():
            if key.startswith("test_"):
                metric = key.removeprefix("test_")
                score = values.mean()
                if metric == "mae":
                    score = -score
                row[metric] = score
        rows.append(row)

    result_frame = pd.DataFrame(rows)
    result_frame.to_csv(outdir / "model_comparison.csv", index=False, encoding="utf-8-sig")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if args.task == "classification" else None,
    )
    best_name = result_frame.iloc[0]["model"]
    best_estimator = models[best_name]
    best_pipeline = Pipeline([("prep", preprocessor), ("model", best_estimator)])
    best_pipeline.fit(X_train, y_train)
    pred = best_pipeline.predict(X_test)

    if args.task == "classification":
        metrics = {
            "accuracy": accuracy_score(y_test, pred),
            "f1_weighted": f1_score(y_test, pred, average="weighted"),
        }
        if hasattr(best_pipeline.named_steps["model"], "predict_proba") and y.nunique() == 2:
            prob = best_pipeline.predict_proba(X_test)[:, 1]
            metrics["roc_auc"] = roc_auc_score(y_test, prob)
    else:
        metrics = {
            "r2": r2_score(y_test, pred),
            "mae": mean_absolute_error(y_test, pred),
        }

    pd.DataFrame({"metric": list(metrics.keys()), "value": list(metrics.values())}).to_csv(
        outdir / "holdout_metrics.csv",
        index=False,
        encoding="utf-8-sig",
    )
    print(f"Saved outputs to {outdir.resolve()}")


if __name__ == "__main__":
    main()
