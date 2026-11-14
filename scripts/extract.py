import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure Logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"

)

# define project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "production_data.csv"

def extract_data(file_path):
    try:
        logging.info("Starting data extraction")

        #Check if the source file exits
        if not file_path.exists():
            raise FileNotFoundError(f"File not found:{file_path}")

        # Extract CSv data
        df =pd.read_csv(file_path)

        # check if dataset is empty

        if df.empty:
            raise ValueError("source dataset is empty")
        logging.info(f"Successfully extracted {len(df)} records")

        return df
    except Exception as e:
        logging.error(f"Data extraction failed:{e}")

        raise
if __name__ == "__main__":
    df = extract_data(RAW_FILE)

    print(df.head())

    print("Dataset shape:",df.shape)
    print(f"Successfully extracted {len(df)} records")
    print(list(df.columns))
    print(f"Number of columns:",len(df.columns))

