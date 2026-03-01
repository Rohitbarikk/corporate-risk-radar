import yfinance as yf
import pandas as pd
import joblib
import numpy as np
import os

Model_Path ="/Users/hardikbhagtani/corporate-risk-radar/models/risk_model.pkl"

def find_ticker(company_name):
    print(f"Searching for {company_name}...")
    try:
        search_results = yf.Search(company_name, news_count=0).quotes

        indian_stocks = [
            r for r in search_results
            if 'symbol' in r and (r['symbol'].endswith('.NS') or r['symbol'].endswith('.BO'))
        ]

        if indian_stocks:
            best_match = indian_stocks[0]
            name = best_match.get('shortName', best_match.get('longName', company_name))
            symbol = best_match['symbol']

            print(f"Found: {name} ({symbol})")
            return symbol
        else:
            print("No Indian stock found. Try adding 'Ltd' or 'India' to the name.")
            return None
    except Exception as e:
        print(f"Search Error: {e}")
        return None
    
def get_financials(ticker_symbol):
    print(f"Fetching financial data for: {ticker_symbol}...")
    stock = yf.Ticker(ticker_symbol)

    try:
        balance_sheet = stock.balance_sheet
        financials = stock.financials

        if balance_sheet.empty or financials.empty:
            print("Error: Could not retrieve financial data from Yahoo Finance.")
            return None
        def get_value(df, row_name, default =0):
            if row_name in df.index:
                return df.loc[row_name].iloc[0]
            return default
        
        total_debt = get_value(balance_sheet, 'Total Debt')
        equity = get_value(balance_sheet, 'Stockholders Equity', default=1)
        curr_assets = get_value(balance_sheet, 'Current Assets')
        curr_liab = get_value(balance_sheet, 'Current Liabilities', default=1)

        ebit = get_value(financials, 'EBIT')
        interest = get_value(financials, 'Interest Expense', default=1)
        net_income = get_value(financials, 'Net Incocme')
        revenue = get_value(financials, 'Total Revenue', default=1)

        data = {
            'Debt_to_Equity' : total_debt/equity,
            'Interest_Coverage' : ebit/interest,
            'Current_Ratio' : curr_assets/curr_liab,
            'Net_Profit_Margin' : net_income/revenue
        }

        print(f"Debt/Equity: {data['Debt_to_Equity']:.2f}")
        print(f"Interest Coverage: {data['Interest_Coverage']:.2f}")
        print(f"Profit Margin: {data['Net_Profit_Margin']:.2%}")

        return pd.DataFrame([data])
    except Exception as e:
        print(f"Data Extraction Error: {e}")
        return None
    
def predict_risk(company_name):
    if not os.path.exists(Model_Path):
        print(f"Error: Model not found at {Model_Path}")
        return
    
    model = joblib.load(Model_Path)

    ticker = find_ticker(company_name)
    if not ticker:
        return
    
    features = get_financials(ticker)
    if features is None:
        return
    
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    print("\n" + "="*40)
    print(f"Final verdict for: {ticker}")
    print("="*40)

    if prediction == 1:
        print(f"RISK LEVEL: HIGH (Risk Score: {probability:.1%})")
        print("WARNING: This company shows signs of financial stress.")
        print("(High Debt, Low Profits, or Poor Coverage)")
    else:
        print(f"RISK LEVEL: SAFE (Safety Score: {1-probability:.1%})")
        print("STATUS: This company looks financially healthy.")
        print("(Strong Profits, Manageable Debt)")
    
    print("="*40 + "\n")

    if __name__ == "__main__":
        while True:
            user_input = input("Enter Company Name (or 'q' to quit): ").strip()
            if user_input.lower() == 'q':
                break
            predict_risk(user_input)