# Backtest Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python backtest engine that executes trading strategies over historical periods using mock data, with diff-based equal-weight rebalancing and multi-currency support.

**Architecture:** Procedural approach — `main.py` loads YAML config, builds `BacktestContext`, imports strategy file, calls `strategy.run(ctx)`. Context holds state (wallet, portfolio, transactions) and delegates action methods to separate files in `actions/`. Mock data providers (prices, FX rates, screener) live alongside actions with `mock_` prefix.

**Tech Stack:** Python 3.12+, PyYAML, python-dateutil, pytest

---

## File Structure

```
backtest/
  main.py                         # CLI entry point: parse args, load config, run strategy
  requirements.txt                # dependencies
  config/
    backtest.yaml                 # default YAML config
  core/
    __init__.py
    models.py                     # dataclasses: Currency, Ticker, Wallet, Portfolio, Transaction, BacktestConfig
    context.py                    # BacktestContext: state + action method delegation
  actions/
    __init__.py
    advance.py                    # advance(ctx) -> bool
    screen_stocks.py              # screen_stocks(ctx) -> list[str]
    rebalance.py                  # rebalance(ctx, tickers) -> list[Transaction]
    execute_transactions.py       # execute_transactions(ctx, transactions)
    display_wallet.py             # display_wallet(ctx)
    display_portfolio.py          # display_portfolio(ctx)
    display_balance.py            # display_balance(ctx)
    mock_prices.py                # get_price(ticker, date) -> Decimal
    mock_fx_rates.py              # get_fx_rate(from, to, date) -> Decimal
    mock_screener.py              # screen_stocks(date, params) -> list[str]
  strategies/
    basic.py                      # basic equal-weight strategy
  tests/
    __init__.py
    test_models.py
    test_advance.py
    test_mock_prices.py
    test_mock_fx_rates.py
    test_mock_screener.py
    test_rebalance.py
    test_execute_transactions.py
    test_display_wallet.py
    test_display_portfolio.py
    test_display_balance.py
    test_screen_stocks.py
    test_context.py
    test_main.py
    test_integration.py
```

---

### Task 1: Project Setup & Data Models

**Files:**
- Create: `requirements.txt`
- Create: `core/__init__.py`
- Create: `core/models.py`
- Create: `tests/__init__.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Create requirements.txt**

```
PyYAML>=6.0
python-dateutil>=2.9
pytest>=8.0
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -r requirements.txt`

- [ ] **Step 3: Write failing tests for data models**

Create `tests/__init__.py` (empty) and `core/__init__.py` (empty).

Create `tests/test_models.py`:

```python
from datetime import date
from decimal import Decimal

from core.models import (
    BacktestConfig,
    Currency,
    Portfolio,
    Ticker,
    Transaction,
    Wallet,
)


def test_currency_creation():
    usd = Currency(code="USD")
    assert usd.code == "USD"


def test_ticker_creation():
    usd = Currency(code="USD")
    aapl = Ticker(symbol="AAPL", currency=usd)
    assert aapl.symbol == "AAPL"
    assert aapl.currency == usd


def test_wallet_creation():
    usd = Currency(code="USD")
    wallet = Wallet(holdings={usd: Decimal("10000")})
    assert wallet.holdings[usd] == Decimal("10000")


def test_wallet_multiple_currencies():
    usd = Currency(code="USD")
    eur = Currency(code="EUR")
    wallet = Wallet(holdings={usd: Decimal("10000"), eur: Decimal("5000")})
    assert len(wallet.holdings) == 2


def test_portfolio_creation():
    usd = Currency(code="USD")
    aapl = Ticker(symbol="AAPL", currency=usd)
    portfolio = Portfolio(positions={aapl: Decimal("10")})
    assert portfolio.positions[aapl] == Decimal("10")


def test_portfolio_empty():
    portfolio = Portfolio(positions={})
    assert len(portfolio.positions) == 0


def test_transaction_creation():
    usd = Currency(code="USD")
    aapl = Ticker(symbol="AAPL", currency=usd)
    tx = Transaction(
        date=date(2025, 1, 15),
        action="buy",
        ticker=aapl,
        quantity=Decimal("10"),
        price=Decimal("150.00"),
    )
    assert tx.action == "buy"
    assert tx.quantity == Decimal("10")
    assert tx.price == Decimal("150.00")


def test_backtest_config_creation():
    config = BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )
    assert config.interval == "month"
    assert config.base_currency == "USD"
    assert config.initial_cash["USD"] == Decimal("10000")
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.models'`

- [ ] **Step 5: Implement data models**

Create `core/models.py`:

```python
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Currency:
    code: str


@dataclass(frozen=True)
class Ticker:
    symbol: str
    currency: Currency


@dataclass
class Wallet:
    holdings: dict[Currency, Decimal] = field(default_factory=dict)


@dataclass
class Portfolio:
    positions: dict[Ticker, Decimal] = field(default_factory=dict)


@dataclass
class Transaction:
    date: date
    action: str
    ticker: Ticker
    quantity: Decimal
    price: Decimal


@dataclass
class BacktestConfig:
    start_date: date
    end_date: date
    interval: str
    base_currency: str
    initial_cash: dict[str, Decimal]
    screening: dict
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_models.py -v`
Expected: All 8 tests PASS

- [ ] **Step 7: Commit**

```bash
git add requirements.txt core/ tests/
git commit -m "feat: add project setup and data models"
```

---

### Task 2: Mock Prices Provider

**Files:**
- Create: `actions/__init__.py`
- Create: `actions/mock_prices.py`
- Create: `tests/test_mock_prices.py`

- [ ] **Step 1: Write failing tests for mock prices**

Create `actions/__init__.py` (empty).

Create `tests/test_mock_prices.py`:

