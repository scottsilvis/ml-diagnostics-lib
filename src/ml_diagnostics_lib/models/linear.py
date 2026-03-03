# src/models/linear.py
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_squared_error, r2_score
from ml_diagnostics_lib.utils.load_features import load_features, default_features_path

FEATURES_DEFAULT = ["age", "sex", "has_ecoli", "has_staph_aureus", "has_flu"]
TARGET_DEFAULT = "log_los" 
GROUP_COL = "subject_id"

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Model LOS associations using OLS on log(LOS+1).")
    p.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="Path to features CSV. Defaults to data/processed/feat_admission_micro_los.csv",
    )
    p.add_argument(
        "--cv-folds",
        type=int,
        default=0,
        help="If >0, run GroupKFold CV and report R2/RMSE on log_los.",
    )
    return p.parse_args()


def fit_clustered_ols(
    df: pd.DataFrame,
    features: List[str] = FEATURES_DEFAULT,
    target: str = TARGET_DEFAULT,
    group_col: str = GROUP_COL,
) -> sm.regression.linear_model.RegressionResultsWrapper:
    # Keep only needed cols and drop missing
    cols = features + [target, group_col]
    d = df[cols].dropna().copy()

    X = d[features]
    X = sm.add_constant(X, has_constant="add")
    y = d[target]

    # Clustered SEs by subject_id (accounts for repeated admissions)
    groups = d[group_col]
    res = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})

    return res


def run_groupkfold_cv(
    df: pd.DataFrame,
    n_splits: int,
    features: List[str] = FEATURES_DEFAULT,
    target: str = TARGET_DEFAULT,
    group_col: str = GROUP_COL,
) -> None:
    cols = features + [target, group_col]
    d = df[cols].dropna().copy()

    X_all = d[features]
    y_all = d[target]
    groups = d[group_col]

    gkf = GroupKFold(n_splits=n_splits)

    r2s = []
    rmses = []

    for fold, (tr, te) in enumerate(gkf.split(X_all, y_all, groups=groups), start=1):
        X_tr = sm.add_constant(X_all.iloc[tr], has_constant="add")
        y_tr = y_all.iloc[tr]

        X_te = sm.add_constant(X_all.iloc[te], has_constant="add")
        y_te = y_all.iloc[te]

        # Plain OLS fit for prediction; clustered SEs aren't needed for CV scoring
        res = sm.OLS(y_tr, X_tr).fit()

        preds = res.predict(X_te)
        r2s.append(r2_score(y_te, preds))
        rmses.append(mean_squared_error(y_te, preds, squared=False))

        print(f"Fold {fold}: R2={r2s[-1]:.4f}  RMSE(log_los)={rmses[-1]:.4f}")

    print("\nGroupKFold CV summary")
    print(f"R2 mean={np.mean(r2s):.4f}  std={np.std(r2s):.4f}")
    print(f"RMSE mean={np.mean(rmses):.4f}  std={np.std(rmses):.4f}")


def main() -> None:
    args = parse_args()
    csv_path = args.csv if args.csv is not None else default_features_path()

    df = load_features(csv_path)

    res = fit_clustered_ols(df)
    print(res.summary())

    if args.cv_folds and args.cv_folds > 1:
        run_groupkfold_cv(df, n_splits=args.cv_folds)


if __name__ == "__main__":
    main()