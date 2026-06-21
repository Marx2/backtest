# Screener Filters

All filters are set under `screening:` in `config/backtest.yaml`.

There are two filter stages:

1. **OpenBB screener filters** — sent directly to `obb.equity.screener()`. Fast, single API call.
2. **Fundamental filters** — applied after screening via per-ticker `obb.equity.fundamental.metrics()` calls. Slower; only activate if at least one is set.

---

## Stage 1 — OpenBB Screener Filters

### Market Cap

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `mktcap_min` | int | fmp, yfinance | Minimum market cap in USD (e.g. `200000000000` = $200B) |
| `mktcap_max` | int | fmp, yfinance | Maximum market cap in USD |

### Price

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `price_min` | float | fmp, yfinance | Minimum stock price |
| `price_max` | float | fmp, yfinance | Maximum stock price |

### Beta

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `beta_min` | float | fmp, yfinance | Minimum beta |
| `beta_max` | float | fmp, yfinance | Maximum beta (e.g. `1.5` excludes high-volatility stocks) |

### Volume

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `volume_min` | int | fmp, yfinance | Minimum daily trading volume |
| `volume_max` | int | fmp, yfinance | Maximum daily trading volume |

### Dividend

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `dividend_min` | float | fmp | Minimum annual dividend amount |
| `dividend_max` | float | fmp | Maximum annual dividend amount |

### Classification

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `sector` | str | fmp, yfinance | Sector name (e.g. `"Technology"`, `"Healthcare"`) |
| `industry` | str | fmp, yfinance | Industry name (e.g. `"Software"`) |
| `country` | str | fmp | Two-letter country code (e.g. `"us"`, `"de"`) |
| `exchange` | str | fmp, yfinance | Exchange code (e.g. `"nyse,nasdaq"`) |

### Flags

| Key | Type | Providers | Description |
|-----|------|-----------|-------------|
| `is_etf` | bool | fmp | `true` to return only ETFs |
| `is_active` | bool | fmp | `false` to return only inactive tickers |
| `limit` | int | fmp | Cap number of screener results |

> **Note:** `obb.equity.screener` returns **current** market data only — it does not support historical screening. The `d` (date) parameter is accepted for interface compatibility but is not sent to the API.

---

## Stage 2 — Fundamental Filters

Applied post-screening via `obb.equity.fundamental.metrics()` (yfinance). Each per-ticker call is slow; only use these when necessary. Results are cached in-process for the duration of the run.

| Key | Type | Field used | Description |
|-----|------|------------|-------------|
| `max_pe` | float | `pe_ratio` | Maximum P/E ratio. Excludes negative or zero P/E. |
| `min_roe` | float | `return_on_equity` | Minimum return on equity (normalized, e.g. `0.10` = 10%) |
| `min_revenue_growth` | float | `revenue_growth` | Minimum revenue growth YoY (normalized, e.g. `0.05` = 5%) |

---

## Example Config

```yaml
screening:
  # Market cap
  mktcap_min: 200000000000    # $200B+ mega-caps only

  # Exchange / geography
  exchange: "nyse,nasdaq"
  country: "us"

  # Risk
  beta_max: 1.5

  # Fundamental filters (slow — requires per-ticker API calls)
  # max_pe: 40
  # min_roe: 0.10
  # min_revenue_growth: 0.05
```

---

## Extending Filters

To add a new screener filter, pass it in `screen_stocks()` inside `openbb_screener.py`:

```python
if "volume_min" in params:
    kwargs["volume_min"] = params["volume_min"]
```

To add a new fundamental filter, extend `_apply_fundamental_filters()` with the field name from `obb.equity.fundamental.metrics()`.
