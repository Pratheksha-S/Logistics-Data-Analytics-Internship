"""
Week 2 Task - Data Collection, Cleaning, and Preprocessing for Logistics Analysis
Logistics Data Analyst Internship (Yuva Intern / NSDC)

Dataset: DataCo Smart Supply Chain (DataCoSupplyChainDataset.csv)
Source: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ---------------------------------------------------------------------------
# 1. Load and inspect
# ---------------------------------------------------------------------------
df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin-1")
print("Shape:", df.shape)  # (180519, 53)

nulls = df.isnull().sum()
print("\nColumns with missing values:")
print(nulls[nulls > 0].sort_values(ascending=False))
# Product Description   180519  (100.0%)
# Order Zipcode         155679  (86.2%)
# Customer Lname              8
# Customer Zipcode            3

# ---------------------------------------------------------------------------
# 2. Drop unusable columns and negligible rows
# ---------------------------------------------------------------------------
df = df.drop(columns=["Product Description", "Order Zipcode"])
df = df.dropna(subset=["Customer Lname", "Customer Zipcode"])
print("\nShape after dropping unusable columns/rows:", df.shape)

# ---------------------------------------------------------------------------
# 3. Check for duplicates
# ---------------------------------------------------------------------------
print("\nFull-row duplicates:", df.duplicated().sum())
print("Duplicate Order Item Id:", df.duplicated(subset=["Order Item Id"]).sum())
# Both came back 0 - no duplicate handling needed for this dataset

# ---------------------------------------------------------------------------
# 4. Fix inconsistent region label formatting
# ---------------------------------------------------------------------------
df["Order Region"] = (
    df["Order Region"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)
# 'South of  USA ' -> 'South of USA'
# 'West of USA '   -> 'West of USA'
# 'US Center '     -> 'US Center'

# ---------------------------------------------------------------------------
# 5. Outlier detection on profit, grouped by shipping mode (IQR method)
# ---------------------------------------------------------------------------
def flag_outliers_iqr(group, col):
    Q1, Q3 = group[col].quantile(0.25), group[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    return (group[col] < lower) | (group[col] > upper)


df["is_outlier"] = df.groupby("Shipping Mode", group_keys=False).apply(
    lambda g: flag_outliers_iqr(g, "Benefit per order")
)
print(
    f"\nOutliers flagged on Benefit per order: "
    f"{df['is_outlier'].sum()} of {len(df)} "
    f"({df['is_outlier'].sum() / len(df) * 100:.1f}%)"
)
# 18958 of 180519 (10.5%)

# ---------------------------------------------------------------------------
# 6. Normalize numeric fields before modelling
# ---------------------------------------------------------------------------
features_to_scale = ["Sales", "Product Price", "Order Item Discount Rate"]
scaler = MinMaxScaler()
df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

print("\nScaled feature summary:")
print(df[features_to_scale].describe())

# ---------------------------------------------------------------------------
# Save cleaned dataset
# ---------------------------------------------------------------------------
df.to_csv("dataco_cleaned.csv", index=False)
print("\nCleaned dataset saved to dataco_cleaned.csv")
