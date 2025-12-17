import yfinance as yf

ticker = "TCS.NS"
company = yf.Ticker(ticker)

print("=" * 50)
print("INCOME STATEMENT COLUMNS:")
print(company.income_stmt.index.tolist() if company.income_stmt is not None else "None")

print("\n" + "=" * 50)
print("BALANCE SHEET COLUMNS:")
print(company.balance_sheet.index.tolist() if company.balance_sheet is not None else "None")

print("\n" + "=" * 50)
print("CASH FLOW COLUMNS:")
print(company.cashflow.index.tolist() if company.cashflow is not None else "None")

print("\n" + "=" * 50)
print("SAMPLE DATA (First few rows of Income Statement):")
if company.income_stmt is not None:
    print(company.income_stmt.head())
else:
    print("No Income Statement data available.")    