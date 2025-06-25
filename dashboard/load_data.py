import pandas as pd


def load_data(start_date=None, end_date=None):
    if start_date and end_date:
        filters = [
            ("TIMESTAMP_VEHICLE", ">=", pd.Timestamp(start_date).tz_localize("America/Los_Angeles")),
            ("TIMESTAMP_VEHICLE", "<=", pd.Timestamp(end_date).tz_localize("America/Los_Angeles")),
        ]
    else:
        filters = None
    df = pd.read_parquet("data/clean_data_minute.parquet", filters=filters, engine="pyarrow")
    return df
