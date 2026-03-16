-- 02_features.sql
-- Build modeling-ready feature table
-- EDA-faithful version: one row per hadm_id

DROP TABLE IF EXISTS feat_admission_micro_los;

CREATE TABLE feat_admission_micro_los AS
WITH

adm_base AS (
  SELECT
    a.hadm_id,
    a.subject_id,
    a.race,
    p.sex,
    p.anchor_age AS age,
    a.admitday,
    a.dischday,
    a.length_of_stay_days
  FROM stg_admissions a
  LEFT JOIN stg_patients p
    ON p.subject_id = a.subject_id
),

-- Match raw micro events to admissions exactly like the EDA concept:
-- same patient, event date falls during admission
matched_micro AS (
  SELECT
    a.hadm_id,
    a.subject_id,
    m.event_day,
    m.org_name_l
  FROM adm_base a
  JOIN stg_micro_events m
    ON m.subject_id = a.subject_id
   AND m.event_day BETWEEN a.admitday AND a.dischday
),

micro_agg AS (
  SELECT
    hadm_id,
    COUNT(*) AS n_micro_events,

    MAX(
      CASE
        WHEN org_name_l LIKE '%escherichia coli%'
          OR org_name_l LIKE '%e. coli%'
        THEN 1 ELSE 0
      END
    ) AS has_ecoli,

    MAX(
      CASE
        WHEN org_name_l LIKE '%staphylococcus aureus%'
          OR org_name_l LIKE '%s. aureus%'
          OR org_name_l LIKE '%staph aureus%'
          OR org_name_l LIKE '%staph aureus coag%'
        THEN 1 ELSE 0
      END
    ) AS has_staph_aureus,

    MAX(
      CASE
        WHEN org_name_l LIKE '%influenza%'
          OR org_name_l LIKE '%flu%'
        THEN 1 ELSE 0
      END
    ) AS has_flu

  FROM matched_micro
  GROUP BY hadm_id
)

SELECT
  a.hadm_id,
  a.subject_id,
  a.race,
  a.sex,
  a.age,
  COALESCE(m.n_micro_events, 0) AS n_micro_events,
  COALESCE(m.has_ecoli, 0) AS has_ecoli,
  COALESCE(m.has_staph_aureus, 0) AS has_staph_aureus,
  COALESCE(m.has_flu, 0) AS has_flu,
  a.length_of_stay_days
FROM adm_base a
LEFT JOIN micro_agg m
  ON m.hadm_id = a.hadm_id
;