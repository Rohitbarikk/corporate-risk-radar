import pandas as pd
import yfinance as yf
import time

INPUT_FILE = '/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Labeled_Data.csv'
OUTPUT_FILE = '/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Dashboard_Data.csv'

print("Starting Name Retrieval...")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} companies")
except FileNotFoundError:
    print("Error: Required file not found!")
    exit()

if 'Ticker' not in df.columns:
    if 'Symbol' in df.columns:
        df.rename(columns = {'Symbol':'Ticker'}, inplace=True)
    elif 'Unnamed : 0' in df.columns:
        df.rename(columns = {'Unnamed:0' : 'Ticker'}, inplace=True)
    else:
        print("Error: your file does not contaiN a ticker column!")
        exit()

company_names =[]
tickers = df['Ticker'].tolist()
total = len(tickers)

print(f"Fetching full names for {total} companies from yahoo finance...")

for i, ticker in enumerate(tickers):
    try:
        stock = yf.Ticker(ticker)
        long_name = stock.info.get('longName', ticker)
        short_name = stock.info.get('shortName', ticker)
        company_names.append(short_name)

        if i%10 == 0:
            print(f" {i}/{total} - {ticker} -> {short_name}")
    except Exception as e:
        print(f" {ticker} could not fetch name using ticker")
        company_names.append(ticker)

df['Company_Names'] = company_names

cols = df.columns.tolist()
cols.insert(1, cols.pop(cols.index('Company_Names')))
df = df[cols]

df.to_csv(OUTPUT_FILE, index = False)
print("Company Names Added!!")

