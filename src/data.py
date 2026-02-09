import pandas as pd
from .config import DATA_DIR


def load_bim_dataset():
    path = DATA_DIR / 'bim_ai_civil_engineering_dataset.csv'
    return pd.read_csv(path)
