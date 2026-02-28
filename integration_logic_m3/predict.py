import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "financial_data_m1", "Dashboard_Data.csv")


FEATURES = [
    "Debt_to_Equity",
    "Interest_Coverage",
    "Current_Ratio",
    "Net_Profit_Margin"
]

def load_model():
    return joblib.load(MODEL_PATH)

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    return df

def get_latest_row(df, ticker):
    sub = df[df["Ticker"] == ticker]
    if sub.empty:
        return None
    return sub.sort_values("Date", ascending=False).iloc[0]

def predict_financial_risk(ticker: str):
    model = load_model()
    df = load_data()

    row = get_latest_row(df, ticker)
    if row is None:
        return {
            "found": False,
            "message": f"Ticker {ticker} not found in dataset."
        }

    X = row[FEATURES].values.reshape(1, -1)
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][1])

    return {
        "found": True,
        "ticker": ticker,
        "company_name": row["Company_Names"],
        "prediction": pred,
        "risk_probability": prob,
        "date_used": str(row["Date"].date())
    }

if __name__ == "__main__":
    print(predict_financial_risk("ADANIENT.NS"))
