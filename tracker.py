import ccxt
import pandas as pd
from datetime import datetime
import time
import os

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

# Folder to store the CSV files
folder_name = 'crypto_data'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)  # Create the folder if it doesn't exist

# Fetch data for each cryptocurrency
for crypto in cryptocurrencies:
    print(f"Fetching data for {crypto}...")
    
    # Convert crypto name to symbol (this might need adjustment for some cryptocurrencies)
    symbol = f"{crypto}/USDT"
    if crypto == 'USDT':
        symbol = 'USDT/USD'
    
    # Fetch historical data
    df = fetch_historical_data(exchange, symbol)
    
    if df is not None:
        # Save the DataFrame as a CSV file in the designated folder
        csv_filename = os.path.join(folder_name, f"{crypto}_ohlcv.csv")
        df.to_csv(csv_filename, index=False)
        print(f"Saved {crypto} data to {csv_filename}")
    
    # Add a delay to avoid hitting rate limits
    time.sleep(1)

print("All data saved successfully.")
