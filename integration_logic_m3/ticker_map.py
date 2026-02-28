import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "financial_data_m1", "Dashboard_Data.csv")

def build_mapping():
    df = pd.read_csv(DATA_PATH)

    mapping = {}

    for _, row in df.iterrows():
        name = str(row["Company_Names"]).strip().lower()
        ticker = str(row["Ticker"]).strip()
        mapping[name] = ticker

    return mapping

COMPANY_TO_TICKER = build_mapping()

def name_to_ticker(name: str):
    return COMPANY_TO_TICKER.get(name.strip().lower())
    