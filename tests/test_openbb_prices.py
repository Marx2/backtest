import pytest
from datetime import date
from decimal import Decimal

from actions.openbb_prices import get_price

TEST_DATE = date(2024, 1, 15)


def test_get_price_returns_decimal():
    result = get_price("AAPL", TEST_DATE)
    assert isinstance(result, Decimal)


def test_get_price_positive():
    result = get_price("AAPL", TEST_DATE)
    assert result > 0


def test_get_price_reasonable_range():
    result = get_price("AAPL", TEST_DATE)
    assert 1 < result < 10000


def test_get_price_two_decimal_places():
    result = get_price("AAPL", TEST_DATE)
    assert result == result.quantize(Decimal("0.01"))


def test_get_price_different_tickers_differ():
    aapl = get_price("AAPL", TEST_DATE)
    msft = get_price("MSFT", TEST_DATE)
    assert aapl != msft


def test_get_price_weekend_returns_price():
    saturday = date(2024, 1, 13)
    result = get_price("AAPL", saturday)
    assert result > 0
