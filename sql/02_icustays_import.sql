-- SQLite import script for icustays.csv
DROP TABLE IF EXISTS "icustays";
CREATE TABLE "icustays" (
  "subject_id" TEXT,
  "hadm_id" TEXT,
  "stay_id" TEXT,
  "first_careunit" TEXT,
  "last_careunit" TEXT,
  "intime" TEXT,
  "outtime" TEXT,
  "los" TEXT
);

.mode csv
.import --skip 1 'data/mimic-iv-demo-subset/icustays.csv' "icustays"
