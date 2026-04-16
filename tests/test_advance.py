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
