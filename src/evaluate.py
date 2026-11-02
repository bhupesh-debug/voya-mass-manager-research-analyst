"""
Voya MASS Manager Research & Selection (MR&S) — End-to-End Evaluation & 15(c) Oversight Runner
Executes synthetic universe ingestion, 6P feature engineering, model comparison, and stress diagnostics.
Author: Bhupesh Chandra Dimri
"""

import os
from data_pipeline import generate_synthetic_manager_universe
from feature_engineering import engineer_manager_research_features
from model import train_and_compare_models


def run_evaluation():
    raw_df = generate_synthetic_manager_universe(n_managers=250, seed=42)
    feat_df = engineer_manager_research_features(raw_df)
    metrics_df, fi_df = train_and_compare_models(feat_df)

    print("=== 1. VOYA MASS MANAGER SELECTION MODEL PERFORMANCE ===")
    print(metrics_df.to_string(index=False))
    print("\n=== 2. TOP 8 ENGINEERED FEATURES BY IMPORTANCE ===")
    print(fi_df.head(8).to_string(index=False))

    watchlist_count = int(feat_df["board_15c_watchlist_flag"].sum())
    print(f"\n=== 3. 15(c) BOARD GOVERNANCE WATCHLIST ALERTS: {watchlist_count} / {len(feat_df)} MANAGERS ===")

    rep_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(rep_dir, exist_ok=True)
    report_path = os.path.join(rep_dir, "model_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Voya MASS Manager Selection & 15(c) Governance — Empirical Model Report\n\n")
        f.write("## Model Performance Comparison\n\n")
        f.write(metrics_df.to_markdown(index=False) + "\n\n")
        f.write("## Top 8 Predictive Manager Features\n\n")
        f.write(fi_df.head(8).to_markdown(index=False) + "\n")
    print(f"[OK] Saved empirical report to {report_path}")


if __name__ == "__main__":
    run_evaluation()

