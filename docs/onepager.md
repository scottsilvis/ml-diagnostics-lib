Table of Contents

## Overview

The goal of this document will eventually be to create a respository for ml models. Because I find it boring to do these things without some data driving things forward, I have decided to use the open-access MIMIC-IV database. This library is already a subset of the full credentialed MIMIC-IV database, but I have further subset specific files that I am interested in investigating. I may add or remove some as time progresses, but for the time being I am including these files in the data folder:

```
.
├── data/
│   └── mimic-iv-demo-subset
│       ├── admissions.csv
│       ├── diagnoses_icd.csv
│       ├── icustays.csv
│       ├── labevents.csv
│       ├── microbiologyevents.csv
│       ├── procedures_icd.csv
│       ├── README.txt
│       ├── SHA252SUMS.txt
│       └── LICENSE.txt
```

The README.txt, SHA252SUMS.txt, and LICENSE.txt files are provided by the creators of the dataset. 

