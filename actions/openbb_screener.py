from datetime import date

from dotenv import load_dotenv
load_dotenv()
from openbb import obb

# Module-level caches — screener and fundamentals don't change within a run
_screener_cache: dict[str, list[str]] = {}  # key: frozenset of params → symbols
_fundamentals_cache: dict[str, dict] = {}   # key: symbol → metrics row


def screen_stocks(d: date, params: dict) -> list[str]:
    # NOTE: obb.equity.screener does not support historical screening.
    # It returns current market data only. The `d` parameter is accepted for interface
    # compatibility but is not used in the API call.
    kwargs = dict(
        mktcap_min=params.get("mktcap_min", 200_000_000_000),
    )
    if "beta_max" in params:
        kwargs["beta_max"] = params["beta_max"]

    cache_key = str(sorted(kwargs.items()))
    if cache_key not in _screener_cache:
        print("[screener] running equity screener...", flush=True)
        _screener_cache[cache_key] = _run_screener(kwargs)

    symbols = _screener_cache[cache_key]
    symbols = _apply_fundamental_filters(symbols, params)
    return symbols


def _run_screener(kwargs: dict) -> list[str]:
    for provider in ["yfinance", "fmp"]:
        provider_kwargs = dict(provider=provider, **kwargs)
        try:
            df = obb.equity.screener(**provider_kwargs).to_df()
            if df.empty:
                continue
            return df["symbol"].dropna().tolist()
        except Exception:
            continue
    raise RuntimeError("OpenBB screener failed: no provider returned data")


def _get_fundamentals(symbol: str) -> dict:
    if symbol not in _fundamentals_cache:
        metrics_df = obb.equity.fundamental.metrics(symbol, provider="yfinance").to_df()
        _fundamentals_cache[symbol] = metrics_df.iloc[0].to_dict() if not metrics_df.empty else {}
    return _fundamentals_cache[symbol]


def _apply_fundamental_filters(symbols: list[str], params: dict) -> list[str]:
    max_pe = params.get("max_pe")
    min_roe = params.get("min_roe")
    min_revenue_growth = params.get("min_revenue_growth")

    if max_pe is None and min_roe is None and min_revenue_growth is None:
        return symbols

    filtered = []
    for symbol in symbols:
        try:
            row = _get_fundamentals(symbol)
            if not row:
                continue

            if max_pe is not None:
                pe = row.get("pe_ratio")
                if pe is None or pe <= 0 or pe > max_pe:
                    continue

            if min_roe is not None:
                roe = row.get("return_on_equity")
                if roe is None or roe < min_roe:
                    continue

            if min_revenue_growth is not None:
                growth = row.get("revenue_growth")
                if growth is None or growth < min_revenue_growth:
                    continue

            filtered.append(symbol)
        except Exception:
            continue

    return filtered
