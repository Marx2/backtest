import pytest
from datetime import date
from decimal import Decimal

from actions.openbb_fx_rates import get_fx_rate

TEST_DATE = date(2024, 1, 15)


def test_get_fx_rate_returns_decimal():
    result = get_fx_rate("EUR", "USD", TEST_DATE)
    assert isinstance(result, Decimal)


def test_get_fx_rate_positive():
    result = get_fx_rate("EUR", "USD", TEST_DATE)
    assert result > 0


def test_get_fx_rate_same_currency_is_one():
    result = get_fx_rate("USD", "USD", TEST_DATE)
    assert result == Decimal("1")


def test_get_fx_rate_eurusd_reasonable_range():
    result = get_fx_rate("EUR", "USD", TEST_DATE)
    assert Decimal("0.5") < result < Decimal("2.0")


def test_get_fx_rate_four_decimal_places():
    result = get_fx_rate("EUR", "USD", TEST_DATE)
    assert result == result.quantize(Decimal("0.0001"))


def test_get_fx_rate_weekend_returns_rate():
    saturday = date(2024, 1, 13)
    result = get_fx_rate("EUR", "USD", saturday)
    assert result > 0
