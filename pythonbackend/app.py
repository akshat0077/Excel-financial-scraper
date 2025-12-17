from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from scraper import FinancialScraper

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

scraper = FinancialScraper()

@app.route('/')
def index():
    return send_from_directory('.', 'scraper.html')

@app.route('/fetch_financials', methods=['POST'])
def fetch_financials():
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()
        metrics = data.get('metrics', [])
        years = int(data.get('years', 5))

        if not ticker or not metrics or years < 1:
            return jsonify({
                'success': False,
                'error': 'Invalid inputs: ticker, metrics, and years are required'
            }), 400

        result = scraper.fetch_financials(ticker, metrics, years)

        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 400

        return jsonify({
            'success': True,
            'ticker': ticker,
            'metrics': metrics,
            'data': result['data'],
            'error': None
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
