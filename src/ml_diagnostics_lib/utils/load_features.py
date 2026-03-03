# src/model_micro_los.py
from pathlib import Path
import numpy as np
import pandas as pd
import argparse
from typing import Optional

def default_features_path(repo_root: Optional[Path] = None) -> Path:
    repo_root = repo_root or Path(__file__).resolve().parents[3]
    return repo_root / "data" / "processed" / "feat_admission_micro_los.csv"

def load_features(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    df = df[df["length_of_stay_days"].notna()].copy()
    df = df[df["length_of_stay_days"] >= 0].copy()

    # Transform LOS to log scale to reduce skewness and handle outliers
    df["log_los"] = np.log1p(df["length_of_stay_days"])

    return df

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Load and clean feature table for modeling.")
    p.add_argument("--csv", type=Path, default=None, help="Path to features CSV. Defaults to data/processed/feat_admission_micro_los.csv")
    return p.parse_args()


def main():
    args = parse_args()
    features_path = args.csv or default_features_path()

    df = load_features(features_path)
    print("Loaded: ", df.shape)
    print(df[["length_of_stay_days", "log_los"]].describe(percentiles=[0.90, 0.95, 0.99, 0.999]))

if __name__ == "__main__":
    main()