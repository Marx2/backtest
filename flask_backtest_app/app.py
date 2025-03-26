from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import yaml
import os
from dotenv import load_dotenv
import openbb_integration
import logging

# Load environment variables from .env file in parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('flask_backtest_app/data/logs/openbb_errors.log'),
        logging.StreamHandler()
    ]
)

def load_strategies():
    try:
        with open('backtest-app/public/strategies.yaml') as f:
            strategies = yaml.safe_load(f)
        return [strategy.replace('-', '').strip() for strategy in strategies]
    except Exception as e:
        print(f"Error loading strategies: {e}")
        return ['Moving Average', 'Mean Reversion', 'Breakout']

@app.route('/', methods=['GET'])
def index():
    strategies = load_strategies()
    return render_template('index.html', strategies=strategies)


@app.route('/backtest', methods=['POST'])
def run_backtest():
    tickers = request.form.get('tickers')
    strategy = request.form.get('strategy')
    year = request.form.get('year')
    
    try:
        # Get price data for backtesting
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        prices = openbb_integration.get_prices_in_range(tickers, start_date, end_date)
        
        # Simple moving average strategy example
        if strategy == "Moving Average":
            prices['SMA_50'] = prices['close'].rolling(50).mean()
            prices['Signal'] = (prices['close'] > prices['SMA_50']).astype(int)
            prices['Position'] = prices['Signal'].diff()
            
            transactions = []
            for idx, row in prices[prices['Position'] != 0].iterrows():
                transactions.append({
                    'date': idx.strftime('%Y-%m-%d'),
                    'ticker': tickers,
                    'quantity': 10 * row['Position'],
                    'price': row['close']
                })
            
            profit = sum(t['quantity'] * t['price'] for t in transactions if t['quantity'] < 0)
        else:
            transactions = []
            profit = 0.0
            
    except Exception as e:
        print(f"Backtest error: {str(e)}")
        transactions = []
        profit = 0.0
    
    strategies = load_strategies()
    return render_template('index.html',
                         strategies=strategies,
                         transactions=transactions,
                         profit=profit)


@app.route("/stock/data/<symbol>", methods=['GET'])
def get_stock_data(symbol):
    logging.info(f"get_stock_data called for symbol: {symbol}")
    print(f"get_stock_data called for symbol: {symbol}")
    try:
        data = openbb_integration.get_stock_data(symbol)
        print(f"Data from openbb_integration: {data}")
        if data:
            logging.info(f"Data from openbb_integration: {data}")
        else:
            logging.warning(f"No data received from openbb_integration for symbol: {symbol}")
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching stock data for {symbol}: {e}")
        return jsonify({'error': str(e)})

@app.route("/stock/details", methods=['GET'])
def get_stock_details():
    symbol = request.args.get('symbol')
    if symbol:
        return redirect(url_for('get_stock_symbol', symbol=symbol))
    else:
        logging.info("get_stock_details called without a symbol")
        return render_template('stock_details.html', symbol=None, message="Please enter a stock symbol to view details.")


@app.route("/stock/details/<symbol>")
def get_stock_symbol(symbol):
    logging.info(f"get_stock_symbol called for symbol: {symbol}")
    try:
        return render_template('stock_details.html', symbol=symbol)
    except Exception as e:
        logging.error(f"Error rendering stock_details.html: {e}")
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)