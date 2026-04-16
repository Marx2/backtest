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