```python
from datetime import date
from decimal import Decimal

from actions.mock_prices import get_price


def test_get_price_returns_decimal():
    price = get_price("AAPL", date(2025, 1, 15))
    assert isinstance(price, Decimal)


def test_get_price_positive():
    price = get_price("AAPL", date(2025, 1, 15))
    assert price > 0


def test_get_price_deterministic():
    price1 = get_price("AAPL", date(2025, 1, 15))
    price2 = get_price("AAPL", date(2025, 1, 15))
    assert price1 == price2


def test_get_price_different_tickers_different_prices():
    price_aapl = get_price("AAPL", date(2025, 1, 15))
    price_msft = get_price("MSFT", date(2025, 1, 15))
    assert price_aapl != price_msft


def test_get_price_different_dates_different_prices():
    price1 = get_price("AAPL", date(2025, 1, 15))
    price2 = get_price("AAPL", date(2025, 2, 15))
    assert price1 != price2


def test_get_price_reasonable_range():
    """Prices should be in a reasonable stock price range."""
    price = get_price("AAPL", date(2025, 6, 15))
    assert Decimal("1") < price < Decimal("10000")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_mock_prices.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'actions.mock_prices'`

- [ ] **Step 3: Implement mock prices**

Create `actions/mock_prices.py`:

```python
import hashlib
from datetime import date
from decimal import Decimal


def get_price(ticker: str, d: date) -> Decimal:
    """Generate a deterministic mock price using seeded random walk.

    Uses hash of ticker to set a base price, then hash of ticker+date
    for daily variation. Simulates random walk by chaining day-over-day.
    """
    base = _ticker_base_price(ticker)
    variation = _date_variation(ticker, d)
    price = base * (Decimal("1") + variation)
    return price.quantize(Decimal("0.01"))


def _ticker_base_price(ticker: str) -> Decimal:
    """Deterministic base price from ticker symbol. Range: 20-500."""
    h = int(hashlib.sha256(ticker.encode()).hexdigest(), 16)
    normalized = (h % 48000 + 2000) / 100
    return Decimal(str(normalized))


def _date_variation(ticker: str, d: date) -> Decimal:
    """Deterministic daily variation from ticker+date. Range: -0.20 to +0.20."""
    seed = f"{ticker}:{d.isoformat()}"
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    variation = ((h % 4000) - 2000) / 10000
    return Decimal(str(variation))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_mock_prices.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/ tests/test_mock_prices.py
git commit -m "feat: add mock prices provider"
```

---

### Task 3: Mock FX Rates Provider

**Files:**
- Create: `actions/mock_fx_rates.py`
- Create: `tests/test_mock_fx_rates.py`

- [ ] **Step 1: Write failing tests for mock FX rates**

Create `tests/test_mock_fx_rates.py`:

```python
from datetime import date
from decimal import Decimal

from actions.mock_fx_rates import get_fx_rate


def test_get_fx_rate_returns_decimal():
    rate = get_fx_rate("EUR", "USD", date(2025, 1, 15))
    assert isinstance(rate, Decimal)


def test_get_fx_rate_positive():
    rate = get_fx_rate("EUR", "USD", date(2025, 1, 15))
    assert rate > 0


def test_get_fx_rate_deterministic():
    rate1 = get_fx_rate("EUR", "USD", date(2025, 1, 15))
    rate2 = get_fx_rate("EUR", "USD", date(2025, 1, 15))
    assert rate1 == rate2


def test_get_fx_rate_same_currency_is_one():
    rate = get_fx_rate("USD", "USD", date(2025, 1, 15))
    assert rate == Decimal("1")


def test_get_fx_rate_different_dates_different_rates():
    rate1 = get_fx_rate("EUR", "USD", date(2025, 1, 15))
    rate2 = get_fx_rate("EUR", "USD", date(2025, 2, 15))
    assert rate1 != rate2


def test_get_fx_rate_reasonable_range():
    """FX rates should be in reasonable range."""
    rate = get_fx_rate("EUR", "USD", date(2025, 6, 15))
    assert Decimal("0.1") < rate < Decimal("10")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_mock_fx_rates.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement mock FX rates**

Create `actions/mock_fx_rates.py`:

```python
import hashlib
from datetime import date
from decimal import Decimal


def get_fx_rate(from_currency: str, to_currency: str, d: date) -> Decimal:
    """Generate a deterministic mock FX rate.

    Same currency returns 1. Otherwise uses hash-based deterministic rate.
    """
    if from_currency == to_currency:
        return Decimal("1")

    base = _pair_base_rate(from_currency, to_currency)
    variation = _date_variation(from_currency, to_currency, d)
    rate = base * (Decimal("1") + variation)
    return rate.quantize(Decimal("0.0001"))


def _pair_base_rate(from_currency: str, to_currency: str) -> Decimal:
    """Deterministic base rate for currency pair. Range: 0.5-2.0."""
    pair = f"{from_currency}/{to_currency}"
    h = int(hashlib.sha256(pair.encode()).hexdigest(), 16)
    normalized = (h % 1500 + 500) / 1000
    return Decimal(str(normalized))


def _date_variation(from_currency: str, to_currency: str, d: date) -> Decimal:
    """Deterministic daily variation. Range: -0.05 to +0.05."""
    seed = f"{from_currency}/{to_currency}:{d.isoformat()}"
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    variation = ((h % 1000) - 500) / 10000
    return Decimal(str(variation))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_mock_fx_rates.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/mock_fx_rates.py tests/test_mock_fx_rates.py
git commit -m "feat: add mock FX rates provider"
```

---

### Task 4: Mock Screener Provider

**Files:**
- Create: `actions/mock_screener.py`
- Create: `tests/test_mock_screener.py`

- [ ] **Step 1: Write failing tests for mock screener**

Create `tests/test_mock_screener.py`:

```python
from datetime import date

from actions.mock_screener import screen_stocks


def test_screen_stocks_returns_list():
    result = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    assert isinstance(result, list)


def test_screen_stocks_returns_strings():
    result = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    for ticker in result:
        assert isinstance(ticker, str)


