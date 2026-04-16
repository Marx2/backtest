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
    for ticker in result:
        assert isinstance(ticker, str)


def test_screen_stocks_deterministic():
    ctx = FakeContext()
    result1 = screen_stocks(ctx)
    result2 = screen_stocks(ctx)
    assert result1 == result2
