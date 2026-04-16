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