def test_screen_stocks_deterministic():
    result1 = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    result2 = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    assert result1 == result2


def test_screen_stocks_subset_of_universe():
    result = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    assert len(result) > 0
    # All returned tickers should be from the hardcoded universe
    from actions.mock_screener import UNIVERSE

    for ticker in result:
        assert ticker in UNIVERSE


def test_screen_stocks_different_dates_can_differ():
    results = set()
    for month in range(1, 13):
        result = tuple(screen_stocks(date(2025, month, 15), {"min_score": 0.5}))
        results.add(result)
    # Over 12 months, we should get at least 2 different screened sets
    assert len(results) >= 2


def test_screen_stocks_higher_min_score_fewer_results():
    low = screen_stocks(date(2025, 1, 15), {"min_score": 0.2})
    high = screen_stocks(date(2025, 1, 15), {"min_score": 0.8})
    assert len(low) >= len(high)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_mock_screener.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement mock screener**

Create `actions/mock_screener.py`:

```python
import hashlib
from datetime import date

UNIVERSE = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "JPM", "V", "WMT"]


def screen_stocks(d: date, params: dict) -> list[str]:
    """Screen stocks from hardcoded universe based on date and params.

    Each ticker gets a deterministic score based on ticker+date hash.
    Tickers with score >= min_score pass the screen.
    """
    min_score = params.get("min_score", 0.5)
    result = []
    for ticker in UNIVERSE:
        score = _ticker_score(ticker, d)
        if score >= min_score:
            result.append(ticker)
    return result


def _ticker_score(ticker: str, d: date) -> float:
    """Deterministic score for ticker on given date. Range: 0.0-1.0."""
    seed = f"{ticker}:{d.isoformat()}"
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    return (h % 1000) / 1000
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_mock_screener.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/mock_screener.py tests/test_mock_screener.py
git commit -m "feat: add mock screener provider"
```

---

### Task 5: Advance Action

**Files:**
- Create: `actions/advance.py`
- Create: `tests/test_advance.py`

- [ ] **Step 1: Write failing tests for advance**

Create `tests/test_advance.py`:

```python
from datetime import date
from decimal import Decimal

from actions.advance import advance
from core.models import BacktestConfig


def _make_config(start="2025-01-01", end="2025-12-31", interval="month"):
    return BacktestConfig(
        start_date=date.fromisoformat(start),
        end_date=date.fromisoformat(end),
        interval=interval,
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


class FakeContext:
    def __init__(self, config, processing_date=None):
        self.config = config
        self.processing_date = processing_date


def test_advance_first_call_sets_start_date():
    ctx = FakeContext(_make_config(), processing_date=None)
    result = advance(ctx)
    assert result is True
    assert ctx.processing_date == date(2025, 1, 1)


def test_advance_month_interval():
    ctx = FakeContext(_make_config(), processing_date=date(2025, 1, 1))
    result = advance(ctx)
    assert result is True
    assert ctx.processing_date == date(2025, 2, 1)


def test_advance_day_interval():
    ctx = FakeContext(_make_config(interval="day"), processing_date=date(2025, 1, 1))
    result = advance(ctx)
    assert result is True
    assert ctx.processing_date == date(2025, 1, 2)


def test_advance_ndays_interval():
    ctx = FakeContext(_make_config(interval="7days"), processing_date=date(2025, 1, 1))
    result = advance(ctx)
    assert result is True
    assert ctx.processing_date == date(2025, 1, 8)


def test_advance_past_end_returns_false():
    ctx = FakeContext(
        _make_config(end="2025-01-31"),
        processing_date=date(2025, 1, 15),
    )
    result = advance(ctx)
    assert result is False


def test_advance_month_end_clamping():
    """Jan 31 + 1 month = Feb 28."""
    ctx = FakeContext(
        _make_config(start="2025-01-31", end="2025-12-31"),
        processing_date=date(2025, 1, 31),
    )
    result = advance(ctx)
    assert result is True
    assert ctx.processing_date == date(2025, 2, 28)


def test_advance_exact_end_date_returns_false():
    """If next date would be past end, return False without advancing."""
    ctx = FakeContext(
        _make_config(end="2025-01-31"),
        processing_date=date(2025, 1, 1),
    )
    result = advance(ctx)
    assert result is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_advance.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement advance action**

Create `actions/advance.py`:

```python
import re
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


def advance(ctx) -> bool:
    """Advance processing_date by interval. Return False if past end boundary."""
    if ctx.processing_date is None:
        ctx.processing_date = ctx.config.start_date
        return True

    next_date = _next_date(ctx.processing_date, ctx.config.interval)
    if next_date > ctx.config.end_date:
        return False

    ctx.processing_date = next_date
    return True


