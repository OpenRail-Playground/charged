# Run this file with
# python dashboard/preprocess_data.py

from dotenv import load_dotenv
from charged.snowflake_utils import create_session
import snowflake.snowpark.functions as F


def preprocess_data():
    # load environment variables from .env file
    load_dotenv()

    # create snowpark session
    session = create_session()

    table = "BATTERIELOK_DATA"
    sdf = session.table(table)

    df = sdf_cleaned(sdf).to_pandas()
    df.to_parquet("data/clean_data.parquet")


def sdf_cleaned(sdf):
    update_columns = [
        "VEHICLE_GPS_X",
        "VEHICLE_GPS_Y",
        "VEHICLE_GPS_Z",
    ]

    sdf_updated = sdf.select(
        *[
            F.when(F.col(column) == 0, None).otherwise(F.col(column)).alias(column)
            if column in update_columns
            else F.col(column).alias(column)
            for column in sdf.schema.names
        ]
    )

    sdf_clean = (
        sdf_updated.filter(F.to_date(F.col("TIMESTAMP_VEHICLE")) >= "2025-03-01")
        .filter(F.to_date(F.col("TIMESTAMP_KAFKA")) >= "2025-03-01")
        .filter(F.col("VEHICLE_ID").isNotNull())
        .filter(
            (F.col("LIFESIGN") >= -32768) & (F.col("LIFESIGN") <= 65535)
            | (F.col("LIFESIGN").isNull())
        )
        .filter(
            (F.col("VEHICLE_GPS_Y") <= 48) & (F.col("VEHICLE_GPS_Y") >= 45.6)
            | (F.col("VEHICLE_GPS_Y").isNull())
        )
        .filter(
            (F.col("VEHICLE_GPS_X") <= 10.7) & (F.col("VEHICLE_GPS_X") >= 5.7)
            | (F.col("VEHICLE_GPS_X").isNull())
        )
        .filter(
            (F.col("VEHICLE_GPS_Z") <= 1500) & (F.col("VEHICLE_GPS_Z") >= 0)
            | (F.col("VEHICLE_GPS_Z").isNull())
        )
        .filter(F.col("VEHICLE_GPS_SPEED") >= 0)
        .filter(F.col("VEHICLE_GPS_SPEED") <= 100)
        .filter(F.col("VEHICLE_SPEED") >= -100)
        .filter(F.col("VEHICLE_SPEED") <= 100)
        .filter(F.col("VEHICLE_OUTSIDE_TEMP") >= -40)
        .filter(F.col("VEHICLE_OUTSIDE_TEMP") <= 60)
        # .filter((F.col("CHARGER_POWER") >= 0) & (F.col("CHARGER_POWER") <= 25) | (F.col("CHARGER_POWER").isNull()))
        .filter(F.col("POWER_1_TRACTION") >= 0)
        .filter(F.col("POWER_1_TRACTION") <= 150)
        .filter(F.col("POWER_COMPRESSOR") >= 0)
        .filter(F.col("POWER_COMPRESSOR") <= 8)
        .filter(F.col("POWER_4") >= 0)
        .filter(F.col("POWER_4") <= 30)
        .filter(F.col("BATTERY_SOC") >= 0)
        .filter(F.col("BATTERY_SOC") <= 100)
        .filter(F.col("BATTERY_SOH") >= 0)
        .filter(F.col("BATTERY_SOH") <= 100)
        .filter(F.col("BATTERY_COOLING_TEMP") >= 0)
        .filter(F.col("BATTERY_COOLING_TEMP") <= 45)
        .filter(F.col("BATTERY_1_TEMP") >= -20)
        .filter(F.col("BATTERY_1_TEMP") <= 45)
        .filter(F.col("BATTERY_1_VOLTAGE") >= 540)
        .filter(F.col("BATTERY_1_VOLTAGE") <= 756)
        .filter(F.col("BATTERY_1_CURRENT") >= -200)
        .filter(F.col("BATTERY_1_CURRENT") <= 200)
        .filter(F.col("BATTERY_2_TEMP") >= -30)
        .filter(F.col("BATTERY_2_TEMP") <= 60)
        .filter(F.col("BATTERY_2_VOLTAGE") >= 540)
        .filter(F.col("BATTERY_2_VOLTAGE") <= 756)
        .filter(F.col("BATTERY_2_CURRENT") >= -200)
        .filter(F.col("BATTERY_2_CURRENT") <= 200)
        .filter(F.col("BATTERY_3_TEMP") >= -20)
        .filter(F.col("BATTERY_3_TEMP") <= 45)
        .filter(F.col("BATTERY_3_VOLTAGE") >= 540)
        .filter(F.col("BATTERY_3_VOLTAGE") <= 756)
        .filter(F.col("BATTERY_3_CURRENT") >= -200)
        .filter(F.col("BATTERY_3_CURRENT") <= 200)
        .with_column(
            "TIMESTAMP_TRUNC",
            F.from_unixtime(
                F.round(F.unix_timestamp(F.col("TIMESTAMP_VEHICLE")) / 60) * 60
            ).cast("TIMESTAMP"),
        )
        .with_column(
            "DATE",
            F.date_trunc("DAY", "TIMESTAMP_VEHICLE").cast("DATE"),
        )
        .with_column("ERROR_SIZE", F.size(F.col("ERRORS")))
    )
    return sdf_clean


if __name__ == "__main__":
    preprocess_data()
