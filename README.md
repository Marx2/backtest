# pfire-backtest

Python backtesting engine for trading strategies. Runs strategies over historical periods with
multi-currency support and diff-based rebalancing. Includes mock providers for fast testing and
real OpenBB providers (yfinance/FMP) for live data.

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

## Strategies

| File | Data | Use |
|------|------|-----|
| `strategies/mock.py` | Deterministic mock data | Testing — fast, no API calls |
| `strategies/basic.py` | Live OpenBB data (yfinance/FMP) | Real backtests |

## Project Structure

```
actions/        # one file per action; mock + OpenBB data providers
core/           # BacktestContext, data models
strategies/     # strategy files
config/         # YAML configs
tests/          # unit + integration tests
```

## Setup

```bash
pip install -r requirements.txt

# Optional: add API credentials for FMP provider
cp .env.example .env
```

## Tests

```bash
pytest tests/
```

## Architecture

- **Procedural** — each action is a standalone function in `actions/`
- **Dual providers** — mock providers (`mock_prices.py`, `mock_fx_rates.py`, `mock_screener.py`)
  for deterministic tests; OpenBB providers (`openbb_prices.py`, `openbb_fx_rates.py`,
  `openbb_screener.py`) for live data via yfinance (free) or FMP (paid). Same interface — swap by
  changing the import.
- **Diff-based rebalancing** — equal-weight allocation, minimal trades
- **Multi-currency** — FX conversion for balance display
