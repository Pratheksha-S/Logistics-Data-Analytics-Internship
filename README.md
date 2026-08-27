# Logistics Data Analytics Internship

Weekly deliverables from a Logistics Data Analyst internship (Yuva Intern / NSDC platform), covering strategic planning, data cleaning, exploratory analysis and visualization, and predictive modeling and optimization — all built in Python.

## Overview

| Week | Focus | Report | Code |
|---|---|---|---|
| 1 | Strategic planning for logistics operations | `Week1_Logistics_Strategic_Planning_Report.docx` | — |
| 2 | Data collection, cleaning, and preprocessing | *(covered in code)* | `Week2_data_cleaning.py` |
| 3 | Exploratory data analysis and visualization | `Week3_Logistics_Data_Analysis_Report.docx` | `01_simulate_data.py`, `02_eda.py`, `03_visualizations.py` |
| 4 | Predictive modeling and optimization | `Week4_Predictive_Modeling_Optimization_Report.docx` | *(see in files.zip)* |

## Week 1 — Strategic Planning

A planning report laying out the objectives, scope, and analytical roadmap for the internship's logistics data work.

## Week 2 — Data Collection, Cleaning, and Preprocessing

Cleans the [DataCo Smart Supply Chain dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) (180,519 rows, 53 columns) with pandas and scikit-learn:

- Dropped columns that were unusable due to near-total missingness (`Product Description` — 100% null, `Order Zipcode` — 86.2% null) and the handful of rows missing `Customer Lname` / `Customer Zipcode`
- Checked for duplicate rows and duplicate order-item IDs (none found)
- Standardized inconsistent whitespace in the `Order Region` labels
- Flagged outliers in `Benefit per order` using the IQR method, grouped by shipping mode (10.5% of rows flagged)
- Scaled `Sales`, `Product Price`, and `Order Item Discount Rate` with `MinMaxScaler`
- Saved the result to `dataco_cleaned.csv`

**Run it:**
```bash
python Week2_data_cleaning.py
```
*(requires `DataCoSupplyChainDataset.csv` in the working directory — download from the Kaggle link above)*

## Week 3 — Exploratory Data Analysis and Visualization

Simulates a realistic 1,200-shipment logistics dataset (six warehouses, five regions, four transport modes) and explores it end to end:

- **`01_simulate_data.py`** — generates `logistics_dataset.csv`, with mode-specific speed, cost, and delay profiles so relationships between distance, cost, and delivery time are realistic rather than random
- **`02_eda.py`** — descriptive statistics, group-wise summaries (by mode, region, warehouse), correlation matrix, and monthly trend table
- **`03_visualizations.py`** — 8 charts (distribution, comparison, relationship, and trend) built with matplotlib and seaborn, each chosen for what it's best suited to show

**Run it (in order):**
```bash
python 01_simulate_data.py
python 02_eda.py
python 03_visualizations.py
```

Key findings are documented in `Week3_Logistics_Data_Analysis_Report.docx`, including that Road transport (despite handling the largest share of shipments) has the weakest on-time rate, and that mode of transport — not shipment size — is the dominant cost driver.

## Week 4 — Predictive Modeling and Optimization

Builds on the Week 3 dataset to forecast `delivery_time_days` using only information known at booking time, then uses the trained model to test a concrete optimization.

- **Model selection:** Linear Regression, Decision Tree, and Random Forest were compared on identical preprocessing (one-hot encoding + pipeline). Linear Regression won (RMSE 1.03 days, R² 0.58) — confirmed by 5-fold cross-validation and a `GridSearchCV` hyperparameter search on the Random Forest, which still didn't beat it.
- **Optimization:** the trained model is used to (1) flag shipments at risk of missing their promised delivery window before dispatch, and (2) simulate reassigning Road shipments to Rail — predicted on-time rate improves from 91.6% to 93.9%, with the biggest gains on longer routes.

Full methodology, code, and results are in `Week4_Predictive_Modeling_Optimization_Report.docx`.

> The four supporting scripts for this week (`01_data_preparation.py`, `02_model_training.py`, `03_model_evaluation.py`, `04_optimization_strategy.py`) are included in the report as code excerpts; add them here as standalone `.py` files to keep the repo consistent with Weeks 1–3.

## Tools and libraries

`pandas` · `numpy` · `scikit-learn` · `matplotlib` · `seaborn` · `joblib`

## Author

**Pratheksha S**
Logistics Data Analyst Intern — Yuva Intern (NSDC Platform)
