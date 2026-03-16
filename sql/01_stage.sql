-- 01_stage.sql
-- SQLite Staging script for MIMIC-IV data
-- This script creates staging tables with cleaned and standardized columns for easier analysis.


-- ===============================
-- Staging table for admissions
-- ===============================

DROP TABLE IF EXISTS stg_admissions;
CREATE TABLE stg_admissions AS
SELECT
  CAST(NULLIF(subject_id, '') AS INTEGER) AS subject_id,
  CAST(NULLIF(hadm_id, '') AS INTEGER)    AS hadm_id,
  NULLIF(admittime, '') AS admittime,
  NULLIF(dischtime, '') AS dischtime,

  CAST(julianday(date(NULLIF(admittime, ''))) AS INTEGER) AS admitday,
  CAST(julianday(date(NULLIF(dischtime, ''))) AS INTEGER) AS dischday,
  
  NULLIF(race, '') AS race,

  (CAST(strftime('%s', NULLIF(dischtime, '')) AS REAL) - CAST(strftime('%s', NULLIF(admittime, '')) AS REAL)) / 86400.0
    AS length_of_stay_days
FROM raw_admissions
WHERE NULLIF(hadm_id, '') IS NOT NULL
  AND NULLIF(admittime, '') IS NOT NULL
  AND NULLIF(dischtime, '') IS NOT NULL
  AND date(NULLIF(admittime, '')) IS NOT NULL
  AND date(NULLIF(dischtime, '')) IS NOT NULL
  AND (CAST(strftime('%s', NULLIF(dischtime, '')) AS REAL) - CAST(strftime('%s', NULLIF(admittime, '')) AS REAL)) >= 0
  AND CAST(julianday(date(NULLIF(dischtime, ''))) AS INTEGER) >= CAST(julianday(date(NULLIF(admittime, ''))) AS INTEGER);

-- ===============================
-- Staging tables for patients
-- ===============================

DROP TABLE IF EXISTS stg_patients;
CREATE TABLE stg_patients AS
SELECT
  CAST(NULLIF(subject_id, '') AS INTEGER) AS subject_id,
  CASE 
    WHEN NULLIF(gender, '') = 'M' THEN 1 
    WHEN NULLIF(gender, '') = 'F' THEN 0 
    ELSE NULL 
  END AS sex,
  CAST(NULLIF(anchor_age, '') AS INTEGER) AS anchor_age
FROM raw_patients
WHERE NULLIF(subject_id, '') IS NOT NULL;

-- ===============================
-- Staging tables for micro events
-- ===============================

DROP TABLE IF EXISTS stg_micro_events;
CREATE TABLE stg_micro_events AS
SELECT
  CAST(NULLIF(subject_id, '') AS INTEGER) AS subject_id,
  CAST(julianday(date(NULLIF(chartdate, ''))) AS INTEGER) AS event_day,
  LOWER(TRIM(org_name)) AS org_name_l
FROM raw_micro_events
WHERE subject_id IS NOT NULL
  AND chartdate IS NOT NULL
  AND org_name IS NOT NULL
  AND TRIM(org_name) <> ''
  AND LOWER(TRIM(org_name)) <> 'cancelled';

-- ===============================
-- Staging tables for omr
-- ===============================

DROP TABLE IF EXISTS stg_omr;
CREATE TABLE stg_omr AS
SELECT
  CAST(NULLIF(subject_id, '') AS INTEGER) AS subject_id,
  CAST(julianday(date(NULLIF(chartdate, ''))) AS INTEGER) AS obs_date,
  LOWER(TRIM(result_name)) AS result_name_l,
  -- value_num will be filled in Python for robustness; keep as nullable REAL here
  NULL AS value_num,
  TRIM(result_value) AS value_raw
FROM raw_omr
WHERE NULLIF(subject_id, '') IS NOT NULL
  AND NULLIF(chartdate, '') IS NOT NULL
  AND NULLIF(result_name, '') IS NOT NULL;



