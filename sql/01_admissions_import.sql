-- SQLite import script for admissions.csv
DROP TABLE IF EXISTS "admissions";
CREATE TABLE "admissions" (
  "subject_id" TEXT,
  "hadm_id" TEXT,
  "admittime" TEXT,
  "dischtime" TEXT,
  "deathtime" TEXT,
  "admission_type" TEXT,
  "admit_provider_id" TEXT,
  "admission_location" TEXT,
  "discharge_location" TEXT,
  "insurance" TEXT,
  "language" TEXT,
  "marital_status" TEXT,
  "race" TEXT,
  "edregtime" TEXT,
  "edouttime" TEXT,
  "hospital_expire_flag" TEXT
);

.mode csv
.import --skip 1 'data/mimic-iv-demo-subset/admissions.csv' "admissions"
