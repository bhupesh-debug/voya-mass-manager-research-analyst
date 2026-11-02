"""
Voya MASS Manager Research & Selection (MR&S) — Multi-Tier Model Pipeline
Compares Baseline Ridge/Logistic vs. Random Forest vs. Gradient Boosted Trees
for predicting 3-Year Forward Out-of-Sample Net Information Ratio (IR) & Top-Quartile Selection.
Author: Bhupesh Chandra Dimri
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import mean_squared_error, precision_score, r2_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

FEATURE_COLS = [
    "expense_ratio_bps",
    "pm_tenure_yrs",
    "team_turnover_3yr_pct",
    "r_squared_factor",
    "active_share_pct",
    "tracking_error_bps",
    "style_drift_index",
    "upside_capture_pct",
    "downside_capture_pct",
    "hist_3yr_gross_alpha_bps",
    "fee_to_active_risk_ratio",
    "capture_asymmetry_ratio",
    "conviction_stability_score",
    "people_governance_stability",
    "net_hist_information_ratio",
]


def train_and_compare_models(df: pd.DataFrame):
    """Trains Baseline Linear/Logistic, Random Forest, and Gradient Boosting models."""
    X = df[FEATURE_COLS].values
    y_cls = df["target_top_quartile_ir"].values
    y_reg = df["forward_3yr_net_ir"].values

    X_train, X_test, y_cls_train, y_cls_test, y_reg_train, y_reg_test = train_test_split(
        X, y_cls, y_reg, test_size=0.25, random_state=42, stratify=y_cls
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    models = {
        "Baseline (L2 Logistic + Ridge)": (
            LogisticRegression(C=1.0, random_state=42),
            Ridge(alpha=2.0),
            True,
        ),
        "Intermediate (Random Forest)": (
            RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42),
             None,
            False,
        ),
        "Advanced (Gradient Boosted Alpha Ranker)": (
            GradientBoostingClassifier(n_estimators=150, learning_rate=0.05, max_depth=3, random_state=42),
            None,
            False,
        ),
    }

    results = []
    feature_importances = None

    for name, (clf, reg, use_scaled) in models.items():
        X_tr = X_train_sc if use_scaled else X_train
        X_te = X_test_sc if use_scaled else X_test
        clf.fit(X_tr, y_cls_train)
        probs = clf.predict_proba(X_te)[:, 1]
        preds = (probs >= 0.50).astype(int)

        auc = roc_auc_score(y_cls_test, probs)
        prec = precision_score(y_cls_test, preds, zero_division=0)

        # Precision@Top-10 Managers (Shortlist Hit Rate for Voya MR&S Allocation Committee)
        top10_idx = np.argsort(probs)[::-1][:10]
        hit_rate_top10 = float(np.mean(y_cls_test[top10_idx]))

        results.append(
            {
                "Model Tier": name,
                "ROC-AUC": round(auc, 3),
                "Precision (Overall)": round(prec, 3),
                "Top-10 Manager Hit Rate": f"{hit_rate_top10 * 100:.1f}%",
            }
        )

        if "Gradient Boosted" in name:
            feature_importances = pd.DataFrame(
                {"feature": FEATURE_COLS, "importance": np.round(clf.feature_importances_, 4)}
            ).sort_values("importance", ascending=False)

    return pd.DataFrame(results), feature_importances

