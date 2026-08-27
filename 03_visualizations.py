import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.0)
PALETTE = "crest"

df = pd.read_csv("logistics_dataset.csv", parse_dates=["ship_date"])
IMG = "images/"

# 1. Histogram of delivery times
plt.figure(figsize=(8, 5))
sns.histplot(df["delivery_time_days"], bins=30, kde=True, color="#2c6e8f")
plt.title("Distribution of Delivery Times")
plt.xlabel("Delivery Time (days)")
plt.ylabel("Number of Shipments")
plt.tight_layout()
plt.savefig(IMG + "01_delivery_time_hist.png", dpi=150)
plt.close()

# 2. Boxplot of delivery time by mode of transport
plt.figure(figsize=(8, 5))
order = df.groupby("mode_of_transport")["delivery_time_days"].median().sort_values().index
sns.boxplot(data=df, x="mode_of_transport", y="delivery_time_days", order=order, palette=PALETTE)
plt.title("Delivery Time by Mode of Transport")
plt.xlabel("Mode of Transport")
plt.ylabel("Delivery Time (days)")
plt.tight_layout()
plt.savefig(IMG + "02_delivery_time_by_mode_box.png", dpi=150)
plt.close()

# 3. Scatter plot: distance vs cost, colored by mode
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="distance_km", y="transportation_cost_inr",
                 hue="mode_of_transport", alpha=0.6, palette="Set2", s=35)
plt.title("Transportation Cost vs. Distance")
plt.xlabel("Distance (km)")
plt.ylabel("Transportation Cost (INR)")
plt.legend(title="Mode")
plt.tight_layout()
plt.savefig(IMG + "03_cost_vs_distance_scatter.png", dpi=150)
plt.close()

# 4. Correlation heatmap
corr_cols = ["distance_km", "shipment_volume_units", "delivery_time_days",
             "transportation_cost_inr", "customer_rating", "delay_days"]
plt.figure(figsize=(7.5, 6))
corr = df[corr_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, square=True,
            cbar_kws={"shrink": 0.8})
plt.title("Correlation Matrix of Key Logistics Metrics")
plt.tight_layout()
plt.savefig(IMG + "04_correlation_heatmap.png", dpi=150)
plt.close()

# 5. Bar chart: average transportation cost by region
plt.figure(figsize=(8, 5))
region_cost = df.groupby("destination_region")["transportation_cost_inr"].mean().sort_values(ascending=False)
sns.barplot(x=region_cost.index, y=region_cost.values, palette=PALETTE)
plt.title("Average Transportation Cost by Destination Region")
plt.xlabel("Region")
plt.ylabel("Average Cost (INR)")
plt.tight_layout()
plt.savefig(IMG + "05_avg_cost_by_region_bar.png", dpi=150)
plt.close()

# 6. On-time delivery rate by mode
plt.figure(figsize=(8, 5))
ontime = df.groupby("mode_of_transport")["on_time_delivery"].mean().sort_values(ascending=False) * 100
sns.barplot(x=ontime.index, y=ontime.values, palette="crest")
plt.title("On-Time Delivery Rate by Mode of Transport")
plt.xlabel("Mode of Transport")
plt.ylabel("On-Time Delivery Rate (%)")
plt.ylim(0, 105)
for i, v in enumerate(ontime.values):
    plt.text(i, v + 1.5, f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(IMG + "06_ontime_rate_by_mode.png", dpi=150)
plt.close()

# 7. Monthly trend: shipment volume and average cost (dual-axis line chart)
monthly = df.groupby("ship_month").agg(
    shipments=("shipment_id", "count"),
    avg_cost=("transportation_cost_inr", "mean"),
).reset_index()

fig, ax1 = plt.subplots(figsize=(9, 5))
color1 = "#2c6e8f"
ax1.plot(monthly["ship_month"], monthly["shipments"], marker="o", color=color1, label="Shipment Count")
ax1.set_xlabel("Month")
ax1.set_ylabel("Number of Shipments", color=color1)
ax1.tick_params(axis="y", labelcolor=color1)

ax2 = ax1.twinx()
color2 = "#c1440e"
ax2.plot(monthly["ship_month"], monthly["avg_cost"], marker="s", color=color2, label="Avg Cost (INR)")
ax2.set_ylabel("Average Transportation Cost (INR)", color=color2)
ax2.tick_params(axis="y", labelcolor=color2)

plt.title("Monthly Shipment Volume and Average Transportation Cost")
fig.tight_layout()
plt.savefig(IMG + "07_monthly_trend.png", dpi=150)
plt.close()

# 8. Shipment volume distribution by warehouse (bar)
plt.figure(figsize=(8, 5))
wh_vol = df.groupby("origin_warehouse")["shipment_volume_units"].sum().sort_values(ascending=False)
sns.barplot(x=wh_vol.index, y=wh_vol.values, palette=PALETTE)
plt.title("Total Shipment Volume by Origin Warehouse")
plt.xlabel("Warehouse")
plt.ylabel("Total Units Shipped")
plt.tight_layout()
plt.savefig(IMG + "08_volume_by_warehouse.png", dpi=150)
plt.close()

print("All visualizations saved.")
