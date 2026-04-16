from datetime import date

from actions.mock_screener import screen_stocks


def test_screen_stocks_returns_list():
    result = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    assert isinstance(result, list)


def test_screen_stocks_returns_strings():
    result = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    for ticker in result:
        assert isinstance(ticker, str)


def test_screen_stocks_deterministic():
    result1 = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    result2 = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    assert result1 == result2


def test_screen_stocks_subset_of_universe():
    result = screen_stocks(date(2025, 1, 15), {"min_score": 0.5})
    assert len(result) > 0
    from actions.mock_screener import UNIVERSE

    for ticker in result:
        assert ticker in UNIVERSE


def test_screen_stocks_different_dates_can_differ():
    results = set()
    for month in range(1, 13):
        result = tuple(screen_stocks(date(2025, month, 15), {"min_score": 0.5}))
        results.add(result)
    assert len(results) >= 2


def test_screen_stocks_higher_min_score_fewer_results():
    low = screen_stocks(date(2025, 1, 15), {"min_score": 0.2})
    high = screen_stocks(date(2025, 1, 15), {"min_score": 0.8})
    assert len(low) >= len(high)
