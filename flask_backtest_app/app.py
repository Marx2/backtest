from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import yaml
import os
from dotenv import load_dotenv
import openbb_integration
import logging

# Load environment variables from .env file in parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)

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

@app.route('/stock/details', methods=['GET'])
def show_stock_details():
    return render_template('stock_details.html')

@app.route('/stock/details', methods=['POST'])
def stock_details():
    data = request.get_json()
    ticker = data.get('ticker')
    logging.info(f"Request received for ticker: {ticker}")
    try:
        # Get prices for last 7 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        logging.info(f"Getting prices for {ticker} from {start_date} to {end_date}")
        prices = openbb_integration.get_prices_in_range(ticker, start_date, end_date)
        
        # Format response
        price_history = []
        for date, row in prices.iterrows():
            if isinstance(date, str):
                date_str = date
            else:
                date_str = date.strftime('%Y-%m-%d')
            price_history.append({
                'date': date_str,
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            })
            
        return jsonify({
            'success': True,
            'ticker': ticker,
            'current_price': prices.iloc[-1]['close'],
            'price_history': price_history,
        })
        print(f"Current price: {prices.iloc[-1]['close']}")
    except Exception as e:
        print(f"Error getting price: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

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

if __name__ == '__main__':
    app.run(debug=True)