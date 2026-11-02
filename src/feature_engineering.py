"""
Voya MASS Manager Research & Selection (MR&S) — 6P Feature Engineering Engine
Computes Top 5 domain-specific features for active/passive manager selection & 15(c) oversight.
Author: Bhupesh Chandra Dimri
"""

import numpy as np
import pandas as pd


def engineer_manager_research_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers the 5 high-signal institutional manager research features:
    1. fee_to_active_risk_ratio: Expense ratio (bps) per unit of Active Share (%) -> detects 'Closet Indexers'
    2. capture_asymmetry_ratio: Upside Capture / Downside Capture -> measures convex payoff profile
    3. conviction_stability_score: Active Share * (1 - Style Drift Index) -> rewards disciplined high conviction
    4. people_governance_stability: log1p(PM Tenure) / (1 + Team Turnover 3Yr / 100) -> quantifies 'People' pillar
    5. net_hist_information_ratio: (Hist Gross Alpha - Expense Ratio) / Tracking Error
    """
    feat = df.copy()
    feat["fee_to_active_risk_ratio"] = np.round(
        feat["expense_ratio_bps"] / np.maximum(feat["active_share_pct"], 10.0), 4
    )
    feat["capture_asymmetry_ratio"] = np.round(
        feat["upside_capture_pct"] / np.maximum(feat["downside_capture_pct"], 50.0), 4
    )
    feat["conviction_stability_score"] = np.round(
        (feat["active_share_pct"] / 100.0) * np.clip(1.0 - feat["style_drift_index"], 0.0, 1.0), 4
    )
    feat["people_governance_stability"] = np.round(
        np.log1p(feat["pm_tenure_yrs"]) / (1.0 + feat["team_turnover_3yr_pct"] / 25.0), 4
    )
    feat["net_hist_information_ratio"] = np.round(
        (feat["hist_3yr_gross_alpha_bps"] - feat["expense_ratio_bps"])
        / np.maximum(feat["tracking_error_bps"], 50.0),
        4,
    )
    # 15(c) Board Watchlist Flag (Closet Indexer or High Style Drift or Severe Team Turnover)
    feat["board_15c_watchlist_flag"] = (
        ((feat["active_share_pct"] < 60.0) & (feat["expense_ratio_bps"] > 65.0))
        | (feat["style_drift_index"] > 0.40)
        | (feat["team_turnover_3yr_pct"] > 35.0)
    ).astype(int)
    return feat

