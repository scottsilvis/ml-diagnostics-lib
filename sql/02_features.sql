-- 02_features.sql
-- Build modeling-ready feature table (1 row per hadm_id)

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

micro_agg AS (
  SELECT
    b.hadm_id,
    COUNT(*) AS n_micro_events,

    MAX(CASE
      WHEN m.org_name_l LIKE '%escherichia coli%' OR m.org_name_l LIKE '%e. coli%'
      THEN 1 ELSE 0 END) AS has_ecoli,

    MAX(CASE
      WHEN m.org_name_l LIKE '%staphylococcus aureus%' OR m.org_name_l LIKE '%s. aureus%'
      THEN 1 ELSE 0 END) AS has_staph_aureus,

    MAX(CASE
      WHEN m.org_name_l LIKE '%influenza%' OR m.org_name_l LIKE '%flu%'
      THEN 1 ELSE 0 END) AS has_flu

  FROM adm_base b
  JOIN stg_micro_events m
    ON m.hadm_id = b.hadm_id
   AND m.event_day BETWEEN b.admitday AND b.dischday
   AND m.org_name_l IS NOT NULL
  GROUP BY b.hadm_id
)

SELECT
  b.hadm_id,
  b.subject_id,

  b.race,
  b.sex,
  b.age,

  COALESCE(m.n_micro_events, 0) AS n_micro_events,
  COALESCE(m.has_ecoli, 0) AS has_ecoli,
  COALESCE(m.has_staph_aureus, 0) AS has_staph_aureus,
  COALESCE(m.has_flu, 0) AS has_flu,

  b.length_of_stay_days

FROM adm_base b
JOIN micro_agg m
  ON m.hadm_id = b.hadm_id;


CREATE INDEX IF NOT EXISTS idx_feat_hadm    ON feat_admission_micro_los(hadm_id);
CREATE INDEX IF NOT EXISTS idx_feat_subject ON feat_admission_micro_los(subject_id);