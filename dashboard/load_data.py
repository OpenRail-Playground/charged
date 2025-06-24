import pandas as pd


def load_data():
    return pd.DataFrame(pd.read_parquet("data/clean_data.parquet"))
