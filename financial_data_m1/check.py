import yfinance as yf

safeStock = yf.Ticker("TCS.NS")

print(safeStock.balance_sheet.head())

risky_stock = yf.Ticker("IDEA.NS")
print(risky_stock.balance_sheet.head())