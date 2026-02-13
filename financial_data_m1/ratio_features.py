import pandas as pd
import numpy as np

INPUT_FILE = "/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Cleaned_Data.csv"
OUTPUT_FILE = "/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Ratio_Data.csv"

print("Starting to add Ratios...")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"loaded {len(df)} companies.")
except:
    print("File not found")
    exit()

print("Calculating Ratios...")

if 'Total Debt' in df.columns and 'Stockholders Equity' in df.columns:
    df['Debt_to_Equity'] = df['Total Debt']/df['Interest Expense'].replace(0, np.nan)
    df['Debt_to_Equity'] = df['Debt_to_Equity'].fillna(0)

if 'EBIT' in df.columns and 'Interest Expense' in df.columns:
    df['Interest_Coverage'] = df['EBIT']/df['Interest Expense'].replace(0, np.nan)
    df['Interest_Coverage'] = df['Interest_Coverage'].fillna(0)

if 'Current Assets' in df.columns and 'Current Liabilities' in df.columns:
    df['Current_Ratio'] = df['Current Assets']/df['Current Liabilities'].replace(0, np.nan)
    df['Current_Ratio'] = df['Current_Ratio'].fillna(0)

if 'Net Income' in df.columns and 'Total Revenue' in df.columns:
    df['Net_Profit_Margin'] = df['Net Income']/df['Total Revenue'].replace(0, np.nan)
    df['Net_Profit_Margin'] = df['Net_Profit_Margin'].fillna(0)

df.replace([np.inf, -np.inf], 0, inplace=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"New file created")