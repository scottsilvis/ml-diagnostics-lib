-- 03_sanity_checks.sql

-- Final table row integrity
SELECT
  COUNT(*) AS feat_rows,
  COUNT(DISTINCT hadm_id) AS distinct_hadm_id,
  COUNT(*) - COUNT(DISTINCT hadm_id) AS duplicate_rows
FROM feat_admission_micro_los;

-- Prevalence and event counts
SELECT
  AVG(has_ecoli) AS prev_ecoli,
  AVG(has_staph_aureus) AS prev_staph,
  AVG(has_flu) AS prev_flu,
  AVG(CASE WHEN n_micro_events > 0 THEN 1.0 ELSE 0.0 END) AS prev_any_micro,
  AVG(n_micro_events) AS mean_micro_events,
  SUM(n_micro_events) AS total_micro_events
FROM feat_admission_micro_los;

-- LOS distribution
SELECT
  MIN(length_of_stay_days) AS min_los,
  AVG(length_of_stay_days) AS mean_los,
  MAX(length_of_stay_days) AS max_los
FROM feat_admission_micro_los;

-- Top admissions by micro event count
SELECT
  hadm_id,
  subject_id,
  n_micro_events,
  has_ecoli,
  has_staph_aureus,
  has_flu
FROM feat_admission_micro_los
ORDER BY n_micro_events DESC
LIMIT 20;