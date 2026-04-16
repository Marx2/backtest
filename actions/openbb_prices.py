from datetime import date, timedelta
from decimal import Decimal

from dotenv import load_dotenv
load_dotenv()
from openbb import obb


def get_price(ticker: str, d: date) -> Decimal:
    for window in [7, 14]:
        start = d - timedelta(days=window - 1)
        for provider in ["yfinance", "fmp"]:
            try:
                df = obb.equity.price.historical(
                    symbol=ticker,
                    start_date=start.isoformat(),
                    end_date=d.isoformat(),
                    interval="1d",
                    provider=provider,
                ).to_df()
                if df.empty:
                    continue
                row = df[df.index <= d]
                if row.empty:
                    continue
                return Decimal(str(row["close"].iloc[-1])).quantize(Decimal("0.01"))
            except Exception:
                continue
    raise RuntimeError(f"Could not fetch price for {ticker} on {d}")
