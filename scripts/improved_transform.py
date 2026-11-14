import pandas as pd
from extract import extract_data, RAW_FILE
from pathlib import Path
import logging

# Configure Logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"

)

# define output directories
BASE_DIR = Path(__file__).resolve().parent.parent
VALID_FILE = BASE_DIR / "data/processed/valid_production_data.csv"
REJECTED_FILE = BASE_DIR / "data/processed/rejected_production_data.csv"

def transform_data(df):
    logging.info("starting data transformation")

    # create a copy to protect original data
    df = df.copy()

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    #2 Convert production date to datetime
    df["production_date"] = pd.to_datetime(
        df["production_date"],errors="coerce"
    )

    #3 Remove duplicates records
    initial_records = len(df)

    df = df.drop_duplicates()

    logging.info(f"Removed {initial_records - len(df)} duplicate records")

        # 4. Handle missing values
    numeric_columns = [
        "oil_rate_bopd",
        "gas_rate_mscfd",
        "water_rate_bwpd",
        "tubing_pressure_psi",
        "casing_pressure_psi",
        "temperature_c"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        # 5. Validate production values
    production_columns = [
        "oil_rate_bopd",
        "gas_rate_mscfd",
        "water_rate_bwpd"
    ]

    for column in production_columns:

        df.loc[df[column] < 0, column] = pd.NA

        # 6. Handle missing values
    for column in numeric_columns:

        df[column] = df[column].fillna(
            df[column].median()
        )
    # 7. Remove records with invalid dates or missing identifiers
    df = df.dropna(
        subset=["production_date", "well_id", "field_name"]
    )

    # 8. Standardise text columns
    df["well_id"] = df["well_id"].astype(str).str.strip().str.upper()

    df["field_name"] = df["field_name"].astype(str).str.strip().str.title()

    logging.info(
        f"Transformation completed. Remaining records: {len(df)}"
    )

    return df
def validation(df):

    # Identify invalid records
    invalid_condition = (
        (df['oil_rate_bopd'] < 0) |
        (df['oil_rate_bopd'] > 5000) |
        (df['oil_rate_bopd'].isna())
    )
        # Separate valid and rejected records
    valid_df = df[~invalid_condition].copy()
    rejected_df = df[invalid_condition].copy()

    # Save both datasets
    valid_df.to_csv(VALID_FILE, index=False)
    rejected_df.to_csv(REJECTED_FILE, index=False)

    logging.info(f"Valid records: {len(valid_df)}")
    logging.info(f"Rejected records: {len(rejected_df)}")

    return valid_df, rejected_df

if __name__ == "__main__":

    # Extract raw data
    raw_df = extract_data(RAW_FILE)

    # Transform data
    transformed_df = transform_data(raw_df)

    valid_df, rejected_df = validation(transformed_df)

    # Save transformed data
    valid_df, rejected_df = validation(transformed_df)

    print("Valid records:", len(valid_df))
    print("Rejected records:", len(rejected_df))
    valid_df.to_csv(VALID_FILE, index=False)
    rejected_df.to_csv(REJECTED_FILE, index=False)

    logging.info(f"Clean and valid data saved to {VALID_FILE}")
    logging.info(f"Invalid data saved to {REJECTED_FILE}")

    print(valid_df.head())

    print("Final dataset shape:", valid_df.shape)
