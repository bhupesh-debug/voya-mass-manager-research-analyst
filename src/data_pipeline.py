"""
Voya MASS Manager Research & Selection (MR&S) — Data Pipeline & Synthetic Universe Generator
Simulates public-markets manager data across Mutual Funds, CITs, ETFs, and SMAs
mirroring schemas from eVestment, Morningstar Direct, FactSet, and BlackRock Aladdin.
Author: Bhupesh Chandra Dimri
"""

import os
import numpy as np
import pandas as pd


def generate_synthetic_manager_universe(n_managers: int = 250, seed: int = 42) -> pd.DataFrame:
    """Generates a realistic panel of institutional managers evaluated by Voya MR&S."""
    rng = np.random.default_rng(seed)

    vehicles = rng.choice(["Mutual Fund", "CIT", "SMA", "ETF", "Closed-End Fund"], size=n_managers, p=[0.35, 0.25, 0.20, 0.12, 0.08])
    asset_classes = rng.choice(
        ["US Large Cap Value", "US Large Cap Growth", "US Small Cap Core", "Intl Developed Equity", "EM Equity", "Core Plus Fixed Income"],
        size=n_managers,
    )

    expense_ratio_bps = np.round(rng.uniform(18, 95, size=n_managers), 1)
    pm_tenure_years = np.round(rng.uniform(1.5, 18.0, size=n_managers), 1)
    team_turnover_3yr_pct = np.round(rng.beta(1.8, 8.0, size=n_managers) * 100, 1)
    aum_bln = np.round(rng.lognormal(mean=1.2, sigma=0.9, size=n_managers), 2)

    # Quantitative factor & portfolio construction metrics (FactSet / Axioma / Barra proxies)
    r_squared_style = np.round(rng.uniform(0.72, 0.99, size=n_managers), 3)
    active_share_pct = np.round(np.clip(100 * (1.0 - (r_squared_style - 0.65) * 0.85) + rng.normal(0, 4, n_managers), 25, 96), 1)
    tracking_error_bps = np.round(rng.uniform(120, 680, size=n_managers), 0)
    style_drift_score = np.round(rng.gamma(shape=2.0, scale=0.12, size=n_managers), 3)
    upside_capture = np.round(rng.normal(102.5, 7.5, size=n_managers), 1)
    downside_capture = np.round(rng.normal(96.0, 8.5, size=n_managers), 1)
    historical_3yr_gross_alpha_bps = np.round(rng.normal(85, 160, size=n_managers), 1)

    # True underlying skill driver: high active share + low style drift + low team turnover + reasonable fee + downside protection
    capture_spread = upside_capture - downside_capture
    skill_signal = (
        0.35 * ((active_share_pct - 60) / 20.0)
        - 0.40 * ((style_drift_score - 0.24) / 0.15)
        - 0.25 * ((team_turnover_3yr_pct - 18.0) / 12.0)
        - 0.25 * ((expense_ratio_bps - 55.0) / 25.0)
        + 0.30 * (capture_spread / 10.0)
        + 0.15 * ((pm_tenure_years - 7.0) / 5.0)
    )

    forward_3yr_net_ir = np.round(0.32 * skill_signal + rng.normal(0.10, 0.28, size=n_managers), 2)
    top_quartile_flag = (forward_3yr_net_ir >= 0.45).astype(int)

    df = pd.DataFrame(
        {
            "manager_id": [f"MGR-{i:03d}" for i in range(1, n_managers + 1)],
            "vehicle_type": vehicles,
            "peer_category": asset_classes,
            "aum_usd_bln": aum_bln,
            "expense_ratio_bps": expense_ratio_bps,
            "pm_tenure_yrs": pm_tenure_years,
            "team_turnover_3yr_pct": team_turnover_3yr_pct,
            "r_squared_factor": r_squared_style,
            "active_share_pct": active_share_pct,
            "tracking_error_bps": tracking_error_bps,
            "style_drift_index": style_drift_score,
            "upside_capture_pct": upside_capture,
            "downside_capture_pct": downside_capture,
            "hist_3yr_gross_alpha_bps": historical_3yr_gross_alpha_bps,
            "forward_3yr_net_ir": forward_3yr_net_ir,
            "target_top_quartile_ir": top_quartile_flag,
        }
    )
    return df


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic")
    os.makedirs(out_dir, exist_ok=True)
    universe_df = generate_synthetic_manager_universe(n_managers=250)
    csv_path = os.path.join(out_dir, "voya_mass_manager_universe.csv")
    universe_df.to_csv(csv_path, index=False)
    print(f"[OK] Saved {len(universe_df)} institutional managers to {csv_path}")
    print(universe_df.head(10).to_string(index=False))

