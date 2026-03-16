from pathlib import Path
import sqlite3
import pandas as pd
import argparse

REPO = Path(__file__).resolve().parents[1]
DB_PATH = REPO / "data" / "mimic.sqlite"
SQL_DIR = REPO / "sql"

def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def run_sql_file(con: sqlite3.Connection, path: Path) -> None:
    print(f"Running {path.name}...")
    con.executescript(read_sql(path))
    con.commit()

def print_query(con: sqlite3.Connection, label: str, sql: str) -> None:
    print(f"\n--- {label} ---")
    df = pd.read_sql_query(sql, con)
    print(df.to_string(index=False))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", action="store_true")
    parser.add_argument("--features", action="store_true")
    parser.add_argument("--sanity", action="store_true")
    args = parser.parse_args()

    if not any([args.stage, args.features, args.sanity]):
        args.stage = args.features = args.sanity = True

    con = sqlite3.connect(DB_PATH)

    if args.stage:
        run_sql_file(con, SQL_DIR / "01_stage.sql")
    if args.features:
        run_sql_file(con, SQL_DIR / "02_features.sql")
    if args.sanity:
        run_sql_file(con, SQL_DIR / "03_sanity_checks.sql")

        print_query(
            con,
            "stg_micro_events count",
            "SELECT COUNT(*) AS stg_micro_rows FROM stg_micro_events"
        )

        print_query(
            con,
            "top staged organisms",
            """
            SELECT org_name_l, COUNT(*) AS n
            FROM stg_micro_events
            GROUP BY org_name_l
            ORDER BY n DESC
            LIMIT 20
            """
        )

        print_query(
            con,
            "feature table integrity",
            """
            SELECT
              COUNT(*) AS feat_rows,
              COUNT(DISTINCT hadm_id) AS distinct_hadm_id,
              COUNT(*) - COUNT(DISTINCT hadm_id) AS dupes
            FROM feat_admission_micro_los
            """
        )

        print_query(
            con,
            "feature prevalence",
            """
            SELECT
              AVG(has_ecoli) AS prev_ecoli,
              AVG(has_staph_aureus) AS prev_staph,
              AVG(has_flu) AS prev_flu,
              AVG(CASE WHEN n_micro_events > 0 THEN 1.0 ELSE 0.0 END) AS prev_any_micro,
              AVG(n_micro_events) AS mean_micro_events,
              SUM(n_micro_events) AS total_micro_events
            FROM feat_admission_micro_los
            """
        )

        print_query(
            con,
            "LOS summary",
            """
            SELECT
              MIN(length_of_stay_days) AS min_los,
              AVG(length_of_stay_days) AS mean_los,
              MAX(length_of_stay_days) AS max_los
            FROM feat_admission_micro_los
            """
        )

    con.close()
    print("\nDone.")

if __name__ == "__main__":
    main()