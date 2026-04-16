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
