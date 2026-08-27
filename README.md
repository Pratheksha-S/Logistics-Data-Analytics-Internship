# Logistics Data Analyst Internship

Weekly task code for the Logistics Data Analyst internship (Yuva Intern / NSDC), 30 July 2026 – 27 August 2026.

Scenario used throughout: **SwiftCart Logistics**, a fictional regional e-commerce distributor running three warehouses and handling last-mile delivery to ~15,000 customers a month. Real analysis and code are run against the [DataCo Smart Supply Chain dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) as a stand-in for SwiftCart's own data.

## Contents

| Week | File | Focus |
|------|------|-------|
| 1 | `week1_strategic_planning.py` | Scenario definition, KPIs, and pseudocode for the proposed analytics roadmap |
| 2 | `week2_data_cleaning.py` | Data collection, cleaning, and preprocessing on the real DataCo dataset |
| 3 | *(coming soon)* | |
| 4 | *(coming soon)* | |

## Week 2 — Data Cleaning Summary

Ran directly against `DataCoSupplyChainDataset.csv` (180,519 rows, 53 columns):

- **Product Description** — 100% missing, column dropped
- **Order Zipcode** — 86.2% missing, column dropped
- **Customer Lname / Customer Zipcode** — 8 / 3 rows missing, dropped
- **Duplicates** — none found
- **Order Region** — whitespace formatting issues fixed (e.g. `'South of  USA '` → `'South of USA'`)
- **Profit outliers** — 10.5% of rows flagged via IQR (grouped by Shipping Mode)
- Normalized `Sales`, `Product Price`, and `Order Item Discount Rate` with min-max scaling ahead of any future clustering work

## Requirements

```
pandas
scikit-learn
```

## Author

Pratheksha S
