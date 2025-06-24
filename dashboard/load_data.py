import pandas as pd

def load_data():
    """
    Load data from the database and return it as a dictionary.
    """
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})