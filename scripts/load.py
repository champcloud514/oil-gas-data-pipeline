import os
import logging
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# File location
VALID_FILE = (
    BASE_DIR / "data" / "processed" / "clean_production_data.csv"
)

# Snowflake configuration
connection_config = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
}


def load_data():

    if not VALID_FILE.exists():
        raise FileNotFoundError(f"File not found: {VALID_FILE}")

    conn = None

    try:
        logging.info("Connecting to Snowflake")

        conn = snowflake.connector.connect(**connection_config)

        cursor = conn.cursor()

        logging.info("Snowflake connection successful")

        # Upload local CSV to Snowflake stage
        file_path = VALID_FILE.resolve().as_posix()
        file_uri = f"file:///{file_path}"

        put_sql = f"""
            PUT '{file_uri}'
            @OIL_GAS_DB.PRODUCTION.PRODUCTION_STAGE/production
            AUTO_COMPRESS=FALSE
            OVERWRITE=TRUE
        """

        cursor.execute(put_sql)

        print("File uploaded successfully")

        # Load staged CSV into Snowflake table
        copy_sql = """
            COPY INTO OIL_GAS_DB.PRODUCTION.PRODUCTION_DATA
            FROM @OIL_GAS_DB.PRODUCTION.PRODUCTION_STAGE/production
            FILES = ('valid_production_data.csv')
            FILE_FORMAT = (
                FORMAT_NAME =
                'OIL_GAS_DB.PRODUCTION.PRODUCTION_CSV_FORMAT'
            )
            ON_ERROR = 'ABORT_STATEMENT'
        """

        cursor.execute(copy_sql)

        for row in cursor.fetchall():
            print(row)

        logging.info("Data loading completed")

    except Exception:
        logging.exception("Snowflake loading failed")
        raise

    finally:
        if conn:
            conn.close()
            logging.info("Snowflake connection closed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_data()