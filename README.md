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
start_date: "2022-01-01"
end_date: "2026-06-01"
interval: "month"       # day | month | Ndays (e.g. 7days)
base_currency: "USD"
initial_cash:
  USD: 10000

screening:
  mktcap_min: 200000000000
  exchange: "nyse,nasdaq"
  country: "us"
  beta_max: 1.5

summary:
  total_return: true
  cagr: true
  max_drawdown: true
  volatility: true
  sharpe_ratio: true
  total_trades: true
  buy_trades: false
  sell_trades: false
  win_rate: true
  profit_factor: true
```

## Writing a Strategy

Create a Python file with a `run(ctx)` function:

```python
def run(ctx):
  ctx.display_config()  # print config at start

  while ctx.advance():
    screened = ctx.openbb_screen_stocks()
    transactions = ctx.openbb_rebalance(screened)
    ctx.execute_transactions(transactions)
    ctx.display_wallet()
    ctx.display_portfolio()
    ctx.openbb_display_balance()
    ctx.openbb_calculate_stats()  # accumulate balance history

  # sell everything at end
  ctx.execute_transactions(ctx.openbb_rebalance([]))
  ctx.display_portfolio()
  ctx.openbb_display_balance()
  ctx.openbb_calculate_stats()

  ctx.display_summary()  # print performance metrics
```

## Strategies

| File | Data | Use |
|------|------|-----|
| `tests/mock_strategy.py` | Deterministic mock data | Testing — fast, no API calls |
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
- **Stats accumulation** — `ctx.openbb_calculate_stats()` called each period tracks balance history
  and avg cost basis; `ctx.display_summary()` uses this to compute total return, CAGR, max drawdown,
  Sharpe, volatility, win rate, and profit factor
- **Configurable summary** — `summary:` section in YAML toggles which metrics are printed
