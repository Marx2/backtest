# Backtest Engine — Design Spec

## Overview

Python backtest application. Executes trading strategies over historical periods using mock data
providers. Three-phase algorithm (init → loop → finish) driven by strategy files. Configuration via
YAML.

CLI: `python main.py -config=config/backtest.yaml -strategy=strategies/basic.py`

## Architecture

**Approach: Procedural.** Functions match draft actions. State in dataclasses. Mock modules
swappable via same interface.

## Data Model

All in `core/models.py`. `Decimal` for financial precision.

```python
@dataclass
class Currency:
  code: str  # "USD", "EUR", "PLN"


@dataclass
class Ticker:
  symbol: str  # "AAPL", "MSFT"
  currency: Currency  # denominated currency


@dataclass
class Wallet:
  holdings: dict[Currency, Decimal]  # currency → amount


@dataclass
class Portfolio:
  positions: dict[Ticker, Decimal]  # ticker → quantity


@dataclass
class Transaction:
  date: date
  action: str  # "buy" | "sell"
  ticker: Ticker
  quantity: Decimal
  price: Decimal


@dataclass
class BacktestConfig:
  start_date: date
  end_date: date
  interval: str  # "day" | "month" | "{N}days"
  base_currency: str  # for display_balance conversion
  initial_cash: dict[str, Decimal]  # currency_code → amount
  screening: dict  # screening parameters
```

## Configuration

YAML config file passed via `-config` CLI arg. Strategy passed via `-strategy` CLI arg.

```yaml
start_date: "2025-01-01"
end_date: "2025-12-31"
interval: "month"
base_currency: "USD"
initial_cash:
  USD: 10000

screening:
  min_score: 0.5
```

## Strategy Interface

Strategy = Python file with `run(ctx: BacktestContext)` function. Controls full backtest flow. All
parameters pre-loaded from config into context.

```python
# strategies/basic.py

def run(ctx: BacktestContext):
  # loop
  while ctx.advance():
    screened = ctx.screen_stocks()
    transactions = ctx.rebalance(screened)
    ctx.execute_transactions(transactions)
    ctx.display_wallet()
    ctx.display_portfolio()
    ctx.display_balance()

  # finish
  transactions = ctx.rebalance([])
  ctx.execute_transactions(transactions)
  ctx.display_portfolio()
  ctx.display_balance()
```

## BacktestContext

Central object in `core/context.py`. Holds state, delegates to action files.

**State:**

- `wallet: Wallet`
- `portfolio: Portfolio`
- `all_transactions: list[Transaction]`
- `processing_date: date | None`
- `config: BacktestConfig`

**Action methods** (each delegates to corresponding file in `actions/`):

- `advance() -> bool` — increment date by interval, return False if past end
- `screen_stocks() -> list[str]` — calls mock_screener with config screening params
- `rebalance(target_tickers: list[str]) -> list[Transaction]` — diff-based equal-weight
- `execute_transactions(transactions: list[Transaction])` — updates wallet + portfolio
- `display_wallet()` — prints wallet state
- `display_portfolio()` — prints portfolio positions
- `display_balance()` — prints total value in base_currency

**Construction in main.py:**

1. Parse CLI args (config path, strategy path)
2. Load YAML → BacktestConfig
3. Build BacktestContext(config) — wallet initialized from config.initial_cash
4. Import strategy, call strategy.run(ctx)

No provider wiring in main. Context imports action modules directly.

## Actions

Each action = separate file in `actions/`. Mocks live alongside with `mock_` prefix.

### advance.py

- If `processing_date` is None → set to `start_date`, return True
- Else increment by interval
- If past `end_date` → return False
- Return True

### screen_stocks.py

- Delegates to `mock_screener.screen_stocks(date, params)`
- Returns list of ticker symbols

### rebalance.py

Diff-based equal-weight rebalancing:

1. Calculate total portfolio value in base_currency (cash + positions via prices + FX)
2. Target per ticker = total value / len(target_tickers) (0 if empty list)
3. Convert target value → target quantity per ticker using current price
4. Diff against current positions:
    - Ticker in portfolio but not in target → sell all
    - Ticker in target but not in portfolio → buy target quantity
    - Ticker in both → buy/sell difference
5. Return list of Transaction objects

Empty target list → all positions sold naturally via step 4.

### execute_transactions.py

- Processes list of transactions: updates wallet (cash in/out) and portfolio (quantity changes)
- Appends transactions to all_transactions
- Uses price already set in Transaction objects (set by rebalance)

### display_wallet.py

- Prints each currency and amount in wallet

### display_portfolio.py

- Prints each ticker and quantity in portfolio

### display_balance.py

- Calculates total value: sum of wallet cash + portfolio positions value
- Converts everything to base_currency using mock_fx_rates
- Prints total

## Mock Data Providers

All in `actions/` with `mock_` prefix. Seeded random walks for reproducibility.

### mock_prices.py

```python
def get_price(ticker: str, date: date) -> Decimal
```

Generates random price series per ticker. Deterministic seed.

### mock_fx_rates.py

```python
def get_fx_rate(from_currency: str, to_currency: str, date: date) -> Decimal
```

Generates random FX rates between currency pairs. Deterministic seed.

### mock_screener.py

```python
def screen_stocks(date: date, params: dict) -> list[str]
```

Hardcoded universe of tickers internally. Returns filtered subset based on params and date.
Deterministic seed.

## Interval & Date Handling

Supported intervals:

- `"day"` — advance 1 day
- `"month"` — advance 1 calendar month (end-of-month clamping: Jan 31 + 1 month = Feb 28)
- `"{N}days"` — advance N days (e.g. `"7days"`, `"14days"`)

Uses `datetime` + `dateutil.relativedelta` for month math.

## File Structure

```
backtest/
  main.py
  requirements.txt
  .env
  config/
    backtest.yaml
  strategies/
    basic.py
  actions/
    __init__.py
    advance.py
    screen_stocks.py
    rebalance.py
    execute_transactions.py
    display_wallet.py
    display_portfolio.py
    display_balance.py
    mock_prices.py
    mock_fx_rates.py
    mock_screener.py
  core/
    __init__.py
    context.py
    models.py
  tests/
    ...
  docs/
    draft.txt
```

## Constraints

- No transaction costs (fees, slippage)
- No partial fills — perfect execution at current mock price
- Console output only
- Python standard library + dateutil + PyYAML
- Decimal for all financial values