def _next_date(current: date, interval: str) -> date:
    """Calculate next date based on interval string."""
    if interval == "day":
        return current + timedelta(days=1)
    elif interval == "month":
        return current + relativedelta(months=1)
    else:
        match = re.match(r"^(\d+)days$", interval)
        if match:
            n = int(match.group(1))
            return current + timedelta(days=n)
        raise ValueError(f"Unknown interval: {interval}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_advance.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/advance.py tests/test_advance.py
git commit -m "feat: add advance date action"
```

---

### Task 6: Display Actions (Wallet, Portfolio, Balance)

**Files:**
- Create: `actions/display_wallet.py`
- Create: `actions/display_portfolio.py`
- Create: `actions/display_balance.py`
- Create: `tests/test_display_wallet.py`
- Create: `tests/test_display_portfolio.py`
- Create: `tests/test_display_balance.py`

- [ ] **Step 1: Write failing tests for display_wallet**

Create `tests/test_display_wallet.py`:

```python
from datetime import date
from decimal import Decimal

from actions.display_wallet import display_wallet
from core.models import BacktestConfig, Currency, Wallet


class FakeContext:
    def __init__(self, wallet):
        self.wallet = wallet
        self.processing_date = date(2025, 3, 1)


def test_display_wallet_single_currency(capsys):
    usd = Currency(code="USD")
    wallet = Wallet(holdings={usd: Decimal("10000.50")})
    ctx = FakeContext(wallet)
    display_wallet(ctx)
    output = capsys.readouterr().out
    assert "USD" in output
    assert "10000.50" in output


def test_display_wallet_multiple_currencies(capsys):
    usd = Currency(code="USD")
    eur = Currency(code="EUR")
    wallet = Wallet(holdings={usd: Decimal("10000"), eur: Decimal("5000")})
    ctx = FakeContext(wallet)
    display_wallet(ctx)
    output = capsys.readouterr().out
    assert "USD" in output
    assert "EUR" in output


def test_display_wallet_empty(capsys):
    wallet = Wallet(holdings={})
    ctx = FakeContext(wallet)
    display_wallet(ctx)
    output = capsys.readouterr().out
    assert output  # should still print something
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_display_wallet.py -v`
Expected: FAIL

- [ ] **Step 3: Implement display_wallet**

Create `actions/display_wallet.py`:

```python
def display_wallet(ctx) -> None:
    """Print wallet contents."""
    print(f"\n=== Wallet ({ctx.processing_date}) ===")
    if not ctx.wallet.holdings:
        print("  (empty)")
        return
    for currency, amount in ctx.wallet.holdings.items():
        print(f"  {currency.code}: {amount}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_display_wallet.py -v`
Expected: All 3 tests PASS

- [ ] **Step 5: Write failing tests for display_portfolio**

Create `tests/test_display_portfolio.py`:

```python
from datetime import date
from decimal import Decimal

from actions.display_portfolio import display_portfolio
from core.models import Currency, Portfolio, Ticker


class FakeContext:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.processing_date = date(2025, 3, 1)


def test_display_portfolio_with_positions(capsys):
    usd = Currency(code="USD")
    aapl = Ticker(symbol="AAPL", currency=usd)
    portfolio = Portfolio(positions={aapl: Decimal("10")})
    ctx = FakeContext(portfolio)
    display_portfolio(ctx)
    output = capsys.readouterr().out
    assert "AAPL" in output
    assert "10" in output


def test_display_portfolio_empty(capsys):
    portfolio = Portfolio(positions={})
    ctx = FakeContext(portfolio)
    display_portfolio(ctx)
    output = capsys.readouterr().out
    assert "empty" in output.lower() or "Portfolio" in output
```

- [ ] **Step 6: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_display_portfolio.py -v`
Expected: FAIL

- [ ] **Step 7: Implement display_portfolio**

Create `actions/display_portfolio.py`:

```python
def display_portfolio(ctx) -> None:
    """Print portfolio positions."""
    print(f"\n=== Portfolio ({ctx.processing_date}) ===")
    if not ctx.portfolio.positions:
        print("  (empty)")
        return
    for ticker, quantity in ctx.portfolio.positions.items():
        print(f"  {ticker.symbol}: {quantity}")
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_display_portfolio.py -v`
Expected: All 2 tests PASS

- [ ] **Step 9: Write failing tests for display_balance**

Create `tests/test_display_balance.py`:

```python
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from actions.display_balance import display_balance
from core.models import BacktestConfig, Currency, Portfolio, Ticker, Wallet


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


class FakeContext:
    def __init__(self, wallet, portfolio):
        self.wallet = wallet
        self.portfolio = portfolio
        self.config = _make_config()
        self.processing_date = date(2025, 3, 1)


def test_display_balance_cash_only(capsys):
    usd = Currency(code="USD")
    wallet = Wallet(holdings={usd: Decimal("10000")})
    portfolio = Portfolio(positions={})
    ctx = FakeContext(wallet, portfolio)

    with patch("actions.display_balance.get_fx_rate", return_value=Decimal("1")):
        display_balance(ctx)

    output = capsys.readouterr().out
    assert "10000" in output


def test_display_balance_with_positions(capsys):
    usd = Currency(code="USD")
    wallet = Wallet(holdings={usd: Decimal("5000")})
    aapl = Ticker(symbol="AAPL", currency=usd)
    portfolio = Portfolio(positions={aapl: Decimal("10")})
    ctx = FakeContext(wallet, portfolio)

    with (
        patch("actions.display_balance.get_price", return_value=Decimal("150")),
        patch("actions.display_balance.get_fx_rate", return_value=Decimal("1")),
    ):
        display_balance(ctx)

    output = capsys.readouterr().out
    # 5000 cash + 10 * 150 = 6500
    assert "6500" in output


def test_display_balance_multi_currency(capsys):
    usd = Currency(code="USD")
    eur = Currency(code="EUR")
    wallet = Wallet(holdings={usd: Decimal("5000"), eur: Decimal("3000")})
    portfolio = Portfolio(positions={})
    ctx = FakeContext(wallet, portfolio)

    def mock_fx(from_cur, to_cur, d):
        if from_cur == "EUR" and to_cur == "USD":
            return Decimal("1.10")
        return Decimal("1")

    with patch("actions.display_balance.get_fx_rate", side_effect=mock_fx):
        display_balance(ctx)

    output = capsys.readouterr().out
    # 5000 + 3000 * 1.10 = 8300
    assert "8300" in output
```

- [ ] **Step 10: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_display_balance.py -v`
Expected: FAIL

- [ ] **Step 11: Implement display_balance**

Create `actions/display_balance.py`:

```python
from decimal import Decimal

from actions.mock_fx_rates import get_fx_rate
from actions.mock_prices import get_price


def display_balance(ctx) -> None:
    """Calculate and print total portfolio value in base currency."""
    base = ctx.config.base_currency
    total = Decimal("0")

    # Sum cash holdings converted to base currency
    for currency, amount in ctx.wallet.holdings.items():
        rate = get_fx_rate(currency.code, base, ctx.processing_date)
        total += amount * rate

    # Sum position values converted to base currency
    for ticker, quantity in ctx.portfolio.positions.items():
        price = get_price(ticker.symbol, ctx.processing_date)
        value = quantity * price
        rate = get_fx_rate(ticker.currency.code, base, ctx.processing_date)
        total += value * rate

    total = total.quantize(Decimal("0.01"))
    print(f"\n=== Balance ({ctx.processing_date}) ===")
    print(f"  Total ({base}): {total}")
```

- [ ] **Step 12: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_display_balance.py -v`
Expected: All 3 tests PASS

- [ ] **Step 13: Commit**

```bash
git add actions/display_wallet.py actions/display_portfolio.py actions/display_balance.py tests/test_display_wallet.py tests/test_display_portfolio.py tests/test_display_balance.py
git commit -m "feat: add display actions (wallet, portfolio, balance)"
```

---

### Task 7: Screen Stocks Action

**Files:**
- Create: `actions/screen_stocks.py`
- Create: `tests/test_screen_stocks.py`

- [ ] **Step 1: Write failing tests for screen_stocks action**

Create `tests/test_screen_stocks.py`:

```python
from datetime import date
from decimal import Decimal

from actions.screen_stocks import screen_stocks
from core.models import BacktestConfig


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


class FakeContext:
    def __init__(self):
        self.config = _make_config()
        self.processing_date = date(2025, 3, 1)


def test_screen_stocks_returns_list():
    ctx = FakeContext()
    result = screen_stocks(ctx)
    assert isinstance(result, list)


def test_screen_stocks_uses_config_params():
    ctx = FakeContext()
    result = screen_stocks(ctx)
    # Should return tickers (strings)
    for ticker in result:
        assert isinstance(ticker, str)


def test_screen_stocks_deterministic():
    ctx = FakeContext()
    result1 = screen_stocks(ctx)
    result2 = screen_stocks(ctx)
    assert result1 == result2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_screen_stocks.py -v`
Expected: FAIL

- [ ] **Step 3: Implement screen_stocks action**

Create `actions/screen_stocks.py`:

```python
from actions.mock_screener import screen_stocks as mock_screen


def screen_stocks(ctx) -> list[str]:
    """Screen stocks using config screening params and current date."""
    return mock_screen(ctx.processing_date, ctx.config.screening)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_screen_stocks.py -v`
Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/screen_stocks.py tests/test_screen_stocks.py
git commit -m "feat: add screen_stocks action"
```

---

### Task 8: Rebalance Action

**Files:**
- Create: `actions/rebalance.py`
- Create: `tests/test_rebalance.py`

- [ ] **Step 1: Write failing tests for rebalance**

Create `tests/test_rebalance.py`:

```python
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from actions.rebalance import rebalance
from core.models import (
    BacktestConfig,
    Currency,
    Portfolio,
    Ticker,
    Transaction,
    Wallet,
)

USD = Currency(code="USD")
AAPL = Ticker(symbol="AAPL", currency=USD)
MSFT = Ticker(symbol="MSFT", currency=USD)
GOOG = Ticker(symbol="GOOG", currency=USD)


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


class FakeContext:
    def __init__(self, wallet_holdings=None, positions=None):
        self.config = _make_config()
        self.processing_date = date(2025, 3, 1)
        self.wallet = Wallet(holdings=wallet_holdings or {USD: Decimal("10000")})
        self.portfolio = Portfolio(positions=positions or {})


def _mock_price(ticker, d):
    prices = {"AAPL": Decimal("100"), "MSFT": Decimal("200"), "GOOG": Decimal("150")}
    return prices.get(ticker, Decimal("100"))


def _mock_fx(from_cur, to_cur, d):
    return Decimal("1")


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_from_cash_only(mock_price, mock_fx):
    """From 10000 cash, buy 2 tickers equally."""
    ctx = FakeContext()
    result = rebalance(ctx, ["AAPL", "MSFT"])
    assert len(result) == 2
    assert all(isinstance(tx, Transaction) for tx in result)
    buys = [tx for tx in result if tx.action == "buy"]
    assert len(buys) == 2


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_equal_weight(mock_price, mock_fx):
    """Each ticker gets equal share of total value."""
    ctx = FakeContext()
    result = rebalance(ctx, ["AAPL", "MSFT"])
    # Total 10000, each gets 5000
    # AAPL at 100 -> 50 shares, MSFT at 200 -> 25 shares
    aapl_tx = next(tx for tx in result if tx.ticker.symbol == "AAPL")
    msft_tx = next(tx for tx in result if tx.ticker.symbol == "MSFT")
    assert aapl_tx.quantity == Decimal("50")
    assert msft_tx.quantity == Decimal("25")


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_sell_removed_ticker(mock_price, mock_fx):
    """Ticker no longer in target → sell all."""
    ctx = FakeContext(positions={AAPL: Decimal("50"), MSFT: Decimal("25")})
    # Only keep AAPL, remove MSFT
    # Total value: 50*100 + 25*200 = 10000, all to AAPL
    result = rebalance(ctx, ["AAPL"])
    sells = [tx for tx in result if tx.action == "sell"]
    assert any(tx.ticker.symbol == "MSFT" for tx in sells)


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_empty_list_sells_all(mock_price, mock_fx):
    """Empty target list → sell all positions."""
    ctx = FakeContext(positions={AAPL: Decimal("50"), MSFT: Decimal("25")})
    result = rebalance(ctx, [])
    assert len(result) == 2
    assert all(tx.action == "sell" for tx in result)


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_diff_minimal_trades(mock_price, mock_fx):
    """Already holding correct amount → no transaction for that ticker."""
    # Total value: 50*100 + 0 cash = 5000, target AAPL only -> 5000/100 = 50
    ctx = FakeContext(
        wallet_holdings={USD: Decimal("0")},
        positions={AAPL: Decimal("50")},
    )
    result = rebalance(ctx, ["AAPL"])
    # Already holding exact target, no trades needed
    assert len(result) == 0


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_returns_transactions_with_prices(mock_price, mock_fx):
    """Each transaction has correct price set."""
    ctx = FakeContext()
    result = rebalance(ctx, ["AAPL"])
    assert result[0].price == Decimal("100")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_rebalance.py -v`
Expected: FAIL

- [ ] **Step 3: Implement rebalance action**

Create `actions/rebalance.py`:

```python
from decimal import Decimal

from actions.mock_fx_rates import get_fx_rate
from actions.mock_prices import get_price
from core.models import Currency, Portfolio, Ticker, Transaction


def rebalance(ctx, target_tickers: list[str]) -> list[Transaction]:
    """Diff-based equal-weight rebalancing.

    Computes total portfolio value, divides equally among target tickers,
    and generates minimal buy/sell transactions.
    """
    base = ctx.config.base_currency
    d = ctx.processing_date
    transactions = []

    # Calculate total portfolio value in base currency
    total_value = Decimal("0")
    for currency, amount in ctx.wallet.holdings.items():
        rate = get_fx_rate(currency.code, base, d)
        total_value += amount * rate
    for ticker, quantity in ctx.portfolio.positions.items():
        price = get_price(ticker.symbol, d)
        rate = get_fx_rate(ticker.currency.code, base, d)
        total_value += quantity * price * rate

    # Calculate target quantities
    target_quantities: dict[str, Decimal] = {}
    if target_tickers:
        value_per_ticker = total_value / len(target_tickers)
        for symbol in target_tickers:
            price = get_price(symbol, d)
            # Convert base currency value to ticker's price
            target_qty = (value_per_ticker / price).quantize(Decimal("1"))
            target_quantities[symbol] = target_qty

    # Build map of current positions by symbol
    current_by_symbol: dict[str, tuple[Ticker, Decimal]] = {}
    for ticker, quantity in ctx.portfolio.positions.items():
        current_by_symbol[ticker.symbol] = (ticker, quantity)

    # Generate sell transactions for tickers not in target
    for symbol, (ticker, quantity) in current_by_symbol.items():
        if symbol not in target_quantities:
            price = get_price(symbol, d)
            transactions.append(Transaction(
                date=d, action="sell", ticker=ticker,
                quantity=quantity, price=price,
            ))

    # Generate buy/sell transactions for target tickers
    for symbol in target_tickers:
        target_qty = target_quantities[symbol]
        if symbol in current_by_symbol:
            ticker, current_qty = current_by_symbol[symbol]
            diff = target_qty - current_qty
        else:
            # New ticker — need to find/create Ticker object
            # Assume USD currency for mock; real provider would know the currency
            ticker = Ticker(symbol=symbol, currency=Currency(code=base))
            diff = target_qty

        price = get_price(symbol, d)
        if diff > 0:
            transactions.append(Transaction(
                date=d, action="buy", ticker=ticker,
                quantity=diff, price=price,
            ))
        elif diff < 0:
            transactions.append(Transaction(
                date=d, action="sell", ticker=ticker,
                quantity=abs(diff), price=price,
            ))
        # diff == 0 → no transaction needed

    return transactions
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_rebalance.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/rebalance.py tests/test_rebalance.py
git commit -m "feat: add diff-based rebalance action"
```

---

### Task 9: Execute Transactions Action

**Files:**
- Create: `actions/execute_transactions.py`
- Create: `tests/test_execute_transactions.py`

- [ ] **Step 1: Write failing tests for execute_transactions**

Create `tests/test_execute_transactions.py`:

```python
from datetime import date
from decimal import Decimal

from actions.execute_transactions import execute_transactions
from core.models import Currency, Portfolio, Ticker, Transaction, Wallet

USD = Currency(code="USD")
AAPL = Ticker(symbol="AAPL", currency=USD)
MSFT = Ticker(symbol="MSFT", currency=USD)


class FakeContext:
    def __init__(self, wallet_holdings=None, positions=None):
        self.wallet = Wallet(holdings=wallet_holdings or {USD: Decimal("10000")})
        self.portfolio = Portfolio(positions=positions or {})
        self.all_transactions = []


def test_execute_buy_updates_wallet_and_portfolio():
    ctx = FakeContext()
    tx = Transaction(
        date=date(2025, 3, 1), action="buy", ticker=AAPL,
        quantity=Decimal("10"), price=Decimal("100"),
    )
    execute_transactions(ctx, [tx])
    assert ctx.portfolio.positions[AAPL] == Decimal("10")
    assert ctx.wallet.holdings[USD] == Decimal("9000")  # 10000 - 10*100


def test_execute_sell_updates_wallet_and_portfolio():
    ctx = FakeContext(positions={AAPL: Decimal("10")})
    tx = Transaction(
        date=date(2025, 3, 1), action="sell", ticker=AAPL,
        quantity=Decimal("10"), price=Decimal("150"),
    )
    execute_transactions(ctx, [tx])
    assert AAPL not in ctx.portfolio.positions or ctx.portfolio.positions[AAPL] == Decimal("0")
    assert ctx.wallet.holdings[USD] == Decimal("11500")  # 10000 + 10*150


def test_execute_appends_to_all_transactions():
    ctx = FakeContext()
    tx = Transaction(
        date=date(2025, 3, 1), action="buy", ticker=AAPL,
        quantity=Decimal("5"), price=Decimal("100"),
    )
    execute_transactions(ctx, [tx])
    assert len(ctx.all_transactions) == 1
    assert ctx.all_transactions[0] is tx


def test_execute_multiple_transactions():
    ctx = FakeContext(wallet_holdings={USD: Decimal("20000")})
    txs = [
        Transaction(
            date=date(2025, 3, 1), action="buy", ticker=AAPL,
            quantity=Decimal("10"), price=Decimal("100"),
        ),
        Transaction(
            date=date(2025, 3, 1), action="buy", ticker=MSFT,
            quantity=Decimal("5"), price=Decimal("200"),
        ),
    ]
    execute_transactions(ctx, txs)
    assert ctx.portfolio.positions[AAPL] == Decimal("10")
    assert ctx.portfolio.positions[MSFT] == Decimal("5")
    # 20000 - 1000 - 1000 = 18000
    assert ctx.wallet.holdings[USD] == Decimal("18000")
    assert len(ctx.all_transactions) == 2


def test_execute_sell_removes_zero_positions():
    ctx = FakeContext(
        wallet_holdings={USD: Decimal("0")},
        positions={AAPL: Decimal("10")},
    )
    tx = Transaction(
        date=date(2025, 3, 1), action="sell", ticker=AAPL,
        quantity=Decimal("10"), price=Decimal("100"),
    )
    execute_transactions(ctx, [tx])
    assert AAPL not in ctx.portfolio.positions
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_execute_transactions.py -v`
Expected: FAIL

- [ ] **Step 3: Implement execute_transactions**

Create `actions/execute_transactions.py`:

```python
from decimal import Decimal

from core.models import Transaction


def execute_transactions(ctx, transactions: list[Transaction]) -> None:
    """Execute transactions: update wallet and portfolio, record in history."""
    for tx in transactions:
        cash_currency = tx.ticker.currency
        cash_amount = tx.quantity * tx.price

        if tx.action == "buy":
            # Deduct cash
            ctx.wallet.holdings[cash_currency] -= cash_amount
            # Add to portfolio
            current = ctx.portfolio.positions.get(tx.ticker, Decimal("0"))
            ctx.portfolio.positions[tx.ticker] = current + tx.quantity
        elif tx.action == "sell":
            # Add cash
            current_cash = ctx.wallet.holdings.get(cash_currency, Decimal("0"))
            ctx.wallet.holdings[cash_currency] = current_cash + cash_amount
            # Remove from portfolio
            current = ctx.portfolio.positions.get(tx.ticker, Decimal("0"))
            new_qty = current - tx.quantity
            if new_qty <= 0:
                ctx.portfolio.positions.pop(tx.ticker, None)
            else:
                ctx.portfolio.positions[tx.ticker] = new_qty

        ctx.all_transactions.append(tx)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_execute_transactions.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add actions/execute_transactions.py tests/test_execute_transactions.py
git commit -m "feat: add execute_transactions action"
```

---

### Task 10: BacktestContext

**Files:**
- Create: `core/context.py`
- Create: `tests/test_context.py`

- [ ] **Step 1: Write failing tests for BacktestContext**

Create `tests/test_context.py`:

```python
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from core.context import BacktestContext
from core.models import BacktestConfig, Currency


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


def test_context_initializes_wallet_from_config():
    ctx = BacktestContext(_make_config())
    usd = Currency(code="USD")
    assert ctx.wallet.holdings[usd] == Decimal("10000")


def test_context_initializes_empty_portfolio():
    ctx = BacktestContext(_make_config())
    assert len(ctx.portfolio.positions) == 0


def test_context_initializes_empty_transactions():
    ctx = BacktestContext(_make_config())
    assert ctx.all_transactions == []


def test_context_processing_date_starts_none():
    ctx = BacktestContext(_make_config())
    assert ctx.processing_date is None


def test_context_advance_delegates():
    ctx = BacktestContext(_make_config())
    result = ctx.advance()
    assert result is True
    assert ctx.processing_date == date(2025, 1, 1)


def test_context_screen_stocks_delegates():
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    result = ctx.screen_stocks()
    assert isinstance(result, list)


def test_context_display_wallet_delegates(capsys):
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    ctx.display_wallet()
    output = capsys.readouterr().out
    assert "USD" in output


def test_context_display_portfolio_delegates(capsys):
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    ctx.display_portfolio()
    output = capsys.readouterr().out
    assert output  # prints something


def test_context_display_balance_delegates(capsys):
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    ctx.display_balance()
    output = capsys.readouterr().out
    assert "10000" in output
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_context.py -v`
Expected: FAIL

- [ ] **Step 3: Implement BacktestContext**

Create `core/context.py`:

```python
from decimal import Decimal

from actions.advance import advance as _advance
from actions.display_balance import display_balance as _display_balance
from actions.display_portfolio import display_portfolio as _display_portfolio
from actions.display_wallet import display_wallet as _display_wallet
from actions.execute_transactions import execute_transactions as _execute_transactions
from actions.rebalance import rebalance as _rebalance
from actions.screen_stocks import screen_stocks as _screen_stocks
from core.models import BacktestConfig, Currency, Portfolio, Transaction, Wallet


class BacktestContext:
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.processing_date = None
        self.all_transactions: list[Transaction] = []

        # Initialize wallet from config
        self.wallet = Wallet(holdings={})
        for currency_code, amount in config.initial_cash.items():
            self.wallet.holdings[Currency(code=currency_code)] = amount

        self.portfolio = Portfolio(positions={})

    def advance(self) -> bool:
        return _advance(self)

    def screen_stocks(self) -> list[str]:
        return _screen_stocks(self)

    def rebalance(self, target_tickers: list[str]) -> list[Transaction]:
        return _rebalance(self, target_tickers)

    def execute_transactions(self, transactions: list[Transaction]) -> None:
        _execute_transactions(self, transactions)

    def display_wallet(self) -> None:
        _display_wallet(self)

    def display_portfolio(self) -> None:
        _display_portfolio(self)

    def display_balance(self) -> None:
        _display_balance(self)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_context.py -v`
Expected: All 9 tests PASS

- [ ] **Step 5: Commit**

```bash
git add core/context.py tests/test_context.py
git commit -m "feat: add BacktestContext with action delegation"
```

---

### Task 11: YAML Config Loading & main.py

**Files:**
- Create: `config/backtest.yaml`
- Create: `main.py`
- Create: `tests/test_main.py`

- [ ] **Step 1: Create default YAML config**

Create `config/backtest.yaml`:

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

- [ ] **Step 2: Write failing tests for main**

Create `tests/test_main.py`:

```python
import sys
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from core.models import BacktestConfig


def test_load_config():
    from main import load_config

    config = load_config("config/backtest.yaml")
    assert isinstance(config, BacktestConfig)
    assert config.start_date == date(2025, 1, 1)
    assert config.end_date == date(2025, 12, 31)
    assert config.interval == "month"
    assert config.base_currency == "USD"
    assert config.initial_cash["USD"] == Decimal("10000")
    assert config.screening == {"min_score": 0.5}


def test_load_strategy():
    from main import load_strategy

    strategy = load_strategy("strategies/basic.py")
    assert hasattr(strategy, "run")
    assert callable(strategy.run)


def test_parse_args():
    from main import parse_args

    with patch.object(
        sys,
        "argv",
        ["main.py", "-config=config/backtest.yaml", "-strategy=strategies/basic.py"],
    ):
        args = parse_args()
        assert args.config == "config/backtest.yaml"
        assert args.strategy == "strategies/basic.py"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_main.py -v`
Expected: FAIL

- [ ] **Step 4: Implement main.py**

Create `main.py`:

```python
import argparse
import importlib.util
from datetime import date
from decimal import Decimal

import yaml

from core.context import BacktestContext
from core.models import BacktestConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Run backtest")
    parser.add_argument("-config", required=True, help="Path to YAML config file")
    parser.add_argument("-strategy", required=True, help="Path to strategy Python file")
    return parser.parse_args()


def load_config(path: str) -> BacktestConfig:
    with open(path) as f:
        raw = yaml.safe_load(f)

    return BacktestConfig(
        start_date=date.fromisoformat(raw["start_date"]),
        end_date=date.fromisoformat(raw["end_date"]),
        interval=raw["interval"],
        base_currency=raw["base_currency"],
        initial_cash={
            k: Decimal(str(v)) for k, v in raw["initial_cash"].items()
        },
        screening=raw.get("screening", {}),
    )


def load_strategy(path: str):
    spec = importlib.util.spec_from_file_location("strategy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    args = parse_args()
    config = load_config(args.config)
    ctx = BacktestContext(config)
    strategy = load_strategy(args.strategy)
    strategy.run(ctx)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_main.py -v`
Expected: All 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add main.py config/backtest.yaml tests/test_main.py
git commit -m "feat: add main.py with YAML config loading"
```

---

### Task 12: Basic Strategy

**Files:**
- Create: `strategies/basic.py`

- [ ] **Step 1: Create basic strategy**

Create `strategies/basic.py`:

```python
from core.context import BacktestContext


def run(ctx: BacktestContext) -> None:
    """Basic equal-weight strategy.

    Screens stocks each period, rebalances to equal weight,
    then sells everything at the end.
    """
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

- [ ] **Step 2: Commit**

```bash
git add strategies/basic.py
git commit -m "feat: add basic equal-weight strategy"
```

---

### Task 13: Integration Test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

Create `tests/test_integration.py`:

```python
from datetime import date
from decimal import Decimal

from core.context import BacktestContext
from core.models import BacktestConfig


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 3, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


def test_full_backtest_runs_without_error(capsys):
    """Run full backtest with basic strategy and verify it completes."""
    from strategies.basic import run

    config = _make_config()
    ctx = BacktestContext(config)
    run(ctx)

    # After finish: portfolio should be empty (all sold)
    assert len(ctx.portfolio.positions) == 0

    # Should have transactions recorded
    assert len(ctx.all_transactions) > 0

    # Wallet should have some cash (from selling)
    total_cash = sum(ctx.wallet.holdings.values())
    assert total_cash > 0

    # Should have printed output
    output = capsys.readouterr().out
    assert "Wallet" in output
    assert "Portfolio" in output
    assert "Balance" in output


def test_full_backtest_deterministic():
    """Two runs with same config produce same results."""
    from strategies.basic import run

    config1 = _make_config()
    ctx1 = BacktestContext(config1)
    run(ctx1)

    config2 = _make_config()
    ctx2 = BacktestContext(config2)
    run(ctx2)

    assert len(ctx1.all_transactions) == len(ctx2.all_transactions)
    for tx1, tx2 in zip(ctx1.all_transactions, ctx2.all_transactions):
        assert tx1.ticker.symbol == tx2.ticker.symbol
        assert tx1.action == tx2.action
        assert tx1.quantity == tx2.quantity
        assert tx1.price == tx2.price


def test_backtest_cli_end_to_end(capsys):
    """Test via main.load_config + strategy load."""
    from main import load_config, load_strategy

    config = load_config("config/backtest.yaml")
    ctx = BacktestContext(config)
    strategy = load_strategy("strategies/basic.py")
    strategy.run(ctx)

    assert len(ctx.portfolio.positions) == 0
    assert len(ctx.all_transactions) > 0
```

- [ ] **Step 2: Run integration tests**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/test_integration.py -v`
Expected: All 3 tests PASS

- [ ] **Step 3: Run all tests**

Run: `cd /Users/i318088/prv/pfire/backtest && pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_integration.py
git commit -m "feat: add integration tests for full backtest flow"
```

---

### Task 14: End-to-End Smoke Test

- [ ] **Step 1: Run the backtest from CLI**

Run: `cd /Users/i318088/prv/pfire/backtest && python main.py -config=config/backtest.yaml -strategy=strategies/basic.py`

Expected: Console output showing wallet, portfolio, and balance at each monthly interval from Jan 2025 to Dec 2025, then final sell-all and balance.

- [ ] **Step 2: Verify output looks correct**

Check that:
- Wallet shows USD amounts changing over time
- Portfolio shows stock positions changing
- Balance shows total value at each step
- Final portfolio is empty
- Final balance shows remaining cash

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete backtest engine v1"
```
