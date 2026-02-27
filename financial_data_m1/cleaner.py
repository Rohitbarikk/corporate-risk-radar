import pandas as pd

INPUT_FILE = "Financial_Dataset.csv"
OUTPUT_FILE = "Cleaned_Data.csv"

print("Starting the Cleaning Process...")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows of raw data")
except FileNotFoundError:
    print("Error: Could not find your file. Make sure it's in the same folder!")
    exit()

fillZero = [
    'Total Debt',
    'Long Term Debt',
    'Total Revenue',
    'Inventory',
    'Cash and Cash Equivalents'
]

for col in fillZero:
    if col in df.columns:
        df[col] = df[col].fillna(0)
        print(f"Fixed empty cells in '{col}'")

if 'Net Income' in df.columns:
    before = len(df)
    df = df.dropna(subset=['Net Income'])
    after = len(df)
    print(f"dropped {before - after} rows because they had no Net Income")

if 'Date' in df.columns and 'Ticker' in df.columns:
    df.sort_values(by = ['Ticker', 'Date'], ascending=[True,True], inplace=True)
    print("dwg sorted data by ticker and date")

df.to_csv(OUTPUT_FILE, index=False)
print("------------------------------------------------")
print(f"SUCCESS! Clean data saved to: {OUTPUT_FILE}")
print(f"Total Rows Ready for AI: {len(df)}")