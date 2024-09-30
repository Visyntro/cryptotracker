import ccxt
import pandas as pd
from datetime import datetime
import time
import os

def fetch_historical_data(exchange, symbol, timeframe='1d', limit=60):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

# Initialize exchange
