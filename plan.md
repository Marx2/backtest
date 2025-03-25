# Backtesting App Development Plan

## OpenBB Integration Module

### File Structure
```
flask_backtest_app/
├── openbb_integration.py   # New module
├── data/
│   ├── cache/             # Cached API responses
│   └── logs/              # Error logs
```

### Module Architecture
```mermaid
graph TD
    A[openbb_integration.py] --> B[Price Endpoints]
    A --> C[Caching]
    A --> D[Error Logging]
    B --> E[get_price_at_date]
    B --> F[get_prices_in_range]
    C --> G[Local Cache]
    C --> H[TTL=24h]
    D --> I[Log to File]
    D --> J[Console Output]
```

### Implementation Details

1. **Price Endpoints**:
   - `get_price_at_date(symbol: str, date: str) -> float`
     * Returns closing price for specific date
   - `get_prices_in_range(symbol: str, start_date: str, end_date: str) -> pd.DataFrame`
     * Returns daily prices (open, high, low, close, volume) for date range

2. **Caching**:
   - Cache location: `flask_backtest_app/data/cache`
   - TTL: 24 hours
   - Cache key format: `{symbol}_{date_or_range}_{endpoint}`

3. **Error Handling**:
   - Log file: `flask_backtest_app/data/logs/openbb_errors.log`
   - Log format: `[timestamp] [ERROR] [symbol] [endpoint] - message`
   - Console output for immediate visibility

4. **Dependencies**:
   - Add to requirements.txt:
     * openbb
     * pandas
     * cachetools