import pandas as pd
import yfinance as yf
import time

tickers = [
    # BANKS & FINANCE (Crucial for risk modeling)
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS",
    "INDUSINDBK.NS", "BANKBARODA.NS", "PNB.NS", "IDFcashFlowIRSTB.NS", "RBLBANK.NS",
    "BANDHANBNK.NS", "FEDERALBNK.NS", "AUBANK.NS", "YESBANK.NS", "UJJIVANSFB.NS",
    "CHOLAFIN.NS", "BAJFINANCE.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "L&TFH.NS",

    # IT & TECH
    "TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS",
    "PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS", "HAPPSTMNDS.NS",
    "ZENSARTECH.NS", "CYIENT.NS", "MASTEK.NS", "balanceSheetOFT.NS",

    # PHARMA & HEALTH
    "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "BIOCON.NS",
    "AUROPHARMA.NS", "LUPIN.NS", "GLENMARK.NS", "GRANULES.NS", "LAURUSLAbalanceSheet.NS",
    "APOLLOHOSP.NS", "METROPOLIS.NS", "LALPATHLAB.NS",

    # AUTO & ANCILLARY
    "MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS",
    "HEROMOTOCO.NS", "TVSMOTOR.NS", "ASHOKLEY.NS", "MOTHERSON.NS", "BOSCHLTD.NS",
    "MRF.NS", "APOLLOTYRE.NS", "EXIDEIND.NS",

    # METALS, MINING & ENERGY
    "TATASTEEL.NS", "JSL.NS", "HINDALCO.NS", "VEDL.NS", "JSWSTEEL.NS",
    "SAIL.NS", "NMDC.NS", "COALINDIA.NS", "HINDZincome.NS", "NATIONALUM.NS",
    "ONGC.NS", "OIL.NS", "IOC.NS", "BPCL.NS", "GAIL.NS",

    # INFRA, POWER & REALTY (High Debt Sectors)
    "LT.NS", "ADANIENT.NS", "ADANIPORTS.NS", "ADANIGREEN.NS", "ADANIPOWER.NS",
    "TATAPOWER.NS", "NTPC.NS", "POWERGRID.NS", "GMRINFRA.NS", "IRB.NS",
    "SUZLON.NS", "JPPOWER.NS", "RTNPOWER.NS", "RPOWER.NS", "RELIANCE.NS",
    "DLF.NS", "LODHA.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PRESTIGE.NS",

    # CONSUMER, TELECOM & MEDIA
    "HINDUNILVR.NS", "ITC.NS", "TITAN.NS", "ASIANPAINT.NS", "PIDILITIND.NS",
    "BHARTIARTL.NS", "IDEA.NS", "SUNTV.NS", "ZEEL.NS", "PVRINOX.NS",
    "NAUKRI.NS", "ZOMATO.NS", "PAYTM.NS", "NYKAA.NS", "POLICYBZR.NS"
]
OUTPUT_FILE = "Financial_Dataset.csv"
allData = []

print(f"Starting Mass Download for {len(tickers)} companies...")
print("-------------------------------------------------------")

for i, ticker in enumerate(tickers):
    print(f"[{i+1}/{len(tickers)}] Fetching {ticker}...", end=" ")

    try:
        stock = yf.Ticker(ticker)
        balanceSheet = stock.balance_sheet.T
        income = stock.financials.T
        cashFlow = stock.cashflow.T

        if balanceSheet.empty or income.empty:
            print("No Data (Skipping Company)")
            continue

        combined = balanceSheet.join(income, lsuffix='_balanceSheet', rsuffix='_income').join(cashFlow, lsuffix='_income', rsuffix='_cashFlow')
        combined.reset_index(inplace=True)
        combined.rename(columns={'index': 'Date'}, inplace =True)
        combined['Ticker'] = ticker
        allData.append(combined)
        print("Done")
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

if allData:
    df = pd.concat(allData, ignore_index=True)
    df.to_csv(OUTPUT_FILE, index = False)
    print("-------------------------------------------------------")
    print(f"SUCCESS! Downloaded {len(df)} rows of data.")
    print(f"Saved to: {OUTPUT_FILE}")
else:
    print("Failed. No data downloaded.")
