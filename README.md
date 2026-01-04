# 📊 Financial Data Scraper

A full-stack web application and Excel add-in for extracting financial metrics from Yahoo Finance (yfinance) for any company. Built with Python Flask backend, Node.js frontend, and designed as a Microsoft Office task pane add-in.

---

## 🎯 Features

- **Extract Any Financial Metric** - Access data from Income Statement, Balance Sheet, and Cash Flow statements
- **Multi-Year Historical Data** - Fetch 1-10 years of financial history for any ticker
- **User-Friendly Interface** - Organized metric selection by financial statement category
- **Export Options** - Download results as CSV or copy as JSON
- **Excel Integration** - Designed to work as an Excel Online task pane add-in (with HTTPS deployment)
- **Indian Company Support** - Works with NSE/BSE tickers (TCS, RELIANCE, HDFCBANK, etc.)

---

## 📋 Supported Metrics

### Income Statement
- Total Revenue, Operating Revenue, Cost Of Revenue
- Gross Profit, Operating Income, EBITDA
- Net Income, Diluted EPS

### Balance Sheet
- Total Assets, Current Assets, Total Non Current Assets
- Cash And Cash Equivalents, Accounts Receivable
- Total Debt, Stockholders Equity, Net PPE, Goodwill

### Cash Flow
- Operating Cash Flow, Free Cash Flow
- Investing Cash Flow, Financing Cash Flow
- Capital Expenditure, Depreciation And Amortization

---

## 🏗️ Project Structure

```
financial-data-scraper/
├── pythonbackend/           # Flask API backend
│   ├── app.py              # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── financial_scraper.py # Data fetching logic
│
├── frontend/                # Node.js web application
│   ├── server.js           # Express server
│   ├── taskpane.html       # UI (also used for Excel add-in)
│   ├── package.json        # Node dependencies
│   └── manifest.xml        # Excel add-in manifest
│
└── README.md              # This file
```

---

## 🚀 Quick Start

### Option 1: Local Development (Recommended for Testing)

#### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

#### Backend Setup (Flask)
```bash
cd pythonbackend
pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5000`

#### Frontend Setup (Node)
```bash
cd frontend
npm install
npm start
```
Frontend runs on `http://localhost:3000`

Visit **http://localhost:3000** in your browser to use the app.

---

### Option 2: Deploy to Production (Render.com)

#### Backend Deployment
1. Push `pythonbackend/` folder to GitHub
2. Create a new **Web Service** on Render.com
3. Set:
   - **Build Command:** `cd pythonbackend && pip install -r requirements.txt`
   - **Start Command:** `cd pythonbackend && python app.py`
4. Deploy → Get URL (e.g., `https://financial-scraper-api.onrender.com`)

#### Frontend Deployment
1. Update `frontend/server.js` to point to your deployed backend:
   ```javascript
   const response = await fetch('https://financial-scraper-api.onrender.com/fetch_financials', {
   ```
2. Push `frontend/` folder to GitHub
3. Create another **Web Service** on Render.com for the frontend
4. Set:
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
5. Deploy → Get URL (e.g., `https://financial-excel-ui.onrender.com`)

#### Excel Add-in Integration
1. Update `manifest.xml` with your frontend URL:
   ```xml
   <SourceLocation DefaultValue="https://financial-excel-ui.onrender.com/taskpane.html"/>
   ```
2. Open Excel Online
3. Go to **Insert → Get Add-ins → Upload My Add-in**
4. Upload the updated `manifest.xml`
5. The add-in will load as an Excel task pane

---

## 📖 Usage

### Web Version
1. Enter a company ticker (e.g., AAPL, TCS, RELIANCE)
2. Specify number of years (1-50)
3. Select desired financial metrics
4. Click "Fetch Data"
5. Export results as CSV or JSON

### Excel Add-in Version (Production)
1. Open Excel Online
2. Click the add-in in the task pane
3. Enter ticker and select metrics
4. Click "Fetch Data"
5. Results appear in the task pane alongside your spreadsheet

---

## 🔧 API Endpoints

### POST `/fetch_financials`
Fetches financial data from yfinance.

**Request Body:**
```json
{
  "ticker": "TCS",
  "metrics": ["Total Revenue", "Net Income", "Operating Cash Flow"],
  "years": 5
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "TCS",
  "data": [
    {
      "year": 2024,
      "Total Revenue": 2500000000,
      "Net Income": 400000000,
      "Operating Cash Flow": 450000000
    }
  ]
}
```

---

## 📦 Dependencies

### Backend (Python)
- Flask 2.3.0
- Flask-CORS 4.0.0
- yfinance 0.2.28
- pandas 2.0.0

### Frontend (Node.js)
- Express 4.x
- Axios (for HTTP requests)

---

## 🔐 Security Considerations

- **CORS Enabled** - Backend accepts requests from any origin (suitable for development)
- **Input Validation** - Ticker symbols and years are validated
- **No Authentication** - Currently public; add auth for production
- **API Rate Limiting** - Consider implementing for production use

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure Flask is installed
pip install -r requirements.txt
# Check if port 5000 is in use
# Change port in app.py if needed
```

### Frontend can't connect to backend
```bash
# Update the API URL in server.js
# For local: http://localhost:5000
# For production: https://your-backend-url.onrender.com
```

### Excel add-in not loading
- Ensure manifest.xml has valid HTTPS URL
- Check browser console for errors
- Try uploading manifest again in Excel Online

### No data returned
- Verify ticker symbol is correct (try AAPL or RELIANCE)
- Check if yfinance has data for that ticker
- Try reducing year range (some tickers have limited history)

---

## 🚀 Future Enhancements

- Real-time stock prices
- Financial ratio calculations
- Comparative analysis (multiple companies)
- Data visualization charts
- Authentication & user accounts
- Advanced filtering & sorting
- Mobile app version

---

## 📄 License

MIT License - Feel free to use this project for educational and commercial purposes.

---

## 👨‍💻 Author

Built as an educational project for financial data analysis and Excel automation.

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the API response for error messages
3. Verify all dependencies are installed correctly
4. Check GitHub Issues if deploying from a repo

---

## 🎓 Learning Resources

- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Excel Add-ins API](https://docs.microsoft.com/en-us/office/dev/add-ins/excel/excel-add-ins-overview)
- [Render Deployment Guide](https://render.com/docs)
