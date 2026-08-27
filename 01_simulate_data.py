"""
Week 3 - Logistics Data Simulation
Generates a hypothetical shipment-level logistics dataset with realistic
relationships between distance, delivery time, cost, mode of transport,
and on-time performance.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 1200  # number of shipments

regions = ["North", "South", "East", "West", "Central"]
region_weights = [0.22, 0.24, 0.18, 0.20, 0.16]

modes = ["Road", "Rail", "Air", "Sea"]
mode_weights = [0.55, 0.15, 0.10, 0.20]

warehouses = [f"WH-{i}" for i in range(1, 7)]

# Base characteristics per mode (avg speed km/day, base cost per km, variability)
mode_profile = {
    "Road": {"speed": 450, "cost_per_km": 38, "delay_prob": 0.22},
    "Rail": {"speed": 500, "cost_per_km": 22, "delay_prob": 0.15},
    "Air":  {"speed": 3200, "cost_per_km": 145, "delay_prob": 0.10},
    "Sea":  {"speed": 380, "cost_per_km": 9, "delay_prob": 0.30},
}

dates = pd.date_range("2026-01-01", periods=180, freq="D")

rows = []
for i in range(1, N + 1):
    region = np.random.choice(regions, p=region_weights)
    mode = np.random.choice(modes, p=mode_weights)
    warehouse = np.random.choice(warehouses)
    ship_date = np.random.choice(dates)

    profile = mode_profile[mode]

    distance_km = max(20, np.random.gamma(shape=2.2, scale=350))
    if mode == "Air":
        distance_km = max(distance_km, 400)  # air used mainly for longer hauls

    shipment_volume = max(1, np.round(np.random.lognormal(mean=3.0, sigma=0.8)))  # units

    base_days = distance_km / profile["speed"]
    handling_days = np.random.uniform(0.3, 1.2)
    delay = 0
    if np.random.rand() < profile["delay_prob"]:
        delay = np.random.exponential(scale=1.5)
    delivery_time_days = round(base_days + handling_days + delay, 2)

    cost_noise = np.random.normal(1, 0.12)
    fuel_surcharge = 1 + (0.15 if mode in ("Road", "Air") else 0.05)
    transportation_cost = round(
        distance_km * profile["cost_per_km"] * fuel_surcharge * cost_noise
        + shipment_volume * np.random.uniform(2, 6),
        2,
    )

    promised_days = {"Road": 4, "Rail": 5, "Air": 2, "Sea": 10}[mode]
    on_time = delivery_time_days <= promised_days + 0.5

    customer_rating = np.clip(
        np.random.normal(4.4 if on_time else 3.0, 0.6), 1, 5
    )

    rows.append(
        {
            "shipment_id": f"SHP{i:05d}",
            "ship_date": ship_date,
            "origin_warehouse": warehouse,
            "destination_region": region,
            "mode_of_transport": mode,
            "distance_km": round(distance_km, 1),
            "shipment_volume_units": int(shipment_volume),
            "delivery_time_days": delivery_time_days,
            "promised_time_days": promised_days,
            "on_time_delivery": on_time,
            "transportation_cost_inr": transportation_cost,
            "customer_rating": round(customer_rating, 1),
        }
    )

df = pd.DataFrame(rows)
df["cost_per_km"] = round(df["transportation_cost_inr"] / df["distance_km"], 2)
df["delay_days"] = (df["delivery_time_days"] - df["promised_time_days"]).clip(lower=0).round(2)
df["ship_month"] = pd.to_datetime(df["ship_date"]).dt.to_period("M").astype(str)

df.to_csv("logistics_dataset.csv", index=False)
print(df.shape)
print(df.head())
print(df.dtypes)
