import hashlib
from datetime import date
from decimal import Decimal


def get_fx_rate(from_currency: str, to_currency: str, d: date) -> Decimal:
    """Generate a deterministic mock FX rate.

    Same currency returns 1. Otherwise uses hash-based deterministic rate.
    """
    if from_currency == to_currency:
        return Decimal("1")

    base = _pair_base_rate(from_currency, to_currency)
    variation = _date_variation(from_currency, to_currency, d)
    rate = base * (Decimal("1") + variation)
    return rate.quantize(Decimal("0.0001"))


def _pair_base_rate(from_currency: str, to_currency: str) -> Decimal:
    """Deterministic base rate for currency pair. Range: 0.5-2.0."""
    pair = f"{from_currency}/{to_currency}"
    h = int(hashlib.sha256(pair.encode()).hexdigest(), 16)
    normalized = (h % 1500 + 500) / 1000
    return Decimal(str(normalized))


def _date_variation(from_currency: str, to_currency: str, d: date) -> Decimal:
    """Deterministic daily variation. Range: -0.05 to +0.05."""
    seed = f"{from_currency}/{to_currency}:{d.isoformat()}"
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    variation = ((h % 1000) - 500) / 10000
    return Decimal(str(variation))
