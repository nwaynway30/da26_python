import pandas as pd


def load_data() -> pd.DataFrame:
    return pd.DataFrame([{"name": "A", "age": 10}, {"name": "B", "age": 11}])
