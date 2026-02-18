import pandas as pd
import numpy as np
import os

INPUT_FILE = "/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Ratio_Data.csv"
OUTPUT_FILE = "/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Labeled_Data.csv"

print("Starting to Label Data...")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} companies")
except FileNotFoundError:
    print(f"Error: could not find {INPUT_FILE}.")
    exit()

high_debt = df['Debt_to_Equity'] >6.0 
bad_coverage = (df['Interest_Coverage']<1.0) & (df['Debt_to_Equity']>1.5)
burning_cash = df['Net_Profit_Margin'] <-0.20

df['Target'] = 0
df.loc[high_debt | bad_coverage | burning_cash, 'Target'] = 1

risk_count = df['Target'].sum()
Total_count = len(df)
print("Analysis Complete")
print(f"Risky Companies Idetnified : {risk_count}")
print(f"Safe Companies Identified : {Total_count - risk_count}")

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved Labeled Data")