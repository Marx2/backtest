from flask import Flask, render_template, request, jsonify
import yaml
import os

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

@app.route('/backtest', methods=['POST'])
def run_backtest():
    tickers = request.form.get('tickers')
    strategy = request.form.get('strategy')
    year = request.form.get('year')
    
    # Placeholder for backtesting logic
    print(f"Running backtest with: {tickers}, {strategy}, {year}")
    
    # Sample results
    transactions = [
        {'date': '2024-01-31', 'ticker': tickers, 'quantity': 10, 'price': 150.00},
        {'date': '2024-02-29', 'ticker': tickers, 'quantity': -10, 'price': 160.00, 'profit': 100.00}
    ]
    profit = 100.00
    
    strategies = load_strategies()
    return render_template('index.html',
                         strategies=strategies,
                         transactions=transactions,
                         profit=profit)

if __name__ == '__main__':
    app.run(debug=True)