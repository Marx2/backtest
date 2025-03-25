import os
from datetime import datetime, timedelta
import pandas as pd
from openbb import obb
from cachetools import TTLCache
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('flask_backtest_app/data/logs/openbb_errors.log'),
        logging.StreamHandler()
    ]
)

# Cache configuration
CACHE_DIR = 'flask_backtest_app/data/cache'
CACHE_TTL = timedelta(hours=24)
price_cache = TTLCache(maxsize=100, ttl=CACHE_TTL.total_seconds())

def get_price_at_date(symbol: str, date: str) -> float:
    """Get closing price for a stock on specific date"""
    try:
        cache_key = f"{symbol}_{date}"
        if cache_key in price_cache:
            return price_cache[cache_key]
            
        try:
            # First try with Yahoo provider
            df = obb.equity.price.historical(symbol, provider="yfinance", start_date=date, end_date=date)
        except Exception as yahoo_error:
            logging.warning(f"Yahoo failed for {symbol}, trying Alpha Vantage: {str(yahoo_error)}")
            try:
                # Fallback to Alpha Vantage
                df = obb.equity.price.historical(symbol, provider="alpha_vantage", start_date=date, end_date=date)
            except Exception as av_error:
                logging.error(f"All providers failed for {symbol}: {str(av_error)}")
                raise ValueError(f"Could not retrieve price data for {symbol} from any provider")
                
        if df.empty:
            raise ValueError(f"No data found for {symbol} on {date}")
            
        close_price = df.iloc[0]['close']
        price_cache[cache_key] = close_price
        return close_price
        
    except Exception as e:
        logging.error(f"Error getting price for {symbol} on {date}: {str(e)}")
        raise

def get_prices_in_range(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Get daily prices (OHLCV) for a stock in date range"""
    try:
        cache_key = f"{symbol}_{start_date}_{end_date}"
        if cache_key in price_cache:
            return price_cache[cache_key]
            
        df = obb.equity.price.historical(symbol, start_date=start_date, end_date=end_date)
        if df.empty:
            raise ValueError(f"No data found for {symbol} between {start_date} and {end_date}")
            
        price_cache[cache_key] = df
        return df
        
    except Exception as e:
        logging.error(f"Error getting prices for {symbol} from {start_date} to {end_date}: {str(e)}")
        raise