-- SQLite import script for microbiologyevents.csv
DROP TABLE IF EXISTS "microbiologyevents";
CREATE TABLE "microbiologyevents" (
  "microevent_id" TEXT,
  "subject_id" TEXT,
  "hadm_id" TEXT,
  "micro_specimen_id" TEXT,
  "order_provider_id" TEXT,
  "chartdate" TEXT,
  "charttime" TEXT,
  "spec_itemid" TEXT,
  "spec_type_desc" TEXT,
  "test_seq" TEXT,
  "storedate" TEXT,
  "storetime" TEXT,
  "test_itemid" TEXT,
  "test_name" TEXT,
  "org_itemid" TEXT,
  "org_name" TEXT,
  "isolate_num" TEXT,
  "quantity" TEXT,
  "ab_itemid" TEXT,
  "ab_name" TEXT,
  "dilution_text" TEXT,
  "dilution_comparison" TEXT,
  "dilution_value" TEXT,
  "interpretation" TEXT,
  "comments" TEXT
);

.mode csv
.import --skip 1 'data/mimic-iv-demo-subset/microbiologyevents.csv' "microbiologyevents"
