import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_historical_data(exchange, symbol, timeframe='1d', limit=7):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

# Initialize exchange
exchange = ccxt.binance()

# List of cryptocurrencies
cryptocurrencies = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'USDC', 'XRP', 'DOGE', 'TRX', 'TON', 'ADA', 'AVAX', 'SHIB', 'LINK', 'BCH', 'DOT', 'LEO', 'DAI', 'LTC', 'NEAR', 'UNI', 'KAS', 'ICP', 'XMR', 'PEPE', 'APT', 'FET', 'XLM', 'ETC', 'FDUSD', 'OKB', 'SUI', 'STX', 'CRO', 'AAVE', 'FIL', 'RENDER', 'IMX', 'MNT', 'TAO', 'MATIC', 'HBAR', 'ARB', 'VET', 'INJ', 'OP', 'ATOM', 'WIF', 'MKR', 'AR']

# Dictionary to store results
results = {}

# Fetch data for each cryptocurrency
for crypto in cryptocurrencies:
    print(f"Fetching data for {crypto}...")
    
    # Convert crypto name to symbol (this might need adjustment for some cryptocurrencies)
    symbol = f"{crypto}/USDT"
    
    # Fetch historical data
    df = fetch_historical_data(exchange, symbol)
    
    if df is not None:
        results[crypto] = df
    
    # Add a delay to avoid hitting rate limits
    time.sleep(1)

# Print results
for crypto, df in results.items():
    print(f"\nHistorical data for {crypto}:")
    print(df)

# You can also save the results to CSV files if needed
# for crypto, df in results.items():
#     df.to_csv(f"{crypto}_historical_data.csv", index=False)