import re
import pytest
from datetime import date

from actions.openbb_screener import screen_stocks

TEST_DATE = date(2024, 1, 15)


def test_screen_stocks_returns_list():
    result = screen_stocks(TEST_DATE, {})
    assert isinstance(result, list)


def test_screen_stocks_returns_strings():
    result = screen_stocks(TEST_DATE, {})
    assert all(isinstance(s, str) for s in result)


def test_screen_stocks_non_empty():
    result = screen_stocks(TEST_DATE, {})
    assert len(result) > 0


def test_screen_stocks_symbols_are_uppercase():
    result = screen_stocks(TEST_DATE, {})
    for symbol in result:
        assert re.match(r"^[A-Z][A-Z0-9.\-]*$", symbol), f"Symbol {symbol!r} not valid ticker format"


def test_screen_stocks_min_score_higher_fewer_or_equal():
    low_filter = screen_stocks(TEST_DATE, {"min_score": 0.3})
    high_filter = screen_stocks(TEST_DATE, {"min_score": 0.7})
    assert len(low_filter) >= len(high_filter)


def test_screen_stocks_custom_mktcap_min():
    default_result = screen_stocks(TEST_DATE, {})
    large_cap_result = screen_stocks(TEST_DATE, {"mktcap_min": 500_000_000_000})
    assert len(default_result) >= len(large_cap_result)


def test_screen_stocks_empty_params():
    result = screen_stocks(TEST_DATE, {})
    assert isinstance(result, list)
