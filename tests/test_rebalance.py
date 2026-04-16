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
    ctx = FakeContext(
        wallet_holdings={USD: Decimal("0")},
        positions={AAPL: Decimal("50")},
    )
    result = rebalance(ctx, ["AAPL"])
    assert len(result) == 0


@patch("actions.rebalance.get_fx_rate", side_effect=_mock_fx)
@patch("actions.rebalance.get_price", side_effect=_mock_price)
def test_rebalance_returns_transactions_with_prices(mock_price, mock_fx):
    """Each transaction has correct price set."""
    ctx = FakeContext()
    result = rebalance(ctx, ["AAPL"])
    assert result[0].price == Decimal("100")
