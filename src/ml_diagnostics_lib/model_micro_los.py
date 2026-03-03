# src/model_micro_los.py
from __future__ import annotations

import argparse
from pathlib import Path

from ml_diagnostics_lib.utils.load_features import load_features, default_features_path
from ml_diagnostics_lib.models.linear import fit_clustered_ols, run_groupkfold_cv, FEATURES_DEFAULT


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Microbiology LOS modeling runner.")
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
        help="If >1, run GroupKFold CV and report R2/RMSE on log_los.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    features_path = args.csv if args.csv is not None else default_features_path()

    df = load_features(features_path)

    print("Loaded:", df.shape)
    print(df[["length_of_stay_days", "log_los"]].describe(percentiles=[0.90, 0.95, 0.99, 0.999]))

    # 1) Clustered OLS (inference-style)
    res = fit_clustered_ols(df, features=FEATURES_DEFAULT, target="log_los", group_col="subject_id")
    print(res.summary())

    # 2) Grouped CV (prediction stability)
    if args.cv_folds and args.cv_folds > 1:
        run_groupkfold_cv(
            df,
            n_splits=args.cv_folds,
            features=FEATURES_DEFAULT,
            target="log_los",
            group_col="subject_id",
        )


if __name__ == "__main__":
    main()