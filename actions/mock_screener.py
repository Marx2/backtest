import hashlib
from datetime import date

UNIVERSE = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "JPM", "V", "WMT"]


def screen_stocks(d: date, params: dict) -> list[str]:
    """Screen stocks from hardcoded universe based on date and params.

    Each ticker gets a deterministic score based on ticker+date hash.
    Tickers with score >= min_score pass the screen.
    """
    min_score = params.get("min_score", 0.5)
    result = []
    for ticker in UNIVERSE:
        score = _ticker_score(ticker, d)
        if score >= min_score:
            result.append(ticker)
    return result


def _ticker_score(ticker: str, d: date) -> float:
    """Deterministic score for ticker on given date. Range: 0.0-1.0."""
    seed = f"{ticker}:{d.isoformat()}"
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    return (h % 1000) / 1000
