# Voya-MASS-ManagerAlpha: Multi-Asset Manager Due Diligence, Style Drift & Persistent Alpha Engine

> **One-Liner**: An institutional Python & DuckDB manager research platform engineered for **Voya Investment Management's Multi-Asset Strategies & Solutions (MASS, $54B+ AUM)** team to automate returns-based/holdings-based factor decomposition (`Axioma`/`Barra`/`Fama-French`), detect manager style drift 2 quarters early, and predict 36-month forward out-of-sample Information Ratio ($IR$) across Mutual Funds, CITs, ETFs, and SMAs.

- **Author**: Bhupesh Chandra Dimri (`M.S. Accounting Analytics & Data Technology, Pace University`)
- **Target Role**: Manager Research Analyst — Manager Research & Selection (`MR&S`), Multi-Asset Strategies & Solutions (`MASS`), Voya Investment Management

---

## 1. Business Problem & Voya MASS Alignment
Voya's MR&S team oversees manager selection, portable alpha, target date funds (`TDFs`), model portfolios, and 15(c) mutual fund / closed-end fund board governance across **$54B+ in multi-asset AUM**. Traditional manager research relies on fragmented manual exports across **eVestment, Morningstar Direct, FactSet, BlackRock Aladdin, and Backstop**, creating three structural bottlenecks:
1. **Closet Indexing & Fee Leakage**: Active equity managers charging `65–85 bps` while delivering `>90%` passive style-factor beta (`Market`, `Size`, `Value`, `Momentum`, `Quality`).
2. **Lagging Style Drift Detection**: Identifying when a Value or Small-Cap manager drifts into Growth/Large-Cap *after* a drawdown hits Voya's TDF glidepath or Mutual Fund Board oversight report.
3. **Manual 15(c) Board & Peer Diagnostic Reporting**: Spending 40+ hours per quarter compiling peer quartiles, upside/downside capture, and Brinson attribution tables.

---

## 2. Three Core Quantitative & ML Modules
1. **Module A — Constrained Factor & Style Drift Decomposition (`src/feature_engineering.py`)**:
   - Rolling 36-month constrained Sharpe/Fama-French 5-Factor + Momentum regression (`Statsmodels` / `CVXPY`) emulating `Axioma` / `Barra` factor exposures, computing **Active Share Proxy ($1 - R^2$)**, **Style Drift Velocity ($\Delta \beta_k$)**, and **Up/Down Capture Asymmetry**.
2. **Module B — Forward Manager Alpha & Watchlist Classifier (`src/model.py`)**:
   - 4-Tier modeling pipeline (`Ridge Baseline` → `XGBoost / LightGBM Forward IR Ranker` → `CVXPY Multi-Manager Portable Alpha & TDF Sleeve Optimizer` → `NLP SEC N-CSR / Backstop Commentary Drift Scorer`) predicting whether an active manager will achieve **Top-Quartile Net Information Ratio ($IR > 0.50$)** over the next 12–36 months or trigger a **15(c) Board Watchlist Alert**.
3. **Module C — Automated 15(c) Board Oversight & Aladdin/eVestment Diagnostic Engine (`src/evaluate.py`)**:
   - Generates reproducible peer-group quartile scorecards, stress-test simulations (`2022 Rate Shock`, `Growth-to-Value Rotation`, `Liquidity Freeze`), and executive tables ready for the **CIO of MASS** and Mutual Fund Board packets.

---

## 3. Repository Structure
```text
ml-project-voya-manager-research-analyst/
├── README.md
├── requirements.txt
├── data/
│   └── synthetic/              # Generated multi-manager eVestment/Morningstar/13F panel
├── src/
│   ├── data_pipeline.py        # DuckDB & Pandas ingestion + synthetic manager universe generator
│   ├── feature_engineering.py  # Rolling 6P factor decomposition, Style Drift Index & Active Share
│   ├── model.py                # Baseline Ridge, XGBoost/LightGBM Alpha Ranker & CVXPY Sleeve Optimizer
│   └── evaluate.py             # Walk-forward validation, 15(c) Board Watchlist & Stress Testing
└── reports/
    └── model_report.md         # Empirical findings & MASS portfolio impact summary
```

## 4. Quick Start (Run in < 30 Seconds)
```bash
pip install -r requirements.txt
python src/data_pipeline.py
python src/evaluate.py
```

