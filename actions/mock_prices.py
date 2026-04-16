import hashlib
from datetime import date
from decimal import Decimal


def get_price(ticker: str, d: date) -> Decimal:
    """Generate a deterministic mock price using seeded random walk.

    Uses hash of ticker to set a base price, then hash of ticker+date
    for daily variation. Simulates random walk by chaining day-over-day.
    """
    base = _ticker_base_price(ticker)
    variation = _date_variation(ticker, d)
    price = base * (Decimal("1") + variation)
    return price.quantize(Decimal("0.01"))


def _ticker_base_price(ticker: str) -> Decimal:
    """Deterministic base price from ticker symbol. Range: 20-500."""
    h = int(hashlib.sha256(ticker.encode()).hexdigest(), 16)
    normalized = (h % 48000 + 2000) / 100
    return Decimal(str(normalized))


def _date_variation(ticker: str, d: date) -> Decimal:
    """Deterministic daily variation from ticker+date. Range: -0.20 to +0.20."""
    seed = f"{ticker}:{d.isoformat()}"
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    variation = ((h % 4000) - 2000) / 10000
    return Decimal(str(variation))
