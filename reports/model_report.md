# Voya MASS Manager Selection & 15(c) Governance — Empirical Model Report

## Model Performance Comparison

| Model Tier                               |   ROC-AUC |   Precision (Overall) | Top-10 Manager Hit Rate   |
|:-----------------------------------------|----------:|----------------------:|:--------------------------|
| Baseline (L2 Logistic + Ridge)           |     0.714 |                 0.7   | 70.0%                     |
| Intermediate (Random Forest)             |     0.709 |                 0.6   | 70.0%                     |
| Advanced (Gradient Boosted Alpha Ranker) |     0.721 |                 0.667 | 70.0%                     |

## Top 8 Predictive Manager Features

| feature                    |   importance |
|:---------------------------|-------------:|
| capture_asymmetry_ratio    |       0.1253 |
| style_drift_index          |       0.1143 |
| hist_3yr_gross_alpha_bps   |       0.1061 |
| upside_capture_pct         |       0.1014 |
| expense_ratio_bps          |       0.0787 |
| conviction_stability_score |       0.0717 |
| r_squared_factor           |       0.0689 |
| downside_capture_pct       |       0.0657 |
