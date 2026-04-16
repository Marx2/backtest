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
