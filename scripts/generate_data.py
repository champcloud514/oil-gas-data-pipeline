import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Number of records
records = 10000

# Generate production data
data = {
    "production_date": pd.date_range(
        start="2025-01-01",
        periods=records,
        freq="h"
    ),

    "well_id": np.random.choice(
        ["FC-23", "FC-24", "FC-25", "FC-26"],
        records
    ),

    "field_name": np.random.choice(
        ["Jubilee", "TEN"],
        records
    ),

    "oil_rate_bopd": np.random.uniform(
        500, 3000, records
    ),

    "gas_rate_mscfd": np.random.uniform(
        100, 1000, records
    ),

    "water_rate_bwpd": np.random.uniform(
        50, 800, records
    ),

    "tubing_pressure_psi": np.random.uniform(
        1000, 4000, records
    ),

    "casing_pressure_psi": np.random.uniform(
        500, 2500, records
    ),

    "temperature_c": np.random.uniform(
        40, 120, records
    )
}

df = pd.DataFrame(data)

# Introduce missing values
df.loc[10:20, "oil_rate_bopd"] = np.nan

# Introduce duplicate records
df = pd.concat(
    [df, df.iloc[0:10]],
    ignore_index=True
)

# Introduce invalid negative production values
df.loc[30:32, "water_rate_bwpd"] = -100

# Save dataset
df.to_csv(
    "data/raw/production_data.csv",
    index=False
)

print("Production dataset generated successfully!")

print("Dataset shape:", df.shape)

print(df.head())