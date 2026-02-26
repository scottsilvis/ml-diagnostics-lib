from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


# ---------- Config ----------

@dataclass
class BuildConfig:
    db_path: Path
    admissions_csv: Path
    patients_csv: Path
    micro_csv: Path
    omr_csv: Path

    sql_stage_path: Path   # 01_stage.sql
    sql_features_path: Path  # 02_features.sql

    export_csv_path: Optional[Path] = None
    export_parquet_path: Optional[Path] = None

    chunksize: int = 200_000  # tune up/down depending on RAM


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    # Speed-friendly pragmas for bulk load + local analytics
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA synchronous=NORMAL;")
    con.execute("PRAGMA temp_store=MEMORY;")
    con.execute("PRAGMA cache_size=-200000;")
    return con


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def create_raw_table_all_text(con: sqlite3.Connection, table: str, columns: list[str]) -> None:
    con.execute(f'DROP TABLE IF EXISTS "{table}";')
    cols_sql = ", ".join([f'"{c}" TEXT' for c in columns])
    con.execute(f'CREATE TABLE "{table}" ({cols_sql});')


def chunked_read_csv(csv_path: Path, chunksize: int) -> Iterable[pd.DataFrame]:
    return pd.read_csv(
        csv_path,
        dtype=str,
        chunksize=chunksize,
        low_memory=False,
        keep_default_na=False,
    )


def load_csv_to_raw(con: sqlite3.Connection, csv_path: Path, table: str, chunksize: int) -> None:
    print(f"Loading {csv_path.name} -> {table}")
    first_chunk = True
    for chunk in chunked_read_csv(csv_path, chunksize):
        if first_chunk:
            create_raw_table_all_text(con, table, list(chunk.columns))
            first_chunk = False

        # append chunk
        chunk.to_sql(table, con, if_exists="append", index=False)
        con.commit()


def run_sql_file(con: sqlite3.Connection, sql_path: Path) -> None:
    print(f"Running SQL: {sql_path.name}")
    con.executescript(read_sql(sql_path))
    con.commit()


def sanity_checks(con: sqlite3.Connection) -> None:
    print("\nSanity checks:")
    n_rows, n_hadm = con.execute(
        "SELECT COUNT(*), COUNT(DISTINCT hadm_id) FROM feat_admission_micro_los;"
    ).fetchone()
    print(f"- feat rows: {n_rows:,} | distinct hadm_id: {n_hadm:,} | dupes: {n_rows - n_hadm:,}")

    prev = con.execute("""
        SELECT
          AVG(has_ecoli),
          AVG(has_staph_aureus),
          AVG(has_flu),
          AVG(CASE WHEN n_micro_events > 0 THEN 1.0 ELSE 0.0 END),
          AVG(n_micro_events)
        FROM feat_admission_micro_los;
    """).fetchone()
    print(f"- prev_ecoli={prev[0]:.4f} prev_staph={prev[1]:.4f} prev_flu={prev[2]:.4f} "
          f"prev_any_micro={prev[3]:.4f} mean_micro_events={prev[4]:.2f}")

    los = con.execute("""
        SELECT MIN(length_of_stay_days), AVG(length_of_stay_days), MAX(length_of_stay_days)
        FROM feat_admission_micro_los;
    """).fetchone()
    print(f"- LOS days: min={los[0]:.2f} mean={los[1]:.2f} max={los[2]:.2f}")


def export_features(con: sqlite3.Connection, csv_path: Optional[Path], parquet_path: Optional[Path]) -> None:
    if csv_path is None and parquet_path is None:
        return

    df = pd.read_sql_query("SELECT * FROM feat_admission_micro_los;", con)

    if csv_path is not None:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False)
        print(f"Exported CSV: {csv_path}")

    if parquet_path is not None:
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(parquet_path, index=False)
        print(f"Exported Parquet: {parquet_path}")


def build(cfg: BuildConfig) -> None:
    con = connect(cfg.db_path)
    try:
        # 1) Load raw tables
        load_csv_to_raw(con, cfg.admissions_csv, "raw_admissions", cfg.chunksize)
        load_csv_to_raw(con, cfg.patients_csv, "raw_patients", cfg.chunksize)
        load_csv_to_raw(con, cfg.micro_csv, "raw_micro_events", cfg.chunksize)
        load_csv_to_raw(con, cfg.omr_csv, "raw_omr", cfg.chunksize)

        # 2) Run staging + features SQL
        run_sql_file(con, cfg.sql_stage_path)
        run_sql_file(con, cfg.sql_features_path)

        # 3) Sanity
        sanity_checks(con)

        # 4) Export
        export_features(con, cfg.export_csv_path, cfg.export_parquet_path)

        print("\nBuild complete.")
    finally:
        con.close()


if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[1]

    cfg = BuildConfig(
        db_path=repo / "data" / "mimic.sqlite",
        admissions_csv=repo / "data" / "mimic-iv" / "admissions.csv",
        patients_csv=repo / "data" / "mimic-iv" / "patients.csv",
        micro_csv=repo / "data" / "mimic-iv" / "microbiologyevents.csv",
        omr_csv=repo / "data" / "mimic-iv" / "omr.csv",

        sql_stage_path=repo / "sql" / "01_stage.sql",
        sql_features_path=repo / "sql" / "02_features.sql",

        export_csv_path=repo / "data" / "processed" / "feat_admission_micro_los.csv",
        chunksize=200_000,
    )

    build(cfg)