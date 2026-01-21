import pandas as pd
import numpy as np
import random

np.random.seed(42)

# -----------------------------
# Vehicle Master Data
# -----------------------------
vehicle_models = [
    {"Model_Code": "ELN", "Segment": "Compact", "Base_MSRP": 23000},
    {"Model_Code": "SON", "Segment": "Sedan", "Base_MSRP": 28000},
    {"Model_Code": "TUC", "Segment": "SUV", "Base_MSRP": 33000},
    {"Model_Code": "SAN", "Segment": "SUV", "Base_MSRP": 38000},
    {"Model_Code": "PAL", "Segment": "SUV", "Base_MSRP": 45000}
]

# ✅ Canadian regions only
regions = {
    "ON": 1.00,  # Ontario
    "QC": 0.98,  # Quebec
    "BC": 1.03,  # British Columbia
    "AB": 0.97,  # Alberta
    "MB": 0.96,  # Manitoba
    "SK": 0.95,  # Saskatchewan
    "NS": 0.95,  # Nova Scotia
    "NB": 0.95,  # New Brunswick
    "NL": 0.94,  # Newfoundland & Labrador
    "PE": 0.94   # Prince Edward Island
}

# -----------------------------
# Market Index by Year
# -----------------------------
market_index = {}
for year in range(2013, 2026):
    if year in [2020, 2021]:
        market_index[year] = np.random.uniform(1.15, 1.30)   # COVID spike
    elif year in [2022, 2023]:
        market_index[year] = np.random.uniform(0.90, 0.98)   # correction
    else:
        market_index[year] = np.random.uniform(0.95, 1.05)

# -----------------------------
# Generate Lease-Level Data
# -----------------------------
rows = []
lease_id = 1

for year in range(2013, 2026):
    for _ in range(17000):  # ~220K rows
        model = random.choice(vehicle_models)
        region = random.choice(list(regions.keys()))

        # MSRP with realistic variance
        msrp = model["Base_MSRP"] * np.random.uniform(0.97, 1.08)

        # Segment-based residual assumptions
        if model["Segment"] == "SUV":
            residual_pct = np.random.uniform(0.58, 0.66)
        elif model["Segment"] == "Sedan":
            residual_pct = np.random.uniform(0.54, 0.61)
        else:
            residual_pct = np.random.uniform(0.50, 0.58)

        residual_value = msrp * residual_pct

        # Mileage (bounded, realistic)
        mileage = int(np.clip(np.random.normal(55000, 13000), 12000, 120000))

        mileage_penalty = max(0, (mileage - 60000) / 90000)

        # Market & region effects
        market_factor = market_index[year]
        region_factor = regions[region]

        random_noise = np.random.normal(0, 0.04)

        sale_price = residual_value * (
            market_factor * region_factor
            - mileage_penalty
            + random_noise
        )

        # Prevent absurd negative prices
        sale_price = max(sale_price, residual_value * 0.55)

        gain_loss = sale_price - residual_value
        gain_loss_pct = (gain_loss / residual_value) * 100

        rows.append([
            lease_id,
            model["Model_Code"],
            model["Segment"],
            year,
            round(residual_value, 2),
            round(sale_price, 2),
            round(gain_loss, 2),
            round(gain_loss_pct, 2),
            mileage,
            region
        ])

        lease_id += 1

# -----------------------------
# Create DataFrame & Export
# -----------------------------
columns = [
    "Lease_ID",
    "Model_Code",
    "Segment",
    "Return_Year",
    "Residual_Value",
    "Actual_Sale_Price",
    "Gain_Loss_Amount",
    "Gain_Loss_Pct",
    "Mileage_At_Return",
    "Region"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("Updated_Fact_Lease_Returns.csv", index=False)

print("✅ Lease-level RV Risk dataset generated")
print(f"Rows: {len(df):,}")
