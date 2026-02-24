-- SQLite import script for labevents.csv
DROP TABLE IF EXISTS "labevents";
CREATE TABLE "labevents" (
  "labevent_id" TEXT,
  "subject_id" TEXT,
  "hadm_id" TEXT,
  "specimen_id" TEXT,
  "itemid" TEXT,
  "order_provider_id" TEXT,
  "charttime" TEXT,
  "storetime" TEXT,
  "value" TEXT,
  "valuenum" TEXT,
  "valueuom" TEXT,
  "ref_range_lower" TEXT,
  "ref_range_upper" TEXT,
  "flag" TEXT,
  "priority" TEXT,
  "comments" TEXT
);

.mode csv
.import --skip 1 'data/mimic-iv-demo-subset/labevents.csv' "labevents"
