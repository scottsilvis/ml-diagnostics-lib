# src/model_micro_los.py
from pathlib import Path
from sklearn.model_selection import GroupKFold
import numpy as np
import pandas as pd
import statsmodels.api as sm
from ml_diagnostics_lib.utils.load_features import load_features, default_features_path
from ml_diagnostics_lib.models.linear import OLSConfig, fit_ols, coef_percent_change

def run_ols(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    X = df[["age", "sex", "has_ecoli", "has_staph_aureus", "has_flu"]]
    X = sm.add_constant(X)
    y = df["log_los"]

    model = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": df["subject_id"]})
    print(model.summary())

    return model

def main():
    

    df = load_features(features_path)

    print("Loaded: ", df.shape)
    print(df[["length_of_stay_days", "log_los"]].describe(percentiles=[0.90, 0.95, 0.99, 0.999]))

    model = run_ols(df)

if __name__ == "__main__":
    main()