-- 03_sanity_checks.sql

-- 1) One row per hadm_id
SELECT
  COUNT(*) AS n_rows,
  COUNT(DISTINCT hadm_id) AS n_distinct_hadm,
  COUNT(*) - COUNT(DISTINCT hadm_id) AS n_dupes
FROM feat_admission_micro_los;

-- 2) Micro prevalence
SELECT
  AVG(has_ecoli) AS prev_ecoli,
  AVG(has_staph_aureus) AS prev_staph_aureus,
  AVG(has_flu) AS prev_flu,
  AVG(CASE WHEN n_micro_events > 0 THEN 1.0 ELSE 0.0 END) AS prev_any_micro,
  AVG(n_micro_events) AS mean_micro_events
FROM feat_admission_micro_los;

-- 3) LOS distribution
SELECT
  MIN(length_of_stay_days) AS min_los,
  AVG(length_of_stay_days) AS mean_los,
  MAX(length_of_stay_days) AS max_los
FROM feat_admission_micro_los;

-- 4) Missingness check
SELECT
  AVG(CASE WHEN age IS NULL THEN 1.0 ELSE 0.0 END) AS missing_age,
  AVG(CASE WHEN sex IS NULL THEN 1.0 ELSE 0.0 END) AS missing_sex,
  AVG(CASE WHEN race IS NULL THEN 1.0 ELSE 0.0 END) AS missing_race
FROM feat_admission_micro_los;