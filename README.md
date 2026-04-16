# pfire-backtest

Python backtesting engine for trading strategies. Runs strategies over historical periods using mock
data providers, with multi-currency support and diff-based rebalancing.

## Usage

```bash
python main.py -config=config/backtest.yaml -strategy=strategies/basic.py
```

## Configuration

Edit `config/backtest.yaml`:

```yaml
start_date: "2025-01-01"
end_date: "2025-12-31"
interval: "month"       # day | month | Ndays (e.g. 7days)
base_currency: "USD"
initial_cash:
  USD: 10000

screening:
  min_score: 0.5
```

## Writing a Strategy

Create a Python file with a `run(ctx)` function:

```python
def run(ctx):
  while ctx.advance():
    screened = ctx.screen_stocks()
    transactions = ctx.rebalance(screened)
    ctx.execute_transactions(transactions)
    ctx.display_wallet()
    ctx.display_portfolio()
    ctx.display_balance()

  # sell everything at end
  ctx.execute_transactions(ctx.rebalance([]))
  ctx.display_portfolio()
  ctx.display_balance()
```

## Project Structure

```
actions/        # one file per action + mock data providers
core/           # BacktestContext, data models
strategies/     # strategy files
config/         # YAML configs
tests/          # unit + integration tests
```

## Setup

```bash
pip install -r requirements.txt
```

## Tests

```bash
pytest tests/
```

## Architecture

- **Procedural** — each action is a standalone function in `actions/`
- **Mock providers** — `mock_prices.py`, `mock_fx_rates.py`, `mock_screener.py` generate
  deterministic random data; swap for real providers with the same interface
- **Diff-based rebalancing** — equal-weight allocation, minimal trades
- **Multi-currency** — FX conversion via mock rates for balance display
