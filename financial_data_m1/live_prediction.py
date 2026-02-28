import yfinance as yf
import pandas as pd
import joblib
import numpy as np

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
    
