from datetime import date, timedelta
from decimal import Decimal

from dotenv import load_dotenv
load_dotenv()
from openbb import obb

from core.cache import cached

_cache: dict[tuple[str, date], Decimal] = {}
_warmed: set[str] = set()

# Set by rebalance so bulk fetches cover the full backtest range
backtest_start: date | None = None
backtest_end: date | None = None


@cached("prices")
def _fetch_ticker_history(ticker: str, fetch_start: date, fetch_end: date) -> dict:
    """Fetch full price history; returns {date_iso: price_str} for cache serialization."""
    print(f"[prices] fetching {ticker}...", flush=True)
    for provider in ["yfinance", "fmp"]:
        try:
            df = obb.equity.price.historical(
                symbol=ticker,
                start_date=fetch_start.isoformat(),
                end_date=fetch_end.isoformat(),
                interval="1d",
                provider=provider,
            ).to_df()
            if df.empty:
                continue
            return {
                (idx_date.date() if hasattr(idx_date, "date") else idx_date).isoformat(): str(row["close"])
                for idx_date, row in df.iterrows()
            }
        except Exception:
            continue
    return {}


def _warm_ticker(ticker: str) -> None:
    """Fetch full price history for a ticker and populate in-process cache."""
    _warmed.add(ticker)
    fetch_start = (backtest_start or date(2020, 1, 1)) - timedelta(days=14)
    fetch_end = backtest_end or date.today()
    history = _fetch_ticker_history(ticker, fetch_start, fetch_end)
    for date_iso, price_str in history.items():
        d = date.fromisoformat(date_iso)
        _cache[(ticker, d)] = Decimal(price_str).quantize(Decimal("0.01"))


def get_price(ticker: str, d: date) -> Decimal:
    if ticker not in _warmed:
        _warm_ticker(ticker)

    key = (ticker, d)
    if key in _cache:
        return _cache[key]

    for delta in range(1, 15):
        k = (ticker, d - timedelta(days=delta))
        if k in _cache:
            _cache[key] = _cache[k]
            return _cache[k]

    raise RuntimeError(f"Could not fetch price for {ticker} on {d}")
