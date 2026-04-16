from datetime import date

from dotenv import load_dotenv
load_dotenv()
from openbb import obb


def screen_stocks(d: date, params: dict) -> list[str]:
    # NOTE: obb.equity.screener does not support historical screening.
    # It returns current market data only. The `d` parameter is accepted for interface
    # compatibility but is not used in the API call. To support true historical screening,
    # a provider with point-in-time data (e.g., Intrinio's historical screener) would
    # be required — not currently available in this integration.
    min_score = params.get("min_score", 0.5)
    mktcap_min = params.get("mktcap_min", 200_000_000_000)

    kwargs = dict(
        mktcap_min=mktcap_min,
    )
    if min_score >= 0.7:
        kwargs["beta_max"] = 1.0
    elif min_score >= 0.5:
        kwargs["beta_max"] = 1.5

    for provider in ["yfinance", "fmp"]:
        provider_kwargs = dict(provider=provider, **kwargs)
        if provider == "fmp":
            provider_kwargs["country"] = "us"
        try:
            df = obb.equity.screener(**provider_kwargs).to_df()
            if df.empty:
                continue
            return df["symbol"].dropna().tolist()
        except Exception:
            continue

    raise RuntimeError("OpenBB screener failed: no provider returned data")
