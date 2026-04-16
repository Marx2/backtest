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
