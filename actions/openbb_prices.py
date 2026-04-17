from datetime import date, timedelta
from decimal import Decimal

from dotenv import load_dotenv
load_dotenv()
from openbb import obb

_cache: dict[tuple[str, date], Decimal] = {}
_warmed: set[str] = set()

# Set by rebalance so bulk fetches cover the full backtest range
backtest_start: date | None = None
backtest_end: date | None = None


def _warm_ticker(ticker: str) -> None:
    """Fetch full price history for a ticker and populate cache."""
    _warmed.add(ticker)
    print(f"[prices] fetching {ticker}...", flush=True)
    fetch_start = (backtest_start or date(2020, 1, 1)) - timedelta(days=14)
    fetch_end = backtest_end or date.today()
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
            for idx_date, row in df.iterrows():
                d = idx_date.date() if hasattr(idx_date, "date") else idx_date
                _cache[(ticker, d)] = Decimal(str(row["close"])).quantize(Decimal("0.01"))
            return
        except Exception:
            continue


def get_price(ticker: str, d: date) -> Decimal:
    # Bulk-fetch full history on first access for this ticker
    if ticker not in _warmed:
        _warm_ticker(ticker)

    key = (ticker, d)
    if key in _cache:
        return _cache[key]

    # Look back up to 14 days for weekends/holidays
    for delta in range(1, 15):
        k = (ticker, d - timedelta(days=delta))
        if k in _cache:
            _cache[key] = _cache[k]
            return _cache[k]

    raise RuntimeError(f"Could not fetch price for {ticker} on {d}")
