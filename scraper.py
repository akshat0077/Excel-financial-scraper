import yfinance as yf
import json

class FinancialScraper:
    def __init__(self):
        pass

    def fetch_financials(self, ticker, metrics, years):
        """
        Fetch financial data using yfinance
        """
        try:
            # Auto-add .NS for Indian companies if not already present
            if not ticker.endswith('.NS') and not ticker.endswith('.BO'):
                ticker = f"{ticker}.NS"

            # Fetch the company data
            company = yf.Ticker(ticker)
            
            # Get income statement (most reliable)
            income_stmt = company.income_stmt
            balance_sht = company.balance_sheet
            cash_flw = company.cashflow

            if income_stmt is None or income_stmt.empty:
                return {'success': False, 'data': None, 'error': f'No data found for ticker {ticker}'}

            # Parse and filter data
            data = []
            
            # Income statement has columns as dates, so we iterate through them
            for date_col in income_stmt.columns:
                year = date_col.year
                year_data = {'year': year}
                
                for metric in metrics:
                    # Map our metric names to yfinance column names
                    yf_metric_map = {
                        # --- Income Statement ---
                        'Total Revenue': 'Total Revenue',
                        'Operating Revenue': 'Operating Revenue',
                        'Cost Of Revenue': 'Cost Of Revenue',
                        'Gross Profit': 'Gross Profit',
                        'Operating Income': 'Operating Income',
                        'EBITDA': 'EBITDA',
                        'Net Income': 'Net Income',
                        'Diluted EPS': 'Diluted EPS',

                        # --- Balance Sheet ---
                        'Total Assets': 'Total Assets',
                        'Current Assets': 'Current Assets',
                        'Total Non Current Assets': 'Total Non Current Assets',
                        'Cash And Cash Equivalents': 'Cash And Cash Equivalents',
                        'Accounts Receivable': 'Accounts Receivable',
                        'Total Debt': 'Total Debt',
                        'Stockholders Equity': 'Stockholders Equity',
                        'Net PPE': 'Net PPE',
                        'Goodwill': 'Goodwill',

                        # --- Cash Flow ---
                        'Operating Cash Flow': 'Operating Cash Flow',
                        'Free Cash Flow': 'Free Cash Flow',
                        'Investing Cash Flow': 'Investing Cash Flow',
                        'Financing Cash Flow': 'Financing Cash Flow',
                        'Capital Expenditure': 'Capital Expenditure',
                        'Depreciation And Amortization': 'Depreciation And Amortization'
                    }
                    
                    yf_name = yf_metric_map.get(metric)
                    
                    # Try to find the metric
                    if yf_name and yf_name in income_stmt.index:
                        value = income_stmt.loc[yf_name, date_col]

                    elif yf_name and yf_name in balance_sht.index:
                        value = balance_sht.loc[yf_name, date_col] 

                    elif yf_name and yf_name in cash_flw.index:
                        value = cash_flw.loc[yf_name, date_col]
                    
                    
                        
                    
                    # Convert to Python type
                    if value is not None and hasattr(value, 'item'):
                        value = value.item()
                    
                    # Check for NaN
                    if value is not None and not (hasattr(value, '__float__') and (value != value)):  # NaN check
                        year_data[metric] = value
                    else:
                        year_data[metric] = None
                
                data.append(year_data)

            # Sort by year and limit to requested years
            data = sorted(data, key=lambda x: x['year'])[-years:]
            
            return {'success': True, 'data': data, 'error': None}

        except Exception as e:
            return {'success': False, 'data': None, 'error': str(e)}


# Test standalone
if __name__ == '__main__':
    scraper = FinancialScraper()
    result = scraper.fetch_financials('TCS', ['revenue', 'ebitda', 'netIncome'], 5)
    print(json.dumps(result, indent=2, default=str))
