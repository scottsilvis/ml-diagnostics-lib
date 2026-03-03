# ml-diagnostics-lib

A small Python library for fitting baseline classification models and evaluating them using diagnostic-focused metrics rather than leaderboard optimization.

The primary use case is understanding when a simple model is sufficient and when increased model flexibility is structurally justified, using tools such as calibration analysis, residual inspection, and ranking stability.

This repository is intentionally minimal and model-agnostic. It is designed for iterative experimentation and extension rather than end-to-end production pipelines.

---

## Scope and Design Philosophy

- Emphasizes model diagnostics over metric maximization
- Treats logistic regression as a reference model
- Uses more flexible models (random forest, gradient boosting) as comparators, not defaults
- Assumes fixed feature sets and no feature leakage
- Prioritizes out-of-fold predictions for evaluation

This library is not intended for:
- Automated model selection
- Hyperparameter tuning competitions
- Deep learning workflows
- Domain-specific inference or causal claims

---

## Repository Structure

```text
ml-diagnostics-lib/
  data.py                 
  splits.py               
  metrics.py              
  diagnostics/
    calibration.py        
    residuals.py          
    ranking.py            
  models/
    logistic.py           
    random_forest.py      
    gradient_boost.py     
  run_compare.py          
```

---

## Core Concepts

### Reference Model

Logistic regression is treated as the baseline against which all structural comparisons are made.

### Diagnostic Signals

Model evaluation focuses on:
- Calibration behavior
- Residual structure
- Ranking stability across resamples
- Diminishing returns with increased complexity

Performance metrics (e.g., PR-AUC) are used descriptively, not prescriptively.

---

## Typical Usage Pattern

1. Load baseline dataset
2. Generate out-of-fold predictions for each model
3. Apply shared diagnostic functions
4. Compare structural behavior across models

---

## Outputs

Model runners return:
- Out-of-fold predicted probabilities
- Fold identifiers
- Fold-level metric summaries
- Optional model artifacts

Diagnostic functions return plot-ready data structures and summary statistics.

---

What This Library Supports
- Defensible conclusions such as:
- When linear decision boundaries are insufficient
- Whether nonlinear models reduce systematic residual patterns
- How calibration and ranking trade off across model classes
- When performance gains plateau with added complexity

What This Library Does Not Claim
- Clinical validity
- Causal interpretation
- Optimal model selection
- Production readiness

## Status

This library is under active iteration and currently scoped to a single dataset. Interfaces are expected to evolve as diagnostics are refined.
