from datetime import date, timedelta
from decimal import Decimal

from dotenv import load_dotenv
load_dotenv()
from openbb import obb


def get_fx_rate(from_currency: str, to_currency: str, d: date) -> Decimal:
    if from_currency == to_currency:
        return Decimal("1")

    pair = f"{from_currency}{to_currency}".lower()
    for window in [7, 14]:
        start = d - timedelta(days=window - 1)
        for provider in ["yfinance", "fmp"]:
            try:
                df = obb.currency.price.historical(
                    symbol=pair,
                    start_date=start.isoformat(),
                    end_date=d.isoformat(),
                    provider=provider,
                ).to_df()
                if df.empty:
                    continue
                row = df[df.index <= d]
                if row.empty:
                    continue
                return Decimal(str(row["close"].iloc[-1])).quantize(Decimal("0.0001"))
            except Exception:
                continue
    raise RuntimeError(f"Could not fetch FX rate for {from_currency}/{to_currency} on {d}")
