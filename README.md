# ml-diagnostics-lib

A personal modeling library for learning and implementing statistical and machine-learning techniques using realistic clinical datasets derived from MIMIC-IV.

The goal of this project is to build a reusable toolkit of modeling workflows, diagnostics, and evaluation strategies while solving artificial but realistic prediction problems.

Rather than focusing on a single research question, this repository serves as a catalog of modeling patterns, each implemented end-to-end with:

- SQL feature engineering
- reproducible data pipelines
- interpretable baseline models
- evaluation and diagnostics
- reusable Python modules

---

## Project Goals

This project is designed to practice and preserve reusable modeling techniques.

Each case study demonstrates how to:

- Construct features from relational healthcare datasets
- Train interpretable statistical models
- Evaluate models using appropriate metrics
- Perform model diagnostics
- Build reproducible data science pipelines
- Package reusable modeling utilities into a Python library

The long-term goal is to maintain a library of modeling patterns that can be reused across future projects.

---

## Data Source

This project uses data derived from the MIMIC-IV clinical database.

MIMIC-IV is a large, publicly available database containing de-identified health-related data associated with patients admitted to intensive care units.

Because of licensing restrictions:

- The MIMIC-IV data is not included in this repository.
- Only schema definitions are stored here.

Users who have access to MIMIC-IV can recreate the dataset using the SQL and pipeline scripts provided.

---

## Repository Structure

```text
ml-diagnostics-lib
│
├── data
│   ├── mimic-iv
│   │   ├── admissions.csv
│   │   ├── microbiologyevents.csv
│   │   ├── patients.csv
│   │   └── ...
│   │
│   ├── processed
│   │   └── feat_admission_micro_los.csv
│   │
│   └── mimic.sqlite
│
├── docs
│   ├── decisions.md
│   ├── methodology.md
│   └── onepager.md
│
├── notebooks
│   └── 01_microbiology_exploration.ipynb
│
├── scripts
│   ├── build_sqlite_db.py
│   └── model_micro_los.py
│
├── sql
│   ├── 01_stage.sql
│   ├── 02_features.sql
│   └── 03_sanity_checks.sql
│
├── src/ml_diagnostics_lib
│   ├── datasets
│   ├── features
│   ├── metrics
│   ├── models
│   │   ├── linear.py
│   │   └── model.py
│   │
│   ├── training
│   └── utils
│
└── tests       
```

---

## Workflow

Each modeling exercise follows a reproducible pipeline.

### 1. Build the SQLite database

Raw MIMIC files are converted into a local SQLite database.

```
python scripts/build_sqlite_db.py
```

### 2. Construct feature tables

Feature engineering is performed using SQL.

The pipeline includes:

1. Stage tables
2. Feature construction
3. Sanity checks


```
sql/
 ├── 01_stage.sql
 ├── 02_features.sql
 └── 03_sanity_checks.sql
```

These scripts produce analysis-ready feature tables.

### 3. Run a model

Model training scripts are located in scripts/.

Example:

```
python scripts/model_micro_los.py
```

This script loads the engineered feature table and trains baseline models.

---

## Example Case Study

Predicting Length of Stay from Microbiology Signals

This experiment explores whether simple microbiology indicators recorded during a hospital stay can help explain variation in length of stay (LOS).

Features include indicators such as:

- presence of E. coli
- presence of Staphylococcus aureus
- presence of influenza
- admission characteristics
- baseline demographic information

The target variable is:

```
log(length_of_stay_days)
```

The model uses:
- linear regression
- grouped cross-validation
- residual diagnostics

This experiment serves as a practice example for:

- feature construction from relational clinical data
- interpretable regression modeling
- model diagnostics

---

## Library Components

The reusable Python package lives in:

```
src/ml_diagnostics_lib
```

### datasets

Dataset loaders and helpers for reading feature tables.

### features

Utilities related to feature construction and metadata.

### models

Reusable model implementations, including:

- linear regression
- logistic regression
- baseline statistical models

### metrics

Evaluation utilities and model scoring functions.

### training

Model training pipelines and cross-validation helpers.

### utils

General utilities such as feature loading.

---

## Planned Modeling Exercises

Future case studies will explore additional modeling techniques, including:
- logistic regression for binary clinical outcomes
- calibration and probability diagnostics
- regularized models (ridge, lasso, elastic net)
- sparse text modeling using TF-IDF
- combined structured + text models
- model comparison and selection strategies

Each case study will focus on learning and documenting a modeling technique rather than solving a single clinical research question.

## Reproducibility

The project is designed to be reproducible locally.

Dependencies are listed in:

```
requirements.txt
```

Install them with:

```
pip install -r requirements.txt
```
## Why This Project Exists

Many machine learning examples online focus on high-level modeling libraries without showing the full workflow.

This project intentionally emphasizes:

- realistic relational data
- SQL feature engineering
- interpretable baseline models
- diagnostic analysis
- reproducible pipelines

The goal is to build intuition about how statistical modeling behaves in real datasets.

## License

This repository contains no protected clinical data.

Users must obtain their own access to MIMIC-IV to recreate the dataset.
