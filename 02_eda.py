import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("logistics_dataset.csv", parse_dates=["ship_date"])

print("=== SHAPE ===")
print(df.shape)

print("\n=== DESCRIBE (numeric) ===")
print(df[["distance_km", "shipment_volume_units", "delivery_time_days",
          "transportation_cost_inr", "customer_rating", "cost_per_km",
          "delay_days"]].describe().round(2))

print("\n=== ON-TIME DELIVERY RATE (overall) ===")
print(df["on_time_delivery"].mean().round(3))

print("\n=== ON-TIME RATE BY MODE ===")
print(df.groupby("mode_of_transport")["on_time_delivery"].mean().round(3))

print("\n=== AVG COST & DELIVERY TIME BY MODE ===")
print(df.groupby("mode_of_transport")[["transportation_cost_inr", "delivery_time_days", "cost_per_km"]].mean().round(2))

print("\n=== AVG COST BY REGION ===")
print(df.groupby("destination_region")["transportation_cost_inr"].mean().round(2).sort_values(ascending=False))

print("\n=== SHIPMENT VOLUME BY WAREHOUSE ===")
print(df.groupby("origin_warehouse")["shipment_volume_units"].sum().sort_values(ascending=False))

print("\n=== CORRELATION MATRIX ===")
corr_cols = ["distance_km", "shipment_volume_units", "delivery_time_days",
             "transportation_cost_inr", "customer_rating", "delay_days"]
print(df[corr_cols].corr().round(2))

print("\n=== MONTHLY TREND: shipments, avg cost, on-time rate ===")
monthly = df.groupby("ship_month").agg(
    shipments=("shipment_id", "count"),
    avg_cost=("transportation_cost_inr", "mean"),
    on_time_rate=("on_time_delivery", "mean"),
).round(2)
print(monthly)
